---
title: RSI Trendline Breakout Baseline
document_id: EXP-001
version: 1.0.3
status: Result
category: Experiment
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-09

depends_on:
  - RSH-001
  - RSH-002
  - RSH-003
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

Code Version (git commit) tercatat di report (`9564eee`).
Run direproduksi deterministik: dua run (130f3f8-dirty, 9564eee)
menghasilkan metrik identik (FR-010, NFR-001).

---

# 16. Sensitivity Analysis (TODO-024)

Metodologi per **RSH-003 §9**: satu parameter divariasikan,
parameter lain tetap (control); variasi dilakukan pada dataset
immutable yang sama dan signal definition LONG yang sama (ENG-003 §10).

Report: `experiments/EXP-001/EXP-001_sensitivity.md`
(Code Version `136fb14` — commit baseline, setelah merge PR #39).

Semua variasi memenuhi syarat sampel (n ≥ 30) dan tetap
expectancy positif, namun magnitude edge bervariasi.

| Parameter      | Value | Trades | Win Rate | Expectancy | PF    | Net P&L  | Max DD  |
| -------------- | ----- | ------ | -------- | ---------- | ----- | -------- | ------- |
| rsi_period     | 7     | 1411   | 0.4961   | 0.8517     | 1.2121| 1201.79  | 388.14  |
| rsi_period     | 14    | 1403   | 0.4954   | 0.8683     | 1.2087| 1218.23  | 402.24  |
| rsi_period     | 21    | 1398   | 0.4857   | 0.5741     | 1.1296| 802.54   | 607.90  |
| price_lookback | 10    | 2368   | 0.4992   | 0.3824     | 1.0876| 905.60   | 627.94  |
| price_lookback | 20    | 1403   | 0.4954   | 0.8683     | 1.2087| 1218.23  | 402.24  |
| price_lookback | 30    | 1132   | 0.4938   | 0.7402     | 1.1708| 837.89   | 414.50  |
| signal_window  | 3     | 1026   | 0.4951   | 1.3354     | 1.3325| 1370.09  | 222.12  |
| signal_window  | 5     | 1403   | 0.4954   | 0.8683     | 1.2087| 1218.23  | 402.24  |
| signal_window  | 10    | 2279   | 0.4967   | 0.8184     | 1.1977| 1865.05  | 496.16  |
| hold_bars      | 5     | 1403   | 0.5118   | 0.8867     | 1.2774| 1244.07  | 336.18  |
| hold_bars      | 10    | 1403   | 0.4954   | 0.8683     | 1.2087| 1218.23  | 402.24  |
| hold_bars      | 20    | 1403   | 0.5153   | 2.0075     | 1.3854| 2816.59  | 416.43  |
| swing_left     | 1     | 1937   | 0.4930   | 0.5365     | 1.1285| 1039.17  | 527.64  |
| swing_left     | 2     | 1403   | 0.4954   | 0.8683     | 1.2087| 1218.23  | 402.24  |
| swing_left     | 3     | 1131   | 0.5049   | 1.3704     | 1.3469| 1549.93  | 256.31  |
| swing_right    | 1     | 1673   | 0.5057   | 0.7081     | 1.1711| 1184.57  | 500.37  |
| swing_right    | 2     | 1403   | 0.4954   | 0.8683     | 1.2087| 1218.23  | 402.24  |
| swing_right    | 3     | 1274   | 0.5008   | 0.8263     | 1.2073| 1052.70  | 425.52  |

Interpretasi:

- **edge tidak fragile secara arah**: tidak ada variasi yang
  menghasilkan expectancy negatif atau PF < 1 — seluruh grid
  tetap positif (RSH-003 §9);
- **parameter paling sensitif** (expectancy menyimpang dari baseline):
  - `price_lookback=10` → expectancy turun ke 0.3824 (−56%)
    dan trade count naik ke 2368 (noise harga → banyak konfirmasi palsu);
  - `rsi_period=21` → expectancy turun ke 0.5741 (−34%);
  - `swing_left=1` → expectancy turun ke 0.5365 (−38%);
- **parameter yang justru memperkuat edge** (tidak dipilih sebagai
  baseline — sensitivity bersifat deskriptif, bukan optimasi
  in-sample, RSH-001 §12):
  - `hold_bars=20` → expectancy 2.0075 (+131%), PF 1.3854;
  - `swing_left=3` → expectancy 1.3704 (+58%), max DD turun ke 256;
  - `signal_window=3` → expectancy 1.3354 (+54%), max DD turun ke 222;
- sinyal peningkatan ini **tidak boleh dipakai untuk optimasi
  baseline** (FND-008 §36 — jangan mengoptimasi sebelum seluruh
  validasi selesai); dieksplorasi pada iterasi lanjutan (M7);
- trade count bervariasi karena jumlah trigger/konfirmasi berubah
  seiring window dan lookback; semua variasi tetap ≥ 1026 (n besar).

Determinisme diverifikasi: run control (nilai baseline) pada setiap
parameter menghasilkan metrik identik dengan baseline (FR-010).

---

# 17. Out-of-Sample Testing (TODO-025)

Metodologi per **RSH-003 §6/§7**: split kronologis (no leakage,
no retroactive allocation); strategi frozen (konfigurasi EXP-001)
dijalankan tanpa perubahan pada kedua segmen.

Report: `experiments/EXP-001/EXP-001_oos.md`
(Code Version `7a8479b`).

Split point: index 70.000 (2021-04-29 18:00 UTC) — 70% train, 30% test.

| Metric        | Baseline | Train  | Test   | Δ Test/Train |
| ------------- | -------- | ------ | ------ | ------------ |
| Trade Count   | 1403     | 943    | 453    | -            |
| Win Rate      | 0.4954   | 0.4931 | 0.5033 | -            |
| Expectancy    | 0.8683   | 0.1187 | 2.4996 | +2004.9%     |
| Profit Factor | 1.2087   | 1.0371 | 1.4042 | +35.4%       |
| Net P&L       | 1218.23  | 111.98 | 1132.30| +911.2%      |
| Max DD        | 402.24   | 243.55 | 402.24 | -            |
| Sufficient    | True     | True   | True   | -            |

Interpretasi:

- **edge tetap positif out-of-sample** (expectancy > 0, PF > 1,
  sample cukup pada test set);
- tidak ada degradasi besar in-sample → OOS (RSH-003 §7) — justru
  **meningkat**: expectancy test (2.4996) jauh di atas train (0.1187);
- perbandingan deskriptif; threshold per RSH-004 dapat dikonfigurasi
  per experiment.

---

# 18. Robustness Analysis (TODO-026)

Metodologi per **RSH-003 §10**: kombinasi parameter/data beragam;
frozen config dievaluasi terhadap perubahan rentang data, market,
dan biaya transaksi (deskriptif, bukan optimasi — RSH-001 §12).

Report: `experiments/EXP-001/EXP-001_robustness.md`
(Code Version `7a8479b`).

## 18.1 Time Period Stability (4 slice kronologis)

| Slice    | Trades | Win Rate | Expectancy | PF    | Net P&L  | Max DD  |
| -------- | ------ | -------- | ---------- | ----- | -------- | ------- |
| period-1 | 397    | 0.5038   | 0.2196     | 1.0625| 87.17    | 243.55  |
| period-2 | 293    | 0.5051   | 0.1938     | 1.0756| 56.78    | 124.91  |
| period-3 | 329    | 0.4559   | -0.1677    | 0.9531| -55.17   | 219.95  |
| period-4 | 379    | 0.5198   | 3.1131     | 1.4721| 1179.88  | 402.24  |

- 3/4 slice expectancy positif; **slice ke-3 negatif** (−0.1677,
  PF < 1) — edge tidak stabil secara temporal, mengindikasikan
  ketergantungan regime market;
- slice ke-4 mendominasi Net P&L baseline (1179.88 dari 1218.23).

## 18.2 Cross-Market (XAGUSD H1, frozen config)

| Market | Trades | Win Rate | Expectancy | PF    | Net P&L | Max DD |
| ------ | ------ | -------- | ---------- | ----- | ------- | ------ |
| XAGUSD | 1122   | 0.5045   | 0.0397     | 1.3050| 44.52   | 16.90  |

- edge positif **tipis** ter-reproduksi out-of-market (expectancy 0.0397
  dengan PF 1.3050) — arah bertahan namun magnitude jauh lebih kecil.

## 18.3 Execution Cost & Slippage (fraksi notional per sisi)

| commission | slippage | Expectancy | PF    | Net P&L  |
| ---------- | -------- | ---------- | ----- | -------- |
| 0          | 0        | 0.8683     | 1.2087| 1218.23  |
| 0.0002     | 0        | 0.1539     | 1.0340| 215.96   |
| 0.0005     | 0        | -0.9176    | 0.8210| -1287.44 |
| 0          | 0.0002   | 0.1539     | 1.0340| 215.96   |
| 0          | 0.0005   | -0.9176    | 0.8210| -1287.44 |
| 0.0002     | 0.0002   | -0.5604    | 0.8862| -786.30  |
| 0.0005     | 0.0005   | -2.7036    | 0.5651| -3793.10 |

- edge **tidak bertahan** terhadap biaya transaksi realistis: biaya
  per sisi 0.02% (round-trip ~0.04%) menyisakan expectancy hampir nol;
  pada 0.05% per sisi expectancy negatif;
- baseline dijalankan tanpa biaya (EXP-001 §9.4) — hipotesis "setelah
  biaya transaksi" belum teruji pada skenario biaya nyata.

## 18.4 Parameter Combinations (price_lookback / rsi_period)

| price_lookback | rsi_period | Trades | Expectancy | PF    |
| -------------- | ---------- | ------ | ---------- | ----- |
| 20 (baseline)  | 14         | 1403   | 0.8683     | 1.2087|
| 10             | 7          | 2324   | 0.4653     | 1.1113|
| 10             | 21         | 2354   | 0.2249     | 1.0505|
| 30             | 7          | 1157   | 0.5684     | 1.1338|
| 30             | 21         | 1119   | 0.3664     | 1.0793|

- seluruh kombinasi (termasuk corner harga) tetap expectancy positif
  dan sample cukup — tidak ada kombinasi fragile pada grid ini.

## 18.5 Assessment Ringkas

- temporal robustness **lemah** (1/4 periode negatif);
- cross-market robustness **tipis** (XAGUSD positif namun marginal);
- execution-cost robustness **gagal** pada biaya realistis;
- parameter-combination robustness **stabil** (5/5 positif).

Timeframe tidak divariasikan: hanya data H1 yang tersedia.

---

# 19. Conclusion

Ditentukan oleh peneliti setelah Result tersedia
(PRD-006 §9 — conclusion manual, bukan otomatis).

---

# 20. Traceability

| Item          | Requirement / TODO           |
| ------------- | ---------------------------- |
| Hypothesis    | RSH-001 §7, TODO-013         |
| Spec fields   | RSH-002 §6, TODO-014         |
| Metrics       | RSH-002 §8, FND-008 §25      |
| Reproducibility | FR-010, NFR-001, RSH-002 §9  |
| Sensitivity   | RSH-003 §9, TODO-024         |
| Out-of-sample | RSH-003 §6/§7, TODO-025      |
| Robustness    | RSH-003 §10, TODO-026        |
| Conclusion    | FR-011, RSH-001 §13          |

---

# 21. Compliance

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

# 22. References

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
- `docs/05-research/RSH-003_Validation_Methodology.md`
- `docs/05-research/RSH-004_Statistical_Methodology.md`
- `docs/05-research/RSH-005_Research_Reporting.md`
- `docs/03-engine/ENG-002_Event_Engine.md`
- `docs/03-engine/ENG-003_Signal_Engine.md`
- `docs/03-engine/ENG-005_Simulation_Engine.md`
- `docs/03-engine/ENG-006_Statistics_Engine.md`
- `docs/03-engine/ENG-007_Reporting_Engine.md`
- `docs/01-product/PRD-006_MVP_Definition.md`

---

# 23. Revision History

| Version | Date       | Changes                      |
| ------- | ---------- | ---------------------------- |
| 1.0.3   | 2026-08-09 | OOS (TODO-025) dan robustness (TODO-026) dicatat (§17, §18) |
| 1.0.2   | 2026-08-08 | Sensitivity analysis (TODO-024) dicatat (§16) |
| 1.0.1   | 2026-08-08 | Run baseline (TODO-023); signal definition diarahkan LONG via trigger_payload |
| 1.0.0   | 2026-08-08 | Initial EXP-001 definition (TODO-022) |

---

**Document Status:** Result

**Document ID:** EXP-001

**Version:** 1.0.3

**End of Document**
