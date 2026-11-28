# PROP-QC-1 Checklist & Frozen Schema (6/6 Hard Pass Required for `LOCKED`)

> Grounded directly in `~/drama-line/EP01_ASSET_GAP_REVIEW_AGY_MEMO.md` §2.1 and `~/drama-line/docs/PROP_REGISTRY.md` (v1.0, 2026-11-28).

## PROP-QC-1 Six Mandatory Checks (All 6/6 Must PASS)

| # | Check Key | Pass Criterion | Auto-Fail Trigger |
| :-: | :--- | :--- | :--- |
| **1** | `era_accuracy` | Late Spring-Autumn pre-Qin form & material (short oxidized bronze sword, plain blank bamboo slips + twin hemp cords; modern coin restricted strictly to `2022`/`2026`). | Han/Tang long iron blade, Ming-Qing dragon guard, tassels, glossy steel/bright gold, thread-bound book, era crossover. |
| **2** | `scale_and_proportion` | Anatomically realistic ratio to human hand/hip (sword hilt `~1.15×` palm width, sheathed tip stops mid-thigh; coin `3.8–4.5 cm`; bamboo slip width `~1 cm`). | Oversized fantasy blade dragging past knee, dinner-plate coin, oversized scroll. |
| **3** | `handedness_and_wear_side` | Correct anatomical side (`anatomical_left_hip` diagonal hang; clean 5-finger left/right grip matching `hold_hand` spec). | Six fingers, twisted wrist, watch/ring on ancient hand, wrong-hip wear. |
| **4** | `state_completeness` | Every required state (`sheathed_hip`, `hand_on_hilt_ecu`, `unsheathed_1inch`; `open` / `half_rolled`) preserves 100% identical pommel, guard, scabbard/bamboo tone & fittings. | "Swapped sword" or mismatched cord/lacquer across states of the same `prop_id`. |
| **5** | `v9_zero_text` *(Veto)* | **2.5× zoom check** across blade, slips, coin face, scabbard, and background: **0 readable characters, 0 pseudo-seal script, 0 logos/watermarks**. | Any single readable glyph or pseudo-character (e.g., `通寶` on `expressions.png` R2C2 — hard-banned from cropping). |
| **6** | `material_lighting_neutrality` | Clean neutral diffuse studio light, zero heavy color cast, zero blown highlights (`blowout_pct ≤ 5%`), safe for `never_inherit: [source_lighting]`. | Harsh neon/orange cast or specular blowout polluting target scene lighting. |

---

## Frozen Prop Card YAML Skeleton (`docs/PROP_REGISTRY.md`)

```yaml
prop_id: "PROP-<TYPE>-<NN>"             # e.g. PROP-SWORD-01, PROP-BAMBOO-01
name: "<Chinese canonical name>"
tier: "hero"                            # hero | recurring | insert
status: "DRAFT"                         # DRAFT | CANDIDATE | LOCKED | SUPERSEDED
used_in_episodes: ["EP-01:S00"]
linked_outfits: ["FANLI-OUTFIT-02"]

allowed_eras: ["春秋"]
forbidden_eras: ["2022", "2026"]
forbidden_outfits: ["FANLI-OUTFIT-01"]

dimensions_cm: "<physical dimensions>"
scale_reference: "<human-scale anchor>"
materials_and_finish: "<matte oxidized material spec>"
silhouette_key_parts:
  - "<invariant visual feature 1>"
  - "<invariant visual feature 2>"
  - "<invariant visual feature 3>"

wear_side: "anatomical_left_hip"        # anatomical_left_hip | tabletop | handheld_only
hold_hand:
  press_or_steady: "anatomical_left_hand"
required_states:
  - state: "<state_1>"

forbidden_elements:
  - "任何銘文、篆字、漢字、數字、浮水印（V9 硬紅線）"

asset_contract:
  role: "prop"
  default_owns: ["prop_appearance"]
  default_never_inherit: ["studio_backdrop", "source_lighting", "overlay_text"]
zh_prompt_anchor: "<positive Chinese prompt anchor>"

ref_images:
  - state: "<state_1>"
    path: "~/drama-line/casting/props/<PROP_ID>/<filename>.jpg"
    resolution: "768x1376"
    seed: 0
    sha256: "<64-hex>"

qc1_record:
  - state: "<state_1>"
    verdict: "PASS (6/6)"
    checks:
      era_accuracy: PASS
      scale_and_proportion: PASS
      handedness_and_wear_side: PASS
      state_completeness: PASS
      v9_zero_text: PASS
      material_lighting_neutrality: PASS
    notes: "<concise visual evidence>"
```
