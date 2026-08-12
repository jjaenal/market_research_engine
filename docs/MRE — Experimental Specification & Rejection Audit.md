# MRE — Experimental Specification & Rejection Audit

You are acting as a **Senior Quantitative Researcher, Research Methodologist, and Software Architecture Reviewer**.

You are working on the repository:

`market_research_engine`

The repository contains the documentation, research methodology, architecture decisions, and historical experiments for the Market Research Engine (MRE).

## Primary Objective

Perform a **forensic audit of the existing research experiments and their specifications**.

The goal is **NOT to improve trading performance**.

The goal is to determine whether the existing experiments were specified precisely enough to support their conclusions.

We have several rejected experiments. Before creating new experiments, we need to answer:

> **Were these strategies actually rejected by valid evidence, or were some experiments affected by ambiguous, incomplete, or non-deterministic strategy specifications?**

Do NOT optimize any strategy.

Do NOT add filters.

Do NOT modify entry/exit rules to improve performance.

Do NOT search for profitable parameters.

Do NOT introduce new trading ideas.

This is a **research methodology and specification audit**, not a strategy optimization task.

---

# 1. Repository Context

First, inspect the repository comprehensively.

Read and understand:

- README
- Documentation Standard
- Project Charter
- Foundation documents
- Architecture documentation
- ADRs
- Specifications
- Research methodology
- Experiment documentation
- TODO
- Roadmap
- All existing experiments
- Relevant source code
- Tests
- Configuration files
- Dataset/data-loading assumptions where documented

Do not assume that the experiment documentation is correct merely because it exists.

Compare documentation against implementation wherever possible.

The repository documentation is the intended source of truth, but this audit must identify discrepancies between:

```text
Documentation
      ↓
Specification
      ↓
Implementation
      ↓
Experiment Results
```

---

# 2. Experiments To Audit

At minimum audit all existing experiments from:

`EXP-001` through the latest completed experiment.

Pay special attention to experiments that were classified as:

- REJECTED
- INCONCLUSIVE
- FAILED
- INVALID

Do not limit the audit to the latest experiment.

The purpose is to identify recurring specification problems across the research history.

---

# 3. Audit Dimensions

For every experiment, audit the following dimensions.

## 3.1 Market Definition

Determine whether these are explicitly defined:

- Instrument
- Dataset
- Timeframe
- Trading session
- Timezone
- Trading hours
- Market availability
- Data source
- Data range
- Missing data handling
- Duplicate data handling
- Candle ordering
- OHLC validity

Classify each item as:

```text
EXPLICIT
IMPLICIT
AMBIGUOUS
MISSING
NOT_APPLICABLE
```

---

# 4. Strategy Definition Audit

Determine whether the strategy itself is defined deterministically.

Audit:

### Market Structure

- Swing high definition
- Swing low definition
- Fractal definition
- Lookback window
- Confirmation rules
- Equal highs/lows
- Tie handling
- Multiple simultaneous structures
- Structure invalidation
- Structure replacement

### Breakout Definition

Determine exactly what constitutes a breakout.

For example:

```text
High > level
Low > level
Close > level
Intrabar penetration
Close confirmation
```

If the documentation does not explicitly choose one, mark it as ambiguous.

Also check:

- Equal price handling
- Wick breakout
- Close breakout
- Gap breakout
- Multiple breakout levels
- Repeated breakout signals

---

# 5. Signal Timing Audit

Determine exactly when information becomes available.

For every signal, identify:

```text
Information available at:
Signal generated at:
Confirmation occurs at:
Order decision occurs at:
Execution occurs at:
```

Check for:

- Lookahead bias
- Future candle information
- Same-bar information leakage
- Fractal confirmation timing
- Indicator calculation timing
- Signal generated using unclosed candles
- Signal generated using future-confirmed structures

This section is extremely important.

Explicitly determine whether every required input was actually known at the moment the strategy would have acted.

---

# 6. Entry Specification Audit

Determine whether entry execution is deterministic.

Audit:

- Market order vs pending order
- Entry price
- Signal candle close
- Next candle open
- Breakout level
- Stop order
- Limit order
- Intrabar execution
- Multiple signals
- Duplicate entries
- Re-entry
- Position already open
- Opposite signal while position exists

The specification must answer:

> If the exact same OHLC dataset is processed twice, will the engine generate exactly the same entry?

If not, explain why.

---

# 7. Stop Loss Audit

Determine whether SL is mathematically and operationally unambiguous.

Audit:

- Exact formula
- Reference price
- Swing reference
- ATR reference
- Fixed distance
- Buffer
- Tick/pip rounding
- Minimum stop distance
- Same-bar SL activation
- SL vs TP collision
- Gap handling

If multiple interpretations are possible, list them.

---

# 8. Take Profit / Exit Audit

Audit:

- TP formula
- R-multiple calculation
- Fixed price target
- Structure-based exit
- Trailing stop
- Time-based expiry
- Opposite signal
- Session close
- End-of-data handling
- Same-bar TP/SL collision
- Priority when both SL and TP are touched in the same candle

The same-bar collision rule is particularly important for OHLC backtesting.

Determine whether the existing implementation uses:

```text
SL first
TP first
Conservative assumption
Optimistic assumption
Intrabar data
Unknown
```

---

# 9. Position Lifecycle Audit

Determine whether the experiment specifies:

- Maximum concurrent positions
- One position per symbol
- Multiple positions allowed
- Pyramiding
- Re-entry
- Position reversal
- Position cancellation
- Pending order cancellation
- Expiration
- Position state transitions

Produce a deterministic state-machine interpretation where useful.

---

# 10. Cost Model Audit

Audit:

- Commission
- Spread
- Slippage
- Fees
- Bid/ask assumptions
- Cost timing
- Entry cost
- Exit cost
- Cost per side
- Cost per round trip

Determine whether the cost model is:

```text
REALISTIC
SIMPLIFIED
UNREALISTIC
MISSING
```

Do not change the cost model.

Only evaluate its specification.

---

# 11. Statistical / Research Methodology Audit

Audit whether the experiment properly defines:

- Primary metric
- Secondary metrics
- Baseline
- Acceptance criteria
- Rejection criteria
- Sample size
- Train/test split
- OOS methodology
- Sensitivity analysis
- Robustness analysis
- Cost sensitivity
- Multiple testing
- Parameter selection
- Data snooping
- Selection bias

Determine whether the stated conclusion logically follows from the preregistered criteria.

---

# 12. Rejection Validity Audit

For every rejected experiment, classify the rejection.

Use exactly these categories where applicable:

```text
VALID_REJECTION

INCONCLUSIVE

SPECIFICATION_AMBIGUITY

IMPLEMENTATION_MISMATCH

METHODOLOGY_FAILURE

INSUFFICIENT_EVIDENCE
```

Then explain why.

For example:

```text
EXP-007

Current classification:
REJECTED

Audit classification:
INCONCLUSIVE

Reason:
The hypothesis was evaluated using a deterministic fractal definition,
but breakout execution timing remains ambiguous between signal-bar close
and next-bar execution. Therefore the reported OOS result cannot be
treated as definitive evidence against the hypothesis.
```

Do not automatically downgrade a rejection.

Only do so when there is concrete evidence that the experiment's validity is compromised.

---

# 13. Documentation vs Implementation Audit

For every experiment, compare:

```text
Experiment documentation
vs
Relevant source code
```

Identify:

- Rules documented but not implemented
- Rules implemented but not documented
- Different parameter values
- Different timing assumptions
- Hidden defaults
- Undocumented edge cases
- Implementation shortcuts
- Data handling differences
- Cost-model differences
- OOS differences

Create a discrepancy table.

---

# 14. Determinism Audit

The MRE research engine should produce deterministic results.

Verify whether the experiment has deterministic definitions for:

- Swing detection
- Signal generation
- Entry
- Exit
- Order sequencing
- Same-bar conflicts
- Multiple signals
- Duplicate signals
- Position conflicts
- Dataset ordering
- Missing data
- Floating-point-sensitive decisions
- Randomness

Identify anything that could cause:

```text
same data
+
same configuration
≠
same result
```

---

# 15. Specification Quality Score

For each experiment, provide a qualitative score:

```text
A — Fully deterministic
B — Minor ambiguity
C — Material ambiguity
D — Invalid / insufficient specification
```

The score must be based on evidence, not subjective judgment.

---

# 16. Cross-Experiment Pattern Analysis

After auditing every experiment individually, identify recurring problems.

Look for patterns such as:

```text
Repeated ambiguous entry timing
Repeated same-bar SL/TP ambiguity
Repeated swing-definition assumptions
Repeated undocumented defaults
Repeated implementation/documentation mismatch
Repeated OOS methodology problems
Repeated cost-model assumptions
```

This section should answer:

> What systemic weaknesses exist in our research framework?

---

# 17. Specification Architecture Recommendation

Determine which rules should live in:

```text
EXP document
SPEC document
ADR
Architecture documentation
Implementation
```

Use this principle:

### EXP

Use EXP for rules specific to the hypothesis being tested.

### SPEC

Use SPEC for reusable, deterministic technical definitions.

Examples:

```text
Swing Detection
Breakout Detection
Signal Timing
Order Execution
Position Lifecycle
Cost Model
```

### ADR

Use ADR when choosing between competing architectural or methodological approaches.

### Implementation

Implementation must execute the frozen specification.

Do not let implementation silently define research methodology.

---

# 18. Required Deliverables

Produce the following outputs.

## A. Executive Summary

Explain:

- How many experiments were audited
- How many have valid conclusions
- How many are inconclusive
- How many have specification problems
- Major recurring issues

---

## B. Experiment Audit Matrix

Create a table:

| Experiment | Current Status | Specification Quality | Rejection Validity | Main Issue |
|---|---|---|---|---|

---

## C. Detailed Audit Per Experiment

For every experiment:

```text
Experiment:
Current Status:

Specification Quality:
Rejection Validity:

Market Definition:
Strategy Definition:
Signal Timing:
Entry:
SL:
TP:
Position Lifecycle:
Cost:
Statistics:
OOS:
Documentation vs Implementation:

Critical Ambiguities:
Evidence:

Conclusion:
```

---

## D. Cross-Experiment Findings

Identify systemic issues.

---

## E. Required Specification Improvements

List only changes required to make future research deterministic.

Do NOT propose strategy improvements.

---

## F. Proposed New / Updated Specifications

If reusable specifications are required, propose them.

For each proposed specification provide:

```text
SPEC ID
Title
Purpose
Scope
Inputs
Deterministic Rules
Edge Cases
Non-Goals
Dependencies
```

Do not implement them yet unless explicitly requested.

---

# 19. Important Research Integrity Rules

These rules are mandatory.

### Rule 1

Do not optimize for profitability.

### Rule 2

Do not change historical experiment results.

### Rule 3

Do not reinterpret rules simply because the result was negative.

### Rule 4

Do not introduce new strategy filters.

### Rule 5

Do not select parameters based on historical performance.

### Rule 6

Do not invalidate a rejection without concrete methodological evidence.

### Rule 7

Do not declare a strategy valid merely because its rules are precise.

### Rule 8

Separate:

```text
Strategy failure
from
Experiment failure
from
Specification failure
from
Implementation failure
```

These are fundamentally different conclusions.

---

# 20. Final Research Decision

At the end of the audit, answer this question explicitly:

> **Is MRE's current research specification mature enough to continue with EXP-009, or should we first perform a Specification Hardening phase?**

Choose one:

```text
CONTINUE_TO_EXP-009

SPECIFICATION_HARDENING_REQUIRED

RESEARCH_METHODOLOGY_REVISION_REQUIRED
```

Explain the decision using evidence from the repository.

---

# 21. Critical Constraint

Do not modify files automatically during this audit.

First produce the audit findings and recommendations.

Any proposed changes must be presented as:

```text
PROPOSED CHANGE
Reason
Affected Document
Expected Benefit
Research Risk
```

The objective is to preserve the integrity of the research history.

We are auditing the research process — not trying to make the historical strategies look better.

---

# Final Principle

Remember the project's core philosophy:

> **Research the market. Test the hypothesis. Follow the evidence.**

The purpose of this audit is therefore not to rescue rejected strategies.

The purpose is to determine whether the evidence is strong enough to justify the conclusions we made.