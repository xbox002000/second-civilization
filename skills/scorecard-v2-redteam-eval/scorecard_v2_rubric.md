# Scorecard v2 Rubric & Calibration Protocol (Frozen Reference)

> Distilled verbatim from `~/drama-line/SCORECARD-V2-PROPOSAL.md` (2026-11-27, proven across 5 EP-01 evaluation runs).

## 1. Six Scored Dimensions (Total = 100 pts)

| # | Dimension | Max | Operational Definition & Anchor Bands (Evidence-First: Quote Shot ID + Lines) |
| :-: | :--- | :-: | :--- |
| **1** | **Opening Hook & Premise Clarity** *(開場鉤子與命題清晰)* | **18** | Before first dialogue turn (~6s): **(a)** protagonist is directly in concrete conflict/anomaly (no intro/greeting/exposition); **(b)** viewer can state the concrete question in 1 sentence; **(c)** partial info makes the gap felt. Bands: `16–18` all 3 met; `10–15` conflict present but vague question; `5–9` visual only, no question; `0–4` exposition opening. |
| **2** | **Causal Coherence & Mechanism Clarity** *(因果連貫與機制清晰)* | **22** | Every major turn is caused by previously stated facts. Binary checks: rules/mechanism/leverage introduced before first use? Zero contradiction with prior scenes/facts? Cold reader can retell causal chain without filling gaps? **BUILT-IN HARD GATE: Any mechanism/POV contradiction or uncaused climax caps TOTAL SCORE AT `59`, regardless of all other dimensions.** |
| **3** | **Escalation, Value Turns & Payoff** *(升級、價值轉折與兌現)* | **18** | Count **value turns** (measurable shift in status/safety/knowledge/relationship), not busyness: ~3–5 real turns across 60–100s with rising stakes, AND at least one setup paid off inside this episode (not pure IOUs). Flat middle or repetitive same-intensity arguing scores low. |
| **4** | **Episode-End Open Loop** *(集尾開放迴路)* | **16** | Final beat opens a **concrete, fairly planted, next-episode-solvable** question and cuts before answering. All 3 required: statable in 1 sentence; planted earlier (no deus-ex cliffhanger); episode already delivered partial payoff. Random blackout / dream fakeout / vague question = `≤ 6`. |
| **5** | **Character Empathy, Motive & Dialogue** *(角色共感、動機與對白)* | **16** | Main characters' wants & leverage readable from action/dialogue (not narration); at least one beat where audience understands protagonist's emotion; dialogue voices distinguishable with names hidden; worthy opposition & costly wins. |
| **6** | **Surprise & Retroactive Freshness** *(驚奇與可回溯的新意)* | **10** | Mid/end turn is unexpected **AND retroactively fair** on second read (contradicting established facts fails D2 instead). **Smallest weight by design; LLM may ONLY serve as documented third vote, NEVER sole decider.** |

---

## 2. Four Project Hard Gates (Zero-Weight Veto — Any FAIL Rejects Draft)

1. **Gate 1 — IP Red Lines**: Accurate `FACT`/`INFERENCE`/`FICTION` layering; real people appear ONLY in the `FACT` news layer (never impersonated, never attributed unverified motives); Fan Li is non-omniscient (memory ≤ Spring-Autumn + 2022–2026).
2. **Gate 2 — One-Sentence Story Test**: Cold reader can answer: who wants what / who blocks them / what happens if they lose.
3. **Gate 3 — AI Shootability**: Every atomic shot `≤ 6.5s`; dialogue rate `≤ 5.0` pure chars/sec (`≤ 5.5` with punctuation; faster scripts inflate TTS length by `> 30%`); zero 3-person long dialogue shots.
4. **Gate 4 — Independent Fact Verification**: Every `FACT` item on the Event Card has an L1/L2 URL, `event_time`, `data_cutoff_at`, and verified metric definition (intraday vs closing, exact date, exact calendar arithmetic, primary historical text).

---

## 3. Calibration & Adjudication Protocol

1. **Evidence first, score second**: Every dimension MUST cite verbatim script lines / shot IDs before assigning a number. Uncited scores are rejected.
2. **Binary sub-checks anchor bands**: Disagreements must localize to a specific binary check (`Y/N`), not vague taste.
3. **Blind & independent**: Evaluators never see author self-scores or each other's scores before submitting.
4. **Adjudication rule**:
   - `|Δtotal| ≤ 5` AND every `|Δdim| ≤ 4` AND identical Hard Gate verdicts → average and close.
   - Any breach (`|Δtotal| > 5`, `|Δdim| > 4`, or Hard Gate mismatch) → **mandatory evidence-based adjudication**. **NEVER silently average a `> 5` gap.**
5. **LLM as third vote only**: Fixed rubric + verbatim quotes; never sole gatekeeper for D6 or Creator Gate A3.
