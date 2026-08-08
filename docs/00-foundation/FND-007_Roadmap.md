---
title: Project Roadmap
document_id: FND-007
version: 1.0.1
status: Active
category: Foundation
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-08

depends_on:
  - FND-001
  - FND-004
  - FND-005
  - FND-006

purpose: Define the strategic development path of Market Research Engine from foundation to validated research capability
---

# Project Roadmap

> **A roadmap is not a list of everything we could build.  
> It is a commitment to the order in which we discover, design, build, and validate.**

---

# 1. Purpose

FND-007 mendefinisikan arah perjalanan
Market Research Engine (MRE).

Roadmap ini menjawab:

- MRE akan dibangun melalui fase apa saja;
- milestone utama apa yang harus dicapai;
- dependency antar fase;
- output setiap fase;
- kapan sebuah fase dianggap selesai;
- apa yang harus ditunda;
- bagaimana project berkembang dari
  dokumentasi menuju research engine;
- bagaimana kita akhirnya sampai pada
  experiment yang menghasilkan evidence.

Roadmap ini bersifat strategis.

Detail task harian berada di:

`FND-008 — TODO`

---

# 2. Roadmap Philosophy

MRE tidak akan dibangun dengan pendekatan:

```text
Code Everything
      ↓
Hope It Works
      ↓
Backtest
```

Pendekatan yang digunakan:

```text
Understand
    ↓
Define
    ↓
Design
    ↓
Build
    ↓
Test
    ↓
Experiment
    ↓
Validate
    ↓
Learn
    ↓
Iterate
```

---

# 3. High-Level Roadmap

```text
                         MARKET RESEARCH ENGINE
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ M0 FOUNDATION   │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ M1 PRODUCT      │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ M2 ARCHITECTURE │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ M3 RESEARCH     │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ M4 ENGINE       │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ M5 BASELINE     │
                         │ EXPERIMENT      │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ M6 VALIDATION   │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ M7 ITERATION    │
                         └─────────────────┘
```

---

# 4. Roadmap Stages

MRE dibagi menjadi:

| ID  | Stage                 | Purpose                              |
| --- | --------------------- | ------------------------------------ |
| M0  | Foundation            | Establish project foundation         |
| M1  | Product Definition    | Define what to build                 |
| M2  | Architecture          | Define how it should work            |
| M3  | Research Methodology  | Define how experiments are performed |
| M4  | Engine Implementation | Build research engine                |
| M5  | Baseline Experiment   | Run first complete experiment        |
| M6  | Validation            | Test robustness and validity         |
| M7  | Iteration             | Improve based on evidence            |
| M8  | Expansion             | Add additional research capabilities |

---

# 5. M0 — Foundation

## Objective

Membangun fondasi project
sebelum implementation dimulai.

---

## Key Outputs

```text
FND-001  Project Charter
FND-002  Documentation Standard
FND-003  Document ID Standard
FND-004  Document Index
FND-005  Project Context
FND-006  Project Status
FND-007  Roadmap
FND-008  TODO
FND-009  Glossary
```

---

## Current Status

```text
IN PROGRESS
```

---

## Exit Criteria

M0 selesai apabila:

- governance tersedia;
- documentation structure tersedia;
- project context jelas;
- project status tracking tersedia;
- roadmap tersedia;
- TODO tersedia;
- glossary tersedia;
- Product phase memiliki entry point yang jelas.

---

# 6. M1 — Product Definition

## Objective

Mengubah project vision menjadi
requirements yang konkret.

Pertanyaan utama:

> **Apa sebenarnya yang harus dibangun?**

---

## Product Questions

M1 harus menjawab:

- siapa pengguna MRE;
- apa workflow utama;
- apa input;
- apa output;
- apa fitur minimum;
- apa batasan;
- apa success criteria;
- apa yang termasuk MVP;
- apa yang tidak termasuk MVP.

---

## Planned Documents

Contoh:

```text
PRD-001  Product Vision
PRD-002  User Personas
PRD-003  Core Workflow
PRD-004  Functional Requirements
PRD-005  Non-Functional Requirements
PRD-006  MVP Definition
PRD-007  Feature Specification
```

Nomor final mengikuti
`FND-003 — Document ID Standard`.

---

## Primary Product Workflow

```text
Import Data
    ↓
Validate Data
    ↓
Configure Research
    ↓
Run Experiment
    ↓
Generate Trades
    ↓
Calculate Statistics
    ↓
Analyze Result
    ↓
Export Research Output
```

---

## Exit Criteria

M1 selesai apabila:

- MVP didefinisikan;
- primary workflow jelas;
- requirements terdokumentasi;
- acceptance criteria tersedia;
- scope boundaries jelas;
- architecture memiliki input yang cukup.

---

# 7. M2 — Architecture

## Objective

Menentukan struktur teknis
yang akan digunakan untuk membangun MRE.

Pertanyaan utama:

> **Bagaimana sistem harus dibangun?**

---

## Architecture Areas

```text
System Architecture
       ↓
Domain Architecture
       ↓
Data Architecture
       ↓
Engine Architecture
       ↓
Module Architecture
       ↓
Experiment Architecture
```

---

## Core Architectural Components

Initial conceptual architecture:

```text
                ┌───────────────┐
                │ Market Data   │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Data Engine   │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Event Engine  │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Signal Engine │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Simulation    │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Statistics    │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Reporting     │
                └───────────────┘
```

Architecture tersebut masih
bersifat conceptual.

Final architecture harus ditentukan
melalui architecture documents.

---

## Exit Criteria

M2 selesai apabila:

- system boundaries jelas;
- modules jelas;
- domain model jelas;
- data contracts jelas;
- interfaces jelas;
- dependency rules jelas;
- testing strategy jelas;
- architecture decisions terdokumentasi.

---

# 8. M3 — Research Methodology

## Objective

Mendefinisikan bagaimana MRE
melakukan penelitian secara valid.

Pertanyaan utama:

> **Bagaimana kita memastikan experiment
> menghasilkan evidence yang meaningful?**

---

# 9. Research Lifecycle

```text
Question
   ↓
Hypothesis
   ↓
Dataset
   ↓
Configuration
   ↓
Experiment
   ↓
Observation
   ↓
Measurement
   ↓
Validation
   ↓
Conclusion
```

---

# 10. Research Methodology Areas

M3 harus mencakup:

- hypothesis definition;
- dataset selection;
- train/test separation;
- signal definition;
- entry rules;
- exit rules;
- position sizing;
- transaction costs;
- slippage;
- execution assumptions;
- probability;
- expectancy;
- drawdown;
- robustness;
- sensitivity analysis;
- out-of-sample testing;
- walk-forward testing;
- Monte Carlo analysis jika relevan.

---

# 11. Core Statistical Objective

Initial research tidak mengejar:

```text
Maximum Profit
```

tetapi:

```text
Reliable Evidence
```

Metrics utama:

```text
Win Rate
Loss Rate
Risk/Reward
Expectancy
Profit Factor
Maximum Drawdown
Sample Size
Return Distribution
Robustness
```

---

# 12. Exit Criteria

M3 selesai apabila:

- experiment methodology terdokumentasi;
- metrics didefinisikan;
- trade lifecycle didefinisikan;
- assumptions didefinisikan;
- validation methodology didefinisikan;
- research reporting requirements tersedia.

---

# 13. M4 — Engine Implementation

## Objective

Membangun research engine
berdasarkan product,
architecture,
dan methodology yang telah disetujui.

---

# 14. Engine Development Sequence

Implementation tidak dilakukan
sekaligus.

Urutan awal:

```text
1. Data Engine
       ↓
2. Indicator Layer
       ↓
3. Event Engine
       ↓
4. Signal Engine
       ↓
5. Trade Simulation
       ↓
6. Statistics Engine
       ↓
7. Reporting Engine
```

---

# 15. Data Engine

Responsibilities:

- load historical data;
- validate schema;
- normalize timestamp;
- sanitize numeric values;
- detect invalid rows;
- provide deterministic data access.

---

# 16. Indicator Layer

Responsibilities:

- calculate indicators;
- maintain deterministic calculations;
- avoid lookahead;
- provide reusable measurements.

Examples:

```text
RSI
EMA
ATR
SMA
Swing High
Swing Low
```

---

# 17. Event Engine

Responsibilities:

Convert market observations
into explicit events.

Example:

```text
RSI crosses 70
RSI crosses 30
Trendline breakout
Swing high formed
Swing low formed
```

---

# 18. Signal Engine

Responsibilities:

Combine events into
research signals.

Example:

```text
RSI Trendline Breakout
+
Trend Confirmation
=
Long Signal
```

---

# 19. Simulation Engine

Responsibilities:

- entry;
- stop loss;
- take profit;
- order state;
- position lifecycle;
- exit;
- P&L;
- costs;
- slippage.

---

# 20. Statistics Engine

Responsibilities:

Calculate:

- win rate;
- loss rate;
- expectancy;
- profit factor;
- drawdown;
- streaks;
- distribution;
- risk metrics.

---

# 21. Reporting Engine

Responsibilities:

Produce:

- summary;
- trade log;
- statistics;
- charts;
- experiment metadata;
- research conclusion.

---

# 22. M4 Exit Criteria

M4 selesai apabila:

```text
Dataset
   ↓
Strategy
   ↓
Simulation
   ↓
Statistics
   ↓
Report
```

dapat dijalankan end-to-end
secara deterministic.

---

# 23. M5 — Baseline Experiment

## Objective

Menjalankan experiment pertama
secara lengkap.

Initial experiment:

```text
EXP-001
RSI Trendline Breakout Baseline
```

---

# 24. Baseline Experiment Goals

Tujuan utama:

> Mengetahui baseline statistical
> characteristics dari strategy.

Bukan mengoptimalkan strategy.

---

# 25. Baseline Questions

Experiment harus menghasilkan jawaban:

```text
1. Berapa trade?
2. Berapa win rate?
3. Berapa loss rate?
4. Bagaimana RR distribution?
5. Berapa expectancy?
6. Berapa profit factor?
7. Berapa maximum drawdown?
8. Bagaimana trade distribution?
9. Apakah hasil stabil?
```

---

# 26. Baseline Rule

Baseline harus menggunakan
parameter yang ditentukan
sebelum melihat hasil.

Tidak boleh:

```text
Backtest
   ↓
See Result
   ↓
Change Parameter
   ↓
Backtest Again
   ↓
Call It Baseline
```

---

# 27. M5 Exit Criteria

M5 selesai apabila:

- experiment reproducible;
- trade log tersedia;
- statistics tersedia;
- result report tersedia;
- configuration tersimpan;
- dataset tercatat;
- code version tercatat;
- conclusion dibuat.

---

# 28. M6 — Validation

## Objective

Menentukan apakah baseline result
memiliki robustness yang cukup.

---

# 29. Validation Layers

```text
Baseline
   ↓
Sensitivity
   ↓
Out-of-Sample
   ↓
Walk Forward
   ↓
Robustness
   ↓
Stress Test
```

---

# 30. Sensitivity Analysis

Parameter dapat divariasikan
secara terkontrol.

Contoh:

```text
RR:
1:1
1:1.5
1:2
1:2.5
1:3
```

Tujuan:

> mengetahui apakah edge hanya muncul
> pada satu parameter tertentu.

---

# 31. Out-of-Sample

Data dibagi:

```text
Historical Data
       │
       ├──────────────┐
       ▼              ▼
    In-Sample      Out-of-Sample
```

Strategy tidak boleh
dioptimalkan menggunakan
out-of-sample data.

---

# 32. Walk-Forward

Concept:

```text
Train
  ↓
Test
  ↓
Move Window
  ↓
Train
  ↓
Test
  ↓
Repeat
```

Tujuan:

> mengetahui apakah strategy
> mampu bertahan ketika market
> berkembang sepanjang waktu.

---

# 33. Robustness

Strategy dianggap lebih robust
apabila performanya tidak runtuh
ketika kondisi berubah secara
reasonable.

Contoh perubahan:

- parameter;
- period;
- market;
- timeframe;
- RR;
- execution assumptions.

---

# 34. M6 Exit Criteria

M6 selesai apabila:

- baseline telah divalidasi;
- sensitivity analysis tersedia;
- out-of-sample result tersedia;
- robustness telah dievaluasi;
- conclusion diperbarui berdasarkan evidence.

---

# 35. M7 — Iteration

## Objective

Mengubah hasil experiment
menjadi improvement yang terukur.

Iteration dapat menghasilkan:

```text
Improve
Reject
Simplify
Redesign
```

---

# 36. Iteration Loop

```text
Experiment
    ↓
Evidence
    ↓
Analysis
    ↓
Hypothesis Revision
    ↓
Architecture / Strategy Change
    ↓
New Experiment
```

---

# 37. Important Rule

Tidak semua experiment
harus menghasilkan improvement.

Possible outcome:

```text
Experiment
    ↓
No Edge
    ↓
Reject Hypothesis
```

Itu tetap merupakan successful research outcome.

---

# 38. M7 Exit Criteria

Iteration selesai ketika
pertanyaan penelitian berikutnya
telah didefinisikan dengan jelas.

Project dapat kembali ke:

- Product;
- Architecture;
- Research;
- Engine;
- Experiment.

Iteration bersifat cyclical.

---

# 39. M8 — Expansion

Expansion dilakukan hanya setelah
core research workflow stabil.

Potential areas:

```text
Multi-Strategy
Multi-Market
Portfolio Research
Advanced Statistics
Optimization
Monte Carlo
Regime Detection
Feature Engineering
Machine Learning
Research UI
Experiment Dashboard
```

---

# 40. Expansion Principle

Tidak ada expansion hanya karena:

> "Keren kalau ada."

Expansion harus memiliki:

```text
Research Value
+
User Value
+
Evidence
```

---

# 41. Strategy Expansion

Setelah baseline RSI selesai,
strategy berikutnya dapat ditambahkan.

Potential examples:

```text
Fibonacci
Breakout
Supply & Demand
Liquidity Sweep
Break of Structure
RSI Divergence
Trend Following
Mean Reversion
```

Strategy harus masuk sebagai
research module,
bukan mengubah core engine.

---

# 42. Market Expansion

Initial focus dapat dimulai
dengan satu market.

Kemudian:

```text
XAUUSD
   ↓
Forex
   ↓
Indices
   ↓
Crypto
   ↓
Other Markets
```

Expansion hanya dilakukan
jika data model mendukung.

---

# 43. Timeframe Expansion

Potential:

```text
M5
M15
M30
H1
H4
D1
```

Timeframe bukan sekadar
parameter teknis.

Perubahan timeframe
dapat mengubah market behavior.

Karena itu harus diperlakukan
sebagai research dimension.

---

# 44. Roadmap Dependency

```text
M0 Foundation
      │
      ▼
M1 Product
      │
      ▼
M2 Architecture
      │
      ├─────────────┐
      ▼             ▼
M3 Research     M4 Engine
      │             │
      └──────┬──────┘
             ▼
        M5 Experiment
             │
             ▼
        M6 Validation
             │
             ▼
        M7 Iteration
             │
             ▼
        M8 Expansion
```

---

# 45. Parallel Work

Tidak semua aktivitas harus
100% sequential.

Contoh:

```text
Product
   │
   ├── Research Methodology
   │
   └── Architecture
```

Namun dependency harus tetap dihormati.

Tidak boleh implementation
mengunci keputusan yang belum
ditentukan.

---

# 46. MVP Definition

MRE MVP bukan:

> "Aplikasi dengan banyak fitur."

MVP adalah:

> **Kemampuan menjalankan satu research
> experiment secara reproducible
> dari data sampai conclusion.**

---

# 47. MVP End-to-End

MVP harus mampu:

```text
CSV
 ↓
Validation
 ↓
Strategy Configuration
 ↓
Signal Detection
 ↓
Trade Simulation
 ↓
Trade Log
 ↓
Statistics
 ↓
Report
```

Jika workflow tersebut berhasil,
MRE sudah memiliki core capability.

---

# 48. MVP Research Case

Initial MVP strategy:

```text
RSI Trendline Breakout
```

MVP tidak membutuhkan
puluhan strategy.

Satu strategy yang benar-benar
dapat diuji sudah cukup untuk
memvalidasi architecture.

---

# 49. MVP Success Criteria

MVP berhasil apabila:

## Data

Historical dataset dapat
dimasukkan dan divalidasi.

## Strategy

Strategy dapat didefinisikan
secara deterministic.

## Simulation

Trade dapat disimulasikan
tanpa lookahead bias.

## Statistics

Core metrics dapat dihitung.

## Reproducibility

Experiment dapat diulang.

## Reporting

Result dapat dibaca dan
ditelusuri kembali.

---

# 50. Research-to-Product Evolution

Roadmap MRE:

```text
Research Tool
      ↓
Research Framework
      ↓
Multi-Strategy Engine
      ↓
Market Research Platform
```

Evolution tidak boleh terjadi
sebelum core research capability
terbukti.

---

# 51. Technical Debt Strategy

Technical debt diperbolehkan
jika:

- explicit;
- documented;
- controlled;
- tidak merusak correctness.

Technical debt tidak boleh
menjadi alasan untuk mengorbankan:

- reproducibility;
- correctness;
- data integrity.

---

# 52. Documentation Alongside Development

Setiap major implementation
harus memiliki documentation impact.

Pattern:

```text
Requirement
    ↓
Architecture
    ↓
Implementation
    ↓
Test
    ↓
Documentation
```

Documentation bukan aktivitas
setelah project selesai.

---

# 53. Research Knowledge Lifecycle

Setiap research result mengikuti:

```text
Experiment
    ↓
Raw Result
    ↓
Analysis
    ↓
Validation
    ↓
Conclusion
    ↓
Research Knowledge
```

Knowledge yang telah tervalidasi
dapat mempengaruhi:

```text
Product
Architecture
Strategy
Future Experiments
```

---

# 54. Roadmap Governance

Roadmap dapat berubah.

Perubahan harus berdasarkan:

- evidence;
- new requirements;
- architecture constraints;
- research findings;
- product feedback.

Roadmap tidak boleh berubah
hanya karena impulse.

---

# 55. Roadmap Change Rule

Jika perubahan besar terjadi:

```text
Current Roadmap
      ↓
Change Proposal
      ↓
Impact Analysis
      ↓
Decision
      ↓
Updated Roadmap
```

Major roadmap changes harus
dicatat dalam decision log.

---

# 56. Roadmap vs TODO

Perbedaan:

## Roadmap

Menjawab:

> **Where are we going?**

## TODO

Menjawab:

> **What exactly should we do next?**

Contoh:

```text
Roadmap:
M2 Architecture

TODO:
- Define DataSchema
- Define Event interface
- Define Simulation API
```

---

# 57. Roadmap vs Project Status

## Roadmap

Future-oriented.

```text
Where are we going?
```

## FND-006

Current-state oriented.

```text
Where are we now?
```

Relationship:

```text
             ROADMAP
                │
                ▼
          Future Direction
                │
                ▼
          Current Status
                │
                ▼
             TODO
                │
                ▼
              TASK
```

---

# 58. Roadmap Health Indicators

Roadmap dianggap sehat apabila:

- current phase jelas;
- next phase jelas;
- dependencies jelas;
- exit criteria jelas;
- scope terkendali;
- milestones measurable;
- research objective tetap visible.

---

# 59. Current Roadmap Position

```text
M0 Foundation
████████████░░░░░░░░  In Progress

M1 Product
░░░░░░░░░░░░░░░░░░░░  Planned

M2 Architecture
░░░░░░░░░░░░░░░░░░░░  Planned

M3 Research
░░░░░░░░░░░░░░░░░░░░  Planned

M4 Engine
░░░░░░░░░░░░░░░░░░░░  Planned

M5 Experiment
░░░░░░░░░░░░░░░░░░░░  Planned

M6 Validation
░░░░░░░░░░░░░░░░░░░░  Planned

M7 Iteration
░░░░░░░░░░░░░░░░░░░░  Planned

M8 Expansion
░░░░░░░░░░░░░░░░░░░░  Planned
```

---

# 60. Current Strategic Priority

Current priority remains:

```text
FOUNDATION
```

Specifically:

```text
FND-007 Roadmap
      ↓
FND-008 TODO
      ↓
FND-009 Glossary
```

Setelah itu:

```text
PRODUCT DEFINITION
```

---

# 61. First Major Technical Goal

Target technical capability:

> Run a complete, deterministic,
> reproducible trading strategy experiment
> from historical CSV to statistical report.

This is the first major
technical proof of MRE.

---

# 62. First Major Research Goal

Target research capability:

> Determine whether RSI Trendline Breakout
> demonstrates measurable statistical edge
> under explicitly defined assumptions.

---

# 63. First Major Product Goal

Target product capability:

> Allow a researcher to define,
> execute,
> inspect,
> and compare experiments
> without manually rewriting
> the research engine.

---

# 64. First Major Architecture Goal

Target architecture capability:

> Add or modify a strategy without
> rewriting the data, simulation,
> statistics, and reporting layers.

---

# 65. First Major Quality Goal

Target quality capability:

> Same dataset + same configuration +
> same code version = reproducible result.

---

# 66. Long-Term Vision

Long-term MRE dapat berkembang menjadi:

```text
                 MARKET RESEARCH ENGINE
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
      Strategies       Markets        Research
          │               │               │
          ▼               ▼               ▼
      Indicators       Timeframes     Experiments
          │               │               │
          └───────────────┼───────────────┘
                          ▼
                  Evidence Engine
                          │
                          ▼
                   Market Knowledge
```

---

# 67. What Success Looks Like

Success bukan:

```text
Huge Backtest Profit
```

Success adalah:

```text
Reliable Research
       +
Reproducible Experiments
       +
Clear Evidence
       +
Extensible Architecture
       +
Accumulated Knowledge
```

---

# 68. Roadmap Completion Criteria

FND-007 dianggap complete apabila:

- [x] Project stages defined.
- [x] Milestones defined.
- [x] Dependencies defined.
- [x] Phase objectives defined.
- [x] Exit criteria defined.
- [x] MVP defined.
- [x] Research progression defined.
- [x] Architecture progression defined.
- [x] Expansion strategy defined.
- [x] Roadmap governance defined.
- [x] Current roadmap position documented.

---

# 69. Final Principle

MRE tidak dibangun untuk
bergerak secepat mungkin.

MRE dibangun untuk:

> **bergerak cukup cepat tanpa kehilangan
> kemampuan untuk mengetahui apakah
> sesuatu benar-benar bekerja.**

Roadmap ini menjaga agar:

```text
Speed
  +
Structure
  +
Evidence
```

tetap seimbang.

---

# Appendix A — Roadmap in One Page

```text
┌─────────────────────────────────────────────┐
│          MARKET RESEARCH ENGINE              │
├─────────────────────────────────────────────┤
│                                             │
│ M0  FOUNDATION                              │
│     Governance + Documentation              │
│                    │                        │
│                    ▼                        │
│ M1  PRODUCT                                 │
│     Requirements + MVP                      │
│                    │                        │
│                    ▼                        │
│ M2  ARCHITECTURE                            │
│     System + Domain + Data                  │
│                    │                        │
│                    ▼                        │
│ M3  RESEARCH                                │
│     Methodology + Validation                │
│                    │                        │
│                    ▼                        │
│ M4  ENGINE                                  │
│     Data → Signal → Simulation → Stats      │
│                    │                        │
│                    ▼                        │
│ M5  EXPERIMENT                              │
│     RSI Trendline Breakout                  │
│                    │                        │
│                    ▼                        │
│ M6  VALIDATION                              │
│     OOS + Sensitivity + Robustness          │
│                    │                        │
│                    ▼                        │
│ M7  ITERATION                               │
│     Evidence → Improvement                  │
│                    │                        │
│                    ▼                        │
│ M8  EXPANSION                               │
│     Multi Strategy / Market / Research      │
│                                             │
└─────────────────────────────────────────────┘
```

---

# Appendix B — AI Resume Context

Jika project dilanjutkan pada
conversation baru:

```text
Market Research Engine (MRE)
is currently in M0 Foundation.

FND-001 through FND-006 define:
- project governance;
- documentation;
- identity;
- knowledge registry;
- project context;
- current project status.

FND-007 defines the roadmap:

M0 Foundation
→ M1 Product
→ M2 Architecture
→ M3 Research
→ M4 Engine
→ M5 Baseline Experiment
→ M6 Validation
→ M7 Iteration
→ M8 Expansion.

Initial MVP goal:
Run one complete deterministic research
experiment from historical CSV to report.

Initial research case:
RSI Trendline Breakout.

Initial research objective:
Measure probability, RR, expectancy,
and robustness.

Current immediate next documents:
FND-008 TODO
FND-009 Glossary.

After Foundation:
Begin Product Definition.
```

---

**Document Status:** Active

**Document ID:** FND-007

**Version:** 1.0.1

**End of Document**
