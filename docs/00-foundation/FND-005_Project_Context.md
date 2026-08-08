---
title: Project Context
document_id: FND-005
version: 1.0.1
status: Active
category: Foundation
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-08

depends_on:
  - FND-001
  - FND-002
  - FND-003
  - FND-004

related_to:
  - PRD-001
  - ARC-001
  - RSH-001

purpose: Provide a concise, persistent, and authoritative context of the Market Research Engine project
---

# Project Context

> **Understand the context before changing the code.**

---

# 1. Purpose

Dokumen ini menyediakan konteks utama
Market Research Engine (MRE).

FND-005 dirancang agar seseorang yang baru
masuk ke project dapat memahami:

- apa project ini;
- mengapa project ini dibuat;
- masalah apa yang ingin diselesaikan;
- siapa target pengguna;
- bagaimana project bekerja secara konseptual;
- apa yang bukan bagian dari project;
- prinsip apa yang harus dijaga;
- posisi project saat ini;
- apa langkah berikutnya.

Dokumen ini juga berfungsi sebagai
**persistent project context** untuk AI assistant,
developer,
researcher,
dan contributor.

---

# 2. Project Identity

| Attribute               | Value                            |
| ----------------------- | -------------------------------- |
| Project Name            | Market Research Engine           |
| Abbreviation            | MRE                              |
| Repository              | `jjaenal/market_research_engine` |
| Project Type            | Research & Backtesting Framework |
| Primary Domain          | Quantitative Market Research     |
| Primary Language        | Python                           |
| Architecture Style      | Modular / Event-Oriented         |
| Current Phase           | Foundation                       |
| Current Focus           | Documentation & Architecture     |
| Primary Market Use Case | Trading Strategy Research        |

---

# 3. One-Sentence Description

Market Research Engine adalah framework penelitian
yang digunakan untuk mengubah historical market data
menjadi evidence statistik yang dapat digunakan
untuk mengevaluasi trading hypothesis.

---

# 4. Project Vision

MRE bertujuan menjadi platform penelitian market
yang memungkinkan researcher:

1. mendefinisikan hypothesis;
2. mengolah historical market data;
3. mendeteksi market events;
4. membangun trading signals;
5. melakukan simulation;
6. menghitung probability dan statistics;
7. membandingkan hasil eksperimen;
8. menghasilkan knowledge yang reproducible.

---

# 5. Why MRE Exists

Trading strategy sering dikembangkan
berdasarkan:

- visual pattern;
- pengalaman subjektif;
- intuisi;
- cherry-picked examples;
- limited sample;
- hasil backtest yang tidak konsisten.

Pendekatan tersebut dapat menghasilkan
kesimpulan yang tidak reliable.

MRE dibuat untuk menyediakan proses
yang lebih sistematis.

Alur utamanya:

```text
Hypothesis
    ↓
Data
    ↓
Detection
    ↓
Signal
    ↓
Simulation
    ↓
Statistics
    ↓
Validation
    ↓
Knowledge
```

---

# 6. Core Problem

Problem utama yang ingin diselesaikan:

> Bagaimana mengetahui apakah sebuah market pattern
> benar-benar memiliki statistical edge,
> bukan sekadar terlihat bagus pada chart?

MRE tidak berusaha menjawab:

> "Strategi mana yang pasti menghasilkan profit?"

MRE berusaha menjawab:

> "Apa yang sebenarnya dikatakan oleh data?"

---

# 7. Core Philosophy

MRE dibangun berdasarkan prinsip:

> **Don't trust the chart. Measure the market.**

Market hypothesis harus diuji
menggunakan data.

Pendapat harus dipisahkan dari evidence.

---

# 8. Research Philosophy

MRE mengikuti pendekatan:

```text
Observation
    ↓
Hypothesis
    ↓
Experiment
    ↓
Measurement
    ↓
Validation
    ↓
Conclusion
```

Kesimpulan tidak boleh ditentukan
sebelum experiment dilakukan.

---

# 9. What MRE Is

MRE adalah:

- research framework;
- backtesting framework;
- statistical analysis framework;
- experiment framework;
- market event detection framework;
- strategy evaluation framework;
- knowledge generation system.

---

# 10. What MRE Is Not

MRE bukan:

- broker;
- trading platform;
- exchange;
- signal-selling service;
- guaranteed-profit system;
- automated financial advisor;
- investment recommendation engine.

MRE tidak menjanjikan profit.

MRE menyediakan tooling untuk penelitian.

---

# 11. Target Users

## 11.1 Quantitative Researcher

User yang ingin menguji
market hypothesis secara sistematis.

---

## 11.2 Algorithmic Trader

User yang ingin mengevaluasi
strategy sebelum deployment.

---

## 11.3 Software Engineer

Developer yang ingin membangun
atau menambahkan research component.

---

## 11.4 Trading Strategy Researcher

User yang ingin mengetahui:

- win probability;
- risk/reward;
- expectancy;
- drawdown;
- robustness;
- market condition dependency.

---

# 12. Primary Use Case

Use case utama MRE:

> Researcher memiliki hypothesis trading
> dan ingin mengetahui apakah hypothesis tersebut
> memiliki statistical edge.

Contoh:

```text
Hypothesis:

RSI Trendline Breakout
memiliki positive expectancy
pada XAUUSD H1.
```

MRE kemudian digunakan untuk:

```text
Load Dataset
      ↓
Detect Events
      ↓
Generate Signals
      ↓
Simulate Trades
      ↓
Calculate Statistics
      ↓
Validate Result
      ↓
Produce Research Report
```

---

# 13. Initial Research Case

Strategi pertama yang digunakan sebagai
research case adalah:

> **RSI Trendline Breakout**

Strategi ini berfungsi sebagai:

- baseline;
- validation case;
- architecture test case;
- experiment case.

Strategi tersebut bukan tujuan akhir MRE.

---

# 14. Strategy Independence

MRE harus bersifat strategy-agnostic.

Framework tidak boleh dibangun
hanya untuk RSI Trendline Breakout.

Strategi lain harus dapat ditambahkan
tanpa mengubah core framework secara signifikan.

Contoh strategi yang secara teoritis
dapat diteliti:

- RSI Divergence;
- Fibonacci;
- Breakout;
- Supply & Demand;
- Liquidity Sweep;
- Break of Structure;
- Moving Average;
- Trend Following;
- Mean Reversion.

---

# 15. Conceptual Processing Model

Model konseptual MRE:

```text
Market Data
     │
     ▼
Observation
     │
     ▼
Detector
     │
     ▼
Event
     │
     ▼
Signal
     │
     ▼
Decision
     │
     ▼
Trade Simulation
     │
     ▼
Outcome
     │
     ▼
Statistics
     │
     ▼
Validation
     │
     ▼
Knowledge
```

---

# 16. Core Domain Concepts

MRE menggunakan terminology resmi berikut.

| Concept      | Meaning                                   |
| ------------ | ----------------------------------------- |
| Observation  | Raw measurable market fact                |
| Event        | Interpreted market occurrence             |
| Detector     | Component that detects Events             |
| Indicator    | Calculation producing market measurements |
| Signal       | Aggregation of Events                     |
| Confirmation | Supporting Event                          |
| Decision     | Evaluation of a Signal                    |
| Trade        | Simulated trading action                  |
| Position     | State of a Trade                          |
| Outcome      | Final Trade result                        |
| Dataset      | Historical market data                    |
| Strategy     | Rules connecting Events and Decisions     |
| Experiment   | Reproducible research process             |
| Hypothesis   | Testable proposition                      |
| Result       | Output of an Experiment                   |
| Knowledge    | Validated insight from Experiments        |

Detailed definitions are maintained in:

`FND-009 — Glossary`

---

# 17. Core Architecture Concept

MRE menggunakan pemisahan tanggung jawab
yang jelas.

Conceptual architecture:

```text
                 ┌──────────────────┐
                 │   Market Data    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   Data Engine    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │  Event Engine    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │  Signal Engine   │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Simulation Engine│
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Statistics Engine│
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Reporting Engine │
                 └──────────────────┘
```

Detail architecture akan didefinisikan
di `02-architecture/`.

---

# 18. Data Philosophy

Historical data merupakan input fundamental MRE.

Data harus:

- traceable;
- validated;
- normalized;
- immutable;
- reproducible.

Original dataset tidak boleh diubah
secara destructive.

---

# 19. Experiment Philosophy

Setiap eksperimen harus dapat dijawab:

```text
What?
Why?
Using What Data?
Using What Configuration?
Using What Strategy?
What Happened?
What Does It Mean?
Can It Be Reproduced?
```

Minimal experiment harus memiliki:

```text
Hypothesis
Dataset
Configuration
Strategy
Execution
Result
Conclusion
```

---

# 20. Probability Philosophy

MRE tidak mengejar:

> "Win rate setinggi mungkin."

Win rate harus dipandang
bersama metric lain.

Contoh:

- Win Rate;
- Loss Rate;
- Risk/Reward;
- Expectancy;
- Profit Factor;
- Maximum Drawdown;
- Sample Size;
- Variance;
- Distribution;
- Robustness.

Probability tidak boleh diinterpretasikan
secara terisolasi.

---

# 21. Risk / Reward Philosophy

Risk/Reward bukan parameter tunggal
yang secara otomatis menentukan kualitas strategy.

MRE harus memungkinkan researcher
menguji berbagai RR.

Contoh:

```text
RR 1:1
RR 1:1.5
RR 1:2
RR 1:3
RR 1:4
```

Tujuan penelitian:

> menemukan relationship antara
> probability, payoff, dan expectancy.

---

# 22. Reproducibility

Eksperimen harus dapat dijalankan kembali
dengan input yang sama.

Reproducibility membutuhkan:

```text
Dataset
+
Configuration
+
Strategy
+
Code Version
+
Experiment ID
```

menghasilkan:

```text
Comparable Result
```

---

# 23. Determinism

Dengan kondisi yang sama:

```text
Same Input
+
Same Configuration
+
Same Code Version
```

harus menghasilkan output
yang sama atau perbedaan yang dapat dijelaskan.

Deterministic behavior merupakan
salah satu quality requirement utama.

---

# 24. Separation of Research and Execution

MRE membedakan:

```text
Research
```

dengan:

```text
Live Trading Execution
```

Core framework fokus pada research.

Live broker execution bukan bagian
dari initial scope.

---

# 25. Scope — Current Phase

Current scope:

## Data

- CSV historical market data;
- OHLCV;
- timestamp;
- symbol;
- timeframe.

## Research

- Event detection;
- Signal generation;
- Trade simulation;
- Probability;
- Statistics;
- Experiment comparison.

## Output

- Trade log;
- Summary statistics;
- Experiment report;
- Charts;
- CSV export.

---

# 26. Out of Scope — Current Phase

Tidak termasuk initial implementation:

- live trading;
- broker API;
- automated order execution;
- portfolio management;
- cloud infrastructure;
- real-time streaming;
- machine learning;
- AI-generated trading signals;
- social trading;
- copy trading.

Fitur tersebut dapat dipertimbangkan
di fase berikutnya jika memiliki
justifikasi yang jelas.

---

# 27. Current Repository Context

Repository utama:

```text
jjaenal/market_research_engine
```

Current documentation structure:

```text
docs/
│
├── README.md
│
├── 00-foundation/
│
├── 01-product/
│
├── 02-architecture/
│
├── 03-engine/
│
├── 04-development/
│
├── 05-research/
│
├── 06-decisions/
│
├── 07-experiments/
│
├── 08-templates/
│
└── 09-reference/
```

---

# 28. Current Project State

Current phase:

```text
Foundation
```

Current activity:

```text
Documentation Development
```

Completed foundation documents:

```text
FND-001  Project Charter
FND-002  Documentation Standard
FND-003  Document ID Standard
FND-004  Document Index
```

Current document:

```text
FND-005  Project Context
```

---

# 29. Current Development State

Source implementation belum menjadi
fokus utama pada phase ini.

Prioritas saat ini:

```text
Documentation
      ↓
Product Definition
      ↓
Architecture
      ↓
Engine Specification
      ↓
Research Methodology
      ↓
Implementation
```

Coding tidak boleh mendahului
keputusan fundamental yang diperlukan.

---

# 30. Known Research Objective

Research objective awal:

> Menentukan apakah RSI Trendline Breakout
> memiliki probabilitas dan risk/reward
> yang memberikan positive expectancy
> pada dataset tertentu.

Objective ini tidak berarti
strategi tersebut diasumsikan profitable.

Hipotesis harus diuji.

---

# 31. Research Questions

Pertanyaan awal yang ingin dijawab:

## Q1

Berapa win probability strategy?

## Q2

Bagaimana hubungan win probability
dengan Risk/Reward?

## Q3

RR berapa yang menghasilkan
expectancy terbaik?

## Q4

Apakah hasil konsisten
di berbagai market condition?

## Q5

Apakah hasil bertahan
di out-of-sample data?

## Q6

Seberapa sensitif hasil
terhadap perubahan parameter?

---

# 32. Success Philosophy

MRE dianggap berhasil
bukan ketika menemukan strategy
dengan profit terbesar.

MRE berhasil ketika researcher dapat:

```text
Formulate Hypothesis
        ↓
Run Experiment
        ↓
Measure Result
        ↓
Validate Result
        ↓
Explain Result
        ↓
Reproduce Result
```

---

# 33. Failure Is a Valid Result

Experiment yang menghasilkan
strategy tidak profitable
tetap dianggap berhasil.

Contoh:

```text
Hypothesis:
RSI Trendline Breakout memiliki edge.

Result:
No statistically meaningful edge.

Conclusion:
Hypothesis rejected.
```

Hasil tersebut merupakan knowledge.

Kegagalan experiment bukan
kegagalan framework.

---

# 34. Anti-Confirmation Bias

MRE tidak boleh didesain
untuk membuktikan hypothesis benar.

Framework harus memberikan
kesempatan yang sama untuk:

```text
Accept
```

atau:

```text
Reject
```

hypothesis.

Researcher tidak boleh mengubah
kriteria setelah melihat hasil
tanpa mencatat perubahan tersebut.

---

# 35. Anti-Overfitting Philosophy

MRE harus memperlakukan
parameter optimization sebagai
proses yang berisiko.

Contoh:

```text
Optimize
   ↓
Backtest
   ↓
Great Result
```

tidak otomatis berarti:

```text
Real Edge
```

Validasi harus mempertimbangkan:

- out-of-sample;
- walk-forward;
- sensitivity;
- robustness;
- sample size;
- Monte Carlo bila relevan.

---

# 36. Knowledge Lifecycle

Knowledge dihasilkan melalui:

```text
Raw Data
   ↓
Observation
   ↓
Event
   ↓
Experiment
   ↓
Result
   ↓
Validation
   ↓
Knowledge
```

Knowledge yang belum divalidasi
tidak boleh dianggap sebagai
established knowledge.

---

# 37. Decision Hierarchy

Ketika terjadi konflik,
prioritas keputusan mengikuti:

```text
Project Charter
      ↓
Architecture Constitution
      ↓
Approved ADR
      ↓
Product Requirements
      ↓
Research Evidence
      ↓
Implementation Preference
```

Detail governance berada pada
`FND-001`.

---

# 38. Important Constraints

MRE harus menjaga constraint berikut:

## Constraint 1 — Reproducibility

Experiment harus dapat diulang.

## Constraint 2 — Determinism

Same input harus menghasilkan
same logical output.

## Constraint 3 — Modularity

Komponen harus loosely coupled.

## Constraint 4 — Explainability

Signal dan Decision harus dapat dijelaskan.

## Constraint 5 — Traceability

Result harus dapat ditelusuri
ke dataset dan configuration.

## Constraint 6 — Immutability

Historical dataset tidak boleh
diubah secara destructive.

---

# 39. Current Working Assumptions

Asumsi awal project:

1. Historical OHLCV data tersedia.
2. Data dapat diproses secara offline.
3. CSV merupakan initial input format.
4. Python digunakan untuk core research engine.
5. Researcher membutuhkan deterministic backtest.
6. Strategy harus dapat dipisahkan dari core engine.
7. Experiment harus dapat direproduksi.

Asumsi ini dapat berubah
jika evidence baru menunjukkan
bahwa asumsi tersebut tidak valid.

Perubahan harus didokumentasikan.

---

# 40. Important Non-Assumptions

MRE tidak mengasumsikan bahwa:

- semua strategy memiliki edge;
- high win rate berarti strategy bagus;
- high RR selalu lebih baik;
- backtest profit berarti live profit;
- historical pattern akan selalu berulang;
- satu dataset cukup;
- satu market cukup;
- satu timeframe cukup.

Semua pernyataan tersebut harus
diposisikan sebagai hypothesis
jika ingin diuji.

---

# 41. Mental Model for Contributors

Contributor baru disarankan
menggunakan mental model berikut:

```text
Do not ask:

"How do I code this?"

Ask:

"What are we trying to learn?"

Then:

"What evidence do we need?"

Then:

"What architecture supports the experiment?"

Then:

"How should it be implemented?"
```

---

# 42. AI Assistant Context

AI assistant yang bekerja pada repository MRE
harus memahami hal berikut sebelum
memberikan rekomendasi teknis:

```text
MRE = Research Framework
```

bukan:

```text
MRE = Trading Bot
```

AI assistant harus:

- menjaga terminology;
- membaca relevant documentation;
- menghormati Architecture Constitution;
- mempertahankan Document ID;
- tidak membuat asumsi tanpa evidence;
- membedakan hypothesis dari fact;
- mempertahankan reproducibility;
- mempertimbangkan research validity.

---

# 43. Context Loading Priority

Jika seluruh repository tidak dapat dibaca,
AI assistant harus memprioritaskan:

```text
1. FND-001 Project Charter
2. FND-005 Project Context
3. FND-006 Project Status
4. FND-004 Document Index
5. Relevant Product Document
6. Relevant Architecture Document
7. Relevant Engine Document
8. Relevant Research Document
9. Relevant Experiment
```

Tujuannya adalah memperoleh:

```text
Identity
↓
Context
↓
Current State
↓
Relevant Knowledge
```

---

# 44. Context Update Rules

FND-005 harus diperbarui apabila terjadi
perubahan fundamental pada:

- project identity;
- project scope;
- core philosophy;
- architecture direction;
- primary use case;
- current phase;
- major constraints;
- research objective.

FND-005 tidak perlu diperbarui
untuk setiap perubahan kecil.

---

# 45. Relationship With Project Status

FND-005 menjawab:

> **"Apa project ini?"**

Sedangkan:

`FND-006 — Project Status`

akan menjawab:

> **"Project ini sedang berada di mana?"**

Perbedaan ini harus dipertahankan.

---

# 46. Relationship With Project Charter

`FND-001` merupakan constitutional document.

`FND-005` merupakan contextual document.

Relationship:

```text
FND-001
Project Charter
     │
     ▼
FND-005
Project Context
```

FND-005 tidak boleh bertentangan
dengan FND-001.

---

# 47. Context Snapshot

Quick project snapshot:

```text
┌────────────────────────────────────────────┐
│          MARKET RESEARCH ENGINE             │
├────────────────────────────────────────────┤
│ Purpose                                    │
│ Quantitative Market Research               │
│                                            │
│ Primary Use Case                           │
│ Trading Strategy Research                  │
│                                            │
│ Current Phase                              │
│ Foundation                                 │
│                                            │
│ Current Focus                              │
│ Documentation                              │
│                                            │
│ Initial Research Case                      │
│ RSI Trendline Breakout                     │
│                                            │
│ Core Principle                             │
│ Don't trust the chart. Measure the market. │
└────────────────────────────────────────────┘
```

---

# 48. Quick Start for New Contributors

Contributor baru harus membaca
dokumen berikut secara berurutan:

```text
1. README.md
2. FND-005 — Project Context
3. FND-001 — Project Charter
4. FND-004 — Document Index
5. Relevant PRD
6. Relevant Architecture
7. Relevant Development Guide
```

Setelah itu contributor dapat
memulai task sesuai `FND-006`.

---

# 49. Definition of Done

FND-005 dianggap selesai apabila:

- [x] Project identity didefinisikan.
- [x] Project vision dijelaskan.
- [x] Core problem didefinisikan.
- [x] Target users didefinisikan.
- [x] Primary use case didefinisikan.
- [x] Initial research case didefinisikan.
- [x] Core terminology dijelaskan.
- [x] Conceptual architecture dijelaskan.
- [x] Current scope dijelaskan.
- [x] Out of scope dijelaskan.
- [x] Current state dicatat.
- [x] Research philosophy dicatat.
- [x] Reproducibility requirements dicatat.
- [x] Anti-overfitting principles dicatat.
- [x] AI context rules dicatat.
- [x] Context update rules didefinisikan.

---

# 50. Closing Statement

Market Research Engine dibangun bukan
untuk mencari jawaban yang ingin kita dengar.

MRE dibangun untuk menemukan
jawaban yang didukung oleh evidence.

Project ini dimulai dari pertanyaan sederhana:

> "Apakah RSI Trendline Breakout memiliki edge?"

Namun framework dirancang untuk menjawab
pertanyaan yang jauh lebih luas:

> "Bagaimana kita dapat meneliti market
> secara sistematis, reproducible,
> dan evidence-driven?"

Itulah konteks utama
Market Research Engine.

> **Research first. Measure carefully. Validate relentlessly. Build knowledge.**

---

# Appendix A — Project Context in 30 Seconds

```text
MRE adalah research framework.

Input:
Historical Market Data.

Process:
Observation
→ Event
→ Signal
→ Decision
→ Simulation
→ Statistics
→ Validation.

Output:
Evidence dan Knowledge.

Initial Strategy:
RSI Trendline Breakout.

Current Phase:
Foundation Documentation.

Current Goal:
Membangun fondasi Product,
Architecture,
Research,
dan Engineering
sebelum Sprint 1.
```

---

# Appendix B — Related Documents

| ID      | Document               | Relationship            |
| ------- | ---------------------- | ----------------------- |
| FND-001 | Project Charter        | Governing context       |
| FND-002 | Documentation Standard | Documentation rules     |
| FND-003 | Document ID Standard   | Identity rules          |
| FND-004 | Document Index         | Knowledge registry      |
| FND-006 | Project Status         | Current execution state |
| FND-007 | Roadmap                | Strategic direction     |
| FND-009 | Glossary               | Terminology             |
| PRD-001 | Product Vision         | Product direction       |
| ARC-001 | System Architecture    | Technical architecture  |
| RSH-001 | Research Methodology   | Research process        |

---

**Document Status:** Active

**Document ID:** FND-005

**Version:** 1.0.1

**End of Document**
