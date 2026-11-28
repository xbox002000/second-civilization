#!/usr/bin/env python3
"""
sys01_composite.py — SYS-01 4-Layer Assembly Composite Template (AMD-05)
Implements WORKFLOW_V2_AMENDMENT_AGY_MEMO.md §7.2 using Python 3.11 + Pillow + ffmpeg.

4-Layer Spec:
  Layer 0 (V1): Clean actor plate (trimmed, normalized).
  Layer 1 (V1_cyan_spill): Directional cyan light grade back onto the actor via
                           Pillow feathered grayscale mask + ffmpeg colorbalance + maskedmerge,
                           modulated by dynamic time envelope alpha(t).
  Layer 2 (V2_ui): Transparent RGBA popup panel (pure geometry + cold monochrome avatar still,
                   ZERO TEXT) + audio-driven ffmpeg showwaves waveform strip inside panel.
  Layer 3 (V3_fx): Entry glitch (rgbashift + 2-frame flicker at t_glitch), gentle hover float,
                   and 3% shared camera breath welding actor, cyan grade, and UI into one shot.

Usage:
  python3 sys01_composite.py \
    --plate demo02/clips/S3a_v2.mp4 \
    --avatar tools/sys01_avatar_silhouette.png \
    --panel-rect 390,260,305,540 \
    --audio demo01/audio/sys.mp3 \
    --output tools/sys01_proof_3s.mp4 \
    --start 0.8 --duration 3.0
"""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps


# ---------------------------------------------------------------------------
# Default Cold Monochrome Geometric Avatar Generator (Zero Text)
# ---------------------------------------------------------------------------

def generate_default_avatar(out_path: Path, size: Tuple[int, int] = (480, 640)) -> Path:
    """
    Generate a clean, cold monochrome geometric silhouette avatar PNG (zero text)
    aligned with memo §7.2 ('極冷感單色幾何剪影／靜態冷峻側廓').
    """
    w, h = size
    im = Image.new("RGBA", (w, h), (6, 20, 28, 255))
    draw = ImageDraw.Draw(im)

    # Subtle geometric radial grid / holographic wireframe backdrop
    cx, cy = w // 2, int(h * 0.42)
    for r in (90, 145, 200, 255):
        draw.ellipse(
            [(cx - r, cy - r), (cx + r, cy + r)],
            outline=(34, 211, 238, 38),
            width=1,
        )
    for ang_deg in range(0, 360, 30):
        ang = math.radians(ang_deg)
        x1 = int(cx + math.cos(ang) * 260)
        y1 = int(cy + math.sin(ang) * 260)
        draw.line([(cx, cy), (x1, y1)], fill=(34, 211, 238, 22), width=1)

    # Soft cyan back-halo behind silhouette
    halo = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    hd.ellipse(
        [(cx - 130, cy - 150), (cx + 130, cy + 140)],
        fill=(34, 211, 238, 85),
    )
    halo = halo.filter(ImageFilter.GaussianBlur(radius=42))
    im = Image.alpha_composite(im, halo)

    # Sculpted cold female head + neck + shoulders geometric silhouette
    sil = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sil)

    # Shoulders / torso polygon
    shoulders = [
        (int(w * 0.08), h),
        (int(w * 0.14), int(h * 0.78)),
        (int(w * 0.30), int(h * 0.67)),
        (int(w * 0.41), int(h * 0.63)),
        (int(w * 0.59), int(h * 0.63)),
        (int(w * 0.70), int(h * 0.67)),
        (int(w * 0.86), int(h * 0.78)),
        (int(w * 0.92), h),
    ]
    sd.polygon(shoulders, fill=(14, 52, 66, 235), outline=(103, 232, 249, 210))

    # Neck
    neck = [
        (int(w * 0.42), int(h * 0.52)),
        (int(w * 0.58), int(h * 0.52)),
        (int(w * 0.60), int(h * 0.66)),
        (int(w * 0.40), int(h * 0.66)),
    ]
    sd.polygon(neck, fill=(18, 66, 82, 240))

    # Sleek hair / crown silhouette (pulled back, clinical/stoic)
    sd.ellipse(
        [(int(w * 0.27), int(h * 0.14)), (int(w * 0.73), int(h * 0.56))],
        fill=(12, 46, 58, 245),
        outline=(56, 224, 245, 220),
        width=2,
    )
    # Face oval + sculpted jawline
    face_poly = [
        (int(w * 0.34), int(h * 0.24)),
        (int(w * 0.50), int(h * 0.20)),
        (int(w * 0.66), int(h * 0.24)),
        (int(w * 0.68), int(h * 0.38)),
        (int(w * 0.63), int(h * 0.50)),
        (int(w * 0.50), int(h * 0.57)),
        (int(w * 0.37), int(h * 0.50)),
        (int(w * 0.32), int(h * 0.38)),
    ]
    sd.polygon(face_poly, fill=(26, 94, 114, 245), outline=(165, 243, 252, 235))

    # Minimal geometric facial planes (eyes/nose/brow contour lines — cold, stoic, no smiling mouth!)
    # Brow line
    sd.line([(int(w * 0.38), int(h * 0.34)), (int(w * 0.47), int(h * 0.35))], fill=(186, 248, 255, 210), width=2)
    sd.line([(int(w * 0.53), int(h * 0.35)), (int(w * 0.62), int(h * 0.34))], fill=(186, 248, 255, 210), width=2)
    # Subtle geometric eye slits
    sd.polygon(
        [(int(w * 0.38), int(h * 0.38)), (int(w * 0.43), int(h * 0.37)), (int(w * 0.47), int(h * 0.38)), (int(w * 0.43), int(h * 0.39))],
        fill=(210, 252, 255, 220),
    )
    sd.polygon(
        [(int(w * 0.53), int(h * 0.38)), (int(w * 0.57), int(h * 0.37)), (int(w * 0.62), int(h * 0.38)), (int(w * 0.57), int(h * 0.39))],
        fill=(210, 252, 255, 220),
    )
    # Nose bridge & geometric facet lines
    sd.line([(int(w * 0.50), int(h * 0.34)), (int(w * 0.50), int(h * 0.45))], fill=(125, 238, 252, 160), width=2)
    sd.line([(int(w * 0.44), int(h * 0.49)), (int(w * 0.56), int(h * 0.49))], fill=(165, 243, 252, 180), width=2)
    # Collar / shoulder geometric wireframe accents
    sd.line([(int(w * 0.30), int(h * 0.67)), (int(w * 0.50), int(h * 0.80))], fill=(56, 224, 245, 160), width=2)
    sd.line([(int(w * 0.70), int(h * 0.67)), (int(w * 0.50), int(h * 0.80))], fill=(56, 224, 245, 160), width=2)

    im = Image.alpha_composite(im, sil)

    # Scanlines across avatar
    scan = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    scd = ImageDraw.Draw(scan)
    for y in range(0, h, 4):
        scd.line([(0, y), (w, y)], fill=(0, 12, 18, 55), width=1)
    im = Image.alpha_composite(im, scan)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    im.save(str(out_path), format="PNG")
    return out_path


# ---------------------------------------------------------------------------
# Video Probing
# ---------------------------------------------------------------------------

def probe_video(path: Path) -> Tuple[int, int, float, float]:
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,duration",
        "-show_entries", "format=duration",
        "-of", "json",
        str(path),
    ]
    data = json.loads(subprocess.check_output(cmd, text=True))
    st = (data.get("streams") or [{}])[0]
    fmt = data.get("format") or {}
    w = int(st.get("width") or 720)
    h = int(st.get("height") or 1280)
    rfr = st.get("r_frame_rate", "24/1")
    if "/" in rfr:
        num, den = rfr.split("/", 1)
        fps = float(num) / max(float(den), 1.0)
    else:
        fps = float(rfr)
    dur = float(st.get("duration") or fmt.get("duration") or 3.0)
    return w, h, fps, dur


# ---------------------------------------------------------------------------
# Layer 1 Asset: Directional Feathered Cyan Spill Mask (Pillow)
# ---------------------------------------------------------------------------

def build_cyan_spill_mask(
    width: int,
    height: int,
    panel_rect: Tuple[int, int, int, int],
    actor_side: str = "left",
    mask_center: Optional[Tuple[float, float, float, float]] = None,
) -> Image.Image:
    """
    Create a 1/4-resolution grayscale feathered directional mask for Layer 1
    (bright on actor face/cheek/collar facing the popup, smoothly fading to 0
    away from the popup and on the dark alley background).
    """
    mw = max(90, width // 4)
    mh = max(160, height // 4)
    px, py, pw, ph = panel_rect

    if mask_center is not None:
        cx_n, cy_n, rx_n, ry_n = mask_center
    else:
        # Auto-derive actor face/collar position opposite the popup panel
        cy_n = (py + ph * 0.45) / float(height)
        if actor_side == "left":
            cx_n = max(0.18, min(0.42, (px / float(width)) - 0.17))
        else:
            cx_n = min(0.82, max(0.58, ((px + pw) / float(width)) + 0.17))
        rx_n = 0.27
        ry_n = 0.30

    yy, xx = np.mgrid[0:mh, 0:mw].astype(np.float32)
    xn = xx / float(mw)
    yn = yy / float(mh)

    # Primary soft elliptical glow over actor's face, cheek, and shoulder
    dx = (xn - cx_n) / max(rx_n, 0.05)
    dy = (yn - cy_n) / max(ry_n, 0.05)
    dist2 = dx * dx + dy * dy
    base_glow = np.exp(-1.55 * dist2)

    # Directional bias: strongest on the edge facing the popup, falls off rapidly behind the actor
    panel_cx_n = (px + pw * 0.5) / float(width)
    if panel_cx_n >= cx_n:
        # Panel is to the RIGHT of actor -> illuminate right half of actor strongly
        dir_ramp = np.clip((xn - (cx_n - rx_n * 0.65)) / max(rx_n * 1.15, 0.08), 0.0, 1.0)
        # Taper softly before entering the panel itself so background behind panel stays deep dark
        right_cut = np.clip(((px / float(width)) + 0.08 - xn) / 0.16, 0.15, 1.0)
        directional = dir_ramp * right_cut
    else:
        # Panel is to the LEFT of actor -> illuminate left half of actor strongly
        dir_ramp = np.clip(((cx_n + rx_n * 0.65) - xn) / max(rx_n * 1.15, 0.08), 0.0, 1.0)
        left_cut = np.clip((xn - (((px + pw) / float(width)) - 0.08)) / 0.16, 0.15, 1.0)
        directional = dir_ramp * left_cut

    mask_f = np.clip(base_glow * (0.25 + 0.75 * directional), 0.0, 1.0)
    # Normalize peak to 1.0 so alpha(t) cleanly controls peak spill
    peak = float(mask_f.max())
    if peak > 1e-4:
        mask_f = mask_f / peak

    # Boost slight mid-intensity curve so face/collar read clearly as cyan bounce light
    mask_f = np.power(mask_f, 0.82)
    mask_u8 = np.clip(mask_f * 255.0, 0, 255).astype(np.uint8)
    mask_img = Image.fromarray(mask_u8, mode="L")
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=max(6, mw // 22)))
    return mask_img


# ---------------------------------------------------------------------------
# Layer 2 Asset: SYS-01 Popup Panel PNG (Geometry + Avatar, ZERO TEXT)
# ---------------------------------------------------------------------------

def build_popup_panel_png(
    avatar_path: Path,
    panel_w: int,
    panel_h: int,
    pad: int = 24,
) -> Tuple[Image.Image, Tuple[int, int, int, int]]:
    """
    Build the transparent RGBA popup panel PNG (geometry + cyan-graded avatar still,
    ZERO TEXT) and return (panel_rgba, waveform_box_rel_to_panel_png).
    """
    cw = panel_w + 2 * pad
    ch = panel_h + 2 * pad
    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))

    # 1. Pre-baked outer cyan glow
    glow = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.rectangle([(pad, pad), (pad + panel_w, pad + panel_h)], outline=(34, 211, 238, 220), width=6)
    glow = glow.filter(ImageFilter.GaussianBlur(radius=14))
    canvas = Image.alpha_composite(canvas, glow)

    # 2. Translucent dark cyan frosted-glass body (#081C24 @ ~74% alpha)
    body = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    bd.rectangle([(pad, pad), (pad + panel_w, pad + panel_h)], fill=(8, 28, 36, 188))

    # Subtle top status geometry bar (pure geometric ticks/segments, ZERO text!)
    hdr_h = max(18, int(panel_h * 0.045))
    bd.rectangle([(pad + 2, pad + 2), (pad + panel_w - 2, pad + hdr_h)], fill=(12, 46, 60, 215))
    # Three geometric indicator bars on left + thin rule across
    bx = pad + 12
    by = pad + hdr_h // 2 - 3
    for idx, bw in enumerate((18, 10, 6)):
        bd.rectangle([(bx, by), (bx + bw, by + 6)], fill=(34, 211, 238, 230 if idx == 0 else 150))
        bx += bw + 6
    bd.line(
        [(bx + 8, pad + hdr_h // 2), (pad + panel_w - 14, pad + hdr_h // 2)],
        fill=(34, 211, 238, 120),
        width=1,
    )
    canvas = Image.alpha_composite(canvas, body)

    # 3. Avatar bay (upper ~68% below header bar)
    inner_m = max(10, int(panel_w * 0.05))
    av_x0 = pad + inner_m
    av_y0 = pad + hdr_h + inner_m
    av_w = panel_w - 2 * inner_m
    av_h = int((panel_h - hdr_h - 3 * inner_m) * 0.72)

    if avatar_path.is_file():
        with Image.open(avatar_path) as av_raw:
            av_rgb = ImageOps.fit(av_raw.convert("RGB"), (av_w, av_h), method=Image.Resampling.LANCZOS)
            # Cold monochrome cyan duotone grade so any input portrait integrates seamlessly
            lum = np.asarray(av_rgb.convert("L"), dtype=np.float32) / 255.0
            # Contrast stretch slightly for clinical clarity
            lum = np.clip((lum - 0.05) * 1.12, 0.0, 1.0)
            r = np.clip(lum * 82.0 + 6.0, 0, 255)
            g = np.clip(lum * 224.0 + 18.0, 0, 255)
            b = np.clip(lum * 246.0 + 24.0, 0, 255)
            a = np.full_like(r, 224.0)
            # Subtle elliptical edge vignette on alpha
            yy, xx = np.mgrid[0:av_h, 0:av_w].astype(np.float32)
            vx = (xx - av_w * 0.5) / max(av_w * 0.5, 1.0)
            vy = (yy - av_h * 0.5) / max(av_h * 0.5, 1.0)
            vig = np.clip(1.18 - 0.35 * (vx * vx + vy * vy), 0.45, 1.0)
            a = np.clip(a * vig, 0, 255)
            av_rgba = Image.fromarray(np.stack([r, g, b, a], axis=-1).astype(np.uint8), mode="RGBA")
            canvas.alpha_composite(av_rgba, dest=(av_x0, av_y0))

    # 4. Waveform recess bay (lower ~24% below avatar bay)
    wf_x0 = pad + inner_m
    wf_y0 = av_y0 + av_h + inner_m
    wf_w = av_w
    wf_h = max(36, (pad + panel_h - inner_m) - wf_y0)

    # Draw recessed waveform frame & crisp borders/brackets (ZERO text)
    fg = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fg)

    # Avatar bay hairline border
    fd.rectangle([(av_x0, av_y0), (av_x0 + av_w, av_y0 + av_h)], outline=(34, 211, 238, 130), width=1)

    # Waveform recessed dark box + baseline
    fd.rectangle([(wf_x0, wf_y0), (wf_x0 + wf_w, wf_y0 + wf_h)], fill=(4, 14, 20, 218), outline=(34, 211, 238, 165), width=1)
    fd.line([(wf_x0 + 6, wf_y0 + wf_h // 2), (wf_x0 + wf_w - 6, wf_y0 + wf_h // 2)], fill=(34, 211, 238, 65), width=1)

    # 4px micro-scanlines across entire panel body
    for sy in range(pad + 2, pad + panel_h - 2, 4):
        fd.line([(pad + 2, sy), (pad + panel_w - 2, sy)], fill=(0, 14, 20, 46), width=1)

    # 2px crisp outer cyan border (#22D3EE)
    fd.rectangle([(pad, pad), (pad + panel_w, pad + panel_h)], outline=(34, 211, 238, 245), width=2)

    # Precision L-shaped geometric corner brackets
    bl = max(14, int(min(panel_w, panel_h) * 0.08))
    x0, y0, x1, y1 = pad - 2, pad - 2, pad + panel_w + 2, pad + panel_h + 2
    br_col = (165, 243, 252, 255)
    # Top-left
    fd.line([(x0, y0 + bl), (x0, y0), (x0 + bl, y0)], fill=br_col, width=3)
    # Top-right
    fd.line([(x1 - bl, y0), (x1, y0), (x1, y0 + bl)], fill=br_col, width=3)
    # Bottom-left
    fd.line([(x0, y1 - bl), (x0, y1), (x0 + bl, y1)], fill=br_col, width=3)
    # Bottom-right
    fd.line([(x1 - bl, y1), (x1, y1), (x1, y1 - bl)], fill=br_col, width=3)

    canvas = Image.alpha_composite(canvas, fg)
    return canvas, (wf_x0 + 4, wf_y0 + 4, max(32, wf_w - 8), max(24, wf_h - 8))


# ---------------------------------------------------------------------------
# Main 4-Layer ffmpeg Compositor
# ---------------------------------------------------------------------------

def composite_sys01(
    plate_path: Path,
    avatar_path: Path,
    panel_rect: Tuple[int, int, int, int],
    audio_path: Path,
    output_path: Path,
    start_sec: float = 0.0,
    duration_sec: float = 3.0,
    t_glitch: float = 0.35,
    actor_side: str = "left",
    cyan_alpha: float = 0.68,
    mask_center: Optional[Tuple[float, float, float, float]] = None,
    audio_offset: float = 0.0,
    camera_breath: bool = True,
) -> None:
    w, h, fps, plate_dur = probe_video(plate_path)
    fps_int = max(24, int(round(fps)))
    dur = min(duration_sec, max(0.5, plate_dur - start_sec)) if duration_sec > 0 else max(0.5, plate_dur - start_sec)
    px, py, pw, ph = panel_rect
    pad = 24

    with tempfile.TemporaryDirectory(prefix="sys01_comp_") as tmp:
        tdir = Path(tmp)
        mask_png = tdir / "mask_cyan.png"
        panel_png = tdir / "panel_ui.png"

        # Generate Layer 1 feathered mask & Layer 2 RGBA panel PNG
        mask_img = build_cyan_spill_mask(w, h, panel_rect, actor_side=actor_side, mask_center=mask_center)
        mask_img.save(str(mask_png), format="PNG")

        panel_img, (wf_rx, wf_ry, wf_w, wf_h) = build_popup_panel_png(avatar_path, pw, ph, pad=pad)
        panel_img.save(str(panel_png), format="PNG")

        # Layer 1 dynamic alpha envelope alpha(t) per memo §7.2:
        # t < tg: 0 | tg..tg+0.07: 0.90 | tg+0.07..tg+0.14: 0.30 | tg+0.14..tg+0.20: 0.85 | >=tg+0.20: cyan_alpha + 0.05*sin(2*PI*T*1.8)
        tg = max(0.0, t_glitch)
        t1 = tg + 0.07
        t2 = tg + 0.14
        t3 = tg + 0.20
        alpha_expr = (
            f"if(lt(T,{tg:.3f}),0,"
            f"if(lt(T,{t1:.3f}),0.90,"
            f"if(lt(T,{t2:.3f}),0.30,"
            f"if(lt(T,{t3:.3f}),0.85,"
            f"({cyan_alpha:.3f}+0.05*sin(2*PI*T*1.8))))))"
        )

        # Panel screen coordinates (accounting for outer glow padding)
        ox = px - pad
        oy = py - pad

        # Entry flicker enable for UI panel: visible from tg onward except 2-frame glitch blink [t1, t2]
        ui_enable = f"gte(t,{tg:.3f})*(1-between(t,{t1:.3f},{t2:.3f}))"

        # Delay audio to t_glitch (in ms) so waveform strip & voice start simultaneously at glitch-in
        delay_ms = int(round(tg * 1000.0))

        # Shared 3% camera breath on Layers 0-2 (welds actor + cyan grade + UI into one shot)
        if camera_breath:
            sw = int(round(w * 1.03))
            sh = int(round(h * 1.03))
            # Make even dimensions
            sw += sw % 2
            sh += sh % 2
            dx_max = (sw - w) // 2
            dy_max = (sh - h) // 2
            breath_chain = (
                f"scale={sw}:{sh}:flags=lanczos,"
                f"crop={w}:{h}:"
                f"x='{dx_max}+round({max(1, dx_max - 2)}*0.35*sin(2*PI*t/4.0))':"
                f"y='{dy_max}+round({max(1, dy_max - 2)}*0.30*cos(2*PI*t/3.4))',"
                f"setsar=1,format=yuv420p"
            )
        else:
            breath_chain = "setsar=1,format=yuv420p"

        # Build complete 4-layer ffmpeg filter_complex
        # Inputs:
        #   0: plate video
        #   1: mask_cyan.png (looped 1/4 res grayscale)
        #   2: panel_ui.png (looped RGBA popup geometry + avatar, zero text)
        #   3: sys audio (drives showwaves AND audible track)
        filter_complex = (
            # Layer 0: Clean Actor Plate
            f"[0:v]fps={fps_int},scale={w}:{h},setsar=1,format=yuv420p,split=2[v0_base][v0_src];"
            # Layer 1: Directional cyan colorbalance grade + feathered dynamic mask + maskedmerge
            f"[v0_src]colorbalance=rs=-0.18:gs=0.14:bs=0.28:rm=-0.14:gm=0.12:bm=0.24:rh=-0.08:gh=0.10:bh=0.18,"
            f"eq=brightness=0.05:contrast=1.06,format=yuv420p[v0_graded];"
            f"[1:v]fps={fps_int},format=yuv420p,"
            f"geq=lum='clip(lum(X,Y)*({alpha_expr}),0,255)':cb=128:cr=128,"
            f"scale={w}:{h}:flags=bilinear,format=yuv420p[mask_dyn];"
            f"[v0_base][v0_graded][mask_dyn]maskedmerge[v1_lit];"
            # Audio prep: delayed sys voice for both showwaves and output audio mix
            f"[3:a]atrim=start={audio_offset:.3f},asetpts=PTS-STARTPTS,"
            f"adelay={delay_ms}|{delay_ms},apad,atrim=0:{dur:.3f},asplit=2[a_wave][a_mix];"
            # Layer 2: Audio-driven showwaves strip composited inside popup panel RGBA
            f"[a_wave]showwaves=s={wf_w}x{wf_h}:mode=cline:rate={fps_int}:colors=0x22D3EE|0xA5F3FC:scale=sqrt,"
            f"format=rgba,colorkey=black:0.06:0.12[wave_rgba];"
            f"[2:v]fps={fps_int},format=rgba[panel_rgba];"
            f"[panel_rgba][wave_rgba]overlay=x={wf_rx}:y={wf_ry}:shortest=1:format=auto[ui_live];"
            # Layer 3: Overlay live UI with hover float + entry flicker + chromatic glitch pulse + shared camera breath
            f"[v1_lit]format=rgba[v1_rgba];"
            f"[v1_rgba][ui_live]overlay=x={ox}:y='{oy}+3*sin(2*PI*t/3.2)':enable='{ui_enable}':format=auto,"
            f"rgbashift=rh=-10:bh=10:enable='between(t,{tg:.3f},{t3:.3f})',"
            f"{breath_chain}[vout]"
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            "ffmpeg",
            "-y",
            "-v", "error",
            "-ss", f"{start_sec:.3f}",
            "-t", f"{dur:.3f}",
            "-i", str(plate_path),
            "-loop", "1", "-t", f"{dur:.3f}", "-i", str(mask_png),
            "-loop", "1", "-t", f"{dur:.3f}", "-i", str(panel_png),
            "-i", str(audio_path),
            "-filter_complex", filter_complex,
            "-map", "[vout]",
            "-map", "[a_mix]",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "18",
            "-c:a", "aac",
            "-b:a", "160k",
            "-t", f"{dur:.3f}",
            "-movflags", "+faststart",
            str(output_path),
        ]
        subprocess.run(cmd, check=True)


def _parse_rect(rect_str: str) -> Tuple[int, int, int, int]:
    parts = [int(x.strip()) for x in rect_str.split(",")]
    if len(parts) != 4 or parts[2] <= 0 or parts[3] <= 0:
        raise ValueError(f"Invalid --panel-rect {rect_str!r}; expected 'x,y,w,h'")
    return (parts[0], parts[1], parts[2], parts[3])


def _parse_mask_center(s: Optional[str]) -> Optional[Tuple[float, float, float, float]]:
    if not s:
        return None
    parts = [float(x.strip()) for x in s.split(",")]
    if len(parts) != 4:
        raise ValueError(f"Invalid --mask-center {s!r}; expected 'cx,cy,rx,ry' normalized 0..1")
    return (parts[0], parts[1], parts[2], parts[3])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="SYS-01 4-Layer Composite Template (AMD-05: Pillow + ffmpeg)"
    )
    parser.add_argument("--plate", help="Clean actor plate video clip (.mp4)")
    parser.add_argument("--avatar", help="Avatar still image (.png/.jpg); if omitted with --make-default-avatar, generates one")
    parser.add_argument("--panel-rect", default="390,260,305,540", help="Popup rect 'x,y,w,h' in plate pixels")
    parser.add_argument("--audio", help="System audio file (.mp3/.wav) driving showwaves & voice track")
    parser.add_argument("--output", help="Output composited video path (.mp4)")
    parser.add_argument("--start", type=float, default=0.0, help="Start offset in plate clip (seconds)")
    parser.add_argument("--duration", type=float, default=3.0, help="Output duration (seconds)")
    parser.add_argument("--t-glitch", type=float, default=0.35, help="Glitch-in trigger time (seconds)")
    parser.add_argument("--actor-side", choices=["left", "right"], default="left", help="Side of frame where actor stands")
    parser.add_argument("--cyan-alpha", type=float, default=0.68, help="Hold cyan spill intensity (0..1)")
    parser.add_argument("--mask-center", default=None, help="Optional normalized actor cyan spill mask 'cx,cy,rx,ry'")
    parser.add_argument("--audio-offset", type=float, default=0.0, help="Start offset inside audio file (seconds)")
    parser.add_argument("--no-camera-breath", action="store_true", help="Disable 3%% shared camera breath")
    parser.add_argument("--make-default-avatar", help="Generate default geometric silhouette avatar PNG at this path and exit")
    args = parser.parse_args()

    if args.make_default_avatar:
        out_av = generate_default_avatar(Path(args.make_default_avatar))
        print(f"GENERATED DEFAULT AVATAR: {out_av} ({out_av.stat().st_size:,} bytes)")
        return 0

    for req_name in ("plate", "avatar", "audio", "output"):
        if not getattr(args, req_name):
            parser.error(f"--{req_name} is required")

    plate = Path(args.plate)
    avatar = Path(args.avatar)
    audio = Path(args.audio)
    output = Path(args.output)

    for label, p in (("plate", plate), ("avatar", avatar), ("audio", audio)):
        if not p.is_file():
            print(f"ERROR: {label} file not found: {p}", file=sys.stderr)
            return 2

    rect = _parse_rect(args.panel_rect)
    mc = _parse_mask_center(args.mask_center)

    composite_sys01(
        plate_path=plate,
        avatar_path=avatar,
        panel_rect=rect,
        audio_path=audio,
        output_path=output,
        start_sec=args.start,
        duration_sec=args.duration,
        t_glitch=args.t_glitch,
        actor_side=args.actor_side,
        cyan_alpha=args.cyan_alpha,
        mask_center=mc,
        audio_offset=args.audio_offset,
        camera_breath=not args.no_camera_breath,
    )

    w, h, fps, dur = probe_video(output)
    print(
        f"COMPOSITED SYS-01: {output} "
        f"({w}x{h}, {fps:.2f}fps, {dur:.2f}s, {output.stat().st_size:,} bytes)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
