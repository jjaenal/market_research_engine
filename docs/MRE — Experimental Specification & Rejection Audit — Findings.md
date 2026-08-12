# MRE — Experimental Specification & Rejection Audit (Findings)

> Companion report to `docs/MRE — Experimental Specification & Rejection Audit.md`.
> Scope: EXP-001 .. EXP-008 (RSI Trendline Breakout H1, Price Breakout H1/H4,
> Swing Breakout H4 + combined mitigations). READ-ONLY audit — no source,
> config, or experiment files were modified. All proposed changes are presented
> as PROPOSED CHANGE blocks in §E/§F; none were applied.

---

# A. Executive Summary

**Experiments audited:** 8 (EXP-001 through EXP-008).

**Counts:**
- Conclusions that are **logically valid** against their own pre-registered criteria: 5 (EXP-002, EXP-003, EXP-004, EXP-005, EXP-006).
- Conclusions that are **inconclusive / compromised** by specification or implementation issues: 3 (EXP-001, EXP-007, EXP-008).
- Experiments with **material specification problems** (grade C or below): 3 (EXP-004, EXP-007, EXP-008).
- Verdicts that are **fully robust** (survive the audit unchanged): 3 (EXP-005, EXP-006 structural rejections; EXP-003 SUPPORTED).

**Major recurring issues:**

1. **Fractal/swing backdating (systemic lookahead, highest severity).** Swing-high events are timestamped at the peak candle (`swing.py:50-54`) but only become knowable `right` (=2) candles later. Every swing-based signal (all strategies) can therefore be emitted — and the trade entered — before the swing is confirmable. EXP-005/006 (swing = confirmation) enter 1–2 candles early; EXP-007/008 (swing = trigger) can consume the entry candle's own close (same-bar leak). The "no lookahead" guarantees in the docs (EXP-002 §4, EXP-004 §10, EXP-007 §8/§16) are **approximately, not exactly, true**. The existing tests check event-prefix consistency, not signal→entry timing.

2. **ATR-multiple SL/TP uses the entry bar's own OHLC** (`simulation_engine.py:134-139`). The SL/TP distance is anchored at `atr_series[entry_bar]`, and Wilder ATR at index `entry_bar` includes the entry bar's own high/low/close — information not available at the entry-bar open where the levels must be set. Affects EXP-004 and EXP-008 (the two experiments whose object is SL/TP).

3. **Duplicate/overlapping trades inflate all pre-EXP-008 runs.** With `cooldown: 0`, `combine()` reuses one confirmation for multiple proximate triggers, and `simulate()` has no overlap/concurrency guard — each signal becomes a full independent trade (verified: 2 triggers + 1 confirmation → 2 identical trades at the same bar). Trade counts (e.g., EXP-005 n=3,882) and aggregate metrics are inflated in EXP-001..007.

4. **Breakeven — a primary pre-registered acceptance metric — is computed by hand in the docs**, not by any engine path. Every "breakeven ≥ X bps" criterion (EXP-002..008 §13) is evaluated via doc-arithmetic interpolation over the printed cost grid. Not reproducible from code.

5. **Decision criteria drifted across the experiment series.** EXP-002 pre-registered only `expectancy > 0 @ 1.0 bps/side, n ≥ 30, breakeven ≥ 1.0 bps` (no stationarity) and was declared SUPPORTED. EXP-003 onward added `OOS train > 0` stationarity and EXP-004 raised the breakeven bar to ≥ 3.44 bps. EXP-007/008 were rejected on the stationarity criterion that did not exist when EXP-002 was approved. The SUPPORTED/REJECTED standard is not comparable across experiments.

6. **No formal multiple-testing / data-snooping control** anywhere in RSH-001..004 or the EXP docs — only pre-registration and narrative "no parameter mining" rules. The robustness combo grid is degenerate (varies `rsi_period` on strategies that do not consume RSI → 2 of 5 rows duplicated), and the cost grid omits the actual 1.0 bps/side venue cost.

7. **Market definition is thin and uniform.** No upstream data origin, no trading session/hours statement, timezone implicit (UTC via YAML), missing/duplicate/gap handling left to code and asserted only as "Integrity: valid". The H4 provenance note (EXP-006/007/008 §7) is the single exception and a model for the rest.

8. **Documentation↔implementation mismatches.** EXP-007/008 "entry at the breakout candle" (§1/§8) contradicts §10 "next bar open" (code = next bar open). EXP-004 §10 "whichever SL/TP is touched first" contradicts code's fixed SL-first priority. EXP-007/008 §10 "exit at open of hold_bars-th bar" contradicts code's exit at the **close** of that bar. Signal `window` is frozen in plugin code, not YAML (FR-012/RSH-002 §9 gap).

9. **Segment artifact hazards.** `run_on_slice` hardcodes the `XAUUSD_H1_` file prefix (`segments.py:59`) — H4 experiments write mislabeled "H1" segment CSVs; cross-market robustness hardcodes `_H1_` (`robustness.py:105`), comparing an H4 strategy against H1 XAGUSD data (disclosed but a genuine confound). Normalized-dataset caching is existence-based with no freshness check (`experiment_runner.py:133-135`, `segments.py:34-36`), and `write_candle_csv`'s `:g` formatting rounds prices to ~6 significant digits, so OOS/robustness segments run on lower-fidelity prices than the baseline.

---

# B. Experiment Audit Matrix

| Experiment | Current Status | Specification Quality | Rejection Validity | Main Issue |
|---|---|---|---|---|
| EXP-001 | REJECTED (M7 final) | B | `VALID_REJECTION` at ≥ 0.05%/side, but overbroad as "realistic cost"; superseded by EXP-002 | No numeric pre-registered criteria; §19.7 breakeven "26 bps" contradicts its own grid (self-flagged by EXP-002 §18.2) |
| EXP-002 | SUPPORTED | B | Valid per §13 (SUPPORTED) | Cost model: 3 components (spread/comm/slip) mapped to 2 rates (0.3+0.7 bps) without stating how spread is folded; OOS train negative yet SUPPORTED (stationarity criterion did not exist) |
| EXP-003 | SUPPORTED | B | Valid per §13 (SUPPORTED) | OOS-train margin razor-thin (+0.1297); post-hoc 4/8 fine slices temper but do not contradict; segment warm-up non-additivity undocumented |
| EXP-004 | REJECTED | C | `VALID_REJECTION` per §13 (breakeven 3.31 < 3.44) — margin is ~0.13 bps on a hand-interpolated breakeven | **Same-bar SL/TP collision doc-vs-code contradiction** ("whichever first" vs SL-first); ATR-at-entry-bar "no lookahead" only approximate; gap & entry-bar SL eligibility undocumented |
| EXP-005 | REJECTED | B | `VALID_REJECTION` (structural, 0/4) — robust | Gross edge absent at zero cost (−3.1186); duplicate-trade inflation; degenerate combo grid (rsi_period inert) |
| EXP-006 | REJECTED | B | `VALID_REJECTION` (structural, 0/4) — robust | Same as EXP-005 + cross-timeframe XAGUSD confound (H4 strategy vs H1 data); Δ sign-convention inconsistency |
| EXP-007 | REJECTED | C | `INCONCLUSIVE` | **Entry timing contradiction** ("breakout candle" vs next-bar open) + **swing backdating lookahead** → gross edge +0.4775 and OOS numbers may be artifacts of early entry; fixed 70/30 split isolates profitable period into test (split-point not run) |
| EXP-008 | REJECTED | C | `INCONCLUSIVE` (rejection itself valid per criteria; the "NOT a stationarity mechanism" conclusion is evidence-compromised) | Inherits EXP-007 contradiction + lookahead; **ATR SL/TP same-bar leak** directly affects the mitigation that drove the risk/cost improvement; breakeven ≈ 8.8 bps is hand-interpolated; no split-point OOS |

**Summary:** 5 verdicts are valid per their own criteria (EXP-002/003/004/005/006); 3 are compromised (EXP-001 partially, EXP-007/008 materially). All four REJECTED verdicts follow logically from their own pre-registered rules, but EXP-007/008 rest on evidence contaminated by the swing-backdating lookahead.

---

# C. Detailed Audit Per Experiment

## C.1 EXP-001 — RSI Trendline Breakout Baseline

**Current Status:** REJECTED (final M7 verdict; originally "PARTIALLY SUPPORTED")

**Specification Quality:** B (deterministic strategy; but no numeric pre-registered decision criteria exist — §13 is "Expected Outputs", not criteria — and the rejection is a researcher conclusion)

**Rejection Validity:** `VALID_REJECTION` for the stated ≥ 0.05%/side threshold (grid unambiguously negative there). **Not** valid as a general claim about "realistic venue costs": the real retail ECN cost later measured at ~0.4–1.2 bps/side (EXP-002) is far below the 2–5 bps grid, and the edge survives there (EXP-002 SUPPORTED). The rejection framing was miscalibrated; superseded.

**Market Definition:** instrument/dataset/timeframe/date-range/candle-count EXPLICIT; timezone IMPLICIT (UTC via YAML + split point); trading session/hours NOT_APPLICABLE-but-undeclared (no session filter, never stated); data source vendor MISSING; missing/duplicate/gap handling MISSING; ordering/OHLC rules IMPLICIT (code `validator.py`, doc only "Integrity: valid").

**Strategy Definition:** trigger `RSI_TRENDLINE_BROKEN` (down-trendline, slope<0) + confirmation `PRICE_CONFIRMATION` (close > 20-bar high, strict). Fractal strictness, tie handling (strict, ties disqualify), close-based breakout — all IMPLICIT (delegated to ADR-003/ADR-004/code). RSI-swing trendline applied to RSI series (not price) — undocumented in EXP-001.

**Signal Timing:** trendline break known at bar t (RSI[t]); price confirmation at c. Entry next-bar open (§10 EXPLICIT). Swing backdating (§C.9 finding) applies to the trendline anchor swings.

**Entry:** next-bar open, market order, size 1.0, zero cost (§10 EXPLICIT). Duplicate/overlapping trades acknowledged in §15 (signal overlap) but not resolved — `cooldown 0`.

**SL/TP:** N/A (None; hold_bars 10). M7 ATR SL/TP appears only in iteration §19.7.

**Position Lifecycle:** LONG-only EXPLICIT; concurrency IMPLICIT (allowed by code).

**Cost:** 0 (baseline by design, §9.4/§10 EXPLICIT); synthetic 2/5 bps grids in §18.3.

**Statistics/OOS:** metrics per RSH-002 §8; **no numeric decision criteria**. OOS split 70/30 @ index 70,000; train 943 + test 453 = 1396 ≠ 1403 baseline — segment re-initialization (warm-up loss at split boundary) unexplained. Multiple-testing: sensitivity winners explicitly not used for optimization (good).

**Documentation vs Implementation:** consistent for entry/exit; §19.7 breakeven table ("26 bps") internally contradicts the same section's grid (expectancy already negative at 5 bps) — self-flagged by EXP-002 §18.2.

**Critical Ambiguities / Evidence:** (1) no numeric pre-registered criteria; (2) §19.7 breakeven inconsistency; (3) market-source/timing documentation gaps; (4) segment non-additivity.

**Conclusion:** the ≥0.05%/side rejection is valid; the "realistic cost" framing was miscalibrated and is superseded by EXP-002/003. Grade B.

## C.2 EXP-002 — Real Venue Execution Cost

**Current Status:** SUPPORTED

**Specification Quality:** B. Pre-registered §13 criteria clear and minimal: `expectancy > 0 @ 1.0 bps/side, n ≥ 30, breakeven ≥ 1.0 bps`.

**Rejection Validity:** Valid — SUPPORTED follows logically (0.5111 > 0, n=1403 ≥ 30, breakeven ≈ 2.43 ≥ 1.0 bps). The doc correctly layers the separate researcher concern (temporally non-stationary, OOS train −0.1605) outside the pre-registered verdict.

**Market Definition:** same as EXP-001 (inherited). **Cost Model:** §9.5 lists three components (spread ~$6/lot, commission $3.50/lot/side, slippage ~$2/lot/side ≈ 0.64 bps/side total) yet freezes two rates (0.3 + 0.7 = 1.0 bps/side); how the spread component maps into the two rates is IMPLICIT. Realism: SIMPLIFIED–APPROXIMATE (public broker reviews, flat across price levels, not tick data).

**Statistics/OOS:** §13 quoted exactly (EXP-002 §13). OOS split 70/30 @ 70,000: train −0.1605 / test +1.9810; non-additivity (1396 ≠ 1403) again unexplained. Robustness: 1/4 slices positive, XAGUSD +0.0342, 3/5 combos.

**Critical Ambiguities:** spread→rates mapping; `atr_period 14` present but unused; segment non-additivity.

**Conclusion:** valid verdict; the main defects are cost-model mapping and inherited market gaps. Grade B.

## C.3 EXP-003 — Volatility Regime Segmentation

**Current Status:** SUPPORTED

**Specification Quality:** B — the regime pre-registration is the clearest of the series (§9.7, §13 four conjunctive criteria).

**Rejection Validity:** Valid — all four §13 criteria met (expectancy 0.8887, n=698; breakeven 3.44; OOS test +2.4853; OOS train +0.1297). Post-hoc 4/8 fine slices and BELUM TRADABLE status are correctly separated from the pre-registered verdict.

**Market Definition:** same as EXP-001/002 (inherited gaps).

**Signal Timing:** regime label anchored at the signal's confirmation candle via `volatility_regime` (causal) — no lookahead in the label itself (EXPLICIT and correct, modulo the swing-backdating caveat for the signal timestamp).

**Statistics/OOS:** OOS train 446 + test 253 = 699 vs baseline 698 — +1 trade edge effect, unexplained. Newer-data deferral thoroughly documented (exemplary §18.4).

**Critical Ambiguities:** OOS-train margin razor-thin (+0.1297 > 0 by construction); 4/8 fine slices; segment warm-up.

**Conclusion:** valid. Grade B.

## C.4 EXP-004 — ATR-multiple SL/TP at Venue Cost

**Current Status:** REJECTED

**Specification Quality:** C — the very experiment whose object is SL/TP has the most material exit-mechanics ambiguities.

**Rejection Validity:** `VALID_REJECTION` per §13 — breakeven ≈ 3.31 < 3.44 bps control. **Caution:** the pass/fail margin is ~0.13 bps, and the breakeven is **hand-interpolated** from the fine grid (expectancy jumps +0.0341 @3.30 → −0.0303 @3.31 bps, a steep crossing). The rejection is logically valid but quantitatively fragile.

**SL/TP:** formula EXPLICIT (SL = entry − 1.0×ATR(14), TP = entry + 4.0×ATR(14)). **Doc-vs-code contradiction:** §10 says "whichever level is touched first" but code applies fixed SL-first priority per bar (conservative). Gap handling and entry-bar SL eligibility MISSING. **ATR anchoring:** "no lookahead" claim (at `atr_series[entry_bar]`) includes the entry bar's own OHLC — approximate, not exact.

**Hypothesis/criterion mismatch:** §6 hypothesis says SL/TP *raises* cost tolerance; §13 only requires breakeven ≥ 3.44 (not lowering). Result fails under either reading, so verdict unaffected — but wording not aligned.

**Statistics/OOS:** train +0.2026 / test +2.9515 (stationary); robustness 3/4 coarse, 6/8 fine, 5/5 combos, 4/4 split-point — the strongest OOS/robustness of the series.

**Conclusion:** valid rejection per criteria; SL/TP exit mechanics under-specified (same-bar, gap, ATR anchor). Grade C.

## C.5 EXP-005 — Price Breakout (Donchian-style) H1

**Current Status:** REJECTED

**Specification Quality:** B

**Rejection Validity:** `VALID_REJECTION` — 0/4 criteria; expectancy −3.4848 @ 1.0 bps/side, negative even at zero cost (−3.1186) → structural failure independent of cost model; OOS train −2.6301 / test −5.2396 both negative; 0/4 slices, 0/5 combos, XAGUSD −0.1232. The structural-failure characterization follows directly from the zero-cost evidence. **Robust.**

**Market Definition:** same gaps as EXP-001 (timezone implicit, session MISSING, origin AMBIGUOUS, tie handling MISSING).

**Strategy Definition:** trigger `PRICE_CONFIRMATION` (close > 20-bar high, strict) → confirmation `SWING_HIGH` (window 5). Breakout = close-based; ties strict (IMPLICIT). Swing = confirmation, subject to **backdating lookahead** (enters 1–2 candles before the swing is confirmable) — this would *help* a momentum strategy, so the negative result is conservative.

**Entry:** next-bar open (§10 EXPLICIT). Duplicate trades via confirmation reuse + cooldown 0 (n=3,882 inflated).

**Statistics/OOS:** §13 quoted exactly (identical 4-criteria block). Robustness combo grid varies `rsi_period` on a non-RSI strategy → 10/7 == 10/21 and 30/7 == 30/21 (only 3 effective points, presented as "0/5").

**Conclusion:** valid, robust rejection. Grade B.

## C.6 EXP-006 — Price Breakout H4

**Current Status:** REJECTED

**Specification Quality:** B

**Rejection Validity:** `VALID_REJECTION` — 0/4; expectancy −8.3297, negative at zero cost (−7.9576); OOS train −5.0451 / test −14.2008; 0/4 slices, 0/5 combos, XAGUSD −0.1232. Robust.

**Market Definition:** H4 provenance exemplary (separate export, cross-verified against 4×H1 aggregate, 1 tail-bar mismatch) — the model for other experiments. Session/origin/tie-handling gaps remain.

**Statistics/OOS:** identical criteria; **Δ Test/Train sign convention inconsistent** with EXP-005 §16 (+181.5% here vs −99.2% there for the same kind of worsening). Cross-market XAGUSD (H1) against an H4 strategy — disclosed, but a confound. Combo grid degenerate as in EXP-005.

**Conclusion:** valid, robust rejection. Grade B.

## C.7 EXP-007 — Swing Breakout (Fractal Structure) H4

**Current Status:** REJECTED (3/4 criteria; line later CLOSED)

**Specification Quality:** C

**Rejection Validity:** `INCONCLUSIVE`. The verdict *logically* follows from the all-or-nothing §13 rule (OOS train −1.8114 < 0). However the evidence is compromised:

- **Entry timing contradiction:** §1/§8 "entry pada candle breakout" vs §10 "next bar open setelah sinyal". Code executes next-bar-open. A backtest fill at the breakout candle would differ materially.
- **Swing backdating lookahead:** swing-high trigger is timestamped at its peak (knowable only `right`=2 bars later); a PRICE_CONFIRMATION at i+1 yields a signal at i+1 and entry at the open of i+2 — which uses the entry candle's own close (same-bar leak). The **gross edge (+0.4775 at zero cost) and the OOS train/test numbers may be artifacts of early entry**, not a genuine edge.
- **Fixed 70/30 split** (index 18,771) isolates the entire profitable final period (period-4-of-4 ≈ 2022–2026) into test; OOS train is structurally starved of the edge era. Split-point OOS (available in RSH-003, used by EXP-003/004) was not run.
- XAGUSD cross-market (H1 vs H4) confound; degenerate combo grid.

The conclusion "first gross edge on XAUUSD, but temporally non-stationary" **cannot be treated as definitive evidence** until the lookahead is removed and timing re-specified.

**Conclusion:** INCONCLUSIVE — the rejection is not validly evidenced. Grade C.

## C.8 EXP-008 — Swing Breakout + Combined Mitigations

**Current Status:** REJECTED (3/4 criteria; line CLOSED §18.4)

**Specification Quality:** C

**Rejection Validity:** `INCONCLUSIVE`. The pre-registered verdict (OOS train −0.6073 < 0 → REJECTED) is *logically* consistent, and the risk/cost-tolerance improvements are striking (breakeven ≈ 8.8 bps/side, Max DD −78%). But:

- **Inherits EXP-007's lookahead + entry-timing contradiction** — the baseline expectancy (+2.6211) and breakeven (~8.8 bps) are computed on lookahead-contaminated trades.
- **ATR SL/TP same-bar leak** directly affects the very mitigation (SL/TP 1.0/4.0) that drove the risk improvement — SL/TP distance uses the entry bar's own OHLC.
- Breakeven ≈ 8.8 bps/side is **hand-interpolated** (§15.3; also a minor labeling imprecision: "comm=0.0005" = 5 bps commission, the 10 bps point is the 5+5 row).
- Same-bar collision priority and gap-through-open fills undocumented (code: SL-first, gap-fill at open).
- No split-point OOS despite the stationarity criterion being the entire object of the experiment.

The conclusion "mitigations are a risk/cost-tolerance mechanism, NOT a stationarity mechanism" is **directionally supported but evidence-compromised** — it should not be treated as a definitive finding until the lookahead is removed.

**Conclusion:** INCONCLUSIVE — the rejection and its interpretive layer rest on lookahead-contaminated evidence. Grade C.

---

# D. Cross-Experiment Findings (systemic weaknesses)

1. **Swing/fractal backdating is systemic** — every strategy uses swing events as trigger or confirmation, and every swing event is timestamped at its (not-yet-knowable) peak. This is the single largest threat to the validity of EXP-001..008 signal timing and therefore their OOS/robustness evidence.

2. **SL/TP execution semantics are under-specified everywhere they appear** — same-bar collision (doc "whichever first" vs code SL-first), gap-through-open fills, entry-bar SL eligibility, and the ATR anchoring point. EXP-004 and EXP-008 both depend on these rules, yet none are deterministic-documented.

3. **Breakeven — the primary acceptance metric — is not engine-computed.** It is hand-interpolated in every doc. Reproducibility (RSH-002 §9, NFR-001) is violated for the metric that decides SUPPORTED/REJECTED in EXP-002..008.

4. **Decision criteria drifted and are not comparable across experiments** — EXP-002 SUPPORTED without the stationarity criterion that later rejected EXP-007/008; EXP-004 raised the breakeven bar. The series does not hold a consistent acceptance standard.

5. **No formal multiple-testing / data-snooping control.** The robustness machinery itself is degenerate (inert `rsi_period` in the combo grid; the cost grid omits the actual 1.0 bps/side venue cost).

6. **Market definition is thin and uniform** — origin, session, timezone, missing/duplicate/gap handling are undocumented except as "Integrity: valid". The H4 provenance note shows the expected standard.

7. **Duplicate-trade inflation** — `cooldown 0` + confirmation reuse + no overlap guard inflate n and distort aggregate metrics in EXP-001..007.

8. **Segment artifacts** — hardcoded `XAUUSD_H1_` prefix for H4 slices; cross-timeframe XAGUSD; `:g` price rounding in segment CSVs; existence-based normalized cache with no freshness check; content-blind dataset versioning.

9. **Documentation↔implementation drift** — entry-at-breakout-candle vs next-bar-open; exit-at-open vs exit-at-close; window frozen in plugin code not YAML; decision criteria recorded inconsistently.

---

# E. Required Specification Improvements (determinism only — no strategy changes)

Each item: PROPOSED CHANGE / Reason / Affected Document / Expected Benefit / Research Risk.

### E-1. Fix swing/fractal backdating
- **PROPOSED CHANGE:** Swing events must carry a `confirmable_at` (or be timestamped at the confirmation bar, `i + right`), and the signal engine / simulation must guarantee entry occurs after all constituent events are knowable. Same-bar leakage must be excluded.
- **Reason:** systemic lookahead in all swing-based signals; invalidates signal-timing and OOS evidence.
- **Affected Document:** SPEC Swing Detection (new), ENG-002, simulation_engine.py, swing.py, event_engine.py.
- **Expected Benefit:** deterministic, truly causal signals; OOS/train/test evidence becomes trustworthy.
- **Research Risk:** reported metrics (EXP-005..008) will change; historical numbers must NOT be rewritten (Rule 2) — they must be re-run under the corrected spec and recorded as new evidence.

### E-2. Fix ATR-multiple SL/TP anchoring
- **PROPOSED CHANGE:** SL/TP ATR distance must anchor at `atr_series[entry_bar − 1]` (the last closed bar), and same-bar collision priority + gap-fill rules must be stated and enforced deterministically.
- **Reason:** ATR at the entry bar uses the entry bar's own OHLC (same-bar leak); collision/gap rules are undocumented.
- **Affected Document:** SPEC SL/TP (new), ENG-005, EXP-004/EXP-008 records.
- **Expected Benefit:** SL/TP exit semantics unambiguous and causal.
- **Research Risk:** SL/TP levels shift slightly; results change.

### E-3. Implement breakeven in code
- **PROPOSED CHANGE:** Add an engine-level breakeven computation (exact solve or interpolation over a code-run cost grid) so the acceptance metric is reproducible.
- **Reason:** breakeven is a primary pre-registered criterion but is hand-interpolated in every doc.
- **Affected Document:** RSH-002 §8/§9, ENG-006, statistics engine, robustness cost grid.
- **Expected Benefit:** acceptance criteria become code-executable (NFR-001).
- **Research Risk:** none to strategy; may revise reported breakeven figures (re-run, don't rewrite).

### E-4. Freeze all strategy parameters in YAML
- **PROPOSED CHANGE:** Move `window` (and any rule attribute) from plugin code into `configs/*.yaml`, enforced by schema validation.
- **Reason:** `window` is documented in "§9.3 frozen" tables but lives only in plugin code (FR-012/RSH-002 §9 partial violation).
- **Affected Document:** configs/EXP-*.yaml, strategies/*.py, load_experiment_config().
- **Expected Benefit:** single source of truth for all frozen params.
- **Research Risk:** none.

### E-5. Deterministic market definition block
- **PROPOSED CHANGE:** A mandatory Market Definition table for every EXP (origin/vendor, session/hours, timezone, missing/duplicate/gap handling, ordering, OHLC rules) — reuse the H4 provenance note standard.
- **Reason:** market definition is the thinnest dimension across EXP-001..008.
- **Affected Document:** RSH-002 §6 spec template; all future EXPs; retro-document current EXPs.
- **Expected Benefit:** data provenance reproducible; missing/duplicate/gap behavior explicit.
- **Research Risk:** none.

### E-6. Fix segment artifact hazards
- **PROPOSED CHANGE:** (a) derive the segment filename prefix from `config.data_config.timeframe/symbol` (not hardcoded `XAUUSD_H1_`); (b) add freshness check (mtime/hash) to the normalized-dataset cache; (c) write segment CSVs at full precision (no `:g` rounding); (d) add content-based dataset versioning.
- **Reason:** H4 segments are mislabeled "H1"; stale normalized data can be silently reused; OOS/robustness run at lower price fidelity; ARC-004 versioning is content-blind.
- **Affected Document:** segments.py, robustness.py, candle_csv.py, normalize.py, ARC-004.
- **Expected Benefit:** correct, non-stale, reproducible segments.
- **Research Risk:** numbers may shift slightly at full precision.

### E-7. Degenerate robustness grids
- **PROPOSED CHANGE:** The combo grid must vary parameters the strategy actually consumes (for price/swing strategies, vary `price_lookback`/`window`/`hold_bars`, not inert `rsi_period`); the cost grid must include the actual representative venue cost (1.0 bps/side).
- **Reason:** 2 of 5 combo rows are duplicates; the venue cost used in baseline is absent from the cost grid.
- **Affected Document:** robustness.py (COST_GRID, COMBO_GRID), RSH-003 §9/§10.
- **Expected Benefit:** meaningful robustness dimensions.
- **Research Risk:** none.

### E-8. Consistent decision criteria + multiple-testing control
- **PROPOSED CHANGE:** (a) a single standardized §13 criterion set across experiments (or explicit justification for deviation); (b) a multiple-testing/data-snooping note per experiment (number of criteria, combos, slices tested; correction or a pre-registered penalty).
- **Reason:** criteria drifted (EXP-002 vs EXP-003..008); no correction for combinatorial testing.
- **Affected Document:** RSH-001/RSH-003/RSH-004, all future EXP §13.
- **Expected Benefit:** verdicts comparable; multiple-testing risk surfaced.
- **Research Risk:** none.

### E-9. Standardize SL/TP exit documentation (same-bar, gap, entry-bar)
- **PROPOSED CHANGE:** Document and reconcile same-bar collision priority, gap-through-open fills, and entry-bar SL eligibility in both SPEC and EXP records; align doc wording with code.
- **Reason:** EXP-004 §10 contradicts code; EXP-008 leaves it undocumented.
- **Affected Document:** SPEC SL/TP (new), EXP-004/008 records.
- **Expected Benefit:** exit mechanics unambiguous.
- **Research Risk:** none.

### E-10. Reconcile entry/exit wording
- **PROPOSED CHANGE:** State the entry fill unambiguously (next-bar open; "entry at breakout candle" refers to the decision candle, not the fill) and the hold-exit price (close of hold_bars-th bar).
- **Reason:** EXP-007/008 §1/§8 vs §10 contradiction; EXP-007/008 §10 "open" vs code "close".
- **Affected Document:** ENG-005, EXP-007/008 records.
- **Expected Benefit:** timing spec unambiguous.
- **Research Risk:** none.

---

# F. Proposed New / Updated Specifications

Proposals only — not implemented (audit constraint §21).

### SPEC-001 — Swing Detection (update/replace ADR-003 semantics in code form)
- **SPEC ID:** SPEC-001
- **Title:** Deterministic Swing High/Low Detection
- **Purpose:** A reusable, deterministic, lookahead-safe fractal definition used by all swing-based strategies.
- **Scope:** swing_high/swing_low on an input price or indicator series; left/right parameters; tie handling; multiple structures; confirmation timing.
- **Inputs:** ordered series (closes or indicator values), left, right.
- **Deterministic Rules:** strict extrema (`values[i] >` all neighbors) as today; ties disqualify; swing is confirmable at bar `i + right`; event timestamp = confirmation bar (or carry `confirmable_at`); no dual high+low on clean data.
- **Edge Cases:** NaN warm-up region (must not emit events); plateaus/equal highs; series ends.
- **Non-Goals:** structure invalidation/replacement (not used by current strategies).
- **Dependencies:** ENG-002, event model.

### SPEC-002 — Breakout Detection
- **SPEC ID:** SPEC-002
- **Title:** Deterministic Price Breakout Detection
- **Purpose:** A reusable close-vs-level breakout definition.
- **Scope:** PRICE_CONFIRMATION; close vs highest-high N-bar; trigger vs confirmation role; ties.
- **Inputs:** OHLC candles, lookback N.
- **Deterministic Rules:** breakout iff `close[i] > max(high[j], j ∈ [i−N, i−1])` (strict); wick/intrabar is NOT a breakout; ties do not fire; level = the swing-high fractal where applicable.
- **Edge Cases:** gap-up through level without close above; equal close; repeated breakouts; level inside window (the EXP-007 "level covered" claim must be proven, not asserted).
- **Non-Goals:** stop/limit order simulation.
- **Dependencies:** SPEC-001, ENG-002.

### SPEC-003 — Signal Timing & Execution
- **SPEC ID:** SPEC-003
- **Title:** Signal Timing and Order Execution Semantics
- **Purpose:** Bind when each piece of information is knowable and when execution occurs; eliminate lookahead.
- **Scope:** information-available, signal-generated, confirmation, order-decision, execution timestamps; market vs pending; entry price; position conflicts.
- **Inputs:** signal (constituent events with confirmation times), candles, execution config.
- **Deterministic Rules:** entry at next-bar open after the signal whose every constituent event is confirmable strictly before that open; no same-bar leakage; each signal → exactly one trade; explicit duplicate/overlap policy; explicit position-lifecycle state machine (open → flat, no concurrency unless stated).
- **Edge Cases:** signal on last candle; duplicate signals at same timestamp; overlapping positions; opposite signal.
- **Non-Goals:** intrabar fills, partial fills.
- **Dependencies:** SPEC-001, SPEC-002, ENG-003, ENG-005.

### SPEC-004 — SL/TP & Exit Rules
- **SPEC ID:** SPEC-004
- **Title:** Stop Loss / Take Profit and Exit Rules
- **Purpose:** Unambiguous SL/TP and hold-exit semantics for OHLC backtesting.
- **Scope:** absolute and ATR-multiple SL/TP; same-bar collision; gap handling; hold-bars exit; end-of-data.
- **Inputs:** entry price, entry bar, ATR series, SL/TP config, hold_bars.
- **Deterministic Rules:** ATR anchor at `entry_bar − 1` (last closed bar); SL-first within a bar (conservative); gap-through-SL fills at open (conservative); gap-through-TP fills at open (favorable) — state explicitly; hold exit at close of `entry_bar + hold_bars`; SL/TP eligible from entry bar onward (state explicitly).
- **Edge Cases:** both SL and TP touched in same bar; open beyond both levels; ATR NaN; last candle.
- **Non-Goals:** trailing stops, time-based session closes.
- **Dependencies:** ENG-005.

### SPEC-005 — Cost Model
- **SPEC ID:** SPEC-005
- **Title:** Venue Cost Model Specification
- **Purpose:** Unambiguous, reproducible cost accounting.
- **Scope:** commission, slippage, spread; per-side vs round-trip; entry/exit timing; breakeven computation.
- **Inputs:** commission_rate, slippage_rate, entry/exit prices, position size.
- **Deterministic Rules:** slippage on entry and exit (conservative direction); commission on (entry+exit) notional; single-price OHLC series (no bid/ask spread — state this explicitly); breakeven = engine-computed (exact solve or grid interpolation in code).
- **Edge Cases:** zero-cost baseline; high-cost grid; NaN prices.
- **Non-Goals:** tick-level execution, venue-specific fee schedules.
- **Dependencies:** ENG-005, ENG-006.

---

# Final Research Decision

> **Is MRE's current research specification mature enough to continue with EXP-009, or should we first perform a Specification Hardening phase?**

## Decision: SPECIFICATION_HARDENING_REQUIRED

**Evidence:**

1. **Systemic lookahead** (swing backdating in `swing.py:50-54`; ATR-at-entry-bar in `simulation_engine.py:134-139`) directly contaminates the signal timing that every pre-registered criterion (OOS train/test) measures. The three most recent REJECTED/CLOSED verdicts (EXP-007/008) and the EXP-007 gross edge rest on lookahead-affected numbers; they are `INCONCLUSIVE` as evidence.

2. **Primary acceptance metrics are not reproducible from code** — breakeven is hand-interpolated in every doc; the venue cost (1.0 bps/side) is absent from the robustness cost grid.

3. **Decision criteria drifted** (EXP-002 SUPPORTED without the stationarity criterion that rejected EXP-007/008), so historical verdicts are not mutually comparable and a future EXP-009 would inherit an unstable acceptance standard.

4. **No multiple-testing/data-snooping control** exists in the formal methodology; the robustness machinery itself is degenerate (inert `rsi_period` combos).

5. **Documentation↔implementation mismatches** (entry-at-breakout-candle, SL/TP same-bar priority, exit-at-open vs close, `window` in plugin code) mean the "frozen config" is not fully deterministic-documented — violating RSH-002 §9 / NFR-001 / FR-012.

6. **The good news:** the core pipeline (`compute_report`) is deterministic given dataset + config; the only nondeterminism is report metadata and the existence-based dataset cache. Configs are internally consistent with their header claims (no parameter tampering). Five of eight verdicts are logically valid against their own criteria, and three (EXP-005/006 structural, EXP-003) are robust. Code versions recorded in docs match the actual pre-registration merge commits.

**Recommendation:** Do NOT open EXP-009 yet. First run a **Specification Hardening phase** implementing E-1..E-10 and SPEC-001..005 (particularly the lookahead fix and code-executable breakeven), re-run the closed experiments under the corrected spec as NEW evidence (without rewriting historical results — Rule 2), and adopt a single standardized §13 criterion set before pre-registering EXP-009. A methodology revision (multiple-testing control, criteria standardization) is part of the hardening, but the blocking defect is specification/implementation determinism, hence SPECIFICATION_HARDENING_REQUIRED rather than RESEARCH_METHODOLOGY_REVISION_REQUIRED.

---

**Constraint honored:** no files were modified during this audit; all changes are presented as proposals above.

**Audit date:** 2026-08-11
