---
title: Project TODO
document_id: FND-008
version: 1.3.32
status: Active
category: Foundation
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-09

depends_on:
  - FND-001
  - FND-003
  - FND-006
  - FND-007

purpose: Provide the actionable execution backlog for Market Research Engine
---

# Project TODO

> **Roadmap tells us where to go.  
> TODO tells us what to do next.**

---

# 1. Purpose

FND-008 merupakan execution backlog
resmi untuk Market Research Engine (MRE).

Dokumen ini menerjemahkan roadmap menjadi
pekerjaan konkret yang dapat dieksekusi.

FND-008 menjawab:

- apa yang harus dikerjakan;
- kenapa harus dikerjakan;
- priority;
- dependency;
- status;
- Definition of Ready;
- Definition of Done;
- next action;
- pekerjaan yang sengaja ditunda.

---

# 2. TODO Philosophy

TODO MRE tidak boleh menjadi:

```text
Dump semua ide
       ↓
Tambah checkbox
       ↓
Tidak pernah selesai
```

TODO harus menjadi:

```text
Objective
    ↓
Task
    ↓
Dependency
    ↓
Execution
    ↓
Validation
    ↓
Done
```

---

# 3. Status Vocabulary

Gunakan status berikut secara konsisten.

| Status        | Meaning                     |
| ------------- | --------------------------- |
| `PLANNED`     | Belum dikerjakan            |
| `READY`       | Dependency terpenuhi        |
| `IN_PROGRESS` | Sedang dikerjakan           |
| `BLOCKED`     | Tidak dapat dilanjutkan     |
| `REVIEW`      | Menunggu review             |
| `DONE`        | Memenuhi Definition of Done |
| `DEFERRED`    | Sengaja ditunda             |
| `CANCELLED`   | Tidak akan dikerjakan       |

---

# 4. Priority Vocabulary

| Priority | Meaning                                |
| -------- | -------------------------------------- |
| `P0`     | Critical — blocking project            |
| `P1`     | High — important for current milestone |
| `P2`     | Medium — useful but not blocking       |
| `P3`     | Low — future enhancement               |

---

# 5. Current Project State

Current:

```text
Phase:
M3 — Research Methodology (complete)

Sprint:
Sprint 3

Focus:
Engine Implementation (M4)

Status:
APPROVED — READY FOR M4
```

---

# 6. Current Execution Queue

Urutan kerja saat ini:

```text
FND-007
   ↓
FND-008
   ↓
FND-009
   ↓
Foundation Review
   ↓
M1 Product Definition
```

---

# 7. Master TODO

| ID       | Task                                  | Priority | Status      |
| -------- | ------------------------------------- | -------: | ----------- |
| TODO-001 | Complete Foundation Documentation     |       P0 | DONE        |
| TODO-002 | Create FND-009 Glossary               |       P0 | DONE        |
| TODO-003 | Foundation Review                     |       P0 | DONE        |
| TODO-004 | Define Product Vision                 |       P1 | DONE        |
| TODO-005 | Define Core Research Workflow         |       P1 | DONE        |
| TODO-006 | Define Functional Requirements        |       P1 | DONE        |
| TODO-007 | Define MVP                            |       P1 | DONE        |
| TODO-008 | Define Non-Functional Requirements  |       P1 | DONE        |
| TODO-009 | Define System Architecture            |       P1 | DONE        |
| TODO-010 | Define Domain Model                   |       P1 | DONE        |
| TODO-011 | Define Data Model                     |       P1 | DONE        |
| TODO-012 | Define Engine Interfaces              |       P1 | DONE        |
| TODO-013 | Define Research Methodology           |       P1 | DONE        |
| TODO-014 | Define Experiment Specification       |       P1 | DONE        |
| TODO-015 | Build Data Engine                     |       P1 | DONE        |
| TODO-016 | Build Indicator Layer                 |       P1 | DONE        |
| TODO-017 | Build Event Engine                    |       P1 | DONE        |
| TODO-018 | Build Signal Engine                   |       P1 | DONE        |
| TODO-019 | Build Simulation Engine               |       P1 | DONE        |
| TODO-020 | Build Statistics Engine               |       P1 | DONE        |
| TODO-021 | Build Reporting Engine                |       P1 | DONE        |
| TODO-022 | Create EXP-001                        |       P1 | DONE        |
| TODO-023 | Run Baseline Experiment               |       P1 | DONE        |
| TODO-024 | Perform Sensitivity Analysis          |       P1 | DONE        |
| TODO-025 | Perform Out-of-Sample Testing         |       P1 | DONE        |
| TODO-026 | Perform Robustness Analysis           |       P1 | DONE        |
| TODO-027 | Produce Research Conclusion           |       P1 | DONE        |
| TODO-028 | Review Architecture Based on Evidence |       P2 | DONE        |
| TODO-029 | Strategy Expansion                    |       P3 | DEFERRED    |
| TODO-030 | Market Expansion                      |       P3 | DEFERRED    |
| TODO-031 | ML Research Layer                     |       P3 | DEFERRED    |
| TODO-032 | M1 Product Definition Review          |       P1 | DONE        |
| TODO-033 | M2 Architecture Review                |       P1 | DONE        |
| TODO-034 | M3 Research Review                    |       P1 | DONE        |
| TODO-035 | Create EXP-002 (real venue cost)      |       P1 | IN PROGRESS |

---

# 8. M0 — Foundation TODO

## TODO-001 — Complete Foundation Documentation

**Priority:** P0

**Status:** DONE

### Objective

Complete minimum documentation
required before Product Definition.

### Deliverables

```text
FND-001
FND-002
FND-003
FND-004
FND-005
FND-006
FND-007
FND-008
FND-009
```

### Definition of Done

- all required documents exist;
- document IDs valid;
- metadata consistent;
- index updated;
- project status updated;
- roadmap references are consistent;
- no critical documentation conflict.

---

# 9. TODO-002 — Create FND-009 Glossary

**Priority:** P0

**Status:** DONE

## Objective

Create a controlled vocabulary
for MRE.

## Minimum Terms

```text
Experiment
Hypothesis
Dataset
Signal
Event
Trade
Entry
Exit
Stop Loss
Take Profit
Risk
Reward
Risk/Reward
Win Rate
Expectancy
Profit Factor
Drawdown
Lookahead Bias
Overfitting
Out-of-Sample
Walk-Forward
Robustness
Strategy
Indicator
Market Regime
```

## Dependency

```text
FND-003
FND-005
FND-007
```

## Definition of Done

- terms documented;
- definitions unambiguous;
- conflicting terminology removed;
- terms referenced consistently.

---

# 10. TODO-003 — Foundation Review

**Priority:** P0

**Status:** DONE

## Objective

Verify Foundation documents
form a coherent system.

## Review Checklist

- [x] Charter consistent with Context
- [x] Context consistent with Roadmap
- [x] Roadmap consistent with Status
- [x] TODO consistent with Roadmap
- [x] Document IDs consistent
- [x] No duplicated responsibilities
- [x] No contradictory principles
- [x] Current status accurate
- [x] Next phase clearly defined

## Definition of Done

Foundation can be used by a new
developer/researcher to understand:

```text
Why
What
Where
Current State
Next Action
```

---

# 11. M1 — Product Definition

---

# 12. TODO-004 — Define Product Vision

**Priority:** P1

**Status:** DONE

## Objective

Translate project vision into
a product-level statement.

## Must Answer

- Who uses MRE?
- What problem does it solve?
- What makes it useful?
- What is the primary workflow?
- What is explicitly out of scope?

---

# 13. TODO-005 — Define Core Research Workflow

**Priority:** P1

**Status:** DONE

## Initial Workflow

```text
Import Dataset
      ↓
Validate Dataset
      ↓
Configure Experiment
      ↓
Execute Strategy
      ↓
Generate Signals
      ↓
Simulate Trades
      ↓
Calculate Statistics
      ↓
Generate Report
      ↓
Evaluate Evidence
```

## Definition of Done

Every major step has:

- input;
- processing;
- output;
- failure conditions.

---

# 14. TODO-006 — Define Functional Requirements

**Priority:** P1

**Status:** DONE

## Initial Requirements

System must be able to:

- load historical data;
- validate data;
- configure strategy;
- execute strategy;
- simulate trades;
- calculate metrics;
- generate trade logs;
- generate reports;
- reproduce experiments.

---

# 15. TODO-007 — Define MVP

**Priority:** P1

**Status:** DONE

## MVP Principle

MVP:

> One complete research workflow.

Not:

> Many features.

## MVP Boundary

```text
CSV
 ↓
Validation
 ↓
Strategy
 ↓
Signal
 ↓
Simulation
 ↓
Statistics
 ↓
Report
```

---

# 16. TODO-008 — Define Non-Functional Requirements

**Priority:** P1

**Status:** DONE

## Initial Areas

- determinism;
- reproducibility;
- correctness;
- performance;
- testability;
- extensibility;
- observability;
- maintainability.

---

# 17. M2 — Architecture

---

# 18. TODO-009 — Define System Architecture

**Priority:** P1

**Status:** DONE

## Objective

Define major system boundaries.

Initial conceptual modules:

```text
Data
Indicator
Event
Signal
Simulation
Statistics
Reporting
Experiment
```

---

# 19. TODO-010 — Define Domain Model

**Priority:** P1

**Status:** DONE

## Initial Entities

```text
Dataset
Candle
Indicator
Event
Signal
Order
Position
Trade
Experiment
Strategy
Result
Report
```

Domain model must distinguish
concepts that are semantically different.

---

# 20. TODO-011 — Define Data Model

**Priority:** P1

**Status:** DONE

## Initial OHLCV

```text
timestamp
open
high
low
close
volume
```

Additional metadata:

```text
symbol
timeframe
timezone
source
dataset_version
```

Final schema must be established
in Architecture documentation.

---

# 21. TODO-012 — Define Engine Interfaces

**Priority:** P1

**Status:** DONE

## Objective

Define contracts between engines.

Example:

```text
DataEngine
    ↓
IndicatorEngine
    ↓
EventEngine
    ↓
SignalEngine
    ↓
SimulationEngine
    ↓
StatisticsEngine
    ↓
ReportingEngine
```

## Critical Requirement

Strategy implementation must not
directly depend on unrelated
infrastructure.

---

# 22. M3 — Research Methodology

---

# 23. TODO-013 — Define Research Methodology

**Priority:** P1

**Status:** DONE

## Must Define

- hypothesis;
- baseline;
- control variables;
- independent variables;
- dependent variables;
- metrics;
- sample requirements;
- validation;
- interpretation.

---

# 24. TODO-014 — Define Experiment Specification

**Priority:** P1

**Status:** DONE

Every experiment should capture:

```text
Experiment ID
Strategy
Dataset
Date Range
Timeframe
Parameters
Execution Assumptions
Cost Assumptions
Code Version
Result
Conclusion
```

---

# 25. Research Metrics TODO

Minimum metrics:

```text
Trade Count
Win Rate
Loss Rate
Average Win
Average Loss
Risk/Reward
Expectancy
Profit Factor
Gross Profit
Gross Loss
Net P&L
Maximum Drawdown
Winning Streak
Losing Streak
```

Additional metrics may be added
after the baseline engine is stable.

---

# 26. M4 — Engine Implementation

---

# 27. TODO-015 — Build Data Engine

**Priority:** P1

**Status:** DONE

## Responsibilities

- load CSV;
- detect schema;
- parse timestamp;
- normalize data;
- validate OHLC;
- handle missing data;
- reject invalid data.

## Tests

- valid CSV;
- missing columns;
- malformed timestamp;
- duplicate timestamp;
- invalid OHLC;
- missing values;
- unsorted data.

---

# 28. TODO-016 — Build Indicator Layer

**Priority:** P1

**Status:** DONE

## Initial Indicators

```text
RSI
EMA
ATR
```

## Critical Requirement

Indicator calculations must not
use future candles.

---

# 29. TODO-017 — Build Event Engine

**Priority:** P1

**Status:** DONE

## Responsibilities

Transform raw indicator/state
information into explicit events.

Example:

```text
RSI Trendline Created
RSI Trendline Broken
Price Confirmation
```

---

# 30. TODO-018 — Build Signal Engine

**Priority:** P1

**Status:** DONE

## Responsibilities

Convert event combinations
into trade signals.

Example:

```text
Event A
+
Event B
+
Filter C
=
LONG
```

---

# 31. TODO-019 — Build Simulation Engine

**Priority:** P1

**Status:** DONE

## Responsibilities

- entry;
- order state;
- SL;
- TP;
- exit;
- trade lifecycle;
- P&L;
- transaction costs;
- slippage assumptions.

## Critical Requirement

No future information may influence
past execution.

---

# 32. TODO-020 — Build Statistics Engine

**Priority:** P1

**Status:** DONE

## Responsibilities

Calculate:

- probability;
- RR;
- expectancy;
- profit factor;
- drawdown;
- distribution;
- streaks.

---

# 33. TODO-021 — Build Reporting Engine

**Priority:** P1

**Status:** DONE

## Outputs

```text
summary
trade_log
statistics
equity_curve
configuration
experiment_metadata
```

---

# 34. M5 — Baseline Experiment

---

# 35. TODO-022 — Create EXP-001

**Priority:** P1

**Status:** DONE

## Experiment

```text
EXP-001
RSI Trendline Breakout Baseline
```

## Objective

Establish baseline performance.

---

# 36. TODO-023 — Run Baseline Experiment

**Priority:** P1

**Status:** DONE

## Output

```text
Trade Count
Win Rate
RR
Expectancy
Profit Factor
Drawdown
Equity Curve
Trade Log
```

## Important

Do not optimize parameters
before baseline is recorded.

---

# 37. M6 — Validation

---

# 38. TODO-024 — Sensitivity Analysis

**Priority:** P1

**Status:** DONE

## Objective

Determine whether results depend
too heavily on a narrow parameter.

Example:

```text
RR = 1.0
RR = 1.5
RR = 2.0
RR = 2.5
RR = 3.0
```

## Output

- EXP-001 §16 — grid sensitivity (6 parameter × 3 nilai) tercatat;
- report: `experiments/EXP-001/EXP-001_sensitivity.md` (gitignored);
- edge tidak fragile secara arah (seluruh variasi expectancy positif),
  namun `price_lookback=10`, `rsi_period=21`, `swing_left=1` sensitif;
- sinyal peningkatan (`hold_bars=20`, `swing_left=3`, `signal_window=3`)
  tidak dipakai untuk optimasi baseline (RSH-001 §12, FND-008 §36).

---

# 39. TODO-025 — Out-of-Sample Testing

**Priority:** P1

**Status:** DONE

## Objective

Evaluate whether observed edge
generalizes to unseen data.

## Result

- module: `src/mre/core/out_of_sample.py` (RSH-003 §6/§7);
- report: `experiments/EXP-001/EXP-001_oos.md` (gitignored);
- split 70/30 (index 70.000, 2021-04-29); train 943 trades (exp 0.1187),
  test 453 trades (exp 2.4996, PF 1.4042);
- **edge tetap positif out-of-sample dan meningkat** — tidak ada degradasi
  in-sample → OOS (RSH-003 §7); tercatat di EXP-001 §17.

---

# 40. TODO-026 — Robustness Analysis

**Priority:** P1

**Status:** DONE

## Objective

Evaluate stability of results
over varying data and assumptions.

## Result

- module: `src/mre/core/robustness.py` (RSH-003 §10);
- report: `experiments/EXP-001/EXP-001_robustness.md` (gitignored);
- dimensions tercatat di EXP-001 §18:
  - time period (4 slice): 3/4 expectancy positif — slice ke-3 negatif
    (temporal robustness lemah);
  - cross-market (XAGUSD H1): expectancy positif tipis (0.0397);
  - execution cost: edge **tidak bertahan** pada biaya realistis
    (0.05%/sisi → expectancy negatif);
  - parameter combinations: 5/5 positif (stabil);
- timeframe tidak divariasikan (hanya data H1 tersedia).

---

# 41. TODO-027 — Research Conclusion

**Priority:** P1

**Status:** DONE

## Possible Outcomes

```text
SUPPORTED
PARTIALLY SUPPORTED
INCONCLUSIVE
REJECTED
```

Tidak ada keharusan bahwa
experiment menghasilkan
strategy yang profitable.

## Result

- verdict: **PARTIALLY SUPPORTED** (EXP-001 §19);
- hipotesis "expectancy positif setelah biaya transaksi" hanya
  terdukung pada asumsi biaya nol/near-zero;
- terdukung: edge arah stabil pada baseline, sensitivity grid, parameter
  combos, dan out-of-sample (meningkat);
- tidak terdukung: bertahan pada biaya realistis (0.05%/sisi → negatif)
  dan robustness temporal penuh (3/4 periode positif);
- evidence cukup (n=1403, FR-011); kesimpulan manual peneliti, bukan
  rekomendasi (RSH-001 §13).

---

# 42. M7 — Iteration

**Status:** DONE

Iteration ditutup. Kedua research question dijawab TIDAK:

```text
RQ-006 (dedup + regime selection): TIDAK — edge tidak bertahan pada biaya realistis (ARC-008 §14.1)
RQ-007 (risk management SL/TP):     TIDAK — SL/TP ATR-multiple menaikkan breakeven namun tidak memulihkan edge (ARC-008 §14.3)

Verdict akhir: hipotesis EXP-001 DITOLAK sebagai strategi yang dapat
diperdagangkan pada biaya realistis; edge hanya bertahan pada biaya
nol/near-zero (EXP-001 §19.8, ARC-008 §14.4).

Tindak lanjut: project kembali ke Research/Experiment untuk mendefinisikan
strategi berikutnya (FND-007 §38). Exit criterion FND-007 §38 terpenuhi.
```

---

# 43. TODO-028 — Architecture Review Based on Evidence

**Priority:** P2

**Status:** DONE

## Objective

Review architecture berdasarkan
pengalaman experiment nyata.

Questions:

- What was difficult?
- What abstraction failed?
- What data was missing?
- What should be simplified?
- What should be generalized?

## Result

- verdict: **CORE HOLDS, PERIPHERY DRIFTS** (ARC-008);
- inti arsitektur (pipeline `compute_report()`, frozen config, pure
  deterministic functions) terbukti menahan beban experiment — dipertahankan;
- yang gagal/belum terwujud: **strategi bukan plugin** (tidak ada
  `strategies/`) — **DONE (ARC-ACT-010)**; config YAML belum ada (hardcode
  di CLI) — **DONE (ARC-ACT-011, `configs/EXP-001.yaml`)**
  ; deduplikasi signal belum didefinisikan
  (signal overlap, EXP-001 §15.3) — **DONE (ARC-ACT-012)**;
- data kurang: timeframe selain H1, market ketiga+, biaya eksekusi nyata,
  label regime market (RQ regime dependency belum bisa dijawab);
- arah iterasi: ARC-ACT-010..014 + next research question
  (deduplikasi signal + eksekusi biaya realistis dengan regime selection);
- critical blockers: 0.

---

# 44. M8 — Expansion

---

# 45. TODO-029 — Strategy Expansion

**Priority:** P3

**Status:** DEFERRED

Potential:

```text
Fibonacci
Breakout
Supply & Demand
Liquidity Sweep
BoS
RSI Divergence
Trend Following
Mean Reversion
```

## Rule

Tidak dikerjakan sebelum
core research workflow stabil.

---

# 46. TODO-030 — Market Expansion

**Priority:** P3

**Status:** DEFERRED

Potential:

```text
XAUUSD
Forex
Indices
Crypto
```

---

# 47. TODO-031 — ML Research Layer

**Priority:** P3

**Status:** DEFERRED

Potential:

```text
Feature Engineering
Regime Classification
Signal Classification
Probability Modeling
Prediction
```

## Critical Rule

ML tidak boleh menjadi
jalan pintas untuk menggantikan
research methodology.

---

# 48. Current Sprint Backlog

## Sprint 0

Objective:

> Complete Foundation.

### Tasks

```text
[x] FND-001
[x] FND-002
[x] FND-003
[x] FND-004
[x] FND-005
[x] FND-006
[x] FND-007
[ ] FND-008
[ ] FND-009
[ ] Foundation Review
```

---

# 49. Sprint 1 Preview

Sprint 1 — Product Definition berjalan.

Candidate objective:

> Define Product Requirements
> for the MRE MVP.

Candidate tasks:

```text
PRD-001  Product Vision          (done)
PRD-002  User Personas          (done)
PRD-003  Core Workflow           (done)
PRD-004  Functional Requirements (done)
PRD-005  Non-Functional Requirements (done)
PRD-006  MVP Definition          (done)
PRD-007  Feature Specification          (done)
```

Exact scope ditentukan
setelah Foundation Review
dan direvisi pada `FND-006 — Project Status`.

---

# 50. Task Dependency Graph

```text
FND-001
   │
   ├── FND-002
   │
   ├── FND-003
   │
   └── FND-004
          │
          ▼
       FND-005
          │
          ▼
       FND-006
          │
          ▼
       FND-007
          │
          ▼
       FND-008
          │
          ▼
       FND-009
          │
          ▼
   Foundation Review
          │
          ▼
     Product Phase
          │
          ▼
   Architecture Phase
          │
          ├──────────────┐
          ▼              ▼
      Research        Engineering
          │              │
          └──────┬───────┘
                 ▼
             Experiment
                 │
                 ▼
             Validation
```

---

# 51. Definition of Ready

Sebuah task boleh masuk
`READY` apabila:

- objective jelas;
- scope jelas;
- dependency terpenuhi;
- input tersedia;
- expected output jelas;
- acceptance criteria jelas;
- tidak ada blocker kritis.

---

# 52. Definition of Done

Sebuah task dapat menjadi
`DONE` apabila:

- objective tercapai;
- acceptance criteria terpenuhi;
- implementation/documentation selesai;
- relevant tests dilakukan;
- hasil diverifikasi;
- dependency downstream tidak rusak;
- documentation terkait diperbarui;
- status project diperbarui jika relevan.

Definition of Done sengaja dibuat sebagai quality gate, bukan sekadar indikator bahwa pekerjaan coding telah berhenti. Praktik engineering umum juga memasukkan testing, review, documentation, dan integration sebagai bagian dari “done”.

---

# 53. Documentation Rule

Jika task mengubah:

- architecture;
- requirements;
- API;
- data model;
- experiment methodology;
- project status;

maka documentation terkait
harus diperbarui dalam task yang sama.

Tidak boleh:

```text
Code Done
   ↓
Documentation Later
   ↓
Forgotten
```

---

# 54. Testing Rule

Task engineering yang memengaruhi
hasil research harus memiliki
test yang sesuai.

Minimal:

```text
Unit Test
+
Integration Test
```

Jika diperlukan:

```text
End-to-End Test
```

---

# 55. Research Correctness Rule

Untuk komponen research engine,
correctness lebih penting daripada
performance.

Priority:

```text
Correctness
    >
Reproducibility
    >
Maintainability
    >
Performance
```

Optimization dilakukan
setelah correctness terbukti.

---

# 56. TODO Prioritization Rule

Ketika ada dua task yang sama-sama
terlihat penting:

Prioritaskan task yang:

1. membuka dependency berikutnya;
2. mengurangi uncertainty;
3. memvalidasi asumsi penting;
4. meningkatkan research capability;
5. mengurangi technical risk.

---

# 57. Anti-Distraction Rule

Jika muncul ide baru:

```text
Idea
 ↓
Is it P0/P1 for current milestone?
 ↓
YES → Add to active backlog
NO  → Add to Deferred Ideas
```

Jangan langsung mengubah
current sprint.

---

# 58. Deferred Ideas

Ide berikut sengaja ditunda:

```text
Advanced ML
Live Trading
Broker Integration
Cloud Infrastructure
Portfolio Optimization
Real-time Market Feed
Mobile UI
Web Dashboard
Automated Strategy Discovery
```

Alasan:

> Core research capability
> belum tervalidasi.

---

# 59. TODO Lifecycle

```text
IDEA
  ↓
PLANNED
  ↓
READY
  ↓
IN_PROGRESS
  ↓
REVIEW
  ↓
DONE
```

Exception:

```text
IN_PROGRESS
     ↓
  BLOCKED
     ↓
  READY
```

atau:

```text
PLANNED
   ↓
DEFERRED
```

---

# 60. Blocker Protocol

Jika task blocked:

Status:

```text
BLOCKED
```

Harus dicatat:

```text
Blocker:
Impact:
Required Action:
Owner:
Next Review:
```

Jangan membiarkan task
`IN_PROGRESS` tanpa progress
selama blocker aktif.

---

# 61. TODO Update Protocol

FND-008 harus diperbarui ketika:

- task dimulai;
- task selesai;
- task blocked;
- priority berubah;
- dependency berubah;
- scope berubah;
- task dibatalkan;
- milestone berubah.

---

# 62. Weekly Review

Pada akhir setiap development cycle:

Review:

```text
Completed
In Progress
Blocked
Deferred
New Tasks
Removed Tasks
Priority Changes
```

Kemudian sinkronkan:

```text
FND-006 Project Status
FND-007 Roadmap
FND-008 TODO
```

---

# 63. TODO Health

TODO dianggap sehat apabila:

- current task jelas;
- next task jelas;
- dependency jelas;
- task tidak terlalu besar;
- priority jelas;
- stale tasks minimal;
- blocked tasks terlihat;
- deferred work tidak bercampur dengan active work.

---

# 64. Current Next Action

Saat ini:

```text
CURRENT
M7 — Iteration CLOSED. Seluruh research question dijawab TIDAK dan verdict
akhir tercatat: hipotesis EXP-001 DITOLAK sebagai strategi yang dapat
diperdagangkan pada biaya realistis (edge hanya bertahan pada biaya
nol/near-zero — ARC-008 §14.4, EXP-001 §19.8)
```

Setelah itu:

```text
NEXT MAJOR PHASE
Project kembali ke Research/Experiment (FND-007 §38) untuk mendefinisikan
strategi berikutnya (EXP-002 atau seterusnya) dengan evidence input dari
temuan M7
```

Kemudian:

```text
NEXT TASK
EXP-002 pre-registered (TODO-035): re-test edge terhadap biaya eksekusi
venue nyata XAUUSD (spread + komisi + slippage retail ECN, ~1.0 bps/side)
alih-alih grid sintetis 0.02%-0.05%/sisi. Berikutnya: TODO-036 run EXP-002.
```

---

# 65. The Golden Path

Jika bingung harus mengerjakan apa,
ikuti:

```text
What is blocking the current milestone?
              │
              ▼
What reduces the most uncertainty?
              │
              ▼
What unlocks the next phase?
              │
              ▼
Do that task first.
```

---

# 66. What We Should NOT Work On Yet

Jangan mengerjakan:

```text
❌ UI
❌ Flutter application
❌ Broker API
❌ Live trading
❌ ML
❌ Portfolio optimizer
❌ Cloud deployment
❌ Microservices
❌ Complex database
❌ Strategy optimizer
```

selama core research workflow
belum terbukti.

---

# 67. First Technical Proof

Target:

```text
Historical CSV
      ↓
Strategy
      ↓
Signals
      ↓
Trades
      ↓
Statistics
      ↓
Report
```

Jika pipeline ini berhasil
secara deterministic:

```text
MRE Core
= PROVEN
```

---

# 68. First Research Proof

Target:

```text
EXP-001
   ↓
Baseline Result
   ↓
Probability
   ↓
RR
   ↓
Expectancy
   ↓
Validation
```

Baru kemudian kita bertanya:

> **Apakah strategy ini punya edge?**

---

# 69. First Product Proof

Target:

> Researcher dapat menjalankan
> experiment tanpa mengubah
> core engine setiap kali strategy
> berubah.

---

# 70. First Architecture Proof

Target:

```text
New Strategy
     ↓
New Strategy Module
     ↓
Same Data Engine
Same Simulation Engine
Same Statistics Engine
Same Reporting Engine
```

Jika tercapai:

> Architecture berhasil mencapai
> extensibility minimum.

---

# 71. First Quality Proof

Target:

```text
Same Dataset
+
Same Configuration
+
Same Code Version
=
Same Result
```

Ini merupakan salah satu
quality gates paling penting
untuk MRE.

---

# 72. Project Progress

Current Foundation progress:

```text
FND-001  ██████████ DONE
FND-002  ██████████ DONE
FND-003  ██████████ DONE
FND-004  ██████████ DONE
FND-005  ██████████ DONE
FND-006  ██████████ DONE
FND-007  ██████████ DONE
FND-008  ██████████ CURRENT
FND-009  ░░░░░░░░░░ PLANNED
```

---

# 73. Milestone Progress

```text
M0 Foundation

██████████████░░░░░░
Approximately 78%

Remaining:
FND-009
Foundation Review
```

Percentage is a planning
indicator, not a measurement
of software quality.

---

# 74. Completion of FND-008

FND-008 is complete when:

- [x] TODO lifecycle defined.
- [x] Status vocabulary defined.
- [x] Priority vocabulary defined.
- [x] Master backlog established.
- [x] Foundation tasks defined.
- [x] Product tasks defined.
- [x] Architecture tasks defined.
- [x] Research tasks defined.
- [x] Engineering tasks defined.
- [x] Experiment tasks defined.
- [x] Validation tasks defined.
- [x] Expansion tasks defined.
- [x] Definition of Ready defined.
- [x] Definition of Done defined.
- [x] Dependency model defined.
- [x] Blocker protocol defined.
- [x] Deferred work defined.
- [x] Current next action defined.

---

# 75. TODO-032 — M1 Product Definition Review

**Priority:** P1

**Status:** DONE

## Objective

Review M1 Product Definition
sebelum transisi ke M2 — Architecture.

## Deliverable

- `docs/01-product/PRD-008_Product_Definition_Review.md`

## Result

```text
Status   : APPROVED (PASS WITH ACTIONS)
Blockers : 0
Actions  : PRD-ACT-001..003
Readiness: 95%
```

---

# 76. TODO-033 — M2 Architecture Review

**Priority:** P1

**Status:** DONE

## Objective

Review M2 Architecture
sebelum transisi ke M3 — Research Methodology.

## Deliverable

- `docs/02-architecture/ARC-007_Architecture_Review.md`

## Result

```text
Status   : APPROVED (PASS WITH ACTIONS)
Blockers : 0
Actions  : ARC-ACT-001..004
Readiness: 95%
```

---

# 77. TODO-034 — M3 Research Review

**Priority:** P1

**Status:** DONE

## Objective

Review M3 Research Methodology
sebelum transisi ke M4 — Engine Implementation.

## Deliverable

- `docs/05-research/RSH-006_Research_Review.md`

## Result

```text
Status   : APPROVED (PASS WITH ACTIONS)
Blockers : 0
Actions  : RSH-ACT-001..003
Readiness: 95%
```

---

# 78. TODO-035 — Create EXP-002 (Real Venue Cost)

**Priority:** P1

**Status:** IN PROGRESS

## Experiment

```text
EXP-002
RSI Trendline Breakout — Real Venue Execution Cost
```

## Objective

Re-test hipotesis EXP-001 terhadap biaya eksekusi venue nyata
(spread + komisi + slippage retail XAUUSD) alih-alih grid sintetis
0.02%–0.05%/sisi (ARC-008 §14.4, FND-006 §17). Pre-registered
(RSH-001 §7.2) sebelum run.

## Deliverable

- `docs/07-experiments/EXP-002_RSI_Trendline_Breakout_Real_Venue_Cost.md`
  (status: Defined — pre-registration);
- `configs/EXP-002.yaml` (config frozen, venue-derived costs).

## Next

```text
TODO-036 Run EXP-002 (baseline on venue cost grid)
```

---

# Appendix A — Quick TODO

```text
NOW
↓
FND-008

NEXT
↓
FND-009

THEN
↓
Foundation Review

THEN
↓
Product Definition

THEN
↓
Architecture

THEN
↓
Research Methodology

THEN
↓
Engine

THEN
↓
EXP-001

THEN
↓
Validation
```

---

# Appendix B — AI Resume Context

Jika project dilanjutkan pada
conversation baru:

```text
Market Research Engine (MRE)
is currently in M0 Foundation.

Completed:
FND-001
FND-002
FND-003
FND-004
FND-005
FND-006
FND-007

Current:
FND-008 — Project TODO

Next:
FND-009 — Project Glossary

After Foundation:
Foundation Review
→ Product Definition
→ Architecture
→ Research Methodology
→ Engine
→ EXP-001
→ Validation
→ Iteration.

Initial research case:
RSI Trendline Breakout.

Initial objective:
Measure probability, RR,
expectancy, and robustness.

Core MVP:
Historical CSV
→ Strategy
→ Signal
→ Simulation
→ Statistics
→ Report.

Golden rule:
Do not optimize before
baseline evidence exists.
```

---

**Document Status:** Active

**Document ID:** FND-008

**Version:** 1.3.32

**End of Document**
