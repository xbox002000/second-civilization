# LOC-QC-1 Checklist & Frozen Schema (7/7 Hard Pass Required for `LOCKED`)

> Grounded directly in `~/drama-line/EP01_ASSET_GAP_REVIEW_AGY_MEMO.md` §2.2 and `~/drama-line/docs/LOCATION_REGISTRY.md` (v1.0, 2026-11-28).

## LOC-QC-1 Seven Mandatory Checks (All 7/7 Must PASS)

| # | Check Key | Pass Criterion | Auto-Fail Trigger |
| :-: | :--- | :--- | :--- |
| **1** | `no_people_rule` *(Veto)* | **100% empty set**: `0` people, `0` silhouettes, `0` hands, `0` reflections (`LOC-TAIHU-NIGHT` allows only tiny distant torch dots on far shore, zero figures). | Any human figure, shadow, hand, or passerby that `<Pic 1>` would propagate as ghost extras. |
| **2** | `light_lock_and_lab` | Light direction & color temperature match `light_lock_id`; `blowout_pct ≤ 5.0%`; multi-angle plates of the same `loc_id` stay within **`\|ΔL*\| ≤ 15`** and **`\|Δb*\| ≤ 12`**. | Streetlamp/window blowout `> 5%`; mismatched color temperature or exposure across angles. |
| **3** | `blocking_and_negative_space` | All script-required landmarks & negative spaces exist (e.g., dark right wall in `LOC-FANLI-STUDIO-26` for `SYS-01` / `S08` card; empty opposite bench in `LOC-TAIHU-DAWN`; arcade pillar + bench in `LOC-TAIPEI-STREET-2022`). | Missing blocking landmark or cramped clutter blocking character/hologram placement. |
| **4** | `v9_zero_readable_text` *(Veto)* | **2.5× zoom check** across street signs, distant LED billboards, palace plaques, notebooks, and monitors: **0 readable CJK/Latin/numeric characters, 0 brand logos**. | Any readable signboard, screen UI, newspaper headline, or palace plaque. |
| **5** | `era_and_geography_accuracy` | Ancient sets obey late Spring-Autumn pre-Qin low austere timber + floor rush mats + low lacquer tables; modern sets carry authentic Taipei texture (mosaic arcade pillars, iron grilles, overcast dusk — not Tokyo/NY/Shanghai). | Ming-Qing red walls / yellow glazed tiles / carved dragons / high chairs / plaques; non-Taipei urban cues. |
| **6** | `aspect_and_composition_9x16` | Native `9:16` vertical framing (`768×1376`), clear foreground/midground/background depth and headroom, ready for `nano2 i2i` or L3 Clay `<Pic 1>`. | Cropped landscape feel, warped horizon, or missing headroom. |
| **7** | `angle_continuity` *(single-angle = `N_A`)* | Secondary angles (`_rev`, `_window`, `_tabletop`) generated via `i2i` anchored to primary angle match wall texture, furniture, floor material, and key light direction. | Furniture, window geometry, or lighting shifts between angles of the same `loc_id`. |

---

## Frozen Location Card YAML Skeleton (`docs/LOCATION_REGISTRY.md`)

```yaml
loc_id: "LOC-<PLACE>-<TIME_OR_ERA>"     # e.g. LOC-FANLI-STUDIO-26, LOC-TAIHU-NIGHT
name: "<Chinese canonical name>"
time_layer: "2026"                      # 春秋 | 2022 | 2026
recurrence: "series_hq"                 # series_hq | multi_episode | single_episode
status: "DRAFT"                         # DRAFT | CANDIDATE | LOCKED | SUPERSEDED
used_in_episodes: ["EP-01:S06-S12"]

light_lock_id: "LK-<NAME>"
key_light_spec: "<key + fill direction & Kelvin>"
target_lab_range:
  bg_L_range: [10.0, 24.0]
  bg_b_range: [-8.0, 1.0]
  max_blowout_pct: 5.0
color_palette_3pt: ["<color1>", "<color2>", "<color3>"]

spatial_anchors:
  - "<foreground anchor>"
  - "<midground anchor>"
  - "<negative space / blocking zone>"
aspect_ratio: "9:16"
usable_angles:
  - angle_id: "main"
    camera_axis: "<lens / angle / framing>"
    purpose_shots: ["S06"]

default_roomtone_id: "<roomtone_48k>"
acoustics_profile: "<acoustic profile>"

no_people_rule: true
forbidden_elements:
  - "任何人物、人影、背影、手部"
  - "任何可讀中文／英文／數字、招牌、匾額、螢幕 UI（V9 硬紅線）"
  - "過曝白光面積 >5%"

asset_contract:
  role: "scene"
  default_owns: ["environment_lighting", "style_palette"]
  default_never_inherit: ["native_audio", "overlay_text"]
zh_prompt_anchor: "<positive Chinese empty-set anchor>"

ref_images:
  - angle_id: "main"
    path: "~/drama-line/casting/scenes/<LOC_ID>/<filename>.jpg"
    resolution: "768x1376"
    seed: 0
    bg_L: 0.00
    bg_b: 0.00
    whole_L: 0.00
    whole_b: 0.00
    blowout_pct: 0.00
    sha256: "<64-hex>"

qc1_record:
  - angle_id: "main"
    verdict: "PASS (7/7)"
    checks:
      no_people_rule: PASS
      light_lock_and_lab: PASS
      blocking_and_negative_space: PASS
      v9_zero_readable_text: PASS
      era_and_geography_accuracy: PASS
      aspect_and_composition_9x16: PASS
      angle_continuity: N_A
    notes: "<telemetry + visual evidence>"
```
