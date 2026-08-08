---
title: Statistics Engine
document_id: ENG-006
version: 1.0.0
status: Draft
category: Engine
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-08

depends_on:
  - FND-001
  - FND-005
  - FND-009
  - ARC-006
  - PRD-003
  - PRD-004
  - PRD-007
  - RSH-002
  - RSH-004
  - DEV-002
  - ENG-005

referenced_by:
  - FND-006
  - FND-008
  - ENG-007

purpose: Define the Statistics Engine implementation spec — minimum metrics and distribution (TODO-020, FEAT-007)
---

# Statistics Engine

> Measure the Market. Discover the Edge.

---

# 1. Purpose

ENG-006 mendefinisikan **Statistics Engine** — spesifikasi implementasi
untuk TODO-020 (Build Statistics Engine) dan FEAT-007 (Calculate Metrics).

Formula mengikuti **RSH-004 §6**; metrik minimum mengikuti **RSH-002 §8**.

---

# 2. Scope

Scope ENG-006:

- metrik minimum (RSH-002 §8);
- distribution analysis (RSH-004 §10);
- equity curve dan sample sufficiency.

Di luar scope ENG-006:

- evidence assessment (FR-011, reporting layer);
- optimasi / machine learning.

---

# 3. Audience

- tim MRE;
- software engineer;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Per ARC-006 §7.6:

```text
StatisticsEngine: calculate(trades, metric_selection) → Result
```

Per PRD-003 §7.7:

- input: Trade ledger, timeline Event/Signal, konfigurasi;
- processing: menghitung metrik statistik;
- failure conditions: jumlah Trade tidak cukup; formula tidak terdefinisi.

Per FR-007: metrik terdefinisi; menangani jumlah Trade yang tidak cukup.

---

# 5. Definitions

| Term       | Definition                              |
| ---------- | --------------------------------------- |
| Trade      | Completed research transaction (FND-009 §15.4) |
| Win Rate   | Probabilitas empiris Trade menang (RSH-004 §6.1) |
| Drawdown   | Penurunan equity peak-to-trough (RSH-004 §6.8) |
| Return     | P&L neto per Trade (RSH-004 §10)        |
| Sample     | Jumlah Trade untuk inferensi (RSH-004 §7) |

---

# 6. Metric Formulas (RSH-004 §6)

```text
Win Rate        = win_count / trade_count
Loss Rate       = loss_count / trade_count
Average Win     = gross_win / win_count
Average Loss    = gross_loss / loss_count
Risk/Reward     = Average Win / Average Loss
Expectancy      = (Win Rate × Average Win) − (Loss Rate × Average Loss)
Profit Factor   = Gross Profit / Gross Loss
Net P&L         = Gross Profit − Gross Loss
Max Drawdown    = penurunan maksimum equity dari peak ke trough
Winning Streak  = deret Trade menang terpanjang
Losing Streak   = deret Trade kalah terpanjang
```

- `win_rate` adalah probabilitas empiris menang
  (initial research question: Probability);
- Average Loss menggunakan magnitude positif;
- Profit Factor = `None` bila Gross Loss = 0.

---

# 7. Distribution (RSH-004 §10)

Dari `returns` (P&L neto tiap Trade):

- mean;
- standard deviation;
- skewness (population, `None` bila Trade < 3).

Digunakan untuk menilai risiko (drawdown, tail).

---

# 8. Equity Curve

```text
equity_t = Σ pnl_neto untuk trade ke-1..t
```

Curve tersimpan sebagai titik `(closed_at, equity)`.

---

# 9. Sample Sufficiency

Per RSH-004 §7:

- minimum 30 Trade untuk statistik dasar (default, dapat dikonfigurasi);
- Trade tidak cukup → `sufficient_sample = False`
  (evidence ditandai tidak cukup, FR-011).

---

# 10. Result Model

| Atribut           | Tipe   | Deskripsi                     |
| ----------------- | ------ | ----------------------------- |
| `trade_count`     | int    | Jumlah Trade                  |
| `win_count`       | int    | Jumlah menang                 |
| `loss_count`      | int    | Jumlah kalah                  |
| `win_rate`        | float  | Probabilitas menang empiris   |
| `loss_rate`       | float  | Probabilitas kalah empiris    |
| `avg_win`         | float  | Rata-rata profit menang       |
| `avg_loss`        | float  | Rata-rata loss (magnitude)    |
| `risk_reward`     | float  | Average Win / Average Loss    |
| `expectancy`      | float  | Net P&L / trade_count         |
| `profit_factor`   | float  | Gross Profit / Gross Loss     |
| `gross_profit`    | float  | Total profit menang           |
| `gross_loss`      | float  | Total loss kalah (magnitude)  |
| `net_pnl`         | float  | Gross Profit − Gross Loss     |
| `max_drawdown`    | float  | Penurunan equity maksimum     |
| `winning_streak`  | int    | Streak menang terpanjang      |
| `losing_streak`   | int    | Streak kalah terpanjang       |
| `returns`         | tuple  | P&L neto tiap Trade           |
| `mean_return`     | float  | Rata-rata return              |
| `std_return`      | float  | Standard deviation return     |
| `skewness`        | float  | Skewness populasi             |
| `equity_curve`    | tuple  | Titik (closed_at, equity)     |
| `sufficient_sample` | bool  | Trade count ≥ min_sample      |

Nilai `None` untuk metrik yang tidak terdefinisi
(misal tidak ada Trade, tidak ada win, tidak ada loss).

---

# 11. Failure Conditions

- `trades` kosong → dihitung sebagai hasil kosong
  (bukan error; ditangani FR-007);
- config invalid (`min_sample < 1`) → ValueError.

---

# 12. Testing (DEV-002)

- unit test formula terhadap data referensi;
- unit test edge case (kosong, all win, all loss);
- unit test sample sufficiency dan determinism.

---

# 13. Traceability

| Item         | Requirement / Feature     |
| ------------ | ------------------------- |
| Metrik       | RSH-002 §8, RSH-004 §6, FR-007 |
| Distribution | RSH-004 §10               |
| Sufficiency  | RSH-004 §7, FR-007        |
| calculate    | ARC-006 §7.6, FEAT-007    |

---

# 14. Compliance

| Article | Statistics requirement   |
| ------- | ------------------------ |
| Article 7 | Deterministic          |
| Article 13 | Result immutable      |

---

# 15. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/02-architecture/ARC-006_Module_Architecture.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`
- `docs/01-product/PRD-007_Feature_Specification.md`
- `docs/05-research/RSH-002_Experiment_Specification.md`
- `docs/05-research/RSH-004_Statistical_Methodology.md`
- `docs/04-development/DEV-002_Testing_Strategy.md`
- `docs/03-engine/ENG-005_Simulation_Engine.md`

---

# 16. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-08-08 | Initial statistics engine spec   |

---

**Document Status:** Draft

**Document ID:** ENG-006

**Version:** 1.0.0

**End of Document**
