# Skill: `repo-sync-and-hygiene`

> **Status**: `distilled-from-run`  
> **Pipeline Coverage**: Inventory #12 — Repo Sync (`~/drama-line/` → `~/repos/sc-sync` on `agy/*`)  
> **Companion Files**: [vm_to_repo_path_map.yaml](vm_to_repo_path_map.yaml), [sync_checklist.md](sync_checklist.md)

---

## 1. Purpose & Trigger

**Purpose**: Synchronize approved documentation, specs, anchor/camera/voice YAML bibles, registries, Python gate tools, and skills from the production VM (`~/drama-line/`) into the GitHub-controlled `second-civilization` repository (`~/repos/sc-sync`) with deterministic path normalization, zero binary leakage, in-clone selftest proof, and absolute `main` branch protection.

**Trigger**: Invoke at the end of any completed spec amendment, tool patch, asset-registry lock, smoke-test report, or skill build that needs to be synced to GitHub `xbox002000/second-civilization`.

---

## 2. Inputs

| Input | Required | Description / Grounding |
| :--- | :---: | :--- |
| **Changed VM File List** | Yes | Exact paths under `~/drama-line/` (text/YAML/JSON/Python/Markdown only). |
| **Base Branch** | Yes | Latest production `agy/*` branch state (e.g., `origin/agy/sys01-manifestation-direction-20261128`) or `origin/main` when explicitly instructed. |
| **New Branch Name** | Yes | Must match `agy/<topic>-YYYYMMDD` (e.g., `agy/asset-prod-v24-sm8-20261128`, `agy/sys01-manifestation-direction-20261128`). Never `main`. |
| **SSH Deploy Key** | Yes | `~/.ssh/github-second-civilization` (already provisioned on `workhorse-90d`). |
| **Path Map** | Yes | [vm_to_repo_path_map.yaml](vm_to_repo_path_map.yaml) (distilled from `sync_batch1.sh`, `sync_batch2.sh`, `ASSET_PROD_REPORT.md` §4.3, `SYS01_DIRECTION_PATCH_REPORT.md` §1). |
| **Task Report Path** | Yes | Target VM report where branch name, base SHA, new commit SHA, and file list will be recorded. |

---

## 3. Protocol

1. **Fetch remote and create a NEW `agy/*` branch** — In `~/repos/sc-sync` (or clone via `GIT_SSH_COMMAND="ssh -i ~/.ssh/github-second-civilization"` if missing, per `sync_batch1.sh`), run `git fetch origin` and check out a new branch `agy/<topic>-YYYYMMDD` from the latest production branch state. Verify `git branch --show-current` starts with `agy/` and is **never** `main`.
2. **Verify git identity** — Ensure `user.name` (`agy (workhorse-90d)`) and `user.email` (`agy@workhorse.local`) are configured in the clone (`sync_batch1.sh` L7–8).
3. **Copy deliverables using the canonical VM-to-repo path map** — Copy only intended text/YAML/JSON/Python/Markdown files according to [vm_to_repo_path_map.yaml](vm_to_repo_path_map.yaml) (normalizing hyphenated VM names such as `STORYBOARD-SPEC-V2.md` → `docs/STORYBOARD_SPEC_V2.md`). Never copy `secrets/`, `*.log`, `*.out`, or working scratch files.
4. **Run the zero-binary & size-cap hygiene check** — Inspect `git status --short` and all staged/untracked files: reject any `.jpg`, `.jpeg`, `.png`, `.webp`, `.mp4`, `.mov`, `.wav`, `.mp3`, `.safetensors`, `.ckpt`, `.pt`, or any single file `> 500 KB`. Binary media stays on the VM (`~/drama-line/casting/`, `audio_lib/`, `sm*/`) and is indexed only as metadata in `docs/ASSETS_MANIFEST.yaml` (`ASSET_PROD_REPORT.md` §4.3).
5. **Re-run gate tool selftests INSIDE `~/repos/sc-sync`** — Execute `python3 tools/preflight_gate.py --selftest` (`64/64 PASS`) and `python3 tools/diff_sheet_gen.py --selftest` (`15/15 PASS`) from inside the repo clone (not just `~/drama-line/`) to prove the synced tools and `bible/` copies are self-consistent (`ASSET_PROD_REPORT.md` §4.3, `SYS01_DIRECTION_PATCH_REPORT.md` §3).
6. **Review `git diff --stat` and commit cleanly** — Stage intended files, verify zero unintended deletions or secrets, and commit with a clear structured message (`<scope>: <summary>`).
7. **Push ONLY the `agy/*` branch** — Push via `git push -u origin agy/<topic>-YYYYMMDD` using `~/.ssh/github-second-civilization`. Never push `main` and never force-push shared branches.
8. **Record provenance in the task report** — Write the new branch name, base branch + base SHA, new commit SHA, synced file mapping, and in-clone selftest counts into the task's `*_REPORT.md` (`SYS01_DIRECTION_PATCH_REPORT.md` §1).

---

## 4. Gates & Tools

| Gate / Tool | Command / Check | Pass Criterion | Source |
| :--- | :--- | :--- | :--- |
| **Branch Protection Gate** | `test "$(git -C ~/repos/sc-sync branch --show-current)" != "main"` | Current branch matches `^agy/` | `sync_batch1.sh`, `ASSET_PROD_REPORT.md` §1 |
| **Zero-Binary & Size Gate** | Check staged paths against banned binary extensions (`jpg\|png\|mp4\|wav\|mp3\|safetensors`) and `size ≤ 512000 B` | `0` binary files, `0` secrets, `0` oversized files | `ASSET_PROD_REPORT.md` §4.3, `SYS01_DIRECTION_PATCH_REPORT.md` §1 |
| **In-Clone Preflight Selftest** | `python3 /home/hatch/repos/sc-sync/tools/preflight_gate.py --selftest` | `64/64 PASS` (exit `0`) | `SYS01_DIRECTION_PATCH_REPORT.md` §3 |
| **In-Clone Diff-Sheet Selftest** | `python3 /home/hatch/repos/sc-sync/tools/diff_sheet_gen.py --selftest` | `15/15 PASS` (exit `0`) | `SYS01_DIRECTION_PATCH_REPORT.md` §3 |
| **Checklist Sign-off** | Complete [sync_checklist.md](sync_checklist.md) | All 8 items checked before push | All 4 proven syncs |

---

## 5. Node Model Tiers

| Judgment Node | Preferred Model | Acceptable Substitute | Sign-Off Rule |
| :--- | :--- | :--- | :--- |
| **Mechanical file copy, path normalization, binary check, selftests, git commit & push to `agy/*`** | **Tier 2** (`Claude Sonnet 5.5` / `Gemini Pro Std`) driving deterministic commands | **Flash / lightweight model** following [vm_to_repo_path_map.yaml](vm_to_repo_path_map.yaml) + [sync_checklist.md](sync_checklist.md) | Branch != `main`, `0` binaries, in-clone selftests PASS. |
| **Deciding whether a new memo/draft belongs in repo vs stays VM-only** | **Tier 2** (`Claude Sonnet 5.5` / `Gemini Pro Std`) | Cross-pool **Tier 1** (`Claude Opus 5.5` / `Gemini Pro High`) | Documented in the sync report; never commit `secrets/` or raw run logs. |
| **Merging `agy/*` PR into `main`** | **Human Only (Creator)** | **None** | `agy` is permanently forbidden from pushing or merging `main`. |

- **Forbidden-Alone**: Any model pushing to `main`, skipping in-clone selftests, or committing binary media/secrets.

---

## 6. Evidence

This workflow is **proven across 4 completed GitHub syncs on `workhorse-90d` (all 2026-11-28)**:

1. **Batch 1 (`sync_batch1.sh`)**: Branch `agy/production-system-sync-20261128`, commit `456b84c` — initial production system sync (`docs/STORYBOARD_SPEC_V2.md`, 20+ memos, `tools/`).
2. **Batch 2 (`sync_batch2.sh`)**: Branch `agy/production-system-sync-20261128`, commits `418a1fe` & `9fa587f` — `DEMO02_v2` records, `bible/anchors/FANLI.yaml`, `PROJECT_STATUS.md`, `ASSETS_MANIFEST.yaml`, `ADR-005..012`, `ROADMAP.md` updates.
3. **Asset Prod + SM-8 + Spec v2.4 (`ASSET_PROD_REPORT.md` §4.3)**: New branch `agy/asset-prod-v24-sm8-20261128`, commit `857e71961eadf998152372edd61f4ed4bcaff56e` — `19 files changed`, `0` binaries, in-clone `59/59` + `15/15` selftests PASS, `main` untouched.
4. **SYS-01 Direction Patch (`SYS01_DIRECTION_PATCH_REPORT.md` §1)**: New branch `agy/sys01-manifestation-direction-20261128`, commit `1bd6712303671c9f9483417bbf80cfb9f89a19b7` — `7 files changed`, `0` binaries, in-clone `64/64` + `15/15` selftests PASS, `main` untouched.

---

## 7. Failure Modes & Fallbacks

| Failure Mode | Observed Signal | Fallback & Recovery Action |
| :--- | :--- | :--- |
| **SSH Auth Failure on Fetch/Push** | `Permission denied (publickey)` | Explicitly pass `GIT_SSH_COMMAND="ssh -i ~/.ssh/github-second-civilization"` (or `git -c core.sshCommand=...`). If key permissions/access fail, stop and report — never modify SSH keys or bypass auth. |
| **Path-Naming Drift (`-` vs `_`)** | Duplicate file created (e.g., `docs/STORYBOARD-SPEC-V2.md` alongside `docs/STORYBOARD_SPEC_V2.md`) | Always look up exact destination in [vm_to_repo_path_map.yaml](vm_to_repo_path_map.yaml) and check `git status` for unexpected new untracked duplicates before committing. |
| **Accidental Binary or Oversized File Staged** | `.jpg`/`.png`/`.mp4`/`.wav` or `> 500 KB` file appears in `git status` | Unstage and remove from clone working tree (never delete VM source); record asset metadata in `docs/ASSETS_MANIFEST.yaml` instead. |
| **In-Clone Selftest Fails While VM Passes** | `preflight_gate.py` or `diff_sheet_gen.py` fails inside `~/repos/sc-sync` | Missing companion file (e.g., updated `bible/anchors/SYS01.yaml` or `bible/camera/named_shots.yaml` not yet copied). Copy missing dependency and re-run selftests until 100% PASS before committing. |
| **Base Branch Staleness** | Branching off `origin/main` drops unmerged `agy/*` production work | Always run `git fetch origin` and check `git branch -r --sort=-committerdate` to base new production branches on the latest `agy/*` head (`857e719` → `1bd6712` pattern). |
| **HTTP 429 Quota Interruption During Dispatch** | `RESOURCE_EXHAUSTED (code 429)` | **Quota rule**: On 429, re-dispatch with `--model "Claude Opus 5.5 (Medium)"` (or switch to Gemini pool if Anthropic third-party quota is exhausted, per `quota-dispatch-and-recovery`). Inspect `git status` and `git log -n 2` in `~/repos/sc-sync` before resuming so commits are never duplicated. |
