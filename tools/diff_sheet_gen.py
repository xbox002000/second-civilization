#!/usr/bin/env python3
"""
diff_sheet_gen.py — Workflow V2 Cross-Shot Diff Sheet Generator & Gate Token Verifier
Implements AMD-02 & AMD-03 (§4.2, §4.3 A/B, §4.4, §5.1, §5.2) from
WORKFLOW_V2_AMENDMENT_AGY_MEMO.md.

Modes:
  1. Generate QC-1 or QC-2 diff sheet + gate JSON skeleton:
     python3 diff_sheet_gen.py --shots shot_list.json --mode qc1 \
       --out-image qc1_diff_sheet.jpg --out-gate qc1_gate.json

  2. Verify filled gate JSON (Stage 4 / Stage 6A token-chaining check):
     python3 diff_sheet_gen.py --verify qc2_gate.json

  3. Built-in self-test:
     python3 diff_sheet_gen.py --selftest
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_CHECK_VALUES = {"PASS", "FAIL", "N_A"}
QC1_CHECK_KEYS = ["age_id", "scar_side", "costume_4pt", "light_lock", "pose_spatial"]
QC2_CHECK_KEYS = [
    "age_id",
    "scar_side",
    "costume_4pt",
    "light_lock",
    "expression_lip",
    "pose_spatial",
]

# Color palette (dark studio review table)
BG_DARK = (16, 18, 22)
PANEL_BG = (26, 30, 38)
HEADER_BG = (34, 40, 52)
CELL_BORDER = (62, 70, 86)
TEXT_PRIMARY = (238, 242, 248)
TEXT_MUTED = (168, 178, 196)
ACCENT_CYAN = (34, 211, 238)
ACCENT_AMBER = (251, 191, 36)
ACCENT_RED = (248, 113, 113)
ACCENT_GREEN = (74, 222, 128)


# ---------------------------------------------------------------------------
# Font & Text Helpers
# ---------------------------------------------------------------------------

def _load_font(size: int, bold: bool = False, cjk: bool = False) -> ImageFont.ImageFont:
    candidates: List[str] = []
    if cjk:
        candidates.extend([
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/noto/NotoSansTC-Regular.otf",
            "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",
        ])
    if bold:
        candidates.extend([
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        ])
    else:
        candidates.extend([
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        ])
    for path in candidates:
        if os.path.isfile(path):
            try:
                return ImageFont.truetype(path, size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def _has_cjk(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def _wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.ImageFont,
    max_width: int,
) -> List[str]:
    if not text:
        return []
    lines: List[str] = []
    for raw_line in text.splitlines():
        if not raw_line:
            lines.append("")
            continue
        cur = ""
        # Tokenize by spaces for Latin, or character-by-character if CJK / long token
        tokens = raw_line.split(" ") if not _has_cjk(raw_line) else list(raw_line)
        sep = " " if not _has_cjk(raw_line) else ""
        for tok in tokens:
            cand = f"{cur}{sep}{tok}" if cur else tok
            bbox = draw.textbbox((0, 0), cand, font=font)
            if (bbox[2] - bbox[0]) <= max_width:
                cur = cand
            else:
                if cur:
                    lines.append(cur)
                # Break overly long single token
                if (draw.textbbox((0, 0), tok, font=font)[2]) > max_width:
                    sub = ""
                    for ch in tok:
                        if draw.textbbox((0, 0), sub + ch, font=font)[2] <= max_width:
                            sub += ch
                        else:
                            if sub:
                                lines.append(sub)
                            sub = ch
                    cur = sub
                else:
                    cur = tok
        if cur:
            lines.append(cur)
    return lines


def _draw_text_line(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int],
    text: str,
    size: int = 20,
    bold: bool = False,
    fill: Tuple[int, int, int] = TEXT_PRIMARY,
) -> int:
    font = _load_font(size, bold=bold, cjk=_has_cjk(text))
    draw.text(xy, text, font=font, fill=fill)
    bbox = draw.textbbox(xy, text, font=font)
    return (bbox[3] - bbox[1]) + 4


# ---------------------------------------------------------------------------
# Crypto & Media Helpers
# ---------------------------------------------------------------------------

def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def probe_video_info(clip_path: str | Path) -> Dict[str, Any]:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height,r_frame_rate,duration",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        str(clip_path),
    ]
    out = subprocess.check_output(cmd, text=True)
    data = json.loads(out)
    stream = (data.get("streams") or [{}])[0]
    fmt = data.get("format") or {}
    dur = float(stream.get("duration") or fmt.get("duration") or 0.0)
    return {
        "width": int(stream.get("width") or 720),
        "height": int(stream.get("height") or 1280),
        "duration": dur,
        "r_frame_rate": stream.get("r_frame_rate", "24/1"),
    }


def extract_frame(clip_path: str | Path, timestamp_sec: float, tmp_dir: str) -> Image.Image:
    out_png = os.path.join(tmp_dir, f"frame_{timestamp_sec:.4f}.png")
    ts = max(0.0, timestamp_sec)
    cmd = [
        "ffmpeg",
        "-y",
        "-v",
        "error",
        "-ss",
        f"{ts:.4f}",
        "-i",
        str(clip_path),
        "-frames:v",
        "1",
        "-q:v",
        "1",
        out_png,
    ]
    subprocess.run(cmd, check=True)
    if not os.path.isfile(out_png):
        # Clamp slightly earlier if timestamp hit exact EOF
        ts = max(0.0, ts - 0.08)
        cmd[5] = f"{ts:.4f}"
        subprocess.run(cmd, check=True)
    with Image.open(out_png) as im:
        return im.convert("RGB").copy()


# ---------------------------------------------------------------------------
# Color Science (CIE Lab & Highlight Blowout)
# ---------------------------------------------------------------------------

def _rgb_to_lab(rgb_arr: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Vectorized sRGB [0..255] -> CIE L*, a*, b* (D65)."""
    rgb = rgb_arr.astype(np.float32) / 255.0
    linear = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    r, g, b = linear[..., 0], linear[..., 1], linear[..., 2]

    x = (r * 0.4124564 + g * 0.3575761 + b * 0.1804375) / 0.95047
    y = (r * 0.2126729 + g * 0.7151522 + b * 0.0721750) / 1.00000
    z = (r * 0.0193339 + g * 0.1191920 + b * 0.9503041) / 1.08883

    eps = 0.008856
    kappa = 903.3

    def f(t: np.ndarray) -> np.ndarray:
        return np.where(t > eps, np.cbrt(np.maximum(t, 0.0)), (kappa * t + 16.0) / 116.0)

    fx, fy, fz = f(x), f(y), f(z)
    L = 116.0 * fy - 16.0
    a = 500.0 * (fx - fy)
    b_val = 200.0 * (fy - fz)
    return L, a, b_val


def compute_frame_metrics(img: Image.Image, shot_size: str = "MS") -> Dict[str, float]:
    """
    Compute background median L*, b* (per V12a: outer 20% border for CU/MCU/ECU
    to avoid skin tones, outer 25% for MS/LS) and highlight blowout % (>245).
    """
    small = img.resize((180, 320), Image.Resampling.BILINEAR)
    arr = np.asarray(small, dtype=np.uint8)
    h, w, _ = arr.shape
    border_frac = 0.20 if shot_size.upper() in {"CU", "MCU", "ECU"} else 0.25
    bh = max(1, int(h * border_frac))
    bw = max(1, int(w * border_frac))

    mask = np.zeros((h, w), dtype=bool)
    mask[:bh, :] = True
    mask[-bh:, :] = True
    mask[:, :bw] = True
    mask[:, -bw:] = True

    L, _, b_val = _rgb_to_lab(arr)
    bg_L = float(np.median(L[mask]))
    bg_b = float(np.median(b_val[mask]))

    # Blowout: pixels where luma > 245 (clipped highlight / sun-flare artifact)
    luma = 0.2126 * arr[..., 0] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 2]
    blowout_pct = float(np.mean(luma > 245.0) * 100.0)
    return {
        "bg_L": round(bg_L, 2),
        "bg_b": round(bg_b, 2),
        "blowout_pct": round(blowout_pct, 2),
    }


# ---------------------------------------------------------------------------
# Zero-Dependency Skin-Tone Face & Collar Locator (Pillow + numpy)
# ---------------------------------------------------------------------------

def detect_face_box(
    img: Image.Image,
    explicit_box: Optional[List[float]] = None,
    prefer_side: Optional[str] = None,
) -> Tuple[int, int, int, int]:
    """
    Return (x0, y0, x1, y1) pixel bounding box for primary subject face.
    Supports explicit normalized [x0, y0, x1, y1] override; otherwise uses
    multi-scale YCbCr skin-tone density scoring (ignores cyan holograms).
    """
    w, h = img.size
    if explicit_box and len(explicit_box) == 4:
        x0 = max(0, min(w - 1, int(explicit_box[0] * w)))
        y0 = max(0, min(h - 1, int(explicit_box[1] * h)))
        x1 = max(x0 + 16, min(w, int(explicit_box[2] * w)))
        y1 = max(y0 + 16, min(h, int(explicit_box[3] * h)))
        return (x0, y0, x1, y1)

    # Downsample for fast integral-image search
    sw = 144
    sh = max(64, int(round(sw * h / max(w, 1))))
    small = img.resize((sw, sh), Image.Resampling.BILINEAR)
    ycbcr = np.asarray(small.convert("YCbCr"), dtype=np.float32)
    Y, Cb, Cr = ycbcr[..., 0], ycbcr[..., 1], ycbcr[..., 2]
    rgb = np.asarray(small, dtype=np.float32)
    R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]

    # Skin mask: warm human skin tones; explicitly rejects cyan/blue holograms (B > R) and clipped lights
    skin = (
        (Y >= 42) & (Y <= 232)
        & (Cb >= 76) & (Cb <= 128)
        & (Cr >= 134) & (Cr <= 176)
        & (R > G * 0.98)
        & (R > B * 1.08)
    ).astype(np.float32)

    # Smoothness filter: real faces have smooth skin gradients; rust pipes / shutters / foliage have high local texture
    gx = np.abs(np.diff(Y, axis=1, prepend=Y[:, :1]))
    gy = np.abs(np.diff(Y, axis=0, prepend=Y[:1, :]))
    grad = gx + gy
    smooth_weight = np.where(grad < 28.0, 1.0, 0.25).astype(np.float32)
    skin = skin * smooth_weight

    # Suppress very top sky / very bottom hands & bags
    skin[: int(sh * 0.14), :] = 0.0
    skin[int(sh * 0.70) :, :] = 0.0
    # Suppress extreme left/right edges (e.g., hand braced on left edge in S1, shutters on right in S2R)
    skin[:, : int(sw * 0.10)] *= 0.10
    skin[:, int(sw * 0.90) :] *= 0.15

    if prefer_side == "left":
        skin[:, int(sw * 0.56) :] *= 0.25
    elif prefer_side == "right":
        skin[:, : int(sw * 0.44)] *= 0.25

    # Vertical prior favoring portrait head zone (y ~ 28%..56%)
    yy = np.linspace(0.0, 1.0, sh, dtype=np.float32)[:, None]
    y_prior = np.exp(-((yy - 0.43) ** 2) / (2 * 0.15 ** 2))
    weighted = skin * (0.50 + 0.50 * y_prior)

    # Integral image for O(1) window sums
    ii = np.pad(weighted, ((1, 0), (1, 0)), mode="constant").cumsum(axis=0).cumsum(axis=1)
    ii_raw = np.pad(skin, ((1, 0), (1, 0)), mode="constant").cumsum(axis=0).cumsum(axis=1)

    best_score = -1.0
    best_rect = (int(sw * 0.28), int(sh * 0.22), int(sw * 0.72), int(sh * 0.48))

    for frac in (0.10, 0.14, 0.20, 0.28, 0.40, 0.52):
        win_w = max(10, int(sw * frac))
        win_h = max(12, int(win_w * 1.20))
        if win_h >= sh - 2 or win_w >= sw - 2:
            continue
        # Sliding sum via integral image
        sums = (
            ii[win_h:, win_w:]
            - ii[:-win_h, win_w:]
            - ii[win_h:, :-win_w]
            + ii[:-win_h, :-win_w]
        )
        raw_sums = (
            ii_raw[win_h:, win_w:]
            - ii_raw[:-win_h, win_w:]
            - ii_raw[win_h:, :-win_w]
            + ii_raw[:-win_h, :-win_w]
        )
        area = float(win_w * win_h)
        density = raw_sums / area
        # Score balances skin density and absolute size so full faces win cleanly
        scores = (sums / (area ** 0.58)) * np.where(density >= 0.18, 1.0, 0.05)
        idx = int(np.argmax(scores))
        sc = float(scores.flat[idx])
        if sc > best_score and float(density.flat[idx]) >= 0.18:
            best_score = sc
            ry, rx = divmod(idx, scores.shape[1])
            best_rect = (rx, ry, rx + win_w, ry + win_h)

    sx0, sy0, sx1, sy1 = best_rect
    scale_x = w / float(sw)
    scale_y = h / float(sh)
    return (
        int(round(sx0 * scale_x)),
        int(round(sy0 * scale_y)),
        int(round(sx1 * scale_x)),
        int(round(sy1 * scale_y)),
    )


def _crop_clamped(
    img: Image.Image, cx: float, cy: float, crop_w: float, crop_h: float
) -> Image.Image:
    w, h = img.size
    cw = max(32, min(w, int(round(crop_w))))
    ch = max(32, min(h, int(round(crop_h))))
    x0 = int(round(cx - cw / 2.0))
    y0 = int(round(cy - ch / 2.0))
    x0 = max(0, min(w - cw, x0))
    y0 = max(0, min(h - ch, y0))
    return img.crop((x0, y0, x0 + cw, y0 + ch))


def make_face_collar_zoom_panel(
    img: Image.Image,
    cell_w: int,
    cell_h: int,
    explicit_face_box: Optional[List[float]] = None,
    explicit_collar_box: Optional[List[float]] = None,
    prefer_side: Optional[str] = None,
    label_prefix: str = "2.5x ZOOM",
    shot_size: str = "MS",
) -> Image.Image:
    """
    Build the mandatory 2.5x Face+Brows (top half) + Crown/Collar (bottom half) zoom cell.
    """
    w, h = img.size
    fx0, fy0, fx1, fy1 = detect_face_box(img, explicit_face_box, prefer_side=prefer_side)
    fw = max(24, fx1 - fx0)
    fh = max(24, fy1 - fy0)
    fcx = (fx0 + fx1) / 2.0
    fcy = (fy0 + fy1) / 2.0

    half_h = cell_h // 2
    aspect = cell_w / float(max(half_h, 1))

    # Top half: zoom on face + both brows + crown/hairpin
    # For CU/ECU faces that already span ~45-65% of frame width, keep full face+brows+hairpin in frame;
    # for MS/2S/MCU, enforce >= 2.5x magnification (crop_w <= w / 2.5).
    if shot_size.upper() in {"CU", "ECU"}:
        face_crop_w = min(w * 0.82, max(fw * 1.55, w * 0.56))
    else:
        face_crop_w = min(w / 2.5, max(fw * 2.1, w / 4.2))
    face_crop_h = face_crop_w / aspect
    face_crop = _crop_clamped(img, fcx, fcy - fh * 0.16, face_crop_w, face_crop_h)
    face_panel = face_crop.resize((cell_w, half_h), Image.Resampling.LANCZOS)

    # Bottom half: zoom on collar overlap (y-right vs left-reverse) + neck/shoulder
    if explicit_collar_box and len(explicit_collar_box) == 4:
        ccx = ((explicit_collar_box[0] + explicit_collar_box[2]) / 2.0) * w
        ccy = ((explicit_collar_box[1] + explicit_collar_box[3]) / 2.0) * h
        collar_crop_w = (explicit_collar_box[2] - explicit_collar_box[0]) * w
        collar_crop_h = collar_crop_w / aspect
    else:
        ccx = fcx
        if shot_size.upper() in {"CU", "ECU"}:
            ccy = min(h * 0.86, fcy + fh * 0.92)
            collar_crop_w = min(w * 0.85, max(fw * 1.75, w * 0.65))
        else:
            ccy = fcy + fh * 1.15
            collar_crop_w = min(w / 2.2, max(fw * 2.6, w / 3.8))
        collar_crop_h = collar_crop_w / aspect
    collar_crop = _crop_clamped(img, ccx, ccy, collar_crop_w, collar_crop_h)
    collar_panel = collar_crop.resize((cell_w, cell_h - half_h), Image.Resampling.LANCZOS)

    out = Image.new("RGB", (cell_w, cell_h), PANEL_BG)
    out.paste(face_panel, (0, 0))
    out.paste(collar_panel, (0, half_h))

    draw = ImageDraw.Draw(out)
    # Divider line between top & bottom zoom halves
    draw.line([(0, half_h), (cell_w, half_h)], fill=ACCENT_CYAN, width=3)

    # Top overlay badges: SCREEN L / SCREEN R orientation markers (to catch S4 mirrored scar!)
    banner_h = max(32, int(cell_h * 0.032))
    draw.rectangle([(0, 0), (cell_w, banner_h)], fill=(12, 16, 22))
    f_sm = _load_font(max(15, cell_w // 34), bold=True)
    draw.text((10, 6), "SCREEN L", font=f_sm, fill=ACCENT_AMBER)
    title_top = f"{label_prefix}: FACE + BROWS"
    tw = draw.textbbox((0, 0), title_top, font=f_sm)[2]
    draw.text(((cell_w - tw) // 2, 6), title_top, font=f_sm, fill=ACCENT_CYAN)
    rw = draw.textbbox((0, 0), "SCREEN R", font=f_sm)[2]
    draw.text((cell_w - rw - 10, 6), "SCREEN R", font=f_sm, fill=ACCENT_AMBER)

    # Subtle vertical center crosshair in top half for left/right scar inspection
    cx_line = cell_w // 2
    for y in range(banner_h + 8, half_h - 8, 16):
        draw.line([(cx_line, y), (cx_line, min(y + 8, half_h - 8))], fill=(255, 255, 255), width=1)

    # Bottom overlay banner
    draw.rectangle([(0, half_h + 2), (cell_w, half_h + banner_h + 2)], fill=(12, 16, 22))
    title_bot = f"{label_prefix}: COLLAR (y-RIGHT) + CROWN/PIN"
    bw = draw.textbbox((0, 0), title_bot, font=f_sm)[2]
    draw.text(((cell_w - bw) // 2, half_h + 8), title_bot, font=f_sm, fill=ACCENT_CYAN)

    return out


def make_master_face_cell(master_path: Optional[str], cell_w: int, cell_h: int) -> Image.Image:
    out = Image.new("RGB", (cell_w, cell_h), PANEL_BG)
    draw = ImageDraw.Draw(out)
    if not master_path or not os.path.isfile(master_path):
        _draw_text_line(draw, (20, cell_h // 2), "NO MASTER FACE REF", size=24, bold=True, fill=ACCENT_RED)
        return out

    with Image.open(master_path) as im:
        rgb = im.convert("RGB")
        # Head-and-shoulders crop centered on face
        fx0, fy0, fx1, fy1 = detect_face_box(rgb)
        fcx = (fx0 + fx1) / 2.0
        fcy = (fy0 + fy1) / 2.0
        w, h = rgb.size
        aspect = cell_w / float(cell_h)
        crop_h = min(h, max((fy1 - fy0) * 3.1, h * 0.58))
        crop_w = crop_h * aspect
        if crop_w > w:
            crop_w = w
            crop_h = crop_w / aspect
        cropped = _crop_clamped(rgb, fcx, fcy + (fy1 - fy0) * 0.22, crop_w, crop_h)
        fitted = cropped.resize((cell_w, cell_h), Image.Resampling.LANCZOS)
        out.paste(fitted, (0, 0))

    # Orientation legend banner (prevents S4 scar mirror blindness)
    f_hdr = _load_font(max(16, cell_w // 32), bold=True)
    bar_h = max(54, int(cell_h * 0.055))
    draw.rectangle([(0, 0), (cell_w, bar_h)], fill=(12, 16, 22))
    draw.text((12, 6), "MASTER FACE ANCHOR (Age B 38-40)", font=f_hdr, fill=ACCENT_CYAN)
    draw.text((12, 6 + max(20, cell_w // 28)), "Anatomical L-Brow Scar = Front Screen RIGHT >>", font=f_hdr, fill=ACCENT_AMBER)
    return out


def make_outfit_anchor_cell(
    outfit_path: Optional[str],
    cell_w: int,
    cell_h: int,
    outfit_id: str,
    checklist: Optional[List[str]] = None,
) -> Image.Image:
    out = Image.new("RGB", (cell_w, cell_h), PANEL_BG)
    draw = ImageDraw.Draw(out)
    if outfit_path and os.path.isfile(outfit_path):
        with Image.open(outfit_path) as im:
            fitted = ImageOps.fit(im.convert("RGB"), (cell_w, cell_h), method=Image.Resampling.LANCZOS)
            out.paste(fitted, (0, 0))
    else:
        _draw_text_line(draw, (20, cell_h // 2), "NO OUTFIT REF", size=24, bold=True, fill=ACCENT_RED)

    # Bottom 4-point checklist strip (v2.3: supports era/anchor-aware checklist)
    if checklist:
        items = checklist
    elif "OUTFIT-01" in outfit_id.upper():
        items = [
            "1. Charcoal blazer + slate mock-neck",
            "2. Modern low nape tail (NO topknot)",
            "3. L-wrist watch + R-hand worn coin",
            "4. ZERO ancient robes/logo/text",
        ]
    elif "OUTFIT-03" in outfit_id.upper():
        items = [
            "1. y-Right dark silk + crimson trim",
            "2. Formal pleated cap + jade hairpin",
            "3. Multi-jade pendant + bixi + L-sword",
            "4. ZERO coin/watch/modern hair",
        ]
    else:
        items = [
            "1. y-Right Collar (L over R) + dark weave",
            "2. Matte black cap + wooden hairpin",
            "3. Rough matte linen + belt jade bi",
            "4. ZERO coin/watch/modern hair/text",
        ]
    f_sm = _load_font(max(15, cell_w // 35), bold=True)
    line_h = max(21, cell_w // 28)
    strip_h = line_h * (len(items) + 1) + 16
    y_start = cell_h - strip_h
    draw.rectangle([(0, y_start), (cell_w, cell_h)], fill=(12, 16, 22))
    draw.text((12, y_start + 6), f"OUTFIT ANCHOR: {outfit_id}", font=f_sm, fill=ACCENT_CYAN)
    for i, item in enumerate(items):
        draw.text((12, y_start + 6 + (i + 1) * line_h), item, font=f_sm, fill=TEXT_PRIMARY)
    return out


def make_dual_anchor_cell(
    master_face_path: Optional[str],
    outfit_path: Optional[str],
    cell_w: int,
    cell_h: int,
    outfit_id: str,
) -> Image.Image:
    """QC-2 Col 1: Top half Master Face, bottom half Outfit collar/crown anchor."""
    half_h = cell_h // 2
    out = Image.new("RGB", (cell_w, cell_h), PANEL_BG)
    top = make_master_face_cell(master_face_path, cell_w, half_h)
    out.paste(top, (0, 0))

    if outfit_path and os.path.isfile(outfit_path):
        with Image.open(outfit_path) as im:
            rgb = im.convert("RGB")
            w, h = rgb.size
            # Crop upper 65% of outfit card (crown + collar + belt)
            crop = rgb.crop((0, 0, w, int(h * 0.68)))
            fitted = ImageOps.fit(crop, (cell_w, cell_h - half_h), method=Image.Resampling.LANCZOS)
            out.paste(fitted, (0, half_h))
    draw = ImageDraw.Draw(out)
    draw.line([(0, half_h), (cell_w, half_h)], fill=ACCENT_CYAN, width=3)
    f_sm = _load_font(max(15, cell_w // 34), bold=True)
    draw.rectangle([(0, half_h + 2), (cell_w, half_h + 32)], fill=(12, 16, 22))
    draw.text((10, half_h + 6), f"OUTFIT ANCHOR: {outfit_id} (y-Right + Cap/Pin)", font=f_sm, fill=ACCENT_CYAN)
    return out


def fit_frame_native(img: Image.Image, cell_w: int, cell_h: int) -> Image.Image:
    """Fit frame cleanly to cell dimensions preserving full aspect ratio."""
    if img.size == (cell_w, cell_h):
        return img.copy()
    return ImageOps.contain(img, (cell_w, cell_h), method=Image.Resampling.LANCZOS)


def paste_centered(canvas: Image.Image, img: Image.Image, x: int, y: int, w: int, h: int) -> None:
    fitted = fit_frame_native(img, w, h)
    ox = x + (w - fitted.width) // 2
    oy = y + (h - fitted.height) // 2
    canvas.paste(fitted, (ox, oy))


# ---------------------------------------------------------------------------
# §5.1 Sampling Points Calculator
# ---------------------------------------------------------------------------

def get_sample_points(
    shot_type: str, trim_in: float, trim_out: float, lip_sensitive: bool = False
) -> List[Tuple[str, float]]:
    """
    Return list of (label, timestamp_sec) within [trim_in, trim_out] per §5.1.
    """
    st = (shot_type or "action").strip().lower()
    if lip_sensitive or st in {"dialogue", "dialogue_cu", "dialogue_mcu"}:
        fracs = [0.0, 0.25, 0.50, 0.75, 1.0]
        labels = ["0%", "25%", "50%", "75%", "100%"]
    elif st in {"two_shot", "2s", "ots"}:
        fracs = [0.0, 1.0 / 3.0, 2.0 / 3.0, 1.0]
        labels = ["0%", "33%", "67%", "100%"]
    elif st in {"reaction", "silent_cu", "silent_mcu", "reverse"}:
        fracs = [0.0, 1.0 / 3.0, 2.0 / 3.0, 1.0]
        labels = ["0%", "33%", "67%", "100%"]
    elif st in {"composite_ui", "cpu_card", "evidence_card"}:
        t_eff = max(0.2, trim_out - trim_in)
        t0 = min(trim_out, trim_in + min(0.3, t_eff * 0.15))
        t1 = trim_in + t_eff * 0.5
        t2 = max(trim_in, trim_out - min(0.2, t_eff * 0.15))
        return [("IN+0.3s", t0), ("50%", t1), ("OUT-0.2s", t2)]
    else:
        # action / LS / MS
        fracs = [0.0, 0.50, 1.0]
        labels = ["0%", "50%", "100%"]

    t_eff = max(0.0, trim_out - trim_in)
    return [(lbl, trim_in + f * t_eff) for lbl, f in zip(labels, fracs)]


def _normalize_shot_entry(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Accept flexible field aliases for master refs, first frame, clip, trim."""
    s = dict(raw)
    mrefs = s.get("master_refs")
    if isinstance(mrefs, dict):
        s.setdefault("master_face_ref", mrefs.get("face") or mrefs.get("master_face"))
        s.setdefault("outfit_ref", mrefs.get("outfit") or mrefs.get("costume"))
    elif isinstance(mrefs, list):
        if len(mrefs) >= 1:
            s.setdefault("master_face_ref", mrefs[0])
        if len(mrefs) >= 2:
            s.setdefault("outfit_ref", mrefs[1])
    s["first_frame"] = s.get("first_frame") or s.get("first_frame_path") or ""
    s["clip"] = s.get("clip") or s.get("clip_path") or ""
    s["shot_id"] = str(s.get("shot_id") or "S?")
    s["shot_size"] = str(s.get("shot_size") or "MS").upper()
    s["shot_type"] = str(s.get("shot_type") or _infer_shot_type(s)).lower()
    return s


def _infer_shot_type(s: Dict[str, Any]) -> str:
    if s.get("lip_sensitive"):
        return "dialogue"
    sz = str(s.get("shot_size") or "").upper()
    if sz in {"2S", "OTS"}:
        return "two_shot"
    if sz in {"CU", "MCU", "ECU"}:
        return "reaction"
    if str(s.get("gen_mode") or "").lower() == "cpu_card":
        return "cpu_card"
    return "action"


# ---------------------------------------------------------------------------
# Sheet Generators (QC-1 & QC-2)
# ---------------------------------------------------------------------------

def _draw_telemetry_col(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    w: int,
    h: int,
    title: str,
    kv_lines: List[Tuple[str, str, Tuple[int, int, int]]],
    flags: List[str],
) -> None:
    draw.rectangle([(x, y), (x + w, y + h)], fill=PANEL_BG, outline=CELL_BORDER, width=2)
    pad = 16
    cy = y + pad
    f_title = _load_font(34, bold=True)
    draw.text((x + pad, cy), title, font=f_title, fill=ACCENT_CYAN)
    cy += 48
    draw.line([(x + pad, cy), (x + w - pad, cy)], fill=CELL_BORDER, width=2)
    cy += 16

    f_key = _load_font(19, bold=True)
    for k, v, col in kv_lines:
        if cy > y + h - 120:
            break
        draw.text((x + pad, cy), k, font=f_key, fill=TEXT_MUTED)
        cy += 24
        f_val = _load_font(20, bold=False, cjk=_has_cjk(v))
        for wl in _wrap_text(draw, v, f_val, w - 2 * pad):
            if cy > y + h - 100:
                break
            draw.text((x + pad, cy), wl, font=f_val, fill=col)
            cy += 25
        cy += 8

    # Auto-flag banner at bottom of Col 0
    if flags:
        fy = max(cy + 8, y + h - (len(flags) * 30 + 46))
        draw.rectangle([(x + 10, fy), (x + w - 10, y + h - 10)], fill=(75, 22, 26), outline=ACCENT_RED, width=2)
        f_fl = _load_font(20, bold=True)
        draw.text((x + 18, fy + 8), "AUTO-FLAGGED:", font=f_fl, fill=ACCENT_RED)
        fy += 34
        f_fi = _load_font(17, bold=False)
        for fl in flags:
            draw.text((x + 18, fy), f"! {fl}", font=f_fi, fill=(255, 220, 220))
            fy += 24
    else:
        fy = y + h - 46
        draw.rectangle([(x + 10, fy), (x + w - 10, y + h - 10)], fill=(18, 52, 34), outline=ACCENT_GREEN, width=2)
        f_ok = _load_font(19, bold=True)
        draw.text((x + 18, fy + 8), "METRICS: WITHIN THRESHOLD", font=f_ok, fill=ACCENT_GREEN)


def generate_qc1(
    spec: Dict[str, Any],
    out_image: Path,
    out_gate: Path,
    cell_width: int = 0,
    quality: int = 92,
) -> Dict[str, Any]:
    shots = [_normalize_shot_entry(s) for s in spec.get("shots") or []]
    if not shots:
        raise ValueError("shot_list.json has no shots")

    # Determine native resolution from first frames (no thumbnail collapse!)
    native_w, native_h = 720, 1280
    for s in shots:
        ff = s["first_frame"]
        if ff and os.path.isfile(ff):
            with Image.open(ff) as im:
                native_w, native_h = im.size
                break
    cw = cell_width if cell_width > 0 else native_w
    ch = int(round(cw * (native_h / float(max(native_w, 1)))))

    # Precompute frame metrics & segment Lab baseline
    shot_imgs: List[Optional[Image.Image]] = []
    shot_metrics: List[Dict[str, float]] = []
    for s in shots:
        ff = s["first_frame"]
        if ff and os.path.isfile(ff):
            with Image.open(ff) as im:
                rgb = im.convert("RGB").copy()
            shot_imgs.append(rgb)
            shot_metrics.append(compute_frame_metrics(rgb, s["shot_size"]))
        else:
            shot_imgs.append(None)
            shot_metrics.append({"bg_L": 0.0, "bg_b": 0.0, "blowout_pct": 0.0})

    # Segment reference Lab (from loc_ref if provided, else median across shots)
    loc_ref = spec.get("loc_ref")
    if loc_ref and os.path.isfile(loc_ref):
        with Image.open(loc_ref) as lim:
            ref_m = compute_frame_metrics(lim.convert("RGB"), "LS")
        seg_L, seg_b = ref_m["bg_L"], ref_m["bg_b"]
    else:
        seg_L = float(np.median([m["bg_L"] for m in shot_metrics]))
        seg_b = float(np.median([m["bg_b"] for m in shot_metrics]))

    # Layout (§4.3 A: 5 columns)
    col0_w = max(440, int(cw * 0.62))
    gap = 12
    header_h = 84
    col_headers = [
        (col0_w, "Col 0: SPEC & CONTINUITY TAG"),
        (cw, "Col 1: IDENTITY MASTER ANCHOR"),
        (cw, "Col 2: COSTUME CARD ANCHOR"),
        (cw, "Col 3: CANDIDATE FIRST FRAME (NATIVE)"),
        (cw, "Col 4: 2.5x FACE + COLLAR ZOOM"),
    ]
    total_w = gap + sum(w + gap for w, _ in col_headers)
    total_h = header_h + gap + len(shots) * (ch + gap)

    canvas = Image.new("RGB", (total_w, total_h), BG_DARK)
    draw = ImageDraw.Draw(canvas)

    # Top title & column headers
    draw.rectangle([(0, 0), (total_w, header_h)], fill=HEADER_BG)
    f_hdr_main = _load_font(26, bold=True)
    f_col_hdr = _load_font(22, bold=True)
    proj = spec.get("project_id", "PROJECT")
    seg = spec.get("segment_id", "SEG-01")
    draw.text(
        (gap, 8),
        f"QC-1 FIRST-FRAME CROSS-SHOT DIFF SHEET | {proj} / {seg} | Native Cell: {cw}x{ch} | Q={quality}",
        font=f_hdr_main,
        fill=ACCENT_CYAN,
    )
    cx = gap
    for w_col, title in col_headers:
        draw.rectangle([(cx, 46), (cx + w_col, header_h - 4)], fill=PANEL_BG, outline=CELL_BORDER, width=1)
        draw.text((cx + 10, 52), title, font=f_col_hdr, fill=TEXT_PRIMARY)
        cx += w_col + gap

    gate_shots: List[Dict[str, Any]] = []

    for idx, s in enumerate(shots):
        ry = header_h + gap + idx * (ch + gap)
        m = shot_metrics[idx]
        dL = round(m["bg_L"] - seg_L, 2)
        db = round(m["bg_b"] - seg_b, 2)
        flags: List[str] = []
        if abs(dL) > 15.0:
            flags.append(f"LIGHT_SHIFT dL*={dL:+.1f}")
        if abs(db) > 12.0:
            flags.append(f"TEMP_SHIFT db*={db:+.1f}")
        if m["blowout_pct"] > 5.0:
            flags.append(f"BLOWOUT {m['blowout_pct']:.1f}% (>5%)")

        # Col 0: Spec & continuity
        x0 = gap
        kv = [
            ("SHOT / SIZE / FACING", f"{s['shot_id']} | {s['shot_size']} | facing={s.get('subject_facing','?')}", TEXT_PRIMARY),
            ("OUTFIT / LIGHT LOCK", f"{s.get('outfit_id','?')} | {s.get('light_lock_id', spec.get('light_lock_id','?'))}", TEXT_PRIMARY),
            ("ENGINE / GEN_MODE", f"{s.get('engine_route','?')} / {s.get('gen_mode','?')}", TEXT_PRIMARY),
            ("FIRST_FRAME SOURCE", f"{s.get('first_frame_source','?')} (ref={s.get('ref_shot_id') or 'none'})", ACCENT_AMBER),
            ("START POSE", str(s.get("start_pose") or "—"), TEXT_PRIMARY),
            ("PREV END STATE", str(s.get("prev_end_state") or "—"), TEXT_MUTED),
            ("LAB BG (L*, b*)", f"L*={m['bg_L']:.1f} (dL*={dL:+.1f}) | b*={m['bg_b']:.1f} (db*={db:+.1f})", TEXT_PRIMARY),
            ("BLOWOUT (>245)", f"{m['blowout_pct']:.2f}%", ACCENT_RED if m["blowout_pct"] > 5.0 else ACCENT_GREEN),
        ]
        _draw_telemetry_col(draw, x0, ry, col0_w, ch, f"{s['shot_id']} [QC-1]", kv, flags)

        # Col 1: Master face anchor
        x1 = x0 + col0_w + gap
        c1 = make_master_face_cell(s.get("master_face_ref"), cw, ch)
        canvas.paste(c1, (x1, ry))
        draw.rectangle([(x1, ry), (x1 + cw, ry + ch)], outline=CELL_BORDER, width=2)

        # Col 2: Outfit card anchor
        x2 = x1 + cw + gap
        c2 = make_outfit_anchor_cell(
            s.get("outfit_ref"),
            cw,
            ch,
            str(s.get("outfit_id") or "OUTFIT"),
            s.get("outfit_checklist"),
        )
        canvas.paste(c2, (x2, ry))
        draw.rectangle([(x2, ry), (x2 + cw, ry + ch)], outline=CELL_BORDER, width=2)

        # Col 3: Candidate first frame (full native)
        x3 = x2 + cw + gap
        draw.rectangle([(x3, ry), (x3 + cw, ry + ch)], fill=PANEL_BG, outline=CELL_BORDER, width=2)
        img = shot_imgs[idx]
        if img is not None:
            paste_centered(canvas, img, x3, ry, cw, ch)
            # Telemetry footer bar
            f_bar = _load_font(max(16, cw // 36), bold=True)
            bar_h = 34
            draw.rectangle([(x3, ry + ch - bar_h), (x3 + cw, ry + ch)], fill=(12, 16, 22))
            bar_txt = f"{s['shot_id']} FIRST FRAME | L*={m['bg_L']:.1f} ({dL:+.1f}) b*={m['bg_b']:.1f} ({db:+.1f}) | Blow={m['blowout_pct']:.1f}%"
            draw.text((x3 + 10, ry + ch - bar_h + 7), bar_txt, font=f_bar, fill=ACCENT_AMBER if flags else TEXT_PRIMARY)

        # Col 4: 2.5x Face + Collar zoom
        x4 = x3 + cw + gap
        if img is not None:
            c4 = make_face_collar_zoom_panel(
                img,
                cw,
                ch,
                explicit_face_box=s.get("face_box"),
                explicit_collar_box=s.get("collar_box"),
                prefer_side=s.get("prefer_side"),
                label_prefix=f"{s['shot_id']} 2.5x",
                shot_size=s["shot_size"],
            )
            canvas.paste(c4, (x4, ry))
        else:
            draw.rectangle([(x4, ry), (x4 + cw, ry + ch)], fill=PANEL_BG)
        draw.rectangle([(x4, ry), (x4 + cw, ry + ch)], outline=ACCENT_CYAN, width=2)

        # Gate skeleton record
        src_files: Dict[str, Any] = {}
        if s["first_frame"] and os.path.isfile(s["first_frame"]):
            ff_abs = str(Path(s["first_frame"]).resolve())
            src_files["first_frame"] = {"path": ff_abs, "sha256": sha256_file(ff_abs)}
        gate_shots.append({
            "shot_id": s["shot_id"],
            "shot_size": s["shot_size"],
            "shot_type": s["shot_type"],
            "source_files": src_files,
            "metrics": {**m, "dL_seg": dL, "db_seg": db},
            "auto_flags": flags,
            "checks": {k: "" for k in QC1_CHECK_KEYS},
            "failed_anchor_ids": [],
            "shot_status": "PENDING",
            "override_reason": "",
            "notes": "",
        })

    out_image.parent.mkdir(parents=True, exist_ok=True)
    out_gate.parent.mkdir(parents=True, exist_ok=True)
    save_q = max(88, min(98, quality))
    canvas.save(str(out_image), format="JPEG", quality=save_q, subsampling=0)

    gate_payload = {
        "schema_version": "2.0",
        "gate_type": "qc1",
        "project_id": proj,
        "segment_id": seg,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "diff_sheet_path": str(out_image.resolve()),
        "diff_sheet_sha256": sha256_file(out_image),
        "sheet_dimensions": {"width": canvas.width, "height": canvas.height, "cell_width": cw, "cell_height": ch, "jpeg_quality": save_q},
        "status": "PENDING",
        "reviewer": "",
        "reviewed_at": "",
        "shots": gate_shots,
    }
    with out_gate.open("w", encoding="utf-8") as fh:
        json.dump(gate_payload, fh, ensure_ascii=False, indent=2)
    return gate_payload


def generate_qc2(
    spec: Dict[str, Any],
    out_image: Path,
    out_gate: Path,
    cell_width: int = 0,
    quality: int = 90,
) -> Dict[str, Any]:
    shots = [_normalize_shot_entry(s) for s in spec.get("shots") or []]
    if not shots:
        raise ValueError("shot_list.json has no shots")

    # Determine native clip resolution (full width, no thumbnail collapse)
    native_w, native_h = 720, 1280
    clip_infos: List[Dict[str, Any]] = []
    for s in shots:
        cp = s["clip"]
        if cp and os.path.isfile(cp):
            info = probe_video_info(cp)
            clip_infos.append(info)
            if native_w == 720 and info["width"] > 0:
                native_w, native_h = info["width"], info["height"]
        else:
            clip_infos.append({"width": 720, "height": 1280, "duration": 0.0})

    cw = cell_width if cell_width > 0 else native_w
    ch = int(round(cw * (native_h / float(max(native_w, 1)))))

    # Sample frames per §5.1 for every shot
    sampled_per_shot: List[List[Tuple[str, float, Image.Image, Dict[str, float]]]] = []
    max_samples = 3
    with tempfile.TemporaryDirectory(prefix="diff_sheet_qc2_") as tmp_dir:
        for idx, s in enumerate(shots):
            cp = s["clip"]
            info = clip_infos[idx]
            dur = info["duration"]
            trim_in = float(s.get("trim_in", 0.5 if dur > 1.5 else 0.0))
            trim_out = float(s.get("trim_out", max(trim_in + 0.1, dur - 0.5) if dur > 1.5 else max(0.1, dur)))
            trim_in = max(0.0, min(trim_in, max(0.0, dur - 0.05)))
            trim_out = max(trim_in + 0.05, min(trim_out, max(0.05, dur - 0.02)))
            pts = get_sample_points(s["shot_type"], trim_in, trim_out, bool(s.get("lip_sensitive", False)))
            max_samples = max(max_samples, len(pts))

            frames_info: List[Tuple[str, float, Image.Image, Dict[str, float]]] = []
            if cp and os.path.isfile(cp):
                shot_tmp = os.path.join(tmp_dir, f"shot_{idx}")
                os.makedirs(shot_tmp, exist_ok=True)
                for lbl, ts in pts:
                    im = extract_frame(cp, ts, shot_tmp)
                    fm = compute_frame_metrics(im, s["shot_size"])
                    frames_info.append((lbl, ts, im, fm))
            sampled_per_shot.append(frames_info)

    # Layout (§4.3 B expanded with exact §5.1 sample columns)
    col0_w = max(440, int(cw * 0.62))
    gap = 12
    header_h = 84
    col_headers: List[Tuple[int, str]] = [
        (col0_w, "Col 0: CLIP TELEMETRY"),
        (cw, "Col 1: MASTER DUAL ANCHOR"),
        (cw, "Col 2: QC-1 FIRST FRAME"),
    ]
    for si in range(max_samples):
        col_headers.append((cw, f"Col {3 + si}: CLIP SAMPLE f_{si} (§5.1)"))
    col_headers.append((cw, f"Col {3 + max_samples}: 2.5x FINAL FACE+COLLAR ZOOM"))

    total_w = gap + sum(w + gap for w, _ in col_headers)
    total_h = header_h + gap + len(shots) * (ch + gap)

    canvas = Image.new("RGB", (total_w, total_h), BG_DARK)
    draw = ImageDraw.Draw(canvas)

    draw.rectangle([(0, 0), (total_w, header_h)], fill=HEADER_BG)
    f_hdr_main = _load_font(28, bold=True)
    f_col_hdr = _load_font(21, bold=True)
    proj = spec.get("project_id", "PROJECT")
    seg = spec.get("segment_id", "SEG-01")
    draw.text(
        (gap, 8),
        f"QC-2 FINAL-CLIP CROSS-SHOT DIFF SHEET | {proj} / {seg} | Native Cell: {cw}x{ch} | Q={quality}",
        font=f_hdr_main,
        fill=ACCENT_CYAN,
    )
    cx = gap
    for w_col, title in col_headers:
        draw.rectangle([(cx, 46), (cx + w_col, header_h - 4)], fill=PANEL_BG, outline=CELL_BORDER, width=1)
        draw.text((cx + 10, 52), title, font=f_col_hdr, fill=TEXT_PRIMARY)
        cx += w_col + gap

    gate_shots: List[Dict[str, Any]] = []

    for idx, s in enumerate(shots):
        ry = header_h + gap + idx * (ch + gap)
        samples = sampled_per_shot[idx]
        info = clip_infos[idx]
        dur = info["duration"]
        trim_in = float(s.get("trim_in", 0.5 if dur > 1.5 else 0.0))
        trim_out = float(s.get("trim_out", max(trim_in + 0.1, dur - 0.5) if dur > 1.5 else max(0.1, dur)))
        net_sec = round(max(0.0, trim_out - trim_in), 2)

        dL_intra = 0.0
        db_intra = 0.0
        peak_dL_intra = 0.0
        peak_db_intra = 0.0
        peak_blowout = 0.0
        blowout_spike = 0.0
        if samples:
            m0 = samples[0][3]
            m_end = samples[-1][3]
            dL_intra = round(m_end["bg_L"] - m0["bg_L"], 2)
            db_intra = round(m_end["bg_b"] - m0["bg_b"], 2)
            peak_dL_intra = round(max((x[3]["bg_L"] - m0["bg_L"] for x in samples), key=abs), 2)
            peak_db_intra = round(max((x[3]["bg_b"] - m0["bg_b"] for x in samples), key=abs), 2)
            peak_blowout = round(max(x[3]["blowout_pct"] for x in samples), 2)
            blowout_spike = round(peak_blowout - m0["blowout_pct"], 2)

        flags: List[str] = []
        if abs(dL_intra) > 12.0:
            flags.append(f"INTRA_LIGHT dL*={dL_intra:+.1f}")
        elif abs(peak_dL_intra) > 12.0:
            flags.append(f"PEAK_LIGHT_SPIKE dL*={peak_dL_intra:+.1f}")
        if abs(db_intra) > 10.0:
            flags.append(f"INTRA_TEMP db*={db_intra:+.1f}")
        elif abs(peak_db_intra) > 10.0:
            flags.append(f"PEAK_TEMP_SPIKE db*={peak_db_intra:+.1f}")
        if peak_blowout > 5.0 or blowout_spike > 5.0:
            flags.append(f"BLOWOUT peak={peak_blowout:.1f}% (spike {blowout_spike:+.1f}%)")
        vad_delta_ms = s.get("vad_delta_ms")
        if vad_delta_ms is not None and abs(float(vad_delta_ms)) > 300.0:
            flags.append(f"LIP_OFFSET {float(vad_delta_ms):+.0f}ms (>300ms)")

        # Col 0: Clip telemetry
        x0 = gap
        kv = [
            ("SHOT / TYPE / SIZE", f"{s['shot_id']} | {s['shot_type']} | {s['shot_size']}", TEXT_PRIMARY),
            ("ENGINE / GEN_MODE", f"{s.get('engine_route','?')} / {s.get('gen_mode','?')}", TEXT_PRIMARY),
            ("EFFECTIVE WINDOW", f"[{trim_in:.2f}s .. {trim_out:.2f}s] net={net_sec:.2f}s (raw {dur:.2f}s)", TEXT_PRIMARY),
            ("SAMPLES (§5.1)", f"{len(samples)} frames: " + ", ".join(f"{x[0]}@{x[1]:.2f}s" for x in samples), TEXT_MUTED),
            ("INTRA LAB (f0->fend / peak)", f"end dL*={dL_intra:+.1f} db*={db_intra:+.1f} | peak dL*={peak_dL_intra:+.1f}", ACCENT_AMBER if (abs(peak_dL_intra) > 12 or abs(peak_db_intra) > 10) else TEXT_PRIMARY),
            ("BLOWOUT PEAK (>245)", f"{peak_blowout:.2f}% (spike {blowout_spike:+.2f}%)", ACCENT_RED if peak_blowout > 5.0 else ACCENT_GREEN),
            ("LIP / VAD OFFSET", f"lip={bool(s.get('lip_sensitive', False))} | delta={vad_delta_ms if vad_delta_ms is not None else 'N/A'} ms", TEXT_PRIMARY),
        ]
        _draw_telemetry_col(draw, x0, ry, col0_w, ch, f"{s['shot_id']} [QC-2]", kv, flags)

        # Col 1: Master dual anchor
        x1 = x0 + col0_w + gap
        c1 = make_dual_anchor_cell(
            s.get("master_face_ref"),
            s.get("outfit_ref"),
            cw,
            ch,
            str(s.get("outfit_id") or "OUTFIT"),
        )
        canvas.paste(c1, (x1, ry))
        draw.rectangle([(x1, ry), (x1 + cw, ry + ch)], outline=CELL_BORDER, width=2)

        # Col 2: Approved QC-1 first frame
        x2 = x1 + cw + gap
        draw.rectangle([(x2, ry), (x2 + cw, ry + ch)], fill=PANEL_BG, outline=CELL_BORDER, width=2)
        ff_path = s["first_frame"]
        if ff_path and os.path.isfile(ff_path):
            with Image.open(ff_path) as ffim:
                paste_centered(canvas, ffim.convert("RGB"), x2, ry, cw, ch)
            f_tag = _load_font(max(16, cw // 36), bold=True)
            draw.rectangle([(x2, ry), (x2 + cw, ry + 32)], fill=(12, 16, 22))
            draw.text((x2 + 10, ry + 6), f"{s['shot_id']} QC-1 FIRST FRAME", font=f_tag, fill=ACCENT_CYAN)

        # Col 3 .. Col (2 + max_samples): §5.1 sampled frames
        f_tag = _load_font(max(16, cw // 36), bold=True)
        for si in range(max_samples):
            xs = x2 + cw + gap + si * (cw + gap)
            draw.rectangle([(xs, ry), (xs + cw, ry + ch)], fill=PANEL_BG, outline=CELL_BORDER, width=2)
            if si < len(samples):
                lbl, ts, fim, fm = samples[si]
                paste_centered(canvas, fim, xs, ry, cw, ch)
                draw.rectangle([(xs, ry), (xs + cw, ry + 34)], fill=(12, 16, 22))
                draw.text(
                    (xs + 10, ry + 7),
                    f"f_{si} {lbl} ({ts:.2f}s) | L*={fm['bg_L']:.1f} b*={fm['bg_b']:.1f} Blow={fm['blowout_pct']:.1f}%",
                    font=f_tag,
                    fill=ACCENT_RED if fm["blowout_pct"] > 5.0 else TEXT_PRIMARY,
                )
            else:
                draw.text((xs + cw // 2 - 40, ry + ch // 2), "— N/A —", font=f_tag, fill=TEXT_MUTED)

        # Last Col: 2.5x Face + Collar zoom from peak-stress frame
        xz = x2 + cw + gap + max_samples * (cw + gap)
        if samples:
            # Pick 67% frame for 4-frame reaction/2S (catches S3a mid-turn drift), else middle frame
            peak_idx = 2 if len(samples) == 4 else len(samples) // 2
            plbl, pts_t, pim, _ = samples[peak_idx]
            cz = make_face_collar_zoom_panel(
                pim,
                cw,
                ch,
                explicit_face_box=s.get("clip_face_box") or s.get("face_box"),
                explicit_collar_box=s.get("clip_collar_box") or s.get("collar_box"),
                prefer_side=s.get("prefer_side"),
                label_prefix=f"{s['shot_id']} {plbl}@{pts_t:.2f}s",
                shot_size=s["shot_size"],
            )
            canvas.paste(cz, (xz, ry))
        else:
            draw.rectangle([(xz, ry), (xz + cw, ry + ch)], fill=PANEL_BG)
        draw.rectangle([(xz, ry), (xz + cw, ry + ch)], outline=ACCENT_CYAN, width=2)

        # Gate skeleton record with SHA256 of first_frame and clip + 6 required QC-2 keys
        src_files: Dict[str, Any] = {}
        if ff_path and os.path.isfile(ff_path):
            ff_abs = str(Path(ff_path).resolve())
            src_files["first_frame"] = {"path": ff_abs, "sha256": sha256_file(ff_abs)}
        if s["clip"] and os.path.isfile(s["clip"]):
            cp_abs = str(Path(s["clip"]).resolve())
            src_files["clip"] = {"path": cp_abs, "sha256": sha256_file(cp_abs)}

        gate_shots.append({
            "shot_id": s["shot_id"],
            "shot_size": s["shot_size"],
            "shot_type": s["shot_type"],
            "trim_in": trim_in,
            "trim_out": trim_out,
            "net_sec": net_sec,
            "sampled_timestamps": [round(x[1], 3) for x in samples],
            "source_files": src_files,
            "metrics": {
                "dL_intra": dL_intra,
                "db_intra": db_intra,
                "peak_blowout_pct": peak_blowout,
                "blowout_spike_pct": blowout_spike,
            },
            "auto_flags": flags,
            "checks": {k: "" for k in QC2_CHECK_KEYS},
            "failed_anchor_ids": [],
            "shot_status": "PENDING",
            "override_reason": "",
            "notes": "",
        })

    out_image.parent.mkdir(parents=True, exist_ok=True)
    out_gate.parent.mkdir(parents=True, exist_ok=True)
    save_q = max(88, min(98, quality))
    canvas.save(str(out_image), format="JPEG", quality=save_q, subsampling=0)

    gate_payload = {
        "schema_version": "2.0",
        "gate_type": "qc2",
        "project_id": proj,
        "segment_id": seg,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "diff_sheet_path": str(out_image.resolve()),
        "diff_sheet_sha256": sha256_file(out_image),
        "sheet_dimensions": {"width": canvas.width, "height": canvas.height, "cell_width": cw, "cell_height": ch, "jpeg_quality": save_q},
        "status": "PENDING",
        "reviewer": "",
        "reviewed_at": "",
        "shots": gate_shots,
    }
    with out_gate.open("w", encoding="utf-8") as fh:
        json.dump(gate_payload, fh, ensure_ascii=False, indent=2)
    return gate_payload


# ---------------------------------------------------------------------------
# Gate Verification Mode (Token-Chaining Lock for Stage 4 / Stage 6A)
# ---------------------------------------------------------------------------

def verify_gate_json(gate_path: Path) -> Tuple[bool, List[str]]:
    """
    Strictly verify a filled qc1_gate.json or qc2_gate.json.
    Returns (passed, messages). Exits non-zero on ANY mismatch, tampering,
    unfilled/invalid check key, or status inconsistency.
    """
    errors: List[str] = []
    if not gate_path.is_file():
        return False, [f"FAIL [IO_ERROR] Gate file not found: {gate_path}"]

    try:
        with gate_path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception as exc:
        return False, [f"FAIL [JSON_PARSE] {exc}"]

    gate_type = str(data.get("gate_type") or "").lower()
    if gate_type not in {"qc1", "qc2"}:
        errors.append(f"FAIL [SCHEMA] Invalid gate_type: {gate_type!r} (expected 'qc1' or 'qc2')")
        required_keys = QC2_CHECK_KEYS
    else:
        required_keys = QC1_CHECK_KEYS if gate_type == "qc1" else QC2_CHECK_KEYS

    top_status = str(data.get("status") or "").upper()
    if top_status not in {"PASS", "BLOCKED", "FAIL", "PENDING"}:
        errors.append(f"FAIL [STATUS] Unknown top-level status: {top_status!r}")

    # 1. Verify diff sheet SHA256
    sheet_path = data.get("diff_sheet_path")
    sheet_hash = data.get("diff_sheet_sha256")
    if not sheet_path or not sheet_hash:
        errors.append("FAIL [DIFF_SHEET_HASH] Missing diff_sheet_path or diff_sheet_sha256")
    elif not os.path.isfile(sheet_path):
        errors.append(f"FAIL [DIFF_SHEET_MISSING] Diff sheet not found: {sheet_path}")
    else:
        actual_sheet_hash = sha256_file(sheet_path)
        if actual_sheet_hash != sheet_hash:
            errors.append(
                f"FAIL [DIFF_SHEET_TAMPERED] SHA256 mismatch on {sheet_path}: "
                f"expected {sheet_hash[:16]}..., got {actual_sheet_hash[:16]}..."
            )

    shots = data.get("shots")
    if not isinstance(shots, list) or not shots:
        errors.append("FAIL [SCHEMA] Gate JSON contains no shots")
        return False, errors

    any_shot_failed = False

    for shot in shots:
        sid = str(shot.get("shot_id") or "?")

        # 2. Verify all source file SHA256 hashes
        src_files = shot.get("source_files")
        if not isinstance(src_files, dict) or not src_files:
            errors.append(f"FAIL [SOURCE_HASH] shot={sid}: missing source_files entries")
        else:
            for role, meta in src_files.items():
                fpath = (meta or {}).get("path")
                expected_sha = (meta or {}).get("sha256")
                if not fpath or not expected_sha:
                    errors.append(f"FAIL [SOURCE_HASH] shot={sid} ({role}): missing path or sha256")
                elif not os.path.isfile(fpath):
                    errors.append(f"FAIL [SOURCE_MISSING] shot={sid} ({role}): file missing at {fpath}")
                else:
                    actual_sha = sha256_file(fpath)
                    if actual_sha != expected_sha:
                        errors.append(
                            f"FAIL [SHA256_MISMATCH] shot={sid} ({role}): {fpath} tampered "
                            f"(expected {expected_sha[:16]}..., got {actual_sha[:16]}...)"
                        )

        # 3. Verify all required check keys are strictly in {PASS, FAIL, N_A}
        checks = shot.get("checks")
        if not isinstance(checks, dict):
            errors.append(f"FAIL [CHECKS_SCHEMA] shot={sid}: missing 'checks' dict")
            any_shot_failed = True
            continue

        shot_has_fail_key = False
        shot_has_invalid_key = False
        for key in required_keys:
            if key not in checks:
                errors.append(f"FAIL [CHECK_MISSING] shot={sid}: missing required key '{key}'")
                shot_has_invalid_key = True
            else:
                val = str(checks.get(key) or "").strip()
                if val not in VALID_CHECK_VALUES:
                    errors.append(
                        f"FAIL [CHECK_INVALID] shot={sid}: key '{key}'={val!r} "
                        f"must be one of {sorted(VALID_CHECK_VALUES)}"
                    )
                    shot_has_invalid_key = True
                elif val == "FAIL":
                    shot_has_fail_key = True

        # 4. Verify shot_status consistency
        shot_status = str(shot.get("shot_status") or "").upper()
        if shot_has_fail_key:
            any_shot_failed = True
            if shot_status == "PASS":
                errors.append(
                    f"FAIL [STATUS_INCONSISTENT] shot={sid}: shot_status='PASS' contradicts FAIL check key(s)"
                )
        elif not shot_has_invalid_key:
            if shot_status != "PASS":
                errors.append(
                    f"FAIL [STATUS_INCONSISTENT] shot={sid}: all checks PASS/N_A but shot_status={shot_status!r}"
                )
            # If auto_flags present and reviewer marked PASS, require override_reason per §4.4
            auto_flags = shot.get("auto_flags") or []
            if auto_flags and not str(shot.get("override_reason") or "").strip():
                errors.append(
                    f"FAIL [OVERRIDE_REQUIRED] shot={sid}: auto_flags={auto_flags} requires non-empty override_reason to PASS"
                )

    # 5. Verify top-level status consistency & gate clearance
    if any_shot_failed and top_status == "PASS":
        errors.append("FAIL [STATUS_INCONSISTENT] Top-level status='PASS' contradicts one or more FAIL shots")
    elif top_status != "PASS":
        errors.append(f"FAIL [GATE_NOT_PASSED] Top-level status={top_status!r} (downstream requires 'PASS')")

    if not errors:
        return True, [
            f"PASS [GATE_VERIFIED] {gate_path} ({gate_type.upper()}): "
            f"{len(shots)} shot(s) verified, all SHA256 hashes & check enums consistent, status=PASS."
        ]
    return False, errors


# ---------------------------------------------------------------------------
# Self-Test Suite
# ---------------------------------------------------------------------------

def _make_synthetic_portrait(path: Path, size: Tuple[int, int] = (360, 640), tint: Tuple[int, int, int] = (205, 160, 130)) -> None:
    w, h = size
    im = Image.new("RGB", size, (24, 34, 48))
    d = ImageDraw.Draw(im)
    # Warm streetlight glow in background
    d.ellipse([(w // 2 - 14, h // 4 - 14), (w // 2 + 14, h // 4 + 14)], fill=(235, 195, 110))
    # Head (skin tone for skin detector)
    d.ellipse([(int(w * 0.34), int(h * 0.25)), (int(w * 0.66), int(h * 0.48))], fill=tint)
    # Robe + y-right collar
    d.rectangle([(int(w * 0.20), int(h * 0.48)), (int(w * 0.80), int(h * 0.92))], fill=(26, 30, 34))
    d.line([(int(w * 0.36), int(h * 0.48)), (int(w * 0.62), int(h * 0.72))], fill=(110, 95, 78), width=10)
    d.line([(int(w * 0.64), int(h * 0.48)), (int(w * 0.48), int(h * 0.63))], fill=(95, 82, 68), width=8)
    im.save(str(path), format="JPEG", quality=92)


def run_selftest() -> int:
    print("=== RUNNING diff_sheet_gen.py SELFTEST ===")
    all_ok = True

    def check(name: str, cond: bool, detail: str = "") -> None:
        nonlocal all_ok
        status = "OK" if cond else "ASSERT_FAIL"
        if not cond:
            all_ok = False
        print(f"  [{status}] {name}" + (f" -- {detail}" if detail else ""))

    with tempfile.TemporaryDirectory(prefix="diff_sheet_selftest_") as td:
        tdir = Path(td)
        master_face = tdir / "master_face.jpg"
        outfit_ref = tdir / "outfit_ref.jpg"
        ff1 = tdir / "S1_first.jpg"
        ff2 = tdir / "S2_first.jpg"
        clip1 = tdir / "S1.mp4"
        clip2 = tdir / "S2.mp4"

        _make_synthetic_portrait(master_face)
        _make_synthetic_portrait(outfit_ref)
        _make_synthetic_portrait(ff1)
        _make_synthetic_portrait(ff2, tint=(210, 165, 135))

        # Generate two 2.0s synthetic mp4 clips via ffmpeg
        for src_img, out_mp4 in ((ff1, clip1), (ff2, clip2)):
            subprocess.run(
                [
                    "ffmpeg", "-y", "-v", "error",
                    "-loop", "1", "-i", str(src_img),
                    "-t", "2.0", "-r", "24",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    str(out_mp4),
                ],
                check=True,
            )

        spec = {
            "project_id": "SELFTEST",
            "segment_id": "SEG-01",
            "light_lock_id": "LK-TEST",
            "shots": [
                {
                    "shot_id": "S1",
                    "shot_size": "MS",
                    "shot_type": "action",
                    "subject_facing": "front",
                    "outfit_id": "FANLI-OUTFIT-02",
                    "engine_route": "flow",
                    "gen_mode": "i2v_first",
                    "first_frame_source": "generated",
                    "start_pose": "Standing against wall",
                    "prev_end_state": "(anchor)",
                    "master_face_ref": str(master_face),
                    "outfit_ref": str(outfit_ref),
                    "first_frame": str(ff1),
                    "clip": str(clip1),
                    "trim_in": 0.2,
                    "trim_out": 1.8,
                    "lip_sensitive": False,
                },
                {
                    "shot_id": "S2",
                    "shot_size": "CU",
                    "shot_type": "dialogue",
                    "subject_facing": "right",
                    "outfit_id": "FANLI-OUTFIT-02",
                    "engine_route": "h3",
                    "gen_mode": "ref2v",
                    "first_frame_source": "derived_shot",
                    "ref_shot_id": "S1",
                    "start_pose": "CU speaking on camera",
                    "prev_end_state": "Standing against wall",
                    "master_face_ref": str(master_face),
                    "outfit_ref": str(outfit_ref),
                    "first_frame": str(ff2),
                    "clip": str(clip2),
                    "trim_in": 0.2,
                    "trim_out": 1.8,
                    "lip_sensitive": True,
                },
            ],
        }

        qc1_img = tdir / "qc1_diff_sheet.jpg"
        qc1_gate = tdir / "qc1_gate.json"
        qc2_img = tdir / "qc2_diff_sheet.jpg"
        qc2_gate = tdir / "qc2_gate.json"

        g1 = generate_qc1(spec, qc1_img, qc1_gate, quality=92)
        g2 = generate_qc2(spec, qc2_img, qc2_gate, quality=90)

        check("qc1_image_created", qc1_img.is_file() and qc1_img.stat().st_size > 20000, f"bytes={qc1_img.stat().st_size}")
        check("qc2_image_created", qc2_img.is_file() and qc2_img.stat().st_size > 20000, f"bytes={qc2_img.stat().st_size}")
        check("qc2_six_keys_empty_skeleton", all(g2["shots"][0]["checks"][k] == "" for k in QC2_CHECK_KEYS))
        check("qc2_dialogue_5_samples", len(g2["shots"][1]["sampled_timestamps"]) == 5)
        check("qc2_action_3_samples", len(g2["shots"][0]["sampled_timestamps"]) == 3)

        # Verify empty skeleton MUST fail
        ok_empty, _ = verify_gate_json(qc2_gate)
        check("verify_rejects_empty_skeleton", not ok_empty)

        # Fill valid PASS gate JSON and verify -> MUST pass
        filled = json.loads(qc2_gate.read_text(encoding="utf-8"))
        filled["status"] = "PASS"
        filled["reviewer"] = "Muse"
        for sh in filled["shots"]:
            for k in QC2_CHECK_KEYS:
                sh["checks"][k] = "PASS"
            sh["shot_status"] = "PASS"
            if sh["auto_flags"]:
                sh["override_reason"] = "Selftest accepted"
        qc2_filled = tdir / "qc2_gate_filled.json"
        qc2_filled.write_text(json.dumps(filled, indent=2), encoding="utf-8")
        ok_filled, msgs = verify_gate_json(qc2_filled)
        check("verify_accepts_valid_filled_gate", ok_filled, "; ".join(msgs))

        # Tamper 1: invalid enum value
        bad_enum = json.loads(qc2_filled.read_text(encoding="utf-8"))
        bad_enum["shots"][0]["checks"]["scar_side"] = "MAYBE"
        p_bad_enum = tdir / "qc2_bad_enum.json"
        p_bad_enum.write_text(json.dumps(bad_enum, indent=2), encoding="utf-8")
        ok_enum, _ = verify_gate_json(p_bad_enum)
        check("verify_rejects_invalid_enum", not ok_enum)

        # Tamper 2: status inconsistency (FAIL key but status=PASS)
        bad_stat = json.loads(qc2_filled.read_text(encoding="utf-8"))
        bad_stat["shots"][1]["checks"]["age_id"] = "FAIL"
        p_bad_stat = tdir / "qc2_bad_status.json"
        p_bad_stat.write_text(json.dumps(bad_stat, indent=2), encoding="utf-8")
        ok_stat, _ = verify_gate_json(p_bad_stat)
        check("verify_rejects_status_inconsistency", not ok_stat)

        # Tamper 3: modify source file bytes -> SHA256 mismatch
        with open(ff1, "ab") as fh:
            fh.write(b"\x00TAMPERED")
        ok_sha, sha_msgs = verify_gate_json(qc2_filled)
        check("verify_catches_sha256_tampering", not ok_sha and any("SHA256_MISMATCH" in m for m in sha_msgs))

    print(f"=== SELFTEST {'PASSED' if all_ok else 'FAILED'} ===")
    return 0 if all_ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Workflow V2 Cross-Shot Diff Sheet Generator & Gate Verifier (AMD-02/03)"
    )
    parser.add_argument("--shots", help="Path to shot_list.json")
    parser.add_argument("--mode", choices=["qc1", "qc2"], help="Diff sheet mode")
    parser.add_argument("--out-image", help="Output JPEG path (default: qc1_diff_sheet.jpg / qc2_diff_sheet.jpg)")
    parser.add_argument("--out-gate", help="Output gate JSON path (default: qc1_gate.json / qc2_gate.json)")
    parser.add_argument("--cell-width", type=int, default=0, help="Visual cell width in px (0 = native resolution)")
    parser.add_argument("--quality", type=int, default=92, help="JPEG quality (>= 88, default 92)")
    parser.add_argument("--verify", help="Verify a filled qc1_gate.json or qc2_gate.json")
    parser.add_argument("--selftest", action="store_true", help="Run built-in self-test suite")
    args = parser.parse_args()

    if args.selftest:
        return run_selftest()

    if args.verify:
        ok, msgs = verify_gate_json(Path(args.verify))
        for m in msgs:
            print(m)
        return 0 if ok else 1

    if not args.shots or not args.mode:
        parser.error("Provide --shots and --mode (qc1|qc2), or --verify, or --selftest")

    shots_path = Path(args.shots)
    if not shots_path.is_file():
        print(f"ERROR: shot list file not found: {shots_path}", file=sys.stderr)
        return 2

    with shots_path.open("r", encoding="utf-8") as fh:
        spec = json.load(fh)

    out_dir = shots_path.parent
    out_img = Path(args.out_image) if args.out_image else (out_dir / f"{args.mode}_diff_sheet.jpg")
    out_gate = Path(args.out_gate) if args.out_gate else (out_dir / f"{args.mode}_gate.json")

    if args.mode == "qc1":
        gate = generate_qc1(spec, out_img, out_gate, cell_width=args.cell_width, quality=args.quality)
    else:
        gate = generate_qc2(spec, out_img, out_gate, cell_width=args.cell_width, quality=args.quality)

    dims = gate["sheet_dimensions"]
    print(
        f"GENERATED {args.mode.upper()}:\n"
        f"  image: {out_img} ({dims['width']}x{dims['height']}, cell={dims['cell_width']}x{dims['cell_height']}, "
        f"Q={dims['jpeg_quality']}, {out_img.stat().st_size:,} bytes)\n"
        f"  gate:  {out_gate} ({len(gate['shots'])} shots, status={gate['status']})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
