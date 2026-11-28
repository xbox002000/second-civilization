# Progress Ledger Schema (`*_PROGRESS.log`)

> Grounded in `~/drama-line/ASSET_PROD_PROGRESS.log`, `RECOVERY_PROGRESS.log`, `SKILLIFY_G_PROGRESS.log`, and `FULL_RUN_PROGRESS.log` (2026-11-28).

## Purpose

An append-only plain-text checkpoint ledger stored at `~/drama-line/<TASK>_PROGRESS.log`. It decouples multi-phase run state from any single LLM context window so a continuation round (possibly on a different model pool after a 429 or timeout) can resume with zero duplicate work or double-spend.

## Line Format

```text
<phase_id> <YYYY-MM-DDTHH:MM:SSZ>: <key=value pairs: artifacts, verdicts, spend deltas>
```

### Reserved Terminal Markers

| Marker | Meaning | Used By |
| :--- | :--- | :--- |
| `DONE` | Initial wrapper completed deliverable check (`ok()` passed) | `run_skillbuild.sh`, `run_recovery.sh`, `run_skillify_g.sh` |
| `CONTINUATION_DONE` | Continuation mandate completed all remaining phases and final report | `ASSET_PROD_PROGRESS.log` |
| `BLOCKED_429` / `INCOMPLETE` | Exhausted bounded probes/rounds; requires human/dispatcher intervention | `run_wrapper.sh.tmpl` |

## Real Proven Example (`~/drama-line/ASSET_PROD_PROGRESS.log`)

```text
fanli mind done, asset production starting 2026-11-28T11:50:31Z

phase_a_cpu_done 2026-11-28: sys01_crops=9/9_LOCKED sys01_yaml=OK fanli_modern_crops=2/2_OK audio_lib=6_roomtones+3_sfx_OK master_hygiene=8_moved_0_rm
phase_b_sm8_done 2026-11-28T12:02:40Z: verdict=GO_PASS (6/6 criteria, take=1/2, flow_pts=12/24, credits=786->774, cu=0.0, dL_span=2.70, max_blowout=0.19%, v9_text=0/5)
phase_a_batch2_done 2026-11-28T12:16:20Z: fanli-modern-ref-45R=LOCKED PROP-SWORD-01(3/3)=LOCKED preflight_v24_selftest=59/59_PASS spec_v24_merged=OK
phase_a_batch3_done 2026-11-28T12:23:10Z: PROP-SWORD-02(1/1)=LOCKED PROP-BAMBOO-01(2/2)=LOCKED docs/PROP_REGISTRY.md=OK diff_sheet_gen=15/15_PASS+SYS01_OK
phase_a_batch4_done 2026-11-28T12:31:00Z: LOC-TAIHU-NIGHT=LOCKED LOC-TAIHU-DAWN=LOCKED LOC-TAIPEI-STREET-2022(_main+_rev, dL=0.87, db=0.52)=LOCKED
round 1 finished 2026-11-28T12:33:19Z
round 2 finished 2026-11-28T12:33:21Z
round 3 finished 2026-11-28T12:33:24Z
DONE

continuation_batch5_done 2026-11-28T13:30:20Z: LOC-FANLI-STUDIO-26(_desk/_window/_tabletop)=LOCKED LOC-YUE-COURT=LOCKED LOC-WENZHONG-GATE=LOCKED docs/LOCATION_REGISTRY.md=OK ASSETS_MANIFEST.yaml(v2)=OK
continuation_sync_done 2026-11-28T13:34:26Z: branch=agy/asset-prod-v24-sm8-20261128 commit=857e71961eadf998152372edd61f4ed4bcaff56e (19 files, 0 binaries, main untouched) report=ASSET_PROD_REPORT.md
CONTINUATION_DONE
```

## Rules

1. **Append immediately after each bounded phase** (never wait until end of mandate).
2. **Always record spend deltas** (`flow_pts`, `credits=before->after`, `cu`, `tts_chars`) on any paid phase so a continuation round can verify remaining cap headroom.
3. **Never delete or rewrite prior lines** — append continuation lines below the interruption point so full audit provenance survives.
