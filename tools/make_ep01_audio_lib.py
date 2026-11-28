#!/usr/bin/env python3
"""
make_ep01_audio_lib.py — Build shared 48kHz stereo roomtone & Foley library
at ~/drama-line/audio_lib/ (100% CPU synthesis, zero ElevenLabs/paid spend).
"""
from __future__ import annotations

import math
import shutil
import wave
from pathlib import Path
import numpy as np

ROOT = Path("/home/hatch/drama-line")
OUT_DIR = ROOT / "audio_lib"
SR = 48000


def write_stereo_wav(path: Path, left: np.ndarray, right: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Apply 0.15s edge cosine crossfade-ready envelope (very gentle loop seam protection)
    stereo = np.stack([left, right], axis=-1)
    stereo = np.clip(stereo, -0.95, 0.95)
    pcm = (stereo * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())


def normalize_rms_dbfs(left: np.ndarray, right: np.ndarray, target_dbfs: float):
    comb = np.concatenate([left, right])
    rms = float(np.sqrt(np.mean(comb ** 2) + 1e-12))
    gain = (10.0 ** (target_dbfs / 20.0)) / rms
    l_out = left * gain
    r_out = right * gain
    peak = max(float(np.max(np.abs(l_out))), float(np.max(np.abs(r_out))), 1e-9)
    if peak > 0.85:
        l_out *= 0.85 / peak
        r_out *= 0.85 / peak
    return l_out, r_out


def fft_shaped(n: int, seed: int, shape_fn) -> np.ndarray:
    rng = np.random.default_rng(seed)
    w = rng.standard_normal(n)
    freqs = np.fft.rfftfreq(n, 1.0 / SR)
    spec = np.fft.rfft(w)
    filt = shape_fn(freqs)
    return np.fft.irfft(spec * filt, n=n)


def make_taihu_night_reed(dur_sec: float = 30.0, target_dbfs: float = -24.0) -> Path:
    """S00: Night lakeside reeds rustling in dark breeze + gentle dark shore water."""
    n = int(dur_sec * SR)
    t = np.linspace(0.0, dur_sec, n, endpoint=False)

    # Low dark open-water ambient rumble
    def water_filt(f):
        fl = 1.0 / np.maximum(f, 20.0) ** 0.85
        fl *= np.exp(-((f / 520.0) ** 2))
        fl[f < 30.0] *= (f[f < 30.0] / 30.0) ** 2
        return fl

    # Soft dry reed rustle band (1.4k - 4.8kHz) modulated by slow wind gusts
    def reed_filt(f):
        return np.exp(-((f - 2800.0) / 1450.0) ** 2) * (f > 650.0)

    wl = fft_shaped(n, 101, water_filt)
    wr = fft_shaped(n, 102, water_filt)
    rl = fft_shaped(n, 103, reed_filt)
    rr = fft_shaped(n, 104, reed_filt)

    wave_mod_l = 0.72 + 0.28 * np.sin(2 * math.pi * 0.17 * t + 0.2) + 0.12 * np.sin(2 * math.pi * 0.31 * t)
    wave_mod_r = 0.72 + 0.28 * np.sin(2 * math.pi * 0.17 * t + 1.1) + 0.12 * np.sin(2 * math.pi * 0.29 * t)
    gust_l = np.clip(0.35 + 0.45 * np.sin(2 * math.pi * 0.09 * t + 0.5) + 0.25 * np.sin(2 * math.pi * 0.21 * t), 0.08, 1.0)
    gust_r = np.clip(0.35 + 0.45 * np.sin(2 * math.pi * 0.09 * t + 1.3) + 0.25 * np.sin(2 * math.pi * 0.19 * t), 0.08, 1.0)

    # Normalize components before mixing
    wl /= np.std(wl) + 1e-9
    wr /= np.std(wr) + 1e-9
    rl /= np.std(rl) + 1e-9
    rr /= np.std(rr) + 1e-9

    left = (0.76 * wl + 0.24 * wr) * wave_mod_l * 0.75 + rl * gust_l * 0.28
    right = (0.76 * wr + 0.24 * wl) * wave_mod_r * 0.75 + rr * gust_r * 0.28

    # Faint shoreline water lap events
    for lap_t, pan in [(2.4, 0.35), (7.9, 0.65), (14.2, 0.4), (20.6, 0.6), (26.1, 0.45)]:
        idx = int(lap_t * SR)
        llen = int(0.85 * SR)
        if idx + llen < n:
            lt = np.linspace(0.0, 0.85, llen, endpoint=False)
            env = np.sin(math.pi * lt / 0.85) ** 2
            lap_noise = fft_shaped(llen, int(lap_t * 100), lambda f: np.exp(-((f - 620.0) / 380.0) ** 2))
            lap_noise /= np.std(lap_noise) + 1e-9
            left[idx:idx + llen] += lap_noise * env * 0.22 * (1.0 - pan)
            right[idx:idx + llen] += lap_noise * env * 0.22 * pan

    left, right = normalize_rms_dbfs(left, right, target_dbfs)
    out = OUT_DIR / "roomtone" / "taihu_night_reed_48k.wav"
    write_stereo_wav(out, left, right)
    return out


def make_taihu_dawn_water(dur_sec: float = 30.0, target_dbfs: float = -24.0) -> Path:
    """S01/S16b/DEMO-03 S0: Misty dawn open lake stillness, gentle wooden skiff water lap."""
    n = int(dur_sec * SR)
    t = np.linspace(0.0, dur_sec, n, endpoint=False)

    def mist_filt(f):
        fl = 1.0 / np.maximum(f, 25.0) ** 0.92
        fl *= np.exp(-((f / 680.0) ** 2))
        fl[f < 25.0] *= (f[f < 25.0] / 25.0) ** 2
        return fl

    def air_filt(f):
        return np.exp(-((f - 1200.0) / 700.0) ** 2) * (f > 250.0)

    ml = fft_shaped(n, 201, mist_filt)
    mr = fft_shaped(n, 202, mist_filt)
    al = fft_shaped(n, 203, air_filt)
    ar = fft_shaped(n, 204, air_filt)
    for arr in (ml, mr, al, ar):
        arr /= np.std(arr) + 1e-9

    swell = 0.85 + 0.15 * np.sin(2 * math.pi * 0.12 * t)
    left = (0.75 * ml + 0.25 * mr) * swell * 0.82 + al * 0.14
    right = (0.75 * mr + 0.25 * ml) * swell * 0.82 + ar * 0.14

    # Soft hull water laps
    for lap_t, pan in [(1.8, 0.42), (6.5, 0.58), (11.7, 0.36), (17.3, 0.64), (23.0, 0.48), (27.8, 0.55)]:
        idx = int(lap_t * SR)
        llen = int(0.65 * SR)
        if idx + llen < n:
            lt = np.linspace(0.0, 0.65, llen, endpoint=False)
            env = np.sin(math.pi * lt / 0.65) ** 1.8
            lap = fft_shaped(llen, int(lap_t * 100) + 50, lambda f: np.exp(-((f - 480.0) / 280.0) ** 2))
            lap /= np.std(lap) + 1e-9
            left[idx:idx + llen] += lap * env * 0.30 * (1.0 - pan)
            right[idx:idx + llen] += lap * env * 0.30 * pan

    left, right = normalize_rms_dbfs(left, right, target_dbfs)
    out = OUT_DIR / "roomtone" / "taihu_dawn_water_48k.wav"
    write_stereo_wav(out, left, right)
    return out


def make_taipei_street_crowd(dur_sec: float = 30.0, target_dbfs: float = -24.0) -> Path:
    """S02-S04c: 2022 Taipei dusk urban street bed — distant traffic wash, diffuse non-intelligible murmur."""
    n = int(dur_sec * SR)
    t = np.linspace(0.0, dur_sec, n, endpoint=False)

    def traffic_filt(f):
        fl = 1.0 / np.maximum(f, 32.0) ** 0.78
        fl *= np.exp(-((f / 1100.0) ** 2))
        fl[f < 35.0] *= (f[f < 35.0] / 35.0) ** 2
        return fl

    def crowd_air_filt(f):
        return (
            0.7 * np.exp(-((f - 520.0) / 240.0) ** 2)
            + 0.45 * np.exp(-((f - 1250.0) / 480.0) ** 2)
        ) * (f > 180.0)

    tl = fft_shaped(n, 301, traffic_filt)
    tr = fft_shaped(n, 302, traffic_filt)
    cl = fft_shaped(n, 303, crowd_air_filt)
    cr = fft_shaped(n, 304, crowd_air_filt)
    for arr in (tl, tr, cl, cr):
        arr /= np.std(arr) + 1e-9

    # Slow traffic surge + subtle passing vehicle whooshes
    surge_l = 0.8 + 0.2 * np.sin(2 * math.pi * 0.08 * t) + 0.1 * np.sin(2 * math.pi * 0.19 * t)
    surge_r = 0.8 + 0.2 * np.sin(2 * math.pi * 0.08 * t + 0.7) + 0.1 * np.sin(2 * math.pi * 0.19 * t + 0.9)

    left = (0.70 * tl + 0.30 * tr) * surge_l * 0.78 + cl * 0.24
    right = (0.70 * tr + 0.30 * tl) * surge_r * 0.78 + cr * 0.24

    # Distant muffled scooter/car pass-by swells (L->R and R->L)
    for pass_t, direction in [(4.5, 1), (13.0, -1), (22.5, 1)]:
        idx = int(pass_t * SR)
        plen = int(2.6 * SR)
        if idx + plen < n:
            pt = np.linspace(0.0, 2.6, plen, endpoint=False)
            env = np.sin(math.pi * pt / 2.6) ** 2
            pan = (pt / 2.6) if direction > 0 else (1.0 - pt / 2.6)
            veh = fft_shaped(plen, int(pass_t * 100) + 9, lambda f: np.exp(-((f - 280.0) / 180.0) ** 2))
            veh /= np.std(veh) + 1e-9
            left[idx:idx + plen] += veh * env * 0.35 * (1.0 - 0.55 * pan)
            right[idx:idx + plen] += veh * env * 0.35 * (0.45 + 0.55 * pan)

    left, right = normalize_rms_dbfs(left, right, target_dbfs)
    out = OUT_DIR / "roomtone" / "taipei_street_crowd_48k.wav"
    write_stereo_wav(out, left, right)
    return out


def make_studio_night_hum(dur_sec: float = 30.0, target_dbfs: float = -26.0) -> Path:
    """S06-S12, S17a-S19: Quiet small 2026 Taipei night studio — dry room air, subtle 60/120Hz hum, muffled city low."""
    n = int(dur_sec * SR)
    t = np.linspace(0.0, dur_sec, n, endpoint=False)

    def room_filt(f):
        fl = 1.0 / np.maximum(f, 24.0) ** 1.05
        fl *= np.exp(-((f / 420.0) ** 2))
        fl[f < 30.0] *= (f[f < 30.0] / 30.0) ** 2
        return fl

    rl = fft_shaped(n, 401, room_filt)
    rr = fft_shaped(n, 402, room_filt)
    rl /= np.std(rl) + 1e-9
    rr /= np.std(rr) + 1e-9

    # Restrained AC/monitor hum (Taiwan 60Hz mains + soft 120Hz harmonic)
    hum = 0.14 * np.sin(2 * math.pi * 60.0 * t) + 0.08 * np.sin(2 * math.pi * 120.0 * t + 0.3) + 0.025 * np.sin(2 * math.pi * 180.0 * t)
    drift = 1.0 + 0.04 * np.sin(2 * math.pi * 0.07 * t)
    left = (0.85 * rl + 0.15 * rr) * drift + hum
    right = (0.85 * rr + 0.15 * rl) * drift + hum * 0.96

    left, right = normalize_rms_dbfs(left, right, target_dbfs)
    out = OUT_DIR / "roomtone" / "studio_night_hum_48k.wav"
    write_stereo_wav(out, left, right)
    return out


def make_ancient_hall_torch(dur_sec: float = 30.0, target_dbfs: float = -24.0) -> Path:
    """S13-S15b: Spring-Autumn wooden hall dark stillness + subtle oil/torch flame flutter & distant crackle."""
    n = int(dur_sec * SR)
    t = np.linspace(0.0, dur_sec, n, endpoint=False)

    def hall_filt(f):
        fl = 1.0 / np.maximum(f, 18.0) ** 1.0
        fl *= np.exp(-((f / 340.0) ** 2))
        fl[f < 22.0] *= (f[f < 22.0] / 22.0) ** 2
        return fl

    def flame_filt(f):
        return np.exp(-((f - 180.0) / 110.0) ** 2) * (f > 45.0)

    hl = fft_shaped(n, 501, hall_filt)
    hr = fft_shaped(n, 502, hall_filt)
    fl = fft_shaped(n, 503, flame_filt)
    fr = fft_shaped(n, 504, flame_filt)
    for arr in (hl, hr, fl, fr):
        arr /= np.std(arr) + 1e-9

    flutter_l = 0.6 + 0.4 * np.sin(2 * math.pi * 1.9 * t) * np.sin(2 * math.pi * 0.37 * t + 0.4)
    flutter_r = 0.6 + 0.4 * np.sin(2 * math.pi * 2.1 * t + 0.8) * np.sin(2 * math.pi * 0.41 * t)

    left = (0.78 * hl + 0.22 * hr) * 0.72 + fl * flutter_l * 0.36
    right = (0.78 * hr + 0.22 * hl) * 0.72 + fr * flutter_r * 0.36

    # Subtle sparse dry pine-torch crackles (very restrained)
    rng = np.random.default_rng(509)
    for ct in rng.uniform(0.8, dur_sec - 0.5, size=26):
        idx = int(ct * SR)
        clen = int(0.018 * SR)
        if idx + clen < n:
            ct_arr = np.linspace(0.0, 0.018, clen, endpoint=False)
            env = np.exp(-ct_arr * 260.0)
            pop = rng.standard_normal(clen) * env
            pan = float(rng.uniform(0.2, 0.8))
            amp = float(rng.uniform(0.18, 0.45))
            left[idx:idx + clen] += pop * amp * (1.0 - pan)
            right[idx:idx + clen] += pop * amp * pan

    left, right = normalize_rms_dbfs(left, right, target_dbfs)
    out = OUT_DIR / "roomtone" / "ancient_hall_torch_48k.wav"
    write_stereo_wav(out, left, right)
    return out


def make_s00_sword_draw_1inch(target_dbfs: float = -18.0) -> Path:
    """S00 Foley: Bronze Yue sword pushed/drawn 1 inch from matte lacquered wood scabbard (1.1s, realistic dry scrape)."""
    dur = 1.1
    n = int(dur * SR)
    t = np.linspace(0.0, dur, n, endpoint=False)

    # Phase 1 (0.08-0.20s): thumb/guard unseat subtle dull bronze click
    click = np.zeros(n)
    c0 = int(0.10 * SR)
    clen = int(0.045 * SR)
    ct = np.linspace(0.0, 0.045, clen, endpoint=False)
    click_sig = (
        0.5 * np.sin(2 * math.pi * 920.0 * ct)
        + 0.35 * np.sin(2 * math.pi * 1680.0 * ct)
        + 0.25 * np.sin(2 * math.pi * 2450.0 * ct)
    ) * np.exp(-ct * 110.0)
    click[c0:c0 + clen] = click_sig

    # Phase 2 (0.16-0.78s): muted bronze-on-lacquered-wood sliding friction + faint bronze resonance
    scrape_noise = fft_shaped(n, 601, lambda f: (
        0.85 * np.exp(-((f - 2300.0) / 950.0) ** 2)
        + 0.45 * np.exp(-((f - 4200.0) / 1100.0) ** 2)
        + 0.35 * np.exp(-((f - 680.0) / 260.0) ** 2)
    ) * (f > 220.0))
    scrape_noise /= np.std(scrape_noise) + 1e-9

    slide_env = np.zeros(n)
    s0, s1 = int(0.16 * SR), int(0.76 * SR)
    st = np.linspace(0.0, 1.0, s1 - s0, endpoint=False)
    # Smooth ease-in-out sliding velocity with micro stick-slip texture
    slide_env[s0:s1] = (np.sin(math.pi * st) ** 1.3) * (0.85 + 0.15 * np.sin(2 * math.pi * 19.0 * st))

    # Very subtle dark bronze modal ring (NOT Hollywood bright steel shing!)
    ring_env = np.zeros(n)
    r0, r1 = int(0.18 * SR), int(0.95 * SR)
    rt = np.linspace(0.0, (r1 - r0) / SR, r1 - r0, endpoint=False)
    ring_env[r0:r1] = np.clip(rt / 0.08, 0.0, 1.0) * np.exp(-rt * 4.8)
    bronze_ring = (
        0.45 * np.sin(2 * math.pi * 1420.0 * t)
        + 0.25 * np.sin(2 * math.pi * 2190.0 * t)
        + 0.15 * np.sin(2 * math.pi * 3110.0 * t)
    ) * ring_env

    # Soft stop detent at 0.74s
    stop = np.zeros(n)
    d0 = int(0.74 * SR)
    dlen = int(0.03 * SR)
    dt = np.linspace(0.0, 0.03, dlen, endpoint=False)
    stop[d0:d0 + dlen] = np.sin(2 * math.pi * 540.0 * dt) * np.exp(-dt * 140.0) * 0.35

    sig = click * 0.55 + scrape_noise * slide_env * 0.65 + bronze_ring * 0.22 + stop
    # Slight anatomical-left-hip stereo bias (pan ~0.38 L / 0.62 R -> subtle)
    left = sig * 0.92
    right = sig * 1.00
    left, right = normalize_rms_dbfs(left, right, target_dbfs)
    out = OUT_DIR / "sfx" / "s00_sword_draw_1inch_48k.wav"
    write_stereo_wav(out, left, right)
    return out


def main() -> int:
    # Copy existing alley roomtone into shared audio_lib/roomtone/ (keep demo02_v2 copy intact for zero broken refs)
    src_alley = ROOT / "demo02_v2" / "audio_lib" / "roomtone" / "alley_night_wet_48k.wav"
    dst_alley = OUT_DIR / "roomtone" / "alley_night_wet_48k.wav"
    dst_alley.parent.mkdir(parents=True, exist_ok=True)
    if src_alley.is_file() and not dst_alley.is_file():
        shutil.copy2(src_alley, dst_alley)
        print(f"Copied shared roomtone -> {dst_alley}")

    # Also copy existing sfx to shared audio_lib/sfx/ for completeness
    for sfx_name in ("distant_scooter_alarm_chirp.wav", "sys01_glitch_ignition_pulse.wav"):
        s = ROOT / "demo02_v2" / "audio_lib" / "sfx" / sfx_name
        d = OUT_DIR / "sfx" / sfx_name
        d.parent.mkdir(parents=True, exist_ok=True)
        if s.is_file() and not d.is_file():
            shutil.copy2(s, d)

    created = [
        make_taihu_night_reed(),
        make_taihu_dawn_water(),
        make_taipei_street_crowd(),
        make_studio_night_hum(),
        make_ancient_hall_torch(),
        make_s00_sword_draw_1inch(),
    ]
    for p in created:
        print(f"OK {p.relative_to(ROOT)} ({p.stat().st_size:,} B)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
