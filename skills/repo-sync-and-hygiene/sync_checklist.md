# Repo Sync Pre-Push Checklist

> Grounded in `sync_batch1.sh`, `sync_batch2.sh`, `ASSET_PROD_REPORT.md` §4.3 (`857e719`), and `SYS01_DIRECTION_PATCH_REPORT.md` §1 (`1bd6712`).

Verify every item before running `git push`:

- [ ] **1. Base branch verified**: Ran `git fetch origin` and branched from the latest production `agy/*` branch (or explicitly instructed base), NOT stale local state.
- [ ] **2. New `agy/*` branch active**: `git branch --show-current` matches `agy/<topic>-YYYYMMDD` and is **NOT `main`**.
- [ ] **3. Canonical path mapping**: Every copied file follows `vm_to_repo_path_map.yaml` (no accidental hyphen/underscore duplicates like `STORYBOARD-SPEC-V2.md` next to `STORYBOARD_SPEC_V2.md`).
- [ ] **4. Zero binaries & zero secrets**: No `.jpg`/`.jpeg`/`.png`/`.mp4`/`.wav`/`.mp3`/`.safetensors`, no `secrets/`, no raw `*.log`/`*.out`, and no staged file `> 500 KB`.
- [ ] **5. In-clone selftests PASS**:
  - `python3 tools/preflight_gate.py --selftest` → `64/64 PASS` (or current updated count)
  - `python3 tools/diff_sheet_gen.py --selftest` → `15/15 PASS` (or current updated count)
- [ ] **6. Diff sanity review**: `git status --short` and `git diff --stat` contain ONLY in-scope changes with zero unintended deletions.
- [ ] **7. Push target verified**: `GIT_SSH_COMMAND="ssh -i ~/.ssh/github-second-civilization" git push -u origin agy/<topic>-YYYYMMDD` (`main` untouched).
- [ ] **8. Provenance logged**: Recorded branch name, base commit SHA, new commit SHA, synced file list, and selftest results in `~/drama-line/<TASK>_REPORT.md`.
