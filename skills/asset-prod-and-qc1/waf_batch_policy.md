# Google Flow `nano2` WAF 403 Batching Policy

> Grounded directly in `~/drama-line/EP01_ASSET_GAP_REVIEW_AGY_MEMO.md` §5.1, `~/drama-line/tools/run_gflow_helper.py`, `~/drama-line/EP01_PREP_REPORT.md` §3, and `~/drama-line/ASSET_PROD_REPORT.md` §1 & §2.4 (17/17 `nano2` stills with **0 WAF 403**).

## Historical Grounding

- **Failure trigger (`EP01_PREP_REPORT.md` §3, 2026-11-28 `09:06Z`)**: Unthrottled `gen_candidates.py` submitted back-to-back `t2i` calls with `0s` spacing immediately after a heavy Flow video batch → triggered `WafRejectionError` (`HTTP 403 PUBLIC_ERROR_UNUSUAL_ACTIVITY`, gRPC 7, exit `10`) on image #2.
- **Proven safe operating envelope (`DEMO02_v2` Stage 3 + `ASSET_PROD_REPORT.md`)**: Sequential `nano2` calls via `tools/run_gflow_helper.py` in small batches (`3–4` images/batch) with `≥ 55–87s` inter-image spacing and CPU-work breaks between batches achieved **4/4 (`DEMO02_v2`) + 17/17 (`EP-01 Asset Prod`) = 21/21 stills with 0 WAF 403**.

## Four Mandatory WAF Rules (Zero-Bypass Discipline)

1. **Session Batch Cap (`≤ 3–4` images/batch)**:
   - Never exceed `4` `nano2` image calls in one contiguous session.
2. **Inter-Image Cooldown (`≥ 45–60s`, recommended `55–85s`) + Visual Inspection**:
   - Inspect each generated image (telemetry + visual sanity) and wait `≥ 45–60s` before issuing the next `run_gflow_helper.py` call.
   - **Never run a tight unthrottled `for` loop over `gflow image`.**
3. **Inter-Batch Spacing (`≥ 30–45 min`) & Video Separation**:
   - Interleave pure CPU work (Pillow crops, YAML/registry updates, audio synthesis, selftest patches) or ElevenLabs API calls between `nano2` batches.
   - Do **not** launch a `nano2` batch immediately after a heavy Flow video generation burst.
4. **Hard Stop on HTTP 403 / Exit Code 10 (Zero-Retry / Zero-Bypass)**:
   - Always call Flow via `python3 ~/drama-line/tools/run_gflow_helper.py`, which checks `rc == 10`, `wafrejectionerror`, `public_error_unusual_activity`, and `http 403` / `403 forbidden`, prints `WAF_403_STOP`, and exits with code **`10`**.
   - On exit `10`: **STOP the batch immediately**, append the UTC timestamp and error tail to `*_PROGRESS.log`, and report to the Creator. **NEVER auto-retry, rotate headers/proxies, or attempt any WAF/CAPTCHA workaround.**

## Canonical Invocation

```bash
python3 ~/drama-line/tools/run_gflow_helper.py image \
  --mode i2i \
  --model nano2 \
  --aspect 9:16 \
  --ref ~/drama-line/casting/scenes/LOC-FANLI-STUDIO-26/loc-fanli-studio-26-desk.jpg \
  --prompt "<positive Traditional Chinese prompt>" \
  --out ~/drama-line/casting/scenes/LOC-FANLI-STUDIO-26/loc-fanli-studio-26-window.jpg \
  --log-json ~/drama-line/tmp/loc_studio_window.json
```
