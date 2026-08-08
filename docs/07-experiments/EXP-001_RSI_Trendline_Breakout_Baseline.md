---
title: RSI Trendline Breakout Baseline
document_id: EXP-001
version: 1.0.1
status: Result
category: Experiment
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-08

depends_on:
  - RSH-001
  - RSH-002
  - RSH-004
  - RSH-005
  - ENG-002
  - ENG-003
  - ENG-005
  - ENG-006
  - ENG-007

referenced_by:
  - FND-006
  - FND-007
  - FND-008
  - FND-009

purpose: Define the first baseline experiment (EXP-001) — pre-registered hypothesis, frozen configuration, and expected outputs
---

# RSI Trendline Breakout Baseline

> Measure the Market. Discover the Edge.

---

# 1. Purpose

EXP-001 mendefinisikan **experiment baseline pertama** MRE
(RSH-002 §10 lifecycle — state `Defined`).

Dokumen ini menjawab TODO-022 — Create EXP-001 (FND-008).

Tujuan EXP-001 (FND-007 §24):

> Mengetahui baseline statistical characteristics
> dari strategy RSI Trendline Breakout.

Bukan mengoptimalkan strategy.

---

# 2. Scope

Scope EXP-001:

- hypothesis baseline (pre-registered);
- dataset tetap (immutable, Article 13);
- configuration frozen (strategy + execution + statistics);
- expected outputs (metrik minimum).

Di luar scope EXP-001:

- optimasi parameter (TODO-024);
- out-of-sample testing (TODO-025);
- robustness analysis (TODO-026);
- konklusi akhir (ditentukan peneliti, PRD-006 §9).

---

# 3. Audience

- tim MRE;
- peneliti;
- quant analyst;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Per FND-005 §37, Research Evidence adalah sumber prioritas keputusan.

Setiap experiment harus reproducible dan pre-registered
(RSH-001 §7.2, RSH-002 §9):

- konfigurasi terkunci (frozen) sebelum experiment dijalankan;
- Code Version dicatat (git commit);
- dataset immutable.

---

# 5. Definitions

Terminologi mengikuti **FND-009** (One Concept, One Name).

| Term                | Definition                                       |
| ------------------- | ------------------------------------------------ |
| Experiment          | Unit penelitian terikat konfigurasi (RSH-002 §5) |
| Event               | Fakta terdeteksi dari data (FND-001 Article 5)  |
| Signal              | Agregasi evidence dari Events (FND-009 §13)      |
| Trade               | Transaksi terukur dari simulasi (FND-009)        |
| Result              | Output terukur (metrics) dari experiment         |
| Baseline            | Reference point tanpa optimization (FND-009 §8.8)|

---

# 6. Hypothesis

Per RSH-001 §7.1, hipotesis dinyatakan dalam bentuk:

> Kondisi **X** (deteksi/Event) menghasilkan
> edge pada **Symbol** (Y) timeframe (**Z**).

Hipotesis EXP-001:

> **Breakout RSI trendline yang dikonfirmasi harga
> (Price Confirmation) pada XAUUSD H1
> menghasilkan expectancy positif
> setelah biaya transaksi.**

Kriteria (RSH-001 §7.2):

- falsifiable;
- terikat dataset dan konfigurasi spesifik (§7, §8);
- dinyatakan sebelum experiment dijalankan (pre-registration).

---

# 7. Dataset

| Field          | Value                                      |
| -------------- | ------------------------------------------ |
| File           | `datasets/XAUUSD_H1.csv`                   |
| Symbol         | XAUUSD                                     |
| Timeframe      | H1                                         |
| Source         | CSV (kolom: timestamp, open, high, low, close, volume) |
| Date Range     | 2009-09-11 18:00 → 2026-05-26 23:00        |
| Candle Count   | 100.000                                    |
| Integrity      | valid (validasi inti PRD-006 §8.2)         |

Dataset bersifat **immutable** (Article 13, ARC-004).
Rentang data dipakai penuh untuk baseline.

---

# 8. Strategy — RSI Trendline Breakout

Alur pemrosesan (config over hardcode, ARC-006):

```text
CSV → Loader → Candle
     → RSI(14)
     → Swing (fractal) → RSI Trendline (create/broken)
     → Price Confirmation
     → Event Engine → Signal Engine → Simulation → Statistics → Report
```

Deteksi mengikuti ADR-003 (Swing) dan ADR-004 (Trendline).

Strategi **LONG-only**: arah breakout (bullish/bearish) dipilih di
Signal Engine via `trigger_payload` (ENG-003 §7), bukan di detector
(ENG-002 §8). Deteksi detil pada §9.3.

---

# 9. Configuration (Frozen)

Konfigurasi dikunci (frozen) sebelum run (RSH-002 §9).

## 9.1 Indicators

| Parameter     | Value |
| ------------- | ----- |
| rsi_period    | 14    |

## 9.2 Event Engine (ENG-002)

| Parameter      | Value |
| -------------- | ----- |
| swing_left     | 2     |
| swing_right    | 2     |
| price_lookback | 20    |

## 9.3 Signal Definition (ENG-003)

| Field           | Value                       |
| --------------- | --------------------------- |
| signal_type     | LONG                        |
| trigger         | RSI_TRENDLINE_BROKEN        |
| trigger_payload | `{ "slope__lt": 0.0 }`      |
| confirmations   | (PRICE_CONFIRMATION)        |
| window          | 5                           |
| source_strategy | rsi_trendline_breakout      |

`trigger_payload` memilih arah bullish saja: break ke atas pada
down-trendline (slope < 0) — ENG-003 §10. Pemilihan arah terjadi di
Signal Engine, bukan detector (ENG-002 §8).

Baseline bersifat **LONG-only**: detector PRICE_CONFIRMATION saat ini
hanya bullish (close > highest high lookback); SHORT membutuhkan
price confirmation arah bawah yang belum ada pada MVP (PRD-006 §8).

## 9.4 Execution (ENG-005)

| Parameter        | Value |
| ---------------- | ----- |
| position_size    | 1.0   |
| commission_rate  | 0.0   |
| slippage_rate    | 0.0   |
| hold_bars        | 10    |
| stop_loss        | None  |
| take_profit      | None  |

TP/SL di luar MVP (PRD-006 §9): baseline berjalan
tanpa exit berbasis harga, hanya hold-based.

## 9.5 Statistics (ENG-006)

| Parameter  | Value |
| ---------- | ----- |
| min_sample | 30    |

---

# 10. Execution Assumptions

Per RSH-001 §14:

- **Entry**: open bar berikutnya setelah Signal (next bar open);
- **Exit**: setelah `hold_bars` (10) bar;
- **Sizing**: `position_size = 1.0` (fixed);
- **Transaction cost**: 0 (baseline murni, tanpa biaya);
- **Slippage**: 0;
- Eksekusi adalah simulasi, bukan live (PRD-006 §9).

---

# 11. Variables

## 11.1 Control Variables

- dataset (XAUUSD H1, rentang penuh);
- execution rules (sizing, biaya, slippage, hold_bars);
- konfigurasi bukan objek uji (§9).

## 11.2 Independent Variables

Tidak ada variasi pada baseline — seluruh parameter
tetap (frozen). Variasi dilakukan di experiment lanjutan
(TODO-024 sensitivity analysis).

## 11.3 Dependent Variables

- metrik minimum (RSH-002 §8);
- equity curve;
- trade log.

---

# 12. Baseline Reference

Per RSH-001 §9, experiment wajib memiliki baseline pembanding:

- **No Trade** — reference tanpa aktivitas (equity 0).

Perbandingan diukur pada rentang data yang sama.

---

# 13. Expected Outputs

Per FND-008 §25 dan RSH-002 §8:

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

Output dirender oleh Reporting Engine (ENG-007)
sebagai report terstruktur dengan Experiment ID.

---

# 14. Record Lifecycle

```text
Defined (spesifikasi + konfigurasi frozen)
    ↓ (TODO-023 Run Baseline Experiment)
Run
    ↓
Result (metrics dicatat)   ← saat ini
    ↓
Conclusion (interpretasi evidence — peneliti, PRD-006 §9)
    ↓
Reviewed (validasi, RSH-003)
```

---

# 15. Result

Diisi dari run baseline (TODO-023) menggunakan Experiment Runner
(`mre.core.experiment_runner`). Report: `experiments/EXP-001/EXP-001_report.md`.

Dataset: XAUUSD H1, 2009-09-11 → 2026-05-26 (100.000 candle).

| Metric           | Value   |
| ---------------- | ------- |
| Trade Count      | 1403    |
| Win Count        | 695     |
| Loss Count       | 708     |
| Win Rate         | 0.4954  |
| Loss Rate        | 0.5046  |
| Average Win      | 10.152  |
| Average Loss     | 8.245   |
| Risk/Reward      | 1.231   |
| Expectancy       | 0.868   |
| Profit Factor    | 1.209   |
| Gross Profit     | 7055.65 |
| Gross Loss       | 5837.42 |
| Net P&L          | 1218.23 |
| Maximum Drawdown | 402.24  |
| Winning Streak   | 11      |
| Losing Streak    | 12      |
| Evidence Sufficient | True (n=1403 ≥ 30) |

Observasi:

- trade count 1403 memenuhi syarat sampel minimum (min_sample 30);
- win rate < 0.5 namun RR > 1 → expectancy positif (+0.868);
- **signal overlap**: banyak Trade duplikat/identik (trigger RSI_TRENDLINE_BROKEN
  berdekatan memakai konfirmasi yang sama) — artefak semantik `combine()`
  (ENG-003 §8), bukan keputusan strategy. Didokumentasikan untuk iterasi
  (kemungkinan deduplikasi Signal pada M6/M7), bukan dioptimasi sebelum
  baseline tercatat (FND-008 §36).

Code Version (git commit) tercatat di report (`130f3f8`).

---

# 16. Conclusion

Ditentukan oleh peneliti setelah Result tersedia
(PRD-006 §9 — conclusion manual, bukan otomatis).

---

# 17. Traceability

| Item          | Requirement / TODO           |
| ------------- | ---------------------------- |
| Hypothesis    | RSH-001 §7, TODO-013         |
| Spec fields   | RSH-002 §6, TODO-014         |
| Metrics       | RSH-002 §8, FND-008 §25      |
| Reproducibility | FR-010, NFR-001, RSH-002 §9  |
| Conclusion    | FR-011, RSH-001 §13          |

---

# 18. Compliance

| Document / Rule          | Experiment requirement             |
| ------------------------ | ---------------------------------- |
| FND-003                  | ID immutable, sekuensial           |
| FND-005 §37              | Research Evidence priority         |
| FND-009                  | Backtest ≠ Proof                   |
| PRD-004 FR-010           | Reproducibility experiment         |
| PRD-004 FR-011           | Evaluate Evidence                  |
| PRD-006 §9               | TP/SL, optimasi, ML di luar MVP    |
| Article 13               | Dataset immutable                  |

---

# 19. References

- `docs/00-foundation/FND-003_Document_ID_Standard.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-006_Project_Status.md`
- `docs/00-foundation/FND-007_Roadmap.md`
- `docs/00-foundation/FND-008_TODO.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/02-architecture/ARC-004_Data_Architecture.md`
- `docs/02-architecture/ARC-006_Module_Architecture.md`
- `docs/06-decisions/ADR-003_Swing_Algorithm.md`
- `docs/06-decisions/ADR-004_Trendline_Algorithm.md`
- `docs/05-research/RSH-001_Research_Methodology.md`
- `docs/05-research/RSH-002_Experiment_Specification.md`
- `docs/05-research/RSH-004_Statistical_Methodology.md`
- `docs/05-research/RSH-005_Research_Reporting.md`
- `docs/03-engine/ENG-002_Event_Engine.md`
- `docs/03-engine/ENG-003_Signal_Engine.md`
- `docs/03-engine/ENG-005_Simulation_Engine.md`
- `docs/03-engine/ENG-006_Statistics_Engine.md`
- `docs/03-engine/ENG-007_Reporting_Engine.md`
- `docs/01-product/PRD-006_MVP_Definition.md`

---

# 20. Revision History

| Version | Date       | Changes                      |
| ------- | ---------- | ---------------------------- |
| 1.0.1   | 2026-08-08 | Run baseline (TODO-023); signal definition diarahkan LONG via trigger_payload |
| 1.0.0   | 2026-08-08 | Initial EXP-001 definition (TODO-022) |

---

**Document Status:** Result

**Document ID:** EXP-001

**Version:** 1.0.1

**End of Document**
