# Production System Sync — Batch 1 (2026-11-28)

Synced by Muse at the Creator's direction (option B: finalized documents now; batch 2 after the full-process mandate completes). Branch: `agy/production-system-sync-20261128`. Main is untouched.

## What this batch contains

**Specs & decision-grade documents (`docs/`)**
- `STORYBOARD_SPEC_V2.md` — storyboard spec v2.2 (segments + atomic shots, director layer Appendix B incl. B.8 QC-D first ruling, workflow amendments Appendix C AMD-01–07, §九 demo-mode boundary clause). NOTE: v2.3 integration is in progress under the agy full-process mandate; batch 2 will supersede this file.
- `WORKFLOW_POSTMORTEM_DEMO02.md` — DEMO-02 failure post-mortem (six QC-D failure classes traced to process causes).
- `DEMO02_DIRECTOR_STATEMENT.md` — DEMO-02 director statement (spec v2.1 Appendix B format).

**Discussion memos, research & test results (`docs/memos/`)**
- Storyboard spec v2 gap analysis + agy spec memo; director-layer draft + agy memo; camera workflow agy memo + H3 camera control ref + clay previs tools ref.
- H3 consistency/camera: user-supplied community survey (REF) + agy verification memo.
- Workflow v2 amendment agy memo (AMD-01–07 source) + gate tools delivery note.
- Post-production chain agy memo + user-supplied editing tools ref.
- Seedance 2.5 ecosystem research (Creator ruling 2026-11-28: borrow methods only, engine stays H3) + cinematic prompt-craft ref (Creator-supplied).
- V2.3 amendment agy memo (Seedance borrowing + cinematic craft, per-item ADAPT verdicts; integration in progress).
- SM7A_RESULT — H3 native 4-ref Ref2VA vs 1-ref smoke test: ADOPT WITH CONDITIONS as the dialogue-CU carrier baseline.
- CLAY_TEST_RESULT — L3 clay previs → H3 Ref2VA smoke test: ADOPT WITH CONDITIONS (0–2 hero shots/episode; CozyClay not agent-operable on the current VM, fallback renderer used).
- SCORECARD_V2_PROPOSAL + DRYRUN_EP01_ARRIVAL_V032 — script scoring card v2 and the EP-01 dry-run script v0.3.2 (Gate A3 verdict still pending with the Creator).

**Tools (`tools/`)** — zero-new-dependency Python, selftests passing (15/15 + 10/10)
- `preflight_gate.py` — script_pack hard gate (routing lock, prompt hygiene, SYS-01 ban, same-location derivation, scale-jump ban).
- `diff_sheet_gen.py` — QC-1/QC-2 cross-shot diff sheets + SHA256 gate-token verification.
- `sys01_composite.py` — SYS-01 popup 4-layer compositor (Pillow + ffmpeg).

## Not in this batch (by design)
- Binary assets (casting masters incl. the patched `fanli-master-ancient-45R.jpg` and the Creator's Doubao modern character card, demo clips, strips) live on the production VM `~/drama-line/` and Muse's workspace, not in git.
- Batch 2 (after the mandate): integrated spec v2.3, DEMO02_v2 repaired cut documentation + FULL_RUN_REPORT.
