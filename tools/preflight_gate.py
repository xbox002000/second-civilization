#!/usr/bin/env python3
"""
preflight_gate.py — Workflow V2.3 Preflight Validation Gate (QC-0)
Implements AMD-01/04/05/06/07 (v2.2) + V2.3 increments:
  - ASSET_CONTRACT & REF_COUNT_BUDGET (Item 1)
  - V13_AUTHORITY_CONFLICT & V13_ORPHAN_ASSET (Item 2)
  - ERA_ANCHOR_CONFLICT (Item 3)
  - PERF_INTENSITY_CONFLICT / PERF_INTENSITY_CEILING / PERF_LEXICON_UNKNOWN / AI_FACE_TABOO (Item 4)
  - CROSS_ERA_CHAR_SCOPE / FLIP_ASSET_BAN / UNSEEN_SIDE_GUARD (Item 5)
  - VOICE_AUTHORITY_LOCK (Item 6)
  - Advisory Craft Checks: CRAFT_LIGHT_SPECIFICITY / CRAFT_OBSERVABLE_ACTION /
    CRAFT_PALETTE_NO_FLUFF / CRAFT_SOUND_DESIGNED (Item 7b, WARN only)
  - AUDIO_BED_HYGIENE (Item 7c)
  - V1_DURATION_ENVELOPE (Item 7d, L4 measured sub-caps)

Usage:
  python3 preflight_gate.py <script_pack.json> [--mode normal|demo] [--json]
  python3 preflight_gate.py --selftest
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Rule Constants
# ---------------------------------------------------------------------------

CU_MCU_SIZES = {"CU", "MCU", "ECU"}
MS_LS_SIZES = {"MS", "LS", "ELS"}
VIDEO_ENGINES = {"h3", "flow", "wan"}

# Shot-size closeness rank (larger = closer)
SHOT_SIZE_RANK: Dict[str, int] = {
    "ELS": 1,
    "LS": 2,
    "2S": 3,
    "MS": 3,
    "OTS": 4,
    "MCU": 5,
    "CU": 6,
    "ECU": 7,
    "INSERT": 6,
}

# Item 1: Role Default Scoped Contracts
ROLE_DEFAULT_CONTRACTS: Dict[str, Dict[str, List[str]]] = {
    "first_frame": {
        "owns": ["framing_pose", "environment_lighting"],
        "never_inherit": ["identity_override", "motion_lock", "overlay_text"],
    },
    "scene": {
        "owns": ["environment_lighting", "style_palette"],
        "never_inherit": ["native_audio", "overlay_text"],
    },
    "character": {
        "owns": ["identity", "costume"],
        "never_inherit": [
            "studio_backdrop",
            "source_lighting",
            "card_layout",
            "overlay_text",
            "native_audio",
        ],
    },
    "prop": {
        "owns": ["prop_appearance"],
        "never_inherit": ["studio_backdrop", "source_lighting", "overlay_text"],
    },
    "previs_video": {
        "owns": ["camera_motion", "blocking_timing"],
        "never_inherit": [
            "clay_material",
            "environment_lighting",
            "identity_override",
            "native_audio",
        ],
    },
}

# Item 4: Built-in Micro-Expression Lexicon Metadata (synced with bible/performance/micro_expressions.yaml)
MICRO_EXPR_LEXICON: Dict[str, Dict[str, str]] = {
    "z1_slow_blink": {"level": "L1", "min_shot_size": "MCU"},
    "z1_steady_hold": {"level": "L1", "min_shot_size": "MCU"},
    "z1_object_to_person": {"level": "L2", "min_shot_size": "MCU"},
    "z1_glare_squint": {"level": "L2", "min_shot_size": "MCU"},
    "z1_sharp_lock": {"level": "L2", "min_shot_size": "CU"},
    "z1_startled_snap": {"level": "L3", "min_shot_size": "MS"},
    "z2_hairline_knit": {"level": "L1", "min_shot_size": "CU"},
    "z2_brow_settle": {"level": "L1", "min_shot_size": "CU"},
    "z2_skeptical_furrow": {"level": "L2", "min_shot_size": "CU"},
    "z2_alert_tension": {"level": "L3", "min_shot_size": "MCU"},
    "z3_closed_still_lips": {"level": "L1", "min_shot_size": "MS"},
    "z3_jaw_clench": {"level": "L2", "min_shot_size": "CU"},
    "z3_chin_tuck": {"level": "L2", "min_shot_size": "MCU"},
    "z3_quiet_part_speak": {"level": "L2", "min_shot_size": "CU"},
    "z3_swallow_hold": {"level": "L2", "min_shot_size": "MCU"},
    "z4_calm_breath": {"level": "L1", "min_shot_size": "MS"},
    "z4_pre_line_exhale": {"level": "L1", "min_shot_size": "MCU"},
    "z4_weight_shift": {"level": "L1", "min_shot_size": "2S"},
    "z4_heavy_heave": {"level": "L3", "min_shot_size": "MS"},
    "z4_back_brace": {"level": "L3", "min_shot_size": "MS"},
    "z_sup_double_take_retreat": {"level": "L4", "min_shot_size": "MS"},
}

# Rule b1: Bare negation freeze words (ZH & EN)
BARE_NEGATION_ZH = [
    "不動", "不动", "不說話", "不说话", "靜止", "静止",
    "不走動", "不走动", "不眨眼", "不轉頭", "不转头",
    "不彎腰", "不弯腰", "動作克制", "动作克制",
    "完全不動", "一動不動", "凝視不動",
]

BARE_NEGATION_EN_PATTERNS = [
    re.compile(r"\bdo\s+not\s+move\b", re.IGNORECASE),
    re.compile(r"\bdon['’]t\s+move\b", re.IGNORECASE),
    re.compile(r"\bno\s+movement\b", re.IGNORECASE),
    re.compile(r"\bno\s+motion\b", re.IGNORECASE),
    re.compile(r"\bdo\s+not\s+speak\b", re.IGNORECASE),
    re.compile(r"\bdon['’]t\s+speak\b", re.IGNORECASE),
    re.compile(r"\bcompletely\s+still\b", re.IGNORECASE),
    re.compile(r"\bfrozen\s+still\b", re.IGNORECASE),
    re.compile(r"\bremain(?:s)?\s+motionless\b", re.IGNORECASE),
    re.compile(r"\bnot\s+moving\b", re.IGNORECASE),
    re.compile(r"\bstay\s+still\b", re.IGNORECASE),
]

# Item 1: H3 bare negation leak from never_inherit[]
H3_BARE_NEVER_INHERIT_PATTERNS = [
    re.compile(r"\bdo\s+not\s+inherit\b", re.IGNORECASE),
    re.compile(r"\bno\s+grey\s+clay\b", re.IGNORECASE),
    re.compile(r"\bno\s+gray\s+clay\b", re.IGNORECASE),
    re.compile(r"\bno\s+studio\s+background\b", re.IGNORECASE),
    re.compile(r"\bno\s+bamboo\s+scroll\b", re.IGNORECASE),
]

# Rule c: Two-shot micro-motion keywords (EN & ZH)
MICRO_MOTION_EN_PATTERNS = [
    re.compile(r"\bblink(?:s|ing|ed)?\b", re.IGNORECASE),
    re.compile(r"\bbreath(?:e|es|ing|ed)?\b", re.IGNORECASE),
    re.compile(r"\bweight\s+shift(?:s|ing)?\b", re.IGNORECASE),
    re.compile(r"\bshift(?:s|ing)?\s+(?:their\s+|his\s+|her\s+)?weight\b", re.IGNORECASE),
    re.compile(r"\bchest\s+ris(?:e|es|ing)\b", re.IGNORECASE),
    re.compile(r"\bshoulder(?:s)?\s+ris(?:e|es|ing)\b", re.IGNORECASE),
    re.compile(r"\bmicro[- ]?(?:motion|movement)\b", re.IGNORECASE),
    re.compile(r"\binhal(?:e|es|ing)\b", re.IGNORECASE),
    re.compile(r"\bexhal(?:e|es|ing)\b", re.IGNORECASE),
    re.compile(r"\bsway(?:s|ing)?\b", re.IGNORECASE),
]

MICRO_MOTION_ZH = [
    "眨眼", "呼吸", "喘息", "重心微移", "重心轉移", "重心转移",
    "重心移動", "重心移动", "起伏", "微動", "微动", "微晃",
    "微動作", "微动作",
]

# Rule e: SYS-01 composite_ui banned terms
SYS01_BANNED_ZH = [
    "全息屏幕", "全息螢幕", "全息投影", "全息人像",
    "彈窗", "弹窗", "女性頭像", "女性头像",
    "懸浮屏幕", "懸浮螢幕", "悬浮屏幕",
]

SYS01_BANNED_EN_PATTERNS = [
    re.compile(r"\bhologram(?:s|ic)?\b", re.IGNORECASE),
    re.compile(r"\bholographic\b", re.IGNORECASE),
    re.compile(r"\bfloating\s+(?:screen|panel|ui|window|interface)\b", re.IGNORECASE),
    re.compile(r"\bpop[- ]?up\s+(?:screen|panel|window|ui)\b", re.IGNORECASE),
    re.compile(r"\bfemale\s+avatar\b", re.IGNORECASE),
]

# Rule g: Scale-jump ban keywords on MS/LS first frames
SCALE_JUMP_ZH = [
    "瞳孔", "睫毛", "眼睫毛", "虹膜", "極近特寫", "极近特写",
    "眼部特寫", "眼部特写", "推至特寫", "推成特寫", "推近至特寫", "毛孔",
]

SCALE_JUMP_EN_PATTERNS = [
    re.compile(r"\bpupil(?:s)?\b", re.IGNORECASE),
    re.compile(r"\b(?:eye)?lash(?:es)?\b", re.IGNORECASE),
    re.compile(r"\biris\b", re.IGNORECASE),
    re.compile(r"\bextreme\s+close[- ]?up\b", re.IGNORECASE),
    re.compile(r"\bmacro\s+(?:eye|shot|close[- ]?up)\b", re.IGNORECASE),
    re.compile(r"\beye\s+reflection\b", re.IGNORECASE),
    re.compile(r"\bskin\s+pore(?:s)?\b", re.IGNORECASE),
    re.compile(r"\bpush(?:es|ing)?\s+into\s+(?:an?\s+)?(?:extreme\s+)?close[- ]?up\b", re.IGNORECASE),
]

# Item 3: Era Anchor Conflicts (checked after stripping Avoid: blocks)
ANCIENT_FORBIDDEN_ZH = [
    "方孔錢", "方孔钱", "銅錢", "铜钱", "腕錶", "腕表", "手錶", "手表", "低馬尾", "低马尾",
]
ANCIENT_FORBIDDEN_EN = [
    re.compile(r"\bsquare[- ]hole\s+(?:bronze\s+)?coin\b", re.IGNORECASE),
    re.compile(r"\bbronze\s+coin\b", re.IGNORECASE),
    re.compile(r"\bwristwatch\b", re.IGNORECASE),
    re.compile(r"\blow\s+ponytail\b", re.IGNORECASE),
]
MODERN_FORBIDDEN_ZH = [
    "緇布冠", "缁布冠", "木笄", "交領深衣", "交领深衣", "素木笄",
]
MODERN_FORBIDDEN_EN = [
    re.compile(r"\btopknot\b", re.IGNORECASE),
    re.compile(r"\bwooden\s+hairpin\b", re.IGNORECASE),
    re.compile(r"\bancient\s+(?:coarse\s+)?linen\s+robe\b", re.IGNORECASE),
]
MODERN_WRONG_WRIST_PATTERNS = [
    re.compile(r"\bright\s+wrist\b", re.IGNORECASE),
    re.compile(r"右腕|右手腕"),
]
COIN_READABLE_PATTERNS = [
    re.compile(r"\breadable\s+(?:coin\s+)?(?:inscription|characters|text)\b", re.IGNORECASE),
    re.compile(r"清晰字跡|清晰字迹|通寶字樣|通宝字样"),
]

# Item 4: Anti-AI-Face Taboo (checked outside Avoid:)
AI_FACE_TABOO_EN = [
    re.compile(r"\bexaggerated\s+gasp\b", re.IGNORECASE),
    re.compile(r"\bjaw\s+drops?\s+wide\s+open\b", re.IGNORECASE),
    re.compile(r"\bwide\s+toothy\s+grin\b", re.IGNORECASE),
    re.compile(r"\bradiant\s+smile\b", re.IGNORECASE),
    re.compile(r"\bcommercial\s+smile\b", re.IGNORECASE),
    re.compile(r"\bmaniacal\b", re.IGNORECASE),
    re.compile(r"\bdramatic\s+tears\b", re.IGNORECASE),
    re.compile(r"\bporcelain\s+skin\b", re.IGNORECASE),
    re.compile(r"\bflawless\s+airbrushed\s+skin\b", re.IGNORECASE),
    re.compile(r"\bbeauty\s+filter\b", re.IGNORECASE),
    re.compile(r"\boverly\s+symmetrical\s+model\s+face\b", re.IGNORECASE),
]

ABSTRACT_EMOTION_ZH = ["感到難過", "感到难过", "很生氣", "很生气", "非常震驚", "非常震惊", "表情複雜", "表情复杂", "內心掙扎", "内心挣扎"]
ABSTRACT_EMOTION_EN = [
    re.compile(r"\bfeels?\s+sad\b", re.IGNORECASE),
    re.compile(r"\blooks?\s+angry\b", re.IGNORECASE),
    re.compile(r"\bvery\s+shocked\b", re.IGNORECASE),
    re.compile(r"\binternal\s+struggle\b", re.IGNORECASE),
]
FLUFF_WORDS_RE = re.compile(r"\b(?:epic|masterpiece|8k|stunning|ultra[- ]?detailed)\b", re.IGNORECASE)
LIGHT_CLUE_RE = re.compile(
    r"\b(?:left|right|top|overhead|back|rim|side|window|lamp|streetlamp|sodium|twilight|soft|hard|cool|warm|moonlight|neon|blue|amber|diffused)\b|"
    r"左|右|頂|背光|側光|窗|路燈|暖|冷|藍調|柔光|硬光",
    re.IGNORECASE,
)
PALETTE_CLUE_RE = re.compile(
    r"\b(?:palette|charcoal|muted|cool\s+blue|amber|desaturated|matte|linen|damp|wet|slate|dark|grain|shadows|monochrome)\b|"
    r"色盤|冷藍|暗褐|啞光|粗麻|墨黑|克制",
    re.IGNORECASE,
)

# Item 5: Flip / Mirror Asset Ban
FLIP_ASSET_RE = re.compile(r"(?:^|[-_/])(flip|mirror|v1-flip-defect)(?:[-_/.]|$)|flip45", re.IGNORECASE)
RIGHT_BROW_CLEAN_RE = re.compile(
    r"scar[- ]?free|unblemished|clean\s+(?:anatomical\s+)?right\s+(?:eye)?brow|smooth\s+(?:unblemished\s+)?(?:anatomical\s+)?right\s+(?:eye)?brow|"
    r"右眉無疤|右眉无疤|右側無疤|右侧无疤",
    re.IGNORECASE,
)

# Dialogue tag in H3 dialect (<d>[Chinese] ...</d>)
H3_DIALOGUE_TAG_RE = re.compile(r"<d>(.*?)</d>", re.DOTALL | re.IGNORECASE)
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
LATIN_RE = re.compile(r"[A-Za-z]")


@dataclass
class Finding:
    level: str  # "FAIL" | "PASS" | "WARN"
    rule: str
    shot_id: str
    message: str
    stamp: Optional[str] = None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _norm_str(val: Any) -> str:
    if val is None:
        return ""
    return str(val).strip()


def _strip_h3_dialogue_tags(text: str) -> str:
    return H3_DIALOGUE_TAG_RE.sub(" ", text)


def _strip_avoid_clause(text: str) -> str:
    """Remove trailing Avoid: / 避免： clauses so negative lists don't trigger positive taboo scans."""
    if not text:
        return ""
    m = re.search(r"\bavoid\s*[:：]|避免\s*[:：]", text, re.IGNORECASE)
    if m:
        return text[: m.start()]
    return text


def _find_bare_negations(text: str) -> List[str]:
    hits: List[str] = []
    if not text:
        return hits
    for term in BARE_NEGATION_ZH:
        if term in text:
            hits.append(term)
    for pat in BARE_NEGATION_EN_PATTERNS:
        m = pat.search(text)
        if m:
            hits.append(m.group(0))
    return hits


def _is_chinese_prose(prompt: str) -> Tuple[bool, int, int]:
    cleaned = _strip_h3_dialogue_tags(prompt)
    cjk_count = len(CJK_RE.findall(cleaned))
    latin_count = len(LATIN_RE.findall(cleaned))
    if cjk_count == 0:
        return False, 0, latin_count
    total = cjk_count + latin_count
    ratio = cjk_count / max(total, 1)
    return (cjk_count >= 4 or ratio > 0.15), cjk_count, latin_count


def _check_h3_dialect(prompt: str, gen_mode: str) -> Optional[str]:
    low = prompt.lower()
    if gen_mode == "ref2v":
        required_any_core = ["subject_definitions", "detailed_description", "overall_soundscape", "non_diegetic_music"]
        missing = [k for k in required_any_core if k not in low]
        if len(missing) >= 2:
            return (
                "H3 ref2v prompt missing §A.4 6-section markers "
                f"(missing: {', '.join(missing)})"
            )
    else:
        has_pic = ("<picture" in low) or ("<pic" in low)
        has_struct = any(
            k in low
            for k in (
                "integrated_multimodal_description",
                "overall_soundscape",
                "non_diegetic_music",
            )
        )
        if not (has_pic and has_struct):
            return (
                "H3 base prompt missing §A.4 structure "
                "(requires <Picture N> alignment + integrated_multimodal_description/overall_soundscape/non_diegetic_music)"
            )
    return None


def _has_micro_motion(shot: Dict[str, Any]) -> bool:
    pb = shot.get("performance_beat")
    if isinstance(pb, dict):
        lex = pb.get("lexicon_ids") or []
        if any(str(x).startswith("z4_") or str(x) == "z1_slow_blink" for x in lex):
            return True
    fields: List[str] = [
        _norm_str(shot.get("video_prompt")),
        _norm_str(shot.get("action")),
        _norm_str(shot.get("microexpression")),
    ]
    if isinstance(pb, dict):
        for k in ("from", "trigger", "to"):
            fields.append(_norm_str(pb.get(k)))
    elif isinstance(pb, str):
        fields.append(pb)

    blob = " ".join(fields)
    for term in MICRO_MOTION_ZH:
        if term in blob:
            return True
    for pat in MICRO_MOTION_EN_PATTERNS:
        if pat.search(blob):
            return True
    return False


def _extract_core_text(text: str) -> str:
    return re.sub(r"[\s\W_]+", "", text, flags=re.UNICODE).lower()


def _mentions_sys01(shot: Dict[str, Any]) -> bool:
    for vfx in shot.get("vfx_beats") or []:
        if isinstance(vfx, dict) and _norm_str(vfx.get("type")).lower() == "composite_ui":
            return True
        if isinstance(vfx, str) and vfx.strip().lower() == "composite_ui":
            return True

    check_fields = [
        _norm_str(shot.get("image_prompt")),
        _norm_str(shot.get("video_prompt")),
        _norm_str(shot.get("action")),
        _norm_str(shot.get("shot_intent")),
        _norm_str(shot.get("continuity_notes")),
    ]
    for ref in shot.get("asset_refs") or []:
        if isinstance(ref, dict):
            check_fields.append(_norm_str(ref.get("asset_id")))
    blob = " ".join(check_fields)
    return bool(re.search(r"\bsys[-_]?01\b", blob, re.IGNORECASE))


def _find_sys01_banned(text: str) -> List[str]:
    hits: List[str] = []
    if not text:
        return hits
    for term in SYS01_BANNED_ZH:
        if term in text:
            hits.append(term)
    for pat in SYS01_BANNED_EN_PATTERNS:
        m = pat.search(text)
        if m:
            hits.append(m.group(0))
    return hits


def _find_scale_jump_terms(text: str) -> List[str]:
    hits: List[str] = []
    if not text:
        return hits
    for term in SCALE_JUMP_ZH:
        if term in text:
            hits.append(term)
    for pat in SCALE_JUMP_EN_PATTERNS:
        m = pat.search(text)
        if m:
            hits.append(m.group(0))
    return hits


def _get_asset_refs_by_role(shot: Dict[str, Any]) -> Dict[str, List[str]]:
    by_role: Dict[str, List[str]] = {
        "first_frame": [],
        "scene": [],
        "character": [],
        "prop": [],
        "previs_video": [],
        "other": [],
    }
    for ref in shot.get("asset_refs") or []:
        if isinstance(ref, dict):
            role = _norm_str(ref.get("role")).lower()
            aid = _norm_str(ref.get("asset_id"))
            if role in by_role:
                by_role[role].append(aid)
            else:
                by_role["other"].append(aid)
    return by_role


def _is_loc_rev_id(asset_id: str) -> bool:
    low = asset_id.lower()
    return ("_rev" in low) or ("loc_rev" in low) or low.endswith("-rev")


def _parse_character_meta(asset_id: str, scope_target: str = "") -> Tuple[str, str, str]:
    """
    Infer (char_id, age_band, outfit_id) from asset_id naming convention.
    """
    up = asset_id.upper()
    if "FANLI" in up:
        char_id = "FANLI"
        if re.search(r"MASTER[-_]A\b", up):
            return (char_id, "A", "FANLI-OUTFIT-01")
        if re.search(r"MASTER[-_]C\b", up):
            return (char_id, "C", "FANLI-OUTFIT-01")
        if "OUTFIT-03" in up or "OUTFIT03" in up:
            return (char_id, "B", "FANLI-OUTFIT-03")
        if "OUTFIT-04" in up or "OUTFIT04" in up:
            return (char_id, "B", "FANLI-OUTFIT-04")
        if "OUTFIT-02" in up or "ANCIENT" in up:
            return (char_id, "B", "FANLI-OUTFIT-02")
        if "OUTFIT-01" in up or "USERFACE" in up or "MODERN" in up or re.search(r"MASTER[-_]B\b", up):
            return (char_id, "B", "FANLI-OUTFIT-01")
        return (char_id, "B", "FANLI-OUTFIT-UNKNOWN")
    if "WITNESS" in up:
        return ("WITNESS-WOMAN-01", "DEFAULT", "WITNESS-CASUAL")
    cid = scope_target.upper() if scope_target else up
    return (cid, "DEFAULT", f"{cid}-OUTFIT")


def _resolve_ref_contract(ref: Dict[str, Any]) -> Tuple[List[str], List[str], str]:
    role = _norm_str(ref.get("role")).lower()
    defaults = ROLE_DEFAULT_CONTRACTS.get(role, {"owns": [], "never_inherit": []})
    owns = ref.get("owns")
    if owns is None:
        resolved_owns = list(defaults["owns"])
    else:
        resolved_owns = [_norm_str(x).lower() for x in owns if _norm_str(x)]
    ni = ref.get("never_inherit")
    if ni is None:
        resolved_ni = list(defaults["never_inherit"])
    else:
        resolved_ni = [_norm_str(x).lower() for x in ni if _norm_str(x)]
    target = _norm_str(ref.get("scope_target"))
    return resolved_owns, resolved_ni, target


def _check_voice_locked(speaker: str) -> Optional[str]:
    """Return status string ('LOCKED' / 'PENDING' / 'MISSING') for a speaker yaml if workspace has voices/."""
    sp = speaker.upper().strip()
    if not sp:
        return None
    base_dir = Path(__file__).resolve().parent.parent
    candidates = [
        base_dir / "bible" / "voices" / f"{sp}.yaml",
        base_dir / "voices" / f"{sp}.yaml",
    ]
    for p in candidates:
        if p.is_file():
            txt = p.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"^\s*status\s*:\s*(\S+)", txt, re.MULTILINE)
            if m:
                return m.group(1).strip().upper()
            return "UNKNOWN"
    return "MISSING"


# ---------------------------------------------------------------------------
# Core Validator
# ---------------------------------------------------------------------------

def validate_script_pack(
    pack: Dict[str, Any], mode_override: Optional[str] = None
) -> Tuple[List[Finding], List[str]]:
    """
    Validate a Schema 2.0–2.3 script_pack dict against AMD-01/04/05/06/07 + v2.3 rules.
    Returns (findings, stamps).
    """
    findings: List[Finding] = []
    stamps: List[str] = []

    prod_mode = mode_override or _norm_str(pack.get("production_mode")) or "normal"
    if prod_mode == "demo":
        findings.append(
            Finding(
                level="PASS",
                rule="DEMO_BOUNDARY",
                shot_id="PACK",
                message="production_mode=demo detected; all v2.2/v2.3 hard gates remain enforced (zero exemption).",
            )
        )

    # Index segments by segment_id
    seg_map: Dict[str, Dict[str, Any]] = {}
    for seg in pack.get("segments") or []:
        if isinstance(seg, dict) and _norm_str(seg.get("segment_id")):
            sid_key = _norm_str(seg.get("segment_id"))
            seg_map[sid_key] = seg
            # Item 6: check audio_groups[] for forbidden voice overrides
            for ag in seg.get("audio_groups") or []:
                if isinstance(ag, dict):
                    for bad_k in ("voice_id", "model_id", "voice_settings"):
                        if bad_k in ag:
                            findings.append(
                                Finding(
                                    level="FAIL",
                                    rule="VOICE_AUTHORITY_LOCK",
                                    shot_id=f"{sid_key}:{_norm_str(ag.get('group_id'))}",
                                    message=f"audio_groups entry must not override '{bad_k}'; timbre is locked in voices/{{speaker}}.yaml.",
                                )
                            )

    shots = pack.get("shots")
    if not isinstance(shots, list) or len(shots) == 0:
        findings.append(
            Finding(
                level="FAIL",
                rule="SCHEMA_SHOTS",
                shot_id="PACK",
                message="script_pack.json must contain a non-empty 'shots' array.",
            )
        )
        return findings, stamps

    all_shot_ids = {_norm_str(s.get("shot_id")) for s in shots if isinstance(s, dict)}
    pack_waiver = bool(pack.get("creator_waiver_signed", False))
    accelerator = _norm_str(pack.get("accelerator") or "L4").upper()

    seg_non_card_count: Dict[str, int] = {}
    seg_seen_characters: Dict[str, Set[str]] = {}

    for idx, shot in enumerate(shots):
        if not isinstance(shot, dict):
            findings.append(
                Finding(
                    level="FAIL",
                    rule="SCHEMA_SHOTS",
                    shot_id=f"#{idx}",
                    message="Shot entry must be a JSON object.",
                )
            )
            continue

        sid = _norm_str(shot.get("shot_id")) or f"#{idx}"
        seg_id = _norm_str(shot.get("segment_id")) or "SEG-DEFAULT"
        seg_obj = seg_map.get(seg_id, {})
        time_layer = _norm_str(seg_obj.get("time_layer"))
        shot_size = _norm_str(shot.get("shot_size")).upper()
        angle_h = _norm_str(shot.get("angle_h")).lower()
        subject_facing = _norm_str(shot.get("subject_facing")).lower()
        engine = _norm_str(shot.get("engine_route")).lower()
        gen_mode = _norm_str(shot.get("gen_mode")).lower()
        control_method = _norm_str(shot.get("control_method") or "L1_prompt")
        face_lock = _norm_str(shot.get("face_lock_level")).lower()
        lip_sensitive = bool(shot.get("lip_sensitive", False))
        outfit_id = _norm_str(shot.get("outfit_id")).upper()
        img_prompt = _norm_str(shot.get("image_prompt"))
        vid_prompt = _norm_str(shot.get("video_prompt"))
        action_txt = _norm_str(shot.get("action"))
        micro_txt = _norm_str(shot.get("microexpression"))
        raw_refs = [r for r in (shot.get("asset_refs") or []) if isinstance(r, dict)]
        refs_by_role = _get_asset_refs_by_role(shot)
        char_refs = refs_by_role["character"]
        scene_refs = refs_by_role["scene"]
        ff_refs = refs_by_role["first_frame"]
        previs_refs = refs_by_role["previs_video"]
        is_cpu_card = gen_mode == "cpu_card" or engine == "ffmpeg_card"
        shot_accel = _norm_str(shot.get("accelerator") or accelerator).upper()

        # ------------------------------------------------------------------
        # Rule a: ROUTING_LOCK (AMD-01 + AMD-07)
        # ------------------------------------------------------------------
        needs_routing_lock = lip_sensitive or (
            face_lock == "strict" and shot_size in CU_MCU_SIZES
        )
        if needs_routing_lock:
            reasons = []
            if gen_mode != "ref2v":
                reasons.append(f"gen_mode='{gen_mode}' (required 'ref2v')")
            if len(char_refs) < 2:
                reasons.append(f"character asset_refs={len(char_refs)} (required >=2)")
            if reasons:
                waived = bool(shot.get("creator_waiver_signed", False)) or pack_waiver
                if waived:
                    waiver_reason = _norm_str(
                        shot.get("demo_waiver_reason") or pack.get("demo_waiver_reason")
                    )
                    if "[ROUTING_WAIVED]" not in stamps:
                        stamps.append("[ROUTING_WAIVED]")
                    findings.append(
                        Finding(
                            level="PASS",
                            rule="ROUTING_LOCK",
                            shot_id=sid,
                            stamp="[ROUTING_WAIVED]",
                            message=(
                                f"[ROUTING_WAIVED] Creator waiver signed; bypassed {', '.join(reasons)}"
                                + (f" (reason: {waiver_reason})" if waiver_reason else "")
                            ),
                        )
                    )
                else:
                    findings.append(
                        Finding(
                            level="FAIL",
                            rule="ROUTING_LOCK",
                            shot_id=sid,
                            message=(
                                f"lip_sensitive={lip_sensitive}, face_lock_level={face_lock}, "
                                f"shot_size={shot_size} violates routing lock: {', '.join(reasons)}"
                            ),
                        )
                    )

        # ------------------------------------------------------------------
        # Rule b: PROMPT_HYGIENE (AMD-07 + Appendix A §A.4 + Item 1 H3 negation leak)
        # ------------------------------------------------------------------
        img_neg = _find_bare_negations(img_prompt)
        vid_neg = _find_bare_negations(vid_prompt)
        if img_neg:
            findings.append(
                Finding(
                    level="FAIL",
                    rule="PROMPT_HYGIENE_NEGATION",
                    shot_id=sid,
                    message=f"image_prompt contains bare negation freeze words: {img_neg}",
                )
            )
        if vid_neg:
            findings.append(
                Finding(
                    level="FAIL",
                    rule="PROMPT_HYGIENE_NEGATION",
                    shot_id=sid,
                    message=f"video_prompt contains bare negation freeze words: {vid_neg}",
                )
            )
        if engine == "h3" and vid_prompt:
            h3_ni_leaks = [p.search(vid_prompt).group(0) for p in H3_BARE_NEVER_INHERIT_PATTERNS if p.search(vid_prompt)]
            if h3_ni_leaks:
                findings.append(
                    Finding(
                        level="FAIL",
                        rule="PROMPT_HYGIENE_NEGATION",
                        shot_id=sid,
                        message=f"H3 video_prompt leaks bare never_inherit negations {h3_ni_leaks}; must use §A.4 positive replacement wording.",
                    )
                )

        if not is_cpu_card and engine in VIDEO_ENGINES:
            if not vid_prompt:
                findings.append(
                    Finding(
                        level="FAIL",
                        rule="PROMPT_HYGIENE_DIALECT",
                        shot_id=sid,
                        message=f"engine_route='{engine}' requires a non-empty compiled video_prompt.",
                    )
                )
            else:
                is_zh, cjk_n, lat_n = _is_chinese_prose(vid_prompt)
                if is_zh:
                    findings.append(
                        Finding(
                            level="FAIL",
                            rule="PROMPT_HYGIENE_DIALECT",
                            shot_id=sid,
                            message=(
                                f"video_prompt for engine '{engine}' contains Chinese prose "
                                f"(CJK={cjk_n}, Latin={lat_n} outside <d> tags); must use §A.4 English engine dialect."
                            ),
                        )
                    )
                elif engine == "h3":
                    h3_err = _check_h3_dialect(vid_prompt, gen_mode)
                    if h3_err:
                        findings.append(
                            Finding(
                                level="FAIL",
                                rule="PROMPT_HYGIENE_DIALECT",
                                shot_id=sid,
                                message=h3_err,
                            )
                        )

        # ------------------------------------------------------------------
        # Rule c: TWO_SHOT_MICRO_MOTION (AMD-07 / §B.8-5)
        # ------------------------------------------------------------------
        if shot_size in {"2S", "TWO-SHOT", "TWO_SHOT"}:
            if not _has_micro_motion(shot):
                findings.append(
                    Finding(
                        level="FAIL",
                        rule="TWO_SHOT_MICRO_MOTION",
                        shot_id=sid,
                        message=(
                            "2S shot lacks required micro-motion keywords "
                            "(blink / breathe / weight shift or ZH equivalents 眨眼/呼吸/重心微移) "
                            "in performance fields or video_prompt."
                        ),
                    )
                )

        # ------------------------------------------------------------------
        # Rule d: LIP_SENSITIVE_DIALOGUE (AMD-07) + Item 6 VOICE_AUTHORITY_LOCK
        # ------------------------------------------------------------------
        dialogue = shot.get("dialogue") or []
        if isinstance(dialogue, list):
            for d_entry in dialogue:
                if isinstance(d_entry, dict):
                    for bad_k in ("voice_id", "model_id", "voice_settings"):
                        if bad_k in d_entry:
                            findings.append(
                                Finding(
                                    level="FAIL",
                                    rule="VOICE_AUTHORITY_LOCK",
                                    shot_id=sid,
                                    message=f"dialogue entry overrides '{bad_k}'; voice timbre is single-point locked in voices/{{speaker}}.yaml.",
                                )
                            )
                    sp = _norm_str(d_entry.get("speaker"))
                    if sp:
                        vstat = _check_voice_locked(sp)
                        if vstat and vstat != "LOCKED":
                            # SYS-01 pending in demo mode -> WARN; normal mode missing -> FAIL
                            if sp.upper() in {"SYS-01", "SYS01"} and prod_mode == "demo":
                                findings.append(
                                    Finding(
                                        level="WARN",
                                        rule="VOICE_AUTHORITY_LOCK",
                                        shot_id=sid,
                                        message=f"speaker '{sp}' voice yaml status={vstat} (allowed in demo reusing existing TTS).",
                                    )
                                )
                            elif prod_mode != "demo" and sp.upper() == "FANLI":
                                findings.append(
                                    Finding(
                                        level="FAIL",
                                        rule="VOICE_AUTHORITY_LOCK",
                                        shot_id=sid,
                                        message=f"speaker '{sp}' voice yaml status={vstat} (required LOCKED).",
                                    )
                                )

        if lip_sensitive:
            spoken_lines: List[str] = []
            if isinstance(dialogue, list):
                for entry in dialogue:
                    if isinstance(entry, dict):
                        line_txt = _norm_str(entry.get("line"))
                        dmode = _norm_str(entry.get("delivery_mode")).lower()
                        if line_txt and dmode != "voiceover":
                            spoken_lines.append(line_txt)
                    elif isinstance(entry, str) and entry.strip():
                        spoken_lines.append(entry.strip())
            if not spoken_lines:
                findings.append(
                    Finding(
                        level="FAIL",
                        rule="LIP_SENSITIVE_DIALOGUE",
                        shot_id=sid,
                        message="lip_sensitive=true shot has no on-camera dialogue text in dialogue[].",
                    )
                )
            else:
                vp_core = _extract_core_text(vid_prompt)
                d_tags = [m.strip() for m in H3_DIALOGUE_TAG_RE.findall(vid_prompt) if m.strip()]
                line_in_prompt = False
                for sl in spoken_lines:
                    sl_core = _extract_core_text(sl)
                    if sl_core and sl_core in vp_core:
                        line_in_prompt = True
                        break
                if not line_in_prompt and d_tags:
                    for dt in d_tags:
                        dt_clean = re.sub(r"\[[^\]]+\]", "", dt).strip()
                        if len(_extract_core_text(dt_clean)) >= 2:
                            line_in_prompt = True
                            break
                if not line_in_prompt:
                    findings.append(
                        Finding(
                            level="FAIL",
                            rule="LIP_SENSITIVE_DIALOGUE",
                            shot_id=sid,
                            message=(
                                "lip_sensitive=true shot does not carry actual dialogue text inside video_prompt "
                                f"(expected line such as {spoken_lines[0]!r})."
                            ),
                        )
                    )

        # ------------------------------------------------------------------
        # Rule e: SYS01_BAN (AMD-05 / V9)
        # ------------------------------------------------------------------
        if _mentions_sys01(shot):
            img_ban = _find_sys01_banned(img_prompt)
            vid_ban = _find_sys01_banned(vid_prompt)
            if img_ban or vid_ban:
                findings.append(
                    Finding(
                        level="FAIL",
                        rule="SYS01_BAN",
                        shot_id=sid,
                        message=(
                            "SYS-01 / composite_ui shot contains banned AI UI terms "
                            f"(image_prompt={img_ban}, video_prompt={vid_ban}); "
                            "SYS-01 must be composited in assembly, never generated."
                        ),
                    )
                )

        # ------------------------------------------------------------------
        # Rule f: SAME_LOCATION_DERIVATION (AMD-04)
        # ------------------------------------------------------------------
        if not is_cpu_card:
            seg_idx = seg_non_card_count.get(seg_id, 0)
            seen_chars = seg_seen_characters.setdefault(seg_id, set())

            ff = shot.get("first_frame")
            if not isinstance(ff, dict):
                ff = {}
            ff_source = _norm_str(ff.get("source")).lower()
            ref_shot_id = _norm_str(ff.get("ref_shot_id"))
            scene_angle_id = _norm_str(ff.get("scene_angle_id"))

            is_reverse_or_ots = (
                angle_h in {"ots", "reverse"}
                or shot_size == "OTS"
                or bool(re.search(r"reverse|反打", _norm_str(shot.get("continuity_notes")), re.IGNORECASE))
            )
            shared_char = any(c in seen_chars for c in char_refs)
            requires_derivation = (seg_idx > 0) or (is_reverse_or_ots and shared_char)

            if requires_derivation:
                if ff_source == "derived_shot":
                    if not ref_shot_id:
                        findings.append(
                            Finding(
                                level="FAIL",
                                rule="SAME_LOCATION_DERIVATION",
                                shot_id=sid,
                                message="first_frame.source='derived_shot' requires non-empty first_frame.ref_shot_id.",
                            )
                        )
                    elif ref_shot_id not in all_shot_ids:
                        findings.append(
                            Finding(
                                level="FAIL",
                                rule="SAME_LOCATION_DERIVATION",
                                shot_id=sid,
                                message=f"first_frame.ref_shot_id='{ref_shot_id}' does not exist in script_pack shots.",
                            )
                        )
                elif ff_source == "generated_dual_lock":
                    has_loc_rev = any(_is_loc_rev_id(s) for s in scene_refs) or _is_loc_rev_id(scene_angle_id)
                    if not has_loc_rev or not ref_shot_id:
                        findings.append(
                            Finding(
                                level="FAIL",
                                rule="SAME_LOCATION_DERIVATION",
                                shot_id=sid,
                                message=(
                                    "first_frame.source='generated_dual_lock' requires both a LOC_rev asset/scene_angle_id "
                                    f"and ref_shot_id (got scene_refs={scene_refs}, scene_angle_id={scene_angle_id!r}, "
                                    f"ref_shot_id={ref_shot_id!r})."
                                ),
                            )
                        )
                elif ff_source in {"l3_clay_frame0", "prev_tail", "ref_shot"}:
                    if ff_source == "ref_shot" and not ref_shot_id:
                        findings.append(
                            Finding(
                                level="FAIL",
                                rule="SAME_LOCATION_DERIVATION",
                                shot_id=sid,
                                message="first_frame.source='ref_shot' requires ref_shot_id.",
                            )
                        )
                else:
                    findings.append(
                        Finding(
                            level="FAIL",
                            rule="SAME_LOCATION_DERIVATION",
                            shot_id=sid,
                            message=(
                                f"Same-segment non-anchor/reverse shot in {seg_id} uses first_frame.source='{ff_source or 'missing'}' "
                                f"(scene_refs={scene_refs}) — forbidden under AMD-04; must use 'derived_shot' (with ref_shot_id) "
                                "or 'generated_dual_lock' (with LOC_rev + ref_shot_id)."
                            ),
                        )
                    )

            seg_non_card_count[seg_id] = seg_idx + 1
            seen_chars.update(char_refs)

        # ------------------------------------------------------------------
        # Rule g: SCALE_JUMP_BAN (AMD-01)
        # ------------------------------------------------------------------
        if shot_size in MS_LS_SIZES:
            sj_hits = _find_scale_jump_terms(vid_prompt)
            mov = shot.get("movement") if isinstance(shot.get("movement"), dict) else {}
            end_sz = _norm_str(mov.get("end_shot_size")).upper()
            size_jump = (
                gen_mode in {"i2v_first", "i2v_first_last"}
                and (
                    (shot_size in {"LS", "ELS"} and end_sz in {"CU", "ECU"})
                    or (shot_size == "MS" and end_sz == "ECU")
                )
            )
            if sj_hits or size_jump:
                detail = []
                if sj_hits:
                    detail.append(f"video_prompt demands extreme-close detail {sj_hits}")
                if size_jump:
                    detail.append(f"movement.end_shot_size jumps {shot_size}->{end_sz} on {gen_mode}")
                findings.append(
                    Finding(
                        level="FAIL",
                        rule="SCALE_JUMP_BAN",
                        shot_id=sid,
                        message=f"MS/LS shot ({shot_size}) violates AMD-01 scale-jump ban: {'; '.join(detail)}.",
                    )
                )

        # ------------------------------------------------------------------
        # v2.3 Item 1 + Item 2 + Item 5: ASSET_CONTRACT, REF_COUNT_BUDGET,
        # V13_AUTHORITY_CONFLICT / V13_ORPHAN_ASSET, CROSS_ERA_CHAR_SCOPE,
        # FLIP_ASSET_BAN, UNSEEN_SIDE_GUARD
        # ------------------------------------------------------------------
        if not is_cpu_card and raw_refs:
            authority_map: Dict[Tuple[str, str], Dict[str, List[str]]] = {}
            image_refs_count = 0
            has_fanli = False
            has_45r = False

            for ref in raw_refs:
                aid = _norm_str(ref.get("asset_id"))
                apath = _norm_str(ref.get("path"))
                role = _norm_str(ref.get("role")).lower()
                media_kind = _norm_str(ref.get("media_kind")).lower() or (
                    "video" if role == "previs_video" else "image"
                )
                if media_kind == "image":
                    image_refs_count += 1

                # Item 5: FLIP_ASSET_BAN
                if FLIP_ASSET_RE.search(aid) or (apath and FLIP_ASSET_RE.search(apath)):
                    findings.append(
                        Finding(
                            level="FAIL",
                            rule="FLIP_ASSET_BAN",
                            shot_id=sid,
                            message=f"Asset '{aid or apath}' violates Step-0 flip-geometry retirement (horizontal mirror assets are banned).",
                        )
                    )

                # Item 1: Uncropped charactercard ban
                if "charactercard" in aid.lower() or "charactercard" in apath.lower():
                    findings.append(
                        Finding(
                            level="FAIL",
                            rule="ASSET_CONTRACT",
                            shot_id=sid,
                            message=f"Uncropped multi-panel charactercard '{aid}' cannot be fed directly (prevents card_layout bleed).",
                        )
                    )

                owns, never_inherit, scope_target = _resolve_ref_contract(ref)

                # Item 1: owns ∩ never_inherit != ∅
                overlap = sorted(set(owns) & set(never_inherit))
                if overlap:
                    findings.append(
                        Finding(
                            level="FAIL",
                            rule="ASSET_CONTRACT",
                            shot_id=sid,
                            message=f"Asset '{aid}' has conflicting owns[] and never_inherit[] overlap: {overlap}.",
                        )
                    )

                # Item 2: V13_ORPHAN_ASSET
                if len(owns) == 0:
                    findings.append(
                        Finding(
                            level="FAIL",
                            rule="V13_ORPHAN_ASSET",
                            shot_id=sid,
                            message=f"Asset '{aid}' owns 0 dimensions after overrides; remove dead reference to preserve L4 VRAM/attention budget.",
                        )
                    )
                    continue

                # Item 1: baked_prop warning on ancient-front when shot has no bamboo scroll
                if "ancient-front" in aid.lower():
                    mentions_scroll = bool(re.search(r"bamboo|scroll|竹簡|竹简", f"{action_txt} {vid_prompt}", re.IGNORECASE))
                    if not mentions_scroll and "baked_prop" not in never_inherit:
                        findings.append(
                            Finding(
                                level="WARN",
                                rule="ASSET_CONTRACT",
                                shot_id=sid,
                                message=f"Asset '{aid}' carries a baked bamboo scroll; add 'baked_prop' to never_inherit[] for empty-handed shots.",
                            )
                        )

                # Character metadata for V13 & Item 5
                if role == "character":
                    char_id, age_band, ref_outfit = _parse_character_meta(aid, scope_target)
                    if char_id == "FANLI":
                        has_fanli = True
                    if "45r" in aid.lower():
                        has_45r = True

                    # Item 5: CROSS_ERA_CHAR_SCOPE
                    if (
                        outfit_id
                        and ref_outfit not in {"", "FANLI-OUTFIT-UNKNOWN"}
                        and ref_outfit != outfit_id
                        and char_id == "FANLI"
                        and "costume" in owns
                    ):
                        findings.append(
                            Finding(
                                level="FAIL",
                                rule="CROSS_ERA_CHAR_SCOPE",
                                shot_id=sid,
                                message=(
                                    f"Cross-outfit character ref '{aid}' ({ref_outfit}) used in shot outfit_id='{outfit_id}' "
                                    "without narrowing owns[] to ['identity'] and excluding 'costume'."
                                ),
                            )
                        )

                    for dim in owns:
                        target = scope_target or char_id
                        if dim == "identity":
                            owner_key = f"{char_id}:{age_band}"
                        elif dim == "costume":
                            owner_key = f"{char_id}:{ref_outfit}"
                        else:
                            owner_key = aid
                        authority_map.setdefault((dim, target), {}).setdefault(owner_key, []).append(aid)
                else:
                    for dim in owns:
                        target = scope_target or "SHOT"
                        owner_key = aid
                        authority_map.setdefault((dim, target), {}).setdefault(owner_key, []).append(aid)

            # Item 2: Evaluate V13 authority conflicts
            for (dim, target), groups in authority_map.items():
                if len(groups) > 1:
                    findings.append(
                        Finding(
                            level="FAIL",
                            rule="V13_AUTHORITY_CONFLICT",
                            shot_id=sid,
                            message=(
                                f"(dimension='{dim}', target='{target}') has {len(groups)} competing owners: "
                                f"{dict(groups)}. Narrow owns[] or remove redundant reference."
                            ),
                        )
                    )

            # Item 1: L3 clay anti-leak & ref count budgets
            if control_method == "L3_clay_ref2v":
                if not (scene_refs or ff_refs):
                    findings.append(
                        Finding(
                            level="FAIL",
                            rule="ASSET_CONTRACT",
                            shot_id=sid,
                            message="L3_clay_ref2v requires a scene or first_frame anchor in <Picture 1> (Clay Test Condition 2 anti-leak).",
                        )
                    )
                for ref in raw_refs:
                    if _norm_str(ref.get("role")).lower() == "previs_video":
                        _, r_ni, _ = _resolve_ref_contract(ref)
                        if "clay_material" not in r_ni:
                            findings.append(
                                Finding(
                                    level="FAIL",
                                    rule="ASSET_CONTRACT",
                                    shot_id=sid,
                                    message="L3_clay_ref2v previs_video must include 'clay_material' in never_inherit[].",
                                )
                            )
                if shot_accel not in {"A100", "G4"} and image_refs_count > 3:
                    findings.append(
                        Finding(
                            level="FAIL",
                            rule="REF_COUNT_BUDGET",
                            shot_id=sid,
                            message=f"L3_clay_ref2v on {shot_accel} has {image_refs_count} image refs (hard cap <=3 + 1 previs_video).",
                        )
                    )
            elif engine == "h3" and gen_mode == "ref2v":
                if image_refs_count > 9:
                    findings.append(
                        Finding(
                            level="FAIL",
                            rule="REF_COUNT_BUDGET",
                            shot_id=sid,
                            message=f"H3 ref2v has {image_refs_count} image refs (official hard cap <=9).",
                        )
                    )
                elif shot_accel not in {"A100", "G4"} and image_refs_count > 4:
                    findings.append(
                        Finding(
                            level="WARN",
                            rule="REF_COUNT_BUDGET",
                            shot_id=sid,
                            message=f"H3 ref2v on {shot_accel} has {image_refs_count} image refs (recommended L4 max-size cap <=4).",
                        )
                    )

            # Item 5: UNSEEN_SIDE_GUARD (right-facing FANLI CU/MCU)
            if has_fanli and subject_facing == "right" and shot_size in {"CU", "MCU"}:
                if not has_45r and not RIGHT_BROW_CLEAN_RE.search(img_prompt):
                    findings.append(
                        Finding(
                            level="FAIL",
                            rule="UNSEEN_SIDE_GUARD",
                            shot_id=sid,
                            message=(
                                "Right-facing FANLI CU/MCU lacks both a 45R scar-free reference in asset_refs "
                                "and explicit scar-free right-brow wording in image_prompt."
                            ),
                        )
                    )

        # ------------------------------------------------------------------
        # v2.3 Item 3: ERA_ANCHOR_CONFLICT
        # ------------------------------------------------------------------
        if not is_cpu_card:
            pos_blob = " ".join([
                action_txt,
                _strip_avoid_clause(img_prompt),
                _strip_avoid_clause(vid_prompt),
            ])
            is_ancient_shot = (
                outfit_id in {"FANLI-OUTFIT-02", "FANLI-OUTFIT-03", "FANLI-OUTFIT-04"}
                or time_layer == "春秋"
            )
            is_modern_outfit = outfit_id == "FANLI-OUTFIT-01"

            if is_ancient_shot:
                era_hits: List[str] = [t for t in ANCIENT_FORBIDDEN_ZH if t in pos_blob]
                for pat in ANCIENT_FORBIDDEN_EN:
                    m = pat.search(pos_blob)
                    if m:
                        era_hits.append(m.group(0))
                if era_hits:
                    findings.append(
                        Finding(
                            level="FAIL",
                            rule="ERA_ANCHOR_CONFLICT",
                            shot_id=sid,
                            message=f"Ancient outfit/era ({outfit_id or time_layer}) contains forbidden modern anchor terms: {era_hits}.",
                        )
                    )
            elif is_modern_outfit:
                era_hits = [t for t in MODERN_FORBIDDEN_ZH if t in pos_blob]
                for pat in MODERN_FORBIDDEN_EN:
                    m = pat.search(pos_blob)
                    if m:
                        era_hits.append(m.group(0))
                if re.search(r"watch|腕錶|腕表|手錶|手表", pos_blob, re.IGNORECASE):
                    for pat in MODERN_WRONG_WRIST_PATTERNS:
                        m = pat.search(pos_blob)
                        if m:
                            era_hits.append(f"watch_on_{m.group(0)}")
                if re.search(r"coin|方孔錢|方孔钱|銅錢|铜钱", pos_blob, re.IGNORECASE):
                    for pat in COIN_READABLE_PATTERNS:
                        m = pat.search(pos_blob)
                        if m:
                            era_hits.append(m.group(0))
                if era_hits:
                    findings.append(
                        Finding(
                            level="FAIL",
                            rule="ERA_ANCHOR_CONFLICT",
                            shot_id=sid,
                            message=f"Modern outfit ({outfit_id}) violates anchor/era rules: {era_hits}.",
                        )
                    )

        # ------------------------------------------------------------------
        # v2.3 Item 4: PERF_INTENSITY_CONFLICT / PERF_LEXICON_UNKNOWN / AI_FACE_TABOO
        # ------------------------------------------------------------------
        pb = shot.get("performance_beat")
        if isinstance(pb, dict):
            intensity = _norm_str(pb.get("intensity")).upper()
            deliberate_hold = bool(pb.get("deliberate_hold", False))
            override_reason = _norm_str(pb.get("intensity_override_reason"))
            lex_ids = pb.get("lexicon_ids") or []

            if deliberate_hold and intensity in {"L3", "L4"}:
                findings.append(
                    Finding(
                        level="FAIL",
                        rule="PERF_INTENSITY_CONFLICT",
                        shot_id=sid,
                        message=f"deliberate_hold=true conflicts with high intensity='{intensity}' (must be L1/L2).",
                    )
                )
            if intensity == "L4":
                fanli_present = any("FANLI" in c.upper() for c in char_refs)
                if fanli_present and not override_reason:
                    findings.append(
                        Finding(
                            level="WARN",
                            rule="PERF_INTENSITY_CEILING",
                            shot_id=sid,
                            message="FANLI shot marked intensity='L4' without intensity_override_reason (FANLI ceiling is L3).",
                        )
                    )

            shot_rank = SHOT_SIZE_RANK.get(shot_size, 3)
            for lid in lex_ids:
                lid_s = _norm_str(lid)
                if not lid_s:
                    continue
                meta = MICRO_EXPR_LEXICON.get(lid_s)
                if not meta:
                    findings.append(
                        Finding(
                            level="FAIL",
                            rule="PERF_LEXICON_UNKNOWN",
                            shot_id=sid,
                            message=f"Unknown performance lexicon_id='{lid_s}' (not in bible/performance/micro_expressions.yaml).",
                        )
                    )
                else:
                    min_sz = meta["min_shot_size"]
                    if shot_rank < SHOT_SIZE_RANK.get(min_sz, 1):
                        findings.append(
                            Finding(
                                level="FAIL",
                                rule="SCALE_JUMP_BAN",
                                shot_id=sid,
                                message=f"lexicon_id='{lid_s}' requires min_shot_size={min_sz}, incompatible with shot_size={shot_size}.",
                            )
                        )

        # Anti-AI-face taboo check (positive text only)
        pos_face_blob = " ".join([
            micro_txt,
            _strip_avoid_clause(img_prompt),
            _strip_avoid_clause(vid_prompt),
        ])
        taboo_hits = [p.search(pos_face_blob).group(0) for p in AI_FACE_TABOO_EN if p.search(pos_face_blob)]
        if taboo_hits:
            findings.append(
                Finding(
                    level="FAIL",
                    rule="AI_FACE_TABOO",
                    shot_id=sid,
                    message=f"Contains banned anti-AI-face / overacting terms: {taboo_hits}.",
                )
            )

        # ------------------------------------------------------------------
        # v2.3 Item 7c: AUDIO_BED_HYGIENE
        # ------------------------------------------------------------------
        voice_mode = _norm_str(shot.get("voice_mode")).lower()
        ambient_source = _norm_str(shot.get("ambient_source")).lower()
        if voice_mode == "tts" and ambient_source == "native_keep":
            findings.append(
                Finding(
                    level="FAIL",
                    rule="AUDIO_BED_HYGIENE",
                    shot_id=sid,
                    message="voice_mode='tts' forbids ambient_source='native_keep' (F7 anti-voice-leak rule); use 'post_roomtone'.",
                )
            )
        seg_amb = seg_obj.get("ambience")
        seg_amb_src = _norm_str(seg_amb.get("source")).lower() if isinstance(seg_amb, dict) else ""
        has_sound_drop = any(
            isinstance(v, dict) and _norm_str(v.get("type")).lower() == "sound_drop"
            for v in (shot.get("vfx_beats") or [])
        )
        if has_sound_drop and seg_amb_src == "silent":
            findings.append(
                Finding(
                    level="WARN",
                    rule="AUDIO_BED_HYGIENE",
                    shot_id=sid,
                    message="Shot has sound_drop vfx_beat but segment ambience.source='silent' (no bed to drop).",
                )
            )

        # ------------------------------------------------------------------
        # v2.3 Item 7d: V1_DURATION_ENVELOPE
        # ------------------------------------------------------------------
        if not is_cpu_card and shot.get("target_net_sec") is not None:
            try:
                net_sec = float(shot["target_net_sec"])
            except (TypeError, ValueError):
                net_sec = 0.0
            trim_policy = _norm_str(shot.get("trim_policy") or "standard_0.5s").lower()
            trim_buf = 1.0 if trim_policy == "standard_0.5s" else (0.5 if trim_policy == "tail_only" else 0.0)
            gen_sec = net_sec + trim_buf

            if engine == "ltx" and net_sec > 2.5:
                findings.append(
                    Finding(
                        level="FAIL",
                        rule="V1_DURATION_ENVELOPE",
                        shot_id=sid,
                        message=f"LTX target_net_sec={net_sec:.2f}s exceeds hard cap 2.5s.",
                    )
                )
            elif control_method == "L3_clay_ref2v" and shot_accel not in {"A100", "G4"} and gen_sec > 5.0:
                findings.append(
                    Finding(
                        level="FAIL",
                        rule="V1_DURATION_ENVELOPE",
                        shot_id=sid,
                        message=f"L3_clay_ref2v on {shot_accel} gen_sec={gen_sec:.2f}s exceeds L4 hard cap 5.0s (Clay Test Condition 3).",
                    )
                )
            elif engine == "h3":
                if gen_sec > 6.5:
                    findings.append(
                        Finding(
                            level="FAIL",
                            rule="V1_DURATION_ENVELOPE",
                            shot_id=sid,
                            message=f"H3 gen_sec={gen_sec:.2f}s exceeds hard cap 6.5s (split shot + L-cut per §B.7).",
                        )
                    )
                elif gen_mode == "ref2v" and gen_sec > 5.5 and shot_accel not in {"A100", "G4"}:
                    findings.append(
                        Finding(
                            level="WARN",
                            rule="V1_DURATION_ENVELOPE",
                            shot_id=sid,
                            message=f"H3 ref2v on {shot_accel} gen_sec={gen_sec:.2f}s exceeds recommended 5.5s stability cap.",
                        )
                    )
            elif engine == "wan" and gen_sec > 6.0:
                findings.append(
                    Finding(
                        level="FAIL",
                        rule="V1_DURATION_ENVELOPE",
                        shot_id=sid,
                        message=f"Wan gen_sec={gen_sec:.2f}s exceeds cap 6.0s.",
                    )
                )
            elif engine == "flow" and gen_sec > 7.5:
                findings.append(
                    Finding(
                        level="FAIL",
                        rule="V1_DURATION_ENVELOPE",
                        shot_id=sid,
                        message=f"Flow gen_sec={gen_sec:.2f}s exceeds stability cap 7.5s.",
                    )
                )

            if gen_sec < 3.0 and shot_size != "INSERT" and angle_h != "reverse":
                findings.append(
                    Finding(
                        level="WARN",
                        rule="V1_DURATION_ENVELOPE",
                        shot_id=sid,
                        message=f"AI shot gen_sec={gen_sec:.2f}s is below 3.0s stability window.",
                    )
                )

        # ------------------------------------------------------------------
        # v2.3 Item 7b: 4 Advisory Craft Checks (WARN only — never FAIL)
        # ------------------------------------------------------------------
        if not is_cpu_card:
            light_blob = " ".join([
                _norm_str(seg_obj.get("lighting_base")),
                _norm_str(shot.get("lighting_state")),
                img_prompt,
            ])
            if re.search(r"\bcinematic\s+lighting\b", light_blob, re.IGNORECASE) or not LIGHT_CLUE_RE.search(light_blob):
                findings.append(
                    Finding(
                        level="WARN",
                        rule="CRAFT_LIGHT_SPECIFICITY",
                        shot_id=sid,
                        message="Lighting lacks explicit direction/quality cues or uses generic 'cinematic lighting'.",
                    )
                )

            act_blob = f"{action_txt} {micro_txt} {vid_prompt}"
            abs_hits = [t for t in ABSTRACT_EMOTION_ZH if t in act_blob]
            abs_hits += [p.search(act_blob).group(0) for p in ABSTRACT_EMOTION_EN if p.search(act_blob)]
            fluff_hits = FLUFF_WORDS_RE.findall(act_blob)
            if abs_hits or fluff_hits:
                findings.append(
                    Finding(
                        level="WARN",
                        rule="CRAFT_OBSERVABLE_ACTION",
                        shot_id=sid,
                        message=f"Prompt/action contains abstract emotion or fluff buzzwords: {abs_hits + fluff_hits}.",
                    )
                )

            pal_blob = " ".join([
                _norm_str(seg_obj.get("atmosphere")),
                img_prompt,
                vid_prompt,
            ])
            if re.search(r"\bcinematic\s+color\s+grade\b", pal_blob, re.IGNORECASE) or not PALETTE_CLUE_RE.search(pal_blob):
                findings.append(
                    Finding(
                        level="WARN",
                        rule="CRAFT_PALETTE_NO_FLUFF",
                        shot_id=sid,
                        message="Missing restrained palette/material cues or contains generic 'cinematic color grade'.",
                    )
                )

            has_seg_amb = bool(seg_amb) and seg_amb_src != "silent"
            has_sfx = bool(shot.get("sfx"))
            has_h3_sound = False
            if engine == "h3":
                m_snd = re.search(r"overall_soundscape\s*:\s*(.+)", vid_prompt, re.IGNORECASE)
                if m_snd and m_snd.group(1).strip().upper() not in {"", "N/A", "NONE"}:
                    has_h3_sound = True
            if not (has_seg_amb or has_sfx or has_h3_sound):
                findings.append(
                    Finding(
                        level="WARN",
                        rule="CRAFT_SOUND_DESIGNED",
                        shot_id=sid,
                        message="No segment ambience bed, shot sfx[], or H3 overall_soundscape specified.",
                    )
                )

    return findings, stamps


def format_report(
    findings: List[Finding], stamps: List[str], label: str = "script_pack.json"
) -> Tuple[str, int]:
    fails = [f for f in findings if f.level == "FAIL"]
    warns = [f for f in findings if f.level == "WARN"]
    lines = [f"=== PREFLIGHT GATE REPORT: {label} ==="]
    if stamps:
        lines.append(f"STAMPS: {' '.join(stamps)}")
    for f in findings:
        lines.append(f"{f.level} [{f.rule}] shot={f.shot_id}: {f.message}")
    if not fails:
        stamp_suffix = f" {' '.join(stamps)}" if stamps else ""
        lines.append(f"RESULT: PASS (0 failures, {len(warns)} warning(s)){stamp_suffix}")
        return "\n".join(lines), 0
    else:
        lines.append(f"RESULT: FAIL ({len(fails)} failure(s), {len(warns)} warning(s))")
        return "\n".join(lines), 1


# ---------------------------------------------------------------------------
# Self-Test Suite
# ---------------------------------------------------------------------------

def _build_compliant_pack() -> Dict[str, Any]:
    return {
        "schema_version": "2.3",
        "episode_id": "DEMO-02-COMPLIANT",
        "production_mode": "demo",
        "accelerator": "L4",
        "segments": [
            {
                "segment_id": "SEG-01",
                "scene_id": "LOC-ALLEY-NIGHT",
                "time_layer": "2022",
                "lighting_base": "Overhead cool blue twilight sky with warm sodium alley streetlamp from far back",
                "light_lock_id": "LK-ALLEY-NIGHT",
                "atmosphere": "Humid dark Taipei narrow alley, muted cool blue and charcoal matte palette",
                "ambience": {
                    "source": "library_roomtone",
                    "asset_id": "alley_night_wet_48k",
                    "target_db": -24.0,
                },
            }
        ],
        "shots": [
            {
                "shot_id": "S1",
                "segment_id": "SEG-01",
                "shot_size": "MS",
                "angle_h": "three-quarter",
                "subject_facing": "left",
                "outfit_id": "FANLI-OUTFIT-02",
                "engine_route": "flow",
                "gen_mode": "i2v_first",
                "control_method": "L1_prompt",
                "face_lock_level": "standard",
                "lip_sensitive": False,
                "voice_mode": "none",
                "ambient_source": "post_roomtone",
                "target_net_sec": 4.0,
                "trim_policy": "standard_0.5s",
                "first_frame": {"source": "generated"},
                "asset_refs": [
                    {"asset_id": "LOC-ALLEY-NIGHT", "role": "scene"},
                    {"asset_id": "FANLI-OUTFIT-02-45", "role": "character"},
                ],
                "movement": {"type": "handheld", "speed": "slow", "end_shot_size": "MS"},
                "action": "Fanli braces one palm against the damp alley wall, chest heaving as he scans the alley entrance.",
                "microexpression": "Tense brow, rapid shallow breaths.",
                "performance_beat": {
                    "from": "off-balance stagger",
                    "trigger": "alley lamp flickers",
                    "to": "braced alert freeze",
                    "deliberate_hold": False,
                    "intensity": "L3",
                    "lexicon_ids": ["z4_heavy_heave"],
                },
                "image_prompt": "9:16 vertical live-action frame. Cool blue twilight from above and warm sodium streetlamp from behind. Medium shot of Fanli in matte black coarse linen robe with y-right collar bracing against wet alley wall. Muted dark charcoal palette. Avoid: readable text.",
                "video_prompt": "Live-action, 5s 9:16 single shot. Cool twilight overhead and warm sodium lamp behind. Handheld camera with subtle anxious sway. Fanli braces his right hand on the damp alley wall, shoulders rising with heavy breathing, then turns his head slightly toward the alley mouth. Muted dark palette. Sound: wet alley night ambience.",
            },
            {
                "shot_id": "S2",
                "segment_id": "SEG-01",
                "shot_size": "2S",
                "angle_h": "front",
                "subject_facing": "front",
                "outfit_id": "FANLI-OUTFIT-02",
                "engine_route": "flow",
                "gen_mode": "i2v_first",
                "control_method": "L1_prompt",
                "face_lock_level": "standard",
                "lip_sensitive": False,
                "voice_mode": "none",
                "ambient_source": "post_roomtone",
                "target_net_sec": 4.0,
                "trim_policy": "standard_0.5s",
                "first_frame": {"source": "derived_shot", "ref_shot_id": "S1"},
                "asset_refs": [
                    {"asset_id": "LOC-ALLEY-NIGHT", "role": "scene"},
                    {"asset_id": "FANLI-OUTFIT-02-45", "role": "character"},
                    {"asset_id": "WITNESS-WOMAN-01", "role": "character"},
                ],
                "movement": {"type": "handheld", "speed": "slow", "amplitude": "small"},
                "action": "Both hold tense standoff; woman raises phone half a step back while Fanli shifts weight against the wall.",
                "microexpression": "Both blink slowly, chests rising with measured breathing.",
                "performance_beat": {
                    "from": "startled freeze",
                    "trigger": "woman lifts phone",
                    "to": "guarded standoff with subtle weight shift and steady breathing",
                    "deliberate_hold": False,
                    "intensity": "L1",
                    "lexicon_ids": ["z4_weight_shift"],
                },
                "image_prompt": "9:16 vertical two-shot derived from S1. Cool blue overhead light and warm alley streetlamp behind. Fanli on left wall in matte black robe, woman with red-white striped bag on right holding phone. Avoid: text.",
                "video_prompt": "Live-action, 5s 9:16 single shot. Cool twilight and warm sodium lamp behind. Subtle handheld breath. The woman steps back half a pace and steadies her phone, blinking nervously as she breathes; Fanli shifts weight slightly against the damp wall, shoulders rising with calm breathing while his lips remain completely closed. Muted dark palette.",
            },
            {
                "shot_id": "S2R",
                "segment_id": "SEG-01",
                "shot_size": "MCU",
                "angle_h": "reverse",
                "subject_facing": "left",
                "outfit_id": "WITNESS-CASUAL",
                "engine_route": "flow",
                "gen_mode": "i2v_first",
                "control_method": "L1_prompt",
                "face_lock_level": "standard",
                "lip_sensitive": False,
                "voice_mode": "none",
                "ambient_source": "post_roomtone",
                "target_net_sec": 2.0,
                "trim_policy": "standard_0.5s",
                "first_frame": {
                    "source": "generated_dual_lock",
                    "ref_shot_id": "S2",
                    "scene_angle_id": "LOC-ALLEY-NIGHT_rev",
                },
                "asset_refs": [
                    {"asset_id": "LOC-ALLEY-NIGHT_rev", "role": "scene"},
                    {"asset_id": "WITNESS-WOMAN-01", "role": "character"},
                ],
                "movement": {"type": "handheld", "speed": "slow", "amplitude": "small"},
                "action": "Witness woman lowers her phone, shakes her head slightly, and turns toward the alley exit.",
                "microexpression": "Confused squint giving way to uneasy retreat.",
                "performance_beat": {
                    "from": "nervous filming",
                    "trigger": "sees empty air next to him",
                    "to": "uneasy retreat",
                    "deliberate_hold": False,
                    "intensity": "L4",
                },
                "image_prompt": "9:16 reverse MCU of witness woman in beige jacket holding red-white bag, cool twilight sky and warm streetlamp light matched to S2. Muted dark alley palette. Avoid: text.",
                "video_prompt": "Live-action, 3s 9:16 single shot. Cool twilight and warm streetlamp from alley mouth. Subtle handheld camera. The woman glances into the dim alley, lowers her phone, gives a small uneasy headshake, and turns to walk briskly out of frame. Muted dark shadows.",
            },
            {
                "shot_id": "S3b",
                "segment_id": "SEG-01",
                "shot_size": "MCU",
                "angle_h": "three-quarter",
                "subject_facing": "right",
                "outfit_id": "FANLI-OUTFIT-02",
                "engine_route": "h3",
                "gen_mode": "ref2v",
                "control_method": "L1_prompt",
                "face_lock_level": "strict",
                "lip_sensitive": False,
                "voice_mode": "none",
                "ambient_source": "post_roomtone",
                "target_net_sec": 4.0,
                "trim_policy": "standard_0.5s",
                "first_frame": {"source": "derived_shot", "ref_shot_id": "S2"},
                "asset_refs": [
                    {"asset_id": "S3B-FIRST-FRAME", "role": "first_frame"},
                    {"asset_id": "FANLI-OUTFIT-02-CU", "role": "character"},
                    {"asset_id": "FANLI-OUTFIT-02-45R", "role": "character"},
                ],
                "vfx_beats": [
                    {"type": "composite_ui", "exec_layer": "assembly"}
                ],
                "movement": {"type": "static", "speed": "slow"},
                "action": "Clean actor plate for SYS-01 assembly: Fanli stands in left 45% staring intently at empty dark alley space on right.",
                "microexpression": "Jaw tightens, guarded eyes locked on right landing zone, lips closed.",
                "performance_beat": {
                    "from": "startled alert",
                    "trigger": "empty right space",
                    "to": "taut guarded stare",
                    "deliberate_hold": False,
                    "intensity": "L3",
                    "lexicon_ids": ["z2_alert_tension", "z4_back_brace"],
                },
                "image_prompt": "9:16 MCU clean plate derived from S2. Cool twilight overhead and warm sodium lamp behind. Fanli positioned on left 45% in matte black linen robe facing screen right with clean anatomical right brow looking into empty dark alley space. Avoid: text or UI.",
                "video_prompt": (
                    "subject_definitions: <Picture 1> approved alley MCU plate defining ONLY framing and lighting; <Picture 2> Fanli age 38 frontal face; <Picture 3> Fanli right 45R scar-free outfit reference.\n"
                    "summary: [Keep identity and lighting locked] Clean silent reaction MCU of Fanli reacting to empty dark space on the right.\n"
                    "retention_analysis: face=fully_preserved, outfit=fully_preserved, background=fully_preserved.\n"
                    "detailed_description: Under cool blue twilight and warm alley streetlamp glow, static camera frames Fanli leaning back against the damp wall on the left side of the frame, staring steadily into the empty dark alley space on the right, chest rising with tense breathing while his lips remain completely closed. Muted charcoal and cool blue night palette.\n"
                    "overall_soundscape: Distant humid night alley hum, faint water drips.\n"
                    "non_diegetic_music: N/A"
                ),
            },
            {
                "shot_id": "S4",
                "segment_id": "SEG-01",
                "shot_size": "CU",
                "angle_h": "three-quarter",
                "subject_facing": "right",
                "outfit_id": "FANLI-OUTFIT-02",
                "engine_route": "h3",
                "gen_mode": "ref2v",
                "control_method": "L1_prompt",
                "face_lock_level": "strict",
                "lip_sensitive": True,
                "voice_mode": "tts",
                "ambient_source": "post_roomtone",
                "target_net_sec": 4.0,
                "trim_policy": "standard_0.5s",
                "first_frame": {"source": "derived_shot", "ref_shot_id": "S3b"},
                "asset_refs": [
                    {"asset_id": "S4-FIRST-FRAME", "role": "first_frame"},
                    {"asset_id": "FANLI-OUTFIT-02-CU", "role": "character"},
                    {"asset_id": "FANLI-OUTFIT-02-45", "role": "character"},
                    {"asset_id": "FANLI-OUTFIT-02-45R", "role": "character"},
                ],
                "dialogue": [
                    {
                        "line_id": "L01",
                        "speaker": "FANLI",
                        "line": "……你，怎知我名？",
                        "delivery_mode": "on_camera",
                        "pause_after_sec": 0.6,
                        "delivery": {"pre_pause_sec": 0.5, "pace": "measured", "volume": "low"},
                    }
                ],
                "movement": {"type": "push-in", "speed": "slow", "amplitude": "small"},
                "action": "Fanli steadies his breath, dips his chin slightly, and speaks quietly on camera.",
                "microexpression": "Eyes narrow with cold suspicion before speaking.",
                "performance_beat": {
                    "from": "guarded silence",
                    "trigger": "hears his own name",
                    "to": "composed sharp question",
                    "deliberate_hold": False,
                    "intensity": "L2",
                    "lexicon_ids": ["z3_chin_tuck", "z3_quiet_part_speak"],
                },
                "image_prompt": "9:16 CU derived from S3b. Cool blue twilight light and faint cyan glow from right. Fanli facing screen right showing clean anatomical right brow, matte black coarse linen robe with y-right collar. Muted dark charcoal palette. Avoid: text.",
                "video_prompt": (
                    "subject_definitions: <Picture 1> approved S4 CU frame defining ONLY alley lighting and framing; <Picture 2> Fanli age 38 frontal face; <Picture 3> Fanli left 45 outfit; <Picture 4> Fanli right 45R scar-free outfit.\n"
                    "summary: [Dialogue close-up with strict identity lock] Fanli delivers one quiet suspicious line on camera.\n"
                    "retention_analysis: face=fully_preserved, outfit=fully_preserved, lighting=fully_preserved.\n"
                    "detailed_description: Under cool blue twilight and subtle cyan bounce from the right, the camera pushes in slowly with small amplitude. Fanli holds a calm breath, subtly lowers his chin, and speaks quietly on camera: <d>[Chinese] ……你，怎知我名？</d> His eyes remain locked forward in muted night tones until the end of the shot.\n"
                    "overall_soundscape: Quiet humid alley room tone.\n"
                    "non_diegetic_music: N/A"
                ),
            },
        ],
    }


def run_selftest() -> int:
    print("=== RUNNING preflight_gate.py v2.3 SELFTEST ===")
    base = _build_compliant_pack()
    all_ok = True

    def assert_case(
        name: str,
        pack: Dict[str, Any],
        expect_pass: bool,
        expect_rule: Optional[str] = None,
        expect_stamp: Optional[str] = None,
        expect_warn: Optional[str] = None,
    ) -> None:
        nonlocal all_ok
        findings, stamps = validate_script_pack(pack)
        fails = [f for f in findings if f.level == "FAIL"]
        warns = [f for f in findings if f.level == "WARN"]
        fail_rules = {f.rule for f in fails}
        warn_rules = {f.rule for f in warns}
        passed = len(fails) == 0

        ok = True
        detail = ""
        if passed != expect_pass:
            ok = False
            detail = f"expected pass={expect_pass}, got pass={passed} (fail_rules={sorted(fail_rules)})"
        elif expect_rule and expect_rule not in fail_rules:
            ok = False
            detail = f"expected fail rule {expect_rule} in {sorted(fail_rules)}"
        elif expect_stamp and expect_stamp not in stamps:
            ok = False
            detail = f"expected stamp {expect_stamp} in {stamps}"
        elif expect_warn and expect_warn not in warn_rules:
            ok = False
            detail = f"expected warn rule {expect_warn} in {sorted(warn_rules)}"

        status = "OK" if ok else "ASSERT_FAIL"
        if not ok:
            all_ok = False
        print(
            f"  [{status}] {name}: fails={sorted(fail_rules)} warns={sorted(warn_rules)} stamps={stamps}"
            + (f" -- {detail}" if detail else "")
        )

    # 0. Compliant v2.3 pack
    assert_case("compliant_pack_v23", copy.deepcopy(base), expect_pass=True)

    # Legacy v2.2 rules (a-g)
    p_a1 = copy.deepcopy(base)
    p_a1["shots"][4]["gen_mode"] = "i2v_first"
    assert_case("rule_a_routing_lock_mode", p_a1, expect_pass=False, expect_rule="ROUTING_LOCK")

    p_a2 = copy.deepcopy(base)
    p_a2["shots"][3]["asset_refs"] = [
        {"asset_id": "S3B-FIRST-FRAME", "role": "first_frame"},
        {"asset_id": "FANLI-OUTFIT-02-45R", "role": "character"},
    ]
    assert_case("rule_a_routing_lock_refs", p_a2, expect_pass=False, expect_rule="ROUTING_LOCK")

    p_a3 = copy.deepcopy(base)
    p_a3["shots"][4]["gen_mode"] = "i2v_first"
    p_a3["shots"][4]["creator_waiver_signed"] = True
    p_a3["shots"][4]["demo_waiver_reason"] = "Colab L4 temporarily offline for layout test"
    assert_case("rule_a_routing_waiver_stamp", p_a3, expect_pass=True, expect_stamp="[ROUTING_WAIVED]")

    p_b1 = copy.deepcopy(base)
    p_b1["shots"][1]["video_prompt"] += " Do not move and remain motionless."
    assert_case("rule_b_bare_negation_en", p_b1, expect_pass=False, expect_rule="PROMPT_HYGIENE_NEGATION")

    p_b1z = copy.deepcopy(base)
    p_b1z["shots"][1]["image_prompt"] += " 男子貼牆不動，兩人都不說話。"
    assert_case("rule_b_bare_negation_zh", p_b1z, expect_pass=False, expect_rule="PROMPT_HYGIENE_NEGATION")

    p_b2 = copy.deepcopy(base)
    p_b2["shots"][0]["video_prompt"] = "真人電影，手持攝影，男子扶著牆喘息，鏡頭輕微晃動。"
    assert_case("rule_b_chinese_prose_flow", p_b2, expect_pass=False, expect_rule="PROMPT_HYGIENE_DIALECT")

    p_b2h = copy.deepcopy(base)
    p_b2h["shots"][3]["video_prompt"] = "Static camera. Fanli looks to the right in the dark alley."
    assert_case("rule_b_h3_missing_dialect", p_b2h, expect_pass=False, expect_rule="PROMPT_HYGIENE_DIALECT")

    p_c = copy.deepcopy(base)
    p_c["shots"][1]["video_prompt"] = "5s 9:16 single shot. Subtle handheld camera. Woman holds phone facing Fanli in the alley."
    p_c["shots"][1]["action"] = "Woman faces Fanli holding phone."
    p_c["shots"][1]["microexpression"] = "Tense stare."
    p_c["shots"][1]["performance_beat"] = {"from": "shock", "trigger": "phone raised", "to": "standoff"}
    assert_case("rule_c_two_shot_micro_motion", p_c, expect_pass=False, expect_rule="TWO_SHOT_MICRO_MOTION")

    p_d = copy.deepcopy(base)
    p_d["shots"][4]["dialogue"] = []
    assert_case("rule_d_lip_sensitive_missing_dialogue", p_d, expect_pass=False, expect_rule="LIP_SENSITIVE_DIALOGUE")

    p_d2 = copy.deepcopy(base)
    p_d2["shots"][4]["video_prompt"] = (
        "subject_definitions: <Pic 1> frame; <Pic 2> face.\n"
        "summary: Fanli speaks softly.\n"
        "retention_analysis: face=fully_preserved.\n"
        "detailed_description: Camera pushes in slowly. Fanli slowly opens his mouth and speaks softly.\n"
        "overall_soundscape: Alley hum.\n"
        "non_diegetic_music: N/A"
    )
    assert_case("rule_d_lip_sensitive_omitted_in_prompt", p_d2, expect_pass=False, expect_rule="LIP_SENSITIVE_DIALOGUE")

    p_e = copy.deepcopy(base)
    p_e["shots"][3]["video_prompt"] += " A glowing hologram floating screen with female avatar appears."
    assert_case("rule_e_sys01_ban_composite_ui", p_e, expect_pass=False, expect_rule="SYS01_BAN")

    p_e2 = copy.deepcopy(base)
    p_e2["shots"][0]["image_prompt"] += " SYS-01 彈窗與女性頭像浮現於右側。"
    assert_case("rule_e_sys01_ban_zh_mention", p_e2, expect_pass=False, expect_rule="SYS01_BAN")

    p_f = copy.deepcopy(base)
    p_f["shots"][2]["first_frame"] = {"source": "generated"}
    p_f["shots"][2]["asset_refs"] = [
        {"asset_id": "LOC-ALLEY-NIGHT", "role": "scene"},
        {"asset_id": "WITNESS-WOMAN-01", "role": "character"},
    ]
    assert_case("rule_f_same_location_lone_loc", p_f, expect_pass=False, expect_rule="SAME_LOCATION_DERIVATION")

    p_g = copy.deepcopy(base)
    p_g["shots"][0]["video_prompt"] += " His pupils contract sharply and eyelashes quiver in an extreme close-up."
    assert_case("rule_g_scale_jump_ban", p_g, expect_pass=False, expect_rule="SCALE_JUMP_BAN")

    # v2.3 Item 1: ASSET_CONTRACT & REF_COUNT_BUDGET
    p_v1_overlap = copy.deepcopy(base)
    p_v1_overlap["shots"][0]["asset_refs"][1]["owns"] = ["identity", "costume"]
    p_v1_overlap["shots"][0]["asset_refs"][1]["never_inherit"] = ["costume"]
    assert_case("v23_item1_owns_never_inherit_overlap", p_v1_overlap, expect_pass=False, expect_rule="ASSET_CONTRACT")

    p_v1_card = copy.deepcopy(base)
    p_v1_card["shots"][0]["asset_refs"][1]["asset_id"] = "fanli-modern-charactercard-main"
    assert_case("v23_item1_uncropped_charactercard", p_v1_card, expect_pass=False, expect_rule="ASSET_CONTRACT")

    p_v1_l3_cap = copy.deepcopy(base)
    p_v1_l3_cap["shots"][0]["engine_route"] = "h3"
    p_v1_l3_cap["shots"][0]["gen_mode"] = "ref2v"
    p_v1_l3_cap["shots"][0]["control_method"] = "L3_clay_ref2v"
    p_v1_l3_cap["shots"][0]["video_prompt"] = p_v1_l3_cap["shots"][3]["video_prompt"]
    p_v1_l3_cap["shots"][0]["asset_refs"] = [
        {"asset_id": "LOC-ALLEY-NIGHT", "role": "scene"},
        {"asset_id": "FANLI-OUTFIT-02-CU", "role": "character"},
        {"asset_id": "FANLI-OUTFIT-02-45", "role": "character"},
        {"asset_id": "FANLI-OUTFIT-02-45R", "role": "character"},
        {"asset_id": "CLAY-S1", "role": "previs_video"},
    ]
    assert_case("v23_item1_l3_l4_ref_budget", p_v1_l3_cap, expect_pass=False, expect_rule="REF_COUNT_BUDGET")

    # v2.3 Item 2: V13_AUTHORITY_CONFLICT & V13_ORPHAN_ASSET
    p_v13_age = copy.deepcopy(base)
    p_v13_age["shots"][4]["asset_refs"].append({"asset_id": "FANLI-MASTER-A", "role": "character", "owns": ["identity"]})
    assert_case("v23_item2_v13_age_conflict", p_v13_age, expect_pass=False, expect_rule="V13_AUTHORITY_CONFLICT")

    p_v13_orphan = copy.deepcopy(base)
    p_v13_orphan["shots"][0]["asset_refs"][0]["owns"] = []
    assert_case("v23_item2_v13_orphan_asset", p_v13_orphan, expect_pass=False, expect_rule="V13_ORPHAN_ASSET")

    p_v13_env = copy.deepcopy(base)
    p_v13_env["shots"][4]["asset_refs"].insert(1, {"asset_id": "LOC-ALLEY-NIGHT", "role": "scene"})
    assert_case("v23_item2_v13_duplicate_env_lighting", p_v13_env, expect_pass=False, expect_rule="V13_AUTHORITY_CONFLICT")

    # v2.3 Item 3: ERA_ANCHOR_CONFLICT
    p_era = copy.deepcopy(base)
    p_era["shots"][0]["action"] += " Fanli fingers a square-hole bronze coin while glancing at his wristwatch."
    assert_case("v23_item3_era_anchor_conflict", p_era, expect_pass=False, expect_rule="ERA_ANCHOR_CONFLICT")

    # v2.3 Item 4: PERF_INTENSITY_CONFLICT, PERF_LEXICON_UNKNOWN, AI_FACE_TABOO, min_shot_size
    p_perf_hold = copy.deepcopy(base)
    p_perf_hold["shots"][0]["performance_beat"]["deliberate_hold"] = True
    p_perf_hold["shots"][0]["performance_beat"]["intensity"] = "L3"
    assert_case("v23_item4_deliberate_hold_l3", p_perf_hold, expect_pass=False, expect_rule="PERF_INTENSITY_CONFLICT")

    p_perf_sz = copy.deepcopy(base)
    p_perf_sz["shots"][0]["performance_beat"]["lexicon_ids"] = ["z2_hairline_knit"]
    assert_case("v23_item4_lexicon_min_shot_size", p_perf_sz, expect_pass=False, expect_rule="SCALE_JUMP_BAN")

    p_taboo = copy.deepcopy(base)
    p_taboo["shots"][4]["image_prompt"] = "9:16 CU of Fanli with porcelain skin and radiant smile. Avoid: text."
    assert_case("v23_item4_ai_face_taboo", p_taboo, expect_pass=False, expect_rule="AI_FACE_TABOO")

    # v2.3 Item 5: CROSS_ERA_CHAR_SCOPE, FLIP_ASSET_BAN, UNSEEN_SIDE_GUARD
    p_xera = copy.deepcopy(base)
    p_xera["shots"][4]["asset_refs"][1] = {"asset_id": "FANLI-MASTER-B-USERFACE", "role": "character"}
    assert_case("v23_item5_cross_era_char_scope", p_xera, expect_pass=False, expect_rule="CROSS_ERA_CHAR_SCOPE")

    p_flip = copy.deepcopy(base)
    p_flip["shots"][4]["asset_refs"][3]["asset_id"] = "fanli-master-ancient-45R.v1-flip-defect"
    assert_case("v23_item5_flip_asset_ban", p_flip, expect_pass=False, expect_rule="FLIP_ASSET_BAN")

    p_unseen = copy.deepcopy(base)
    p_unseen["shots"][4]["asset_refs"] = [
        {"asset_id": "S4-FIRST-FRAME", "role": "first_frame"},
        {"asset_id": "FANLI-OUTFIT-02-CU", "role": "character"},
        {"asset_id": "FANLI-OUTFIT-02-45", "role": "character"},
    ]
    p_unseen["shots"][4]["image_prompt"] = "9:16 CU of Fanli facing screen right in dark alley. Avoid: text."
    assert_case("v23_item5_unseen_side_guard", p_unseen, expect_pass=False, expect_rule="UNSEEN_SIDE_GUARD")

    # v2.3 Item 6: VOICE_AUTHORITY_LOCK
    p_voice = copy.deepcopy(base)
    p_voice["shots"][4]["dialogue"][0]["voice_id"] = "rogue_voice_999"
    assert_case("v23_item6_voice_override_ban", p_voice, expect_pass=False, expect_rule="VOICE_AUTHORITY_LOCK")

    # v2.3 Item 7b: Advisory WARN (passes with rc=0, emits WARN)
    p_warn = copy.deepcopy(base)
    p_warn["shots"][0]["video_prompt"] += " Epic masterpiece 8K."
    assert_case("v23_item7b_advisory_craft_warn", p_warn, expect_pass=True, expect_warn="CRAFT_OBSERVABLE_ACTION")

    # v2.3 Item 7c: AUDIO_BED_HYGIENE
    p_aud = copy.deepcopy(base)
    p_aud["shots"][4]["ambient_source"] = "native_keep"
    assert_case("v23_item7c_audio_bed_hygiene", p_aud, expect_pass=False, expect_rule="AUDIO_BED_HYGIENE")

    # v2.3 Item 7d: V1_DURATION_ENVELOPE (L3 on L4 > 5.0s)
    p_dur = copy.deepcopy(base)
    p_dur["shots"][0]["engine_route"] = "h3"
    p_dur["shots"][0]["gen_mode"] = "ref2v"
    p_dur["shots"][0]["control_method"] = "L3_clay_ref2v"
    p_dur["shots"][0]["target_net_sec"] = 4.5
    p_dur["shots"][0]["trim_policy"] = "standard_0.5s"  # gen_sec = 5.5 > 5.0
    p_dur["shots"][0]["video_prompt"] = p_dur["shots"][3]["video_prompt"]
    assert_case("v23_item7d_l3_l4_duration_cap", p_dur, expect_pass=False, expect_rule="V1_DURATION_ENVELOPE")

    print(f"=== SELFTEST {'PASSED' if all_ok else 'FAILED'} ===")
    return 0 if all_ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Workflow V2.3 Preflight Validation Gate (QC-0)"
    )
    parser.add_argument("script_pack", nargs="?", help="Path to script_pack.json (schema 2.0–2.3)")
    parser.add_argument("--mode", choices=["normal", "demo"], default=None, help="Override production_mode")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    parser.add_argument("--selftest", action="store_true", help="Run built-in self-test suite")
    args = parser.parse_args()

    if args.selftest:
        return run_selftest()

    if not args.script_pack:
        parser.error("Provide script_pack.json path or --selftest")

    path = Path(args.script_pack)
    if not path.is_file():
        print(f"FAIL [IO_ERROR] file not found: {path}", file=sys.stderr)
        return 2

    with path.open("r", encoding="utf-8") as fh:
        pack = json.load(fh)

    findings, stamps = validate_script_pack(pack, mode_override=args.mode)
    if args.json:
        fails = [f for f in findings if f.level == "FAIL"]
        payload = {
            "file": str(path),
            "result": "PASS" if not fails else "FAIL",
            "stamps": stamps,
            "findings": [asdict(f) for f in findings],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if not fails else 1

    report, rc = format_report(findings, stamps, label=str(path))
    print(report)
    return rc


if __name__ == "__main__":
    sys.exit(main())
