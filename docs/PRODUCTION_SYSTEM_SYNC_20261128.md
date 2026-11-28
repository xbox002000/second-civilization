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

---

# Batch 2 + Repo HQ upgrade (2026-11-28, same branch)

Executed after the agy full-process mandate completed and Muse's receipt verification (frame-level spot-check against the six original QC-D failure classes: verified).

**Version note (honest bookkeeping)**
- `docs/STORYBOARD_SPEC_V2.md` and the `tools/` scripts were already at **v2.3** in batch 1: the mandate's Phase 1 integration landed (~15:24 Taipei) before the batch-1 snapshot was taken (~15:47), so batch 1's "v2.2" label in the section above was stale — the file content was v2.3 all along (Seedance-borrowing items 1–7, SM-7A 3 conditions, clay-test 4 conditions; preflight selftest 32/32). Batch 2 re-copied them and git confirms no content diff.

**New production records (`docs/memos/`)**
- `DEMO02_V2_FULL_RUN_REPORT.md` — the mandate's full run report (per-shot routes/takes/costs, gate JSONs, honest residual defects, EP-01 readiness).
- `DEMO02_V2_SCRIPT_PACK.json`, `DEMO02_V2_QC1_GATE.json`, `DEMO02_V2_QC2_GATE.json` — the production contract and signed gate records (SHA256-chained).

**New bible files**
- `bible/anchors/FANLI.yaml` — cross-shot identity anchor checklist; `bible/performance/MICRO_EXPRESSIONS.yaml` — micro-expression lexicon with intensity grades.

**Repo HQ upgrade (Creator-approved plan A)**
- `docs/PROJECT_STATUS.md` — the single current-state page: locked decisions, proven pipeline facts, pending Creator decisions, next steps.
- `docs/DECISIONS.md` — ADR backfill ADR-005…ADR-012 (face lock, voice lock, independent-account channel, H3 routing ruling, Omni default, Seedance borrow-only, 2022-entry canon, SYS-01 composite + demo boundary).
- `docs/ROADMAP.md` — two stale checkboxes corrected to reality (character look & voice Creator-confirmed 2026-11-27).
- `docs/ASSETS_MANIFEST.yaml` — asset registry (IDs, status, storage locations; binaries stay out of git).
