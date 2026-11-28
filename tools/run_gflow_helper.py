#!/usr/bin/env python3
"""
run_gflow_helper.py — Clean, WAF-safe wrapper around gflow image i2i/t2i and video i2v.
Strictly stops on WAF 403 (exit code 10 or HTTP 403 / UNUSUAL_ACTIVITY) without retrying.
Always converts image output to clean JPEG Q95 or PNG and logs telemetry JSON.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

GFLOW = "/home/hatch/.local/bin/gflow"


def check_waf(rc: int, out: str, err: str) -> bool:
    comb = (out + "\n" + err).lower()
    return (
        rc == 10
        or "wafrejectionerror" in comb
        or "public_error_unusual_activity" in comb
        or "http 403" in comb
        or "status 403" in comb
        or "403 forbidden" in comb
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("image")
    pi.add_argument("--mode", choices=["i2i", "t2i"], required=True)
    pi.add_argument("--prompt", required=True)
    pi.add_argument("--ref", action="append", default=[])
    pi.add_argument("--model", default="nano2")
    pi.add_argument("--aspect", default="9:16")
    pi.add_argument("--out", required=True)
    pi.add_argument("--log-json", default="")

    pv = sub.add_parser("video")
    pv.add_argument("--initial-frame", required=True)
    pv.add_argument("--prompt", required=True)
    pv.add_argument("--model", default="omni-1.2-flash")
    pv.add_argument("--aspect", default="9:16")
    pv.add_argument("--duration", type=int, default=4)
    pv.add_argument("--max-credits", type=int, default=24)
    pv.add_argument("--out", required=True)
    pv.add_argument("--log-json", default="")

    args = ap.parse_args()
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env.setdefault("DISPLAY", ":99")

    if args.cmd == "image":
        if args.mode == "i2i":
            cmd = [GFLOW, "image", "i2i", args.prompt]
            for r in args.ref:
                cmd.extend(["--ref", r])
        else:
            cmd = [GFLOW, "image", "t2i", args.prompt]
        cmd.extend([
            "--model", args.model,
            "--aspect", args.aspect,
            "--count", "1",
            "--out-file", str(out_path),
            "--json",
        ])
    else:
        cmd = [
            GFLOW, "video", "i2v",
            "--initial-frame", args.initial_frame,
            args.prompt,
            "--model", args.model,
            "--aspect", args.aspect,
            "--duration", str(args.duration),
            "--max-credits", str(args.max_credits),
            "--out-file", str(out_path),
            "--json",
        ]

    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    dt = round(time.time() - t0, 2)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if check_waf(proc.returncode, proc.stdout, proc.stderr):
        print(f"WAF_403_STOP ts={ts} rc={proc.returncode} elapsed={dt}s", file=sys.stderr)
        print("STDOUT:", proc.stdout[-1500:], file=sys.stderr)
        print("STDERR:", proc.stderr[-1500:], file=sys.stderr)
        return 10

    if proc.returncode != 0:
        print(f"GFLOW_ERROR ts={ts} rc={proc.returncode} elapsed={dt}s", file=sys.stderr)
        print("STDOUT:", proc.stdout[-2000:], file=sys.stderr)
        print("STDERR:", proc.stderr[-2000:], file=sys.stderr)
        return proc.returncode

    meta = {}
    start_i = proc.stdout.find("{")
    if start_i >= 0:
        try:
            meta = json.loads(proc.stdout[start_i:])
        except Exception:
            meta = {"raw_stdout": proc.stdout[-1000:]}

    if args.cmd == "image" and out_path.is_file() and out_path.suffix.lower() in (".jpg", ".jpeg"):
        from PIL import Image
        with Image.open(out_path) as im:
            im.convert("RGB").save(str(out_path), format="JPEG", quality=95, subsampling=0)

    sha = hashlib.sha256(out_path.read_bytes()).hexdigest() if out_path.is_file() else ""
    rec = {
        "cmd": args.cmd,
        "out": str(out_path),
        "bytes": out_path.stat().st_size if out_path.is_file() else 0,
        "sha256": sha,
        "elapsed_sec": dt,
        "timestamp": ts,
        "gflow_meta": meta,
    }
    if args.log_json:
        Path(args.log_json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.log_json).write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rec, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
