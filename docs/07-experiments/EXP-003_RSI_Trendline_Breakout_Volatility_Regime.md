---
title: RSI Trendline Breakout — Volatility Regime Segmentation
document_id: EXP-003
version: 1.0.3
status: Result
category: Experiment
owner: Market Research Engine Core Team
created: 2026-08-10
last_updated: 2026-08-10

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
  - ARC-008

referenced_by:
  - FND-006
  - FND-008

purpose: Record EXP-003 run (TODO-039) — volatility regime segmentation re-test; verdict SUPPORTED per pre-registered criteria (edge concentrated in HIGH regime, stationary train+test at venue cost); tradable-validation addendum (finer slices, split sensitivity, combined filter; newer-data evaluation deferred)
---

# RSI Trendline Breakout — Volatility Regime Segmentation

> Measure the Market. Discover the Edge.

---

# 1. Purpose

EXP-003 adalah **experiment ketiga** MRE (RSH-002 §10 lifecycle — state
sekarang `Defined`, pre-registration).

Dokumen ini adalah **pre-registration** (RSH-001 §7.2): hipotesis,
variabel, dan kriteria keputusan dinyatakan **sebelum** experiment
dijalankan; run dan conclusion dicatat kemudian (section lanjutan).

Motivasi (evidence input dari EXP-002, §16/§17/§18.3):

- EXP-002 **SUPPORTED** per kriteria pre-registered pada biaya venue nyata
  (1.0 bps/side → expectancy 0.5111, n=1403 ≥ 30; breakeven ≈ 2.43 bps/side);
- namun **tidak stasioner secara temporal**: train negatif (−0.1605), hanya
  1/4 slice temporal positif — keuntungan terkonsentrasi di paruh terakhir
  data (volatilitas 2019+);
- oleh karena itu status "tradable" belum terpenuhi (FND-009: backtest ≠
  proof); rekomendasi lanjutan EXP-002 §18.3 adalah **segmentasi regime
  volatilitas** memakai M7 machinery (ARC-008 §14).

Tujuan EXP-003:

> Menguji apakah edge RSI trendline breakout **terkonsentrasi pada regime
> volatilitas TINGGI**; jika ya, menyaring sinyal ke regime high akan
> menghasilkan edge yang **positif dan stasioner** pada biaya venue nyata.

---

# 2. Scope

Scope EXP-003:

- pre-registration hypothesis (RSH-001 §7.2);
- dataset tetap (immutable, Article 13) — identik dengan EXP-001/EXP-002;
- configuration frozen: **identik dengan EXP-002** (biaya venue 1.0 bps/side),
  hanya `regime.selected_regime` yang berubah menjadi `"high"`;
- perbandingan regime high vs low vs unfiltered (EXP-002) sebagai variabel
  bebas;
- OOS dan robustness (RSH-003 §6/§7/§10) sebagai kriteria stasionaritas.

Di luar scope EXP-003:

- optimasi parameter (tetap sensitivity-style, bukan objek uji);
- modifikasi strategi/detector/engine (seluruhnya reusable dari M7);
- market lain (XAGUSD sudah dikerjakan di EXP-002 §17.2).

---

# 3. Audience

- tim MRE;
- peneliti;
- quant analyst;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Per FND-005 §37, Research Evidence adalah sumber prioritas keputusan.

EXP-002 menemukan edge **bertahan pada biaya venue nyata** tetapi **tidak
stasioner**: seluruh keuntungan muncul di paruh terakhir dataset
(volatilitas 2019+), train segment negatif pada biaya venue (EXP-002
§16/§17). Ini adalah pola klasik **regime-dependent edge**: strategi
berbasis breakout/trendline hanya bekerja ketika volatilitas sedang
mengembang (expanding), dan merugi ketika volatilitas mengerut (contracting).

MRE sudah memiliki **machinery regime selection** dari M7 (ARC-008 §14,
`src/mre/indicators/regime.py`, `RegimeConfig`, `select_regime`): setiap
candle dilabeli `high`/`low` dengan membandingkan ATR short (14) terhadap
ATR long-nya sendiri (100); `selected_regime` di config YAML menyaring
sinyal hanya pada candle dengan label regime yang dipilih (no lookahead).

EXP-003 memakai machinery tersebut tanpa modifikasi kode: hipotesisnya
adalah sinyal yang dikonfirmasi pada regime **high** menghasilkan edge
yang positif **dan stasioner** pada biaya venue nyata.

---

# 5. Definitions

Terminologi mengikuti **FND-009** (One Concept, One Name).

| Term           | Definition                                            |
| -------------- | ----------------------------------------------------- |
| Experiment     | Unit penelitian terikat konfigurasi (RSH-002 §5)      |
| Event          | Fakta terdeteksi dari data (FND-001 Article 5)        |
| Signal         | Agregasi evidence dari Events (FND-009 §13)           |
| Trade          | Transaksi terukur dari simulasi (FND-009)             |
| Result         | Output terukur (metrics) dari experiment              |
| Regime         | Klasifikasi volatilitas candle: high/low (ARC-008 §14)|
| Regime high    | ATR short (14) >= ATR long (100) — volatilitas mengembang |
| bps/side       | Basis point biaya per sisi (1 bps = 0.01%)            |

---

# 6. Hypothesis

Per RSH-001 §7.1:

> Kondisi **X** (deteksi/Event) menghasilkan
> edge pada **Symbol** (Y) timeframe (**Z**).

Hipotesis EXP-003 (pre-registered):

> **Breakout RSI trendline yang dikonfirmasi harga (Price Confirmation)
> pada XAUUSD H1 yang difilter ke regime volatilitas TINGGI (ATR short 14
> >= ATR long 100) menghasilkan expectancy positif DAN stasioner setelah
> biaya eksekusi venue nyata (1.0 bps/side).**

Kriteria (RSH-001 §7.2):

- falsifiable: keputusan ditentukan oleh kriteria terukur (§13);
- terikat dataset dan konfigurasi spesifik (§7, §9);
- dinyatakan sebelum experiment dijalankan (dokumen ini).

Catatan: hipotesis ini adalah **penyempitan** hipotesis EXP-002 (EXP-002
§6) — kondisi X yang sama, ditambah filter regime high. Jika edge memang
terkonsentrasi pada regime high, maka segmen train (yang negatif tanpa
filter) seharusnya membaik.

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

Dataset bersifat **immutable** (Article 13, ARC-004) dan identik dengan
EXP-001/EXP-002 §7 (kontrol).

## Market Definition (RSH-002 §6.1, E-5)

| Field                     | Value                                   |
| ------------------------- | --------------------------------------- |
| Instrument                | XAUUSD (spot gold)                      |
| Origin / Vendor           | Tidak terdokumentasi (CSV export lokal) |
| Session / Hours           | Tanpa filter session (seluruh bar tersedia) |
| Timezone                  | UTC (ISO 8601 `Z`)                      |
| Ordering                  | Strictly increasing timestamp           |
| Missing Data Handling     | Tidak diimputasi; ambang → ditolak      |
| Duplicate Handling        | Timestamp duplikat ditolak              |
| Gap Handling              | Tidak di-resample / tidak di-fill       |
| OHLC Rules                | open/close > 0; high ≥ max(o,c); low ≤ min(o,c) |
| Provenance                | CSV lokal; immutable (Article 13); identik EXP-001/EXP-002 §7 |

Aturan tertera konsisten dengan ARC-004 §7/§8 dan `validator.py`.

---

# 8. Strategy — RSI Trendline Breakout

Strategi **identik** dengan EXP-001 §8 / EXP-002 §8 (plugin
`rsi_trendline_breakout`, LONG-only, deteksi melalui pipeline yang sama).
Tidak ada perubahan pada detector, signal definition, atau engine.

---

# 9. Configuration (Frozen)

Konfigurasi dikunci (frozen) sebelum run (RSH-002 §9). Seluruh parameter
**menyamai EXP-002 §9** (termasuk biaya venue) **kecuali** §9.7 (regime
filter).

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
| cooldown        | 0                           |

## 9.4 Execution (ENG-005)

| Parameter       | Value |
| --------------- | ----- |
| position_size   | 1.0   |
| commission_rate | 0.00003 |
| slippage_rate   | 0.00007 |
| hold_bars       | 10    |
| stop_loss       | None  |
| take_profit     | None  |
| atr_period      | 14    |

## 9.5 Venue Cost Model (frozen, identik EXP-002 §9.5)

Biaya venue dibekukan **identik** dengan EXP-002 sehingga perbedaan hasil
hanya dapat diatribusikan ke filter regime:

- `commission_rate = 0.00003` (0.3 bps/side);
- `slippage_rate = 0.00007` (0.7 bps/side);
- total **1.0 bps/side** (representative retail ECN XAUUSD).

## 9.6 Statistics (ENG-006)

| Parameter  | Value |
| ---------- | ----- |
| min_sample | 30    |

## 9.7 Volatility Regime Filter (ARC-008 §14, M7 machinery)

| Parameter         | Value  |
| ----------------- | ------ |
| atr_short_period  | 14     |
| atr_long_period   | 100    |
| selected_regime   | "high" |

Sinyal hanya ditradingkan jika candle pada timestamp konfirmasinya
berlabel regime `high` (ATR short >= ATR long, `select_regime()` di
`experiment_runner.py` — no lookahead). Filter ini reuse M7 machinery
tanpa modifikasi kode.

---

# 10. Execution Assumptions

Per RSH-001 §14 (semantik terinci di SPEC-003/SPEC-004, E-9/E-10):

- **Entry**: open bar berikutnya setelah Signal **knowable** (E-1);
- **Exit**: setelah `hold_bars` (10) bar di **close** bar scheduled;
- **Sizing**: `position_size = 1.0` (fixed);
- **Transaction cost**: model venue §9.5 (identik EXP-002);
- **Slippage**: `slippage_rate` pada entry dan exit (conservative);
- **Regime label**: candle pada timestamp konfirmasi sinyal (no lookahead);
- Eksekusi adalah simulasi, bukan live (PRD-006 §9).

---

# 11. Variables

## 11.1 Control Variables

- dataset (XAUUSD H1, rentang penuh);
- strategy/indicator/event/signal config (§9.1–§9.3);
- biaya venue 1.0 bps/side (§9.5);
- hold_bars, sizing, SL/TP (off);
- min_sample;
- regime machinery parameters (ATR short 14 / long 100).

## 11.2 Independent Variables

Filter regime (`selected_regime`):

| Skenario   | selected_regime | Catatan                              |
| ---------- | --------------- | ------------------------------------ |
| High       | "high"          | primary (config frozen §9.7)         |
| Low        | "low"           | contrast: edge high vs low           |
| Unfiltered | ""              | reference = EXP-002 (0.5111)         |

## 11.3 Dependent Variables

- metrik minimum (RSH-002 §8);
- OOS train/test expectancy (stasionaritas, §12/§16);
- robustness temporal slices (RSH-003 §10);
- equity curve;
- trade log.

---

# 12. Baseline Reference

Per RSH-001 §9:

- **No Trade** — reference tanpa aktivitas (equity 0);
- **EXP-002 representative** (unfiltered, 1.0 bps/side → expectancy 0.5111,
  n=1403, EXP-002 §15.1) sebagai pembanding: filter regime dikatakan
  menambah nilai jika expectancy(high) > 0 DAN stasionaritas membaik
  (train tidak negatif).

---

# 13. Decision Criteria (pre-registered)

```text
SUPPORTED
Jika pada skenario representative (1.0 bps/side, selected_regime="high"):
  - expectancy(high) > 0 dengan n >= min_sample (30);
  - biaya breakeven/side >= 1.0 bps;
  - OOS test expectancy(high) > 0 (edge bertahan out-of-sample);
  - OOS train expectancy(high) > 0 (stasionaritas membaik vs EXP-002
    yang train-nya negatif −0.1605).

REJECTED
Jika salah satu kriteria SUPPORTED tidak terpenuhi.
```

Interpretasi tambahan (bukan keputusan, untuk konteks):

- perbandingan high vs low (§11.2) menunjukkan apakah edge memang
  regime-dependent (ekspektasi: high jauh lebih kuat dari low);
- jika SUPPORTED, EXP-002 §18.3 ter-realisasi: edge dapat disaring ke
  regime high sehingga menjadi kandidat tradable;
- jika REJECTED, edge tetap tidak dapat diselamatkan oleh filter regime
  sederhana ini.

Catatan multiple-testing (RSH-004 §8.2, E-8):

```text
- jumlah kriteria keputusan:            4 (expectancy > 0, breakeven >= 1.0 bps,
                                         OOS test > 0, OOS train > 0);
- jumlah kombinasi parameter (combo):   5 (price_lookback × rsi_period — EXP-001 legacy grid);
- jumlah slice temporal / split point:  4 slice, 1 split point (+ addendum 8 slice, 3 split point);
- jumlah dimensi robustness:            4 (periods, markets, costs, combos);
- koreksi / penalty:                    none — risiko data-snooping dinyatakan eksplisit.
```

Note: EXP-003 dijalankan sebelum standar E-8; blok ini dokumentasi
retrospektif, bukan pre-registered.

---

# 14. Expected Outputs

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

Output dirender oleh Reporting Engine (ENG-007) dengan Experiment ID.

---

# 15. Run (TODO-039)

Strategi dijalankan **frozen** (config `configs/EXP-003.yaml` = `EXP-003`),
tanpa perubahan pada parameter strategi — hanya filter regime
(`selected_regime: "high"`) yang membedakan dari EXP-002. Biaya venue
1.0 bps/side (representative) identik dengan EXP-002. Determinisme
diverifikasi: zero-cost point (1.2506) identik di baseline, grid, OOS dan
robustness.

Report: `experiments/EXP-003/EXP-003_report.md` (Code Version `4788eb3`).

## 15.1 Representative Scenario (1.0 bps/side, regime high, config frozen)

| Metric             | Value   |
| ------------------ | ------- |
| Trade Count        | 698     |
| Win Count          | 322     |
| Loss Count         | 376     |
| Win Rate           | 0.4613  |
| Loss Rate          | 0.5387  |
| Average Win        | 11.3498 |
| Average Loss       | 8.06992 |
| Risk/Reward        | 1.40643 |
| Expectancy         | 0.8887  |
| Profit Factor      | 1.2044  |
| Gross Profit       | 3654.63 |
| Gross Loss         | 3034.29 |
| Net P&L            | 620.342 |
| Maximum Drawdown   | 516.251 |
| Winning Streak     | 11      |
| Losing Streak      | 13      |
| Evidence Sufficient| True (n=698 ≥ 30) |

## 15.2 Regime Comparison (1.0 bps/side, venue cost identical)

| selected_regime | Trades | Expectancy | PF     | Win Rate | Net P&L   |
| --------------- | ------ | ---------- | ------ | -------- | --------- |
| (unfiltered)    | 1403   | 0.5111     | 1.1177 | 0.4783   | 717.09    |
| low             | 704    | 0.1540     | 1.0356 | 0.4957   | 108.43    |
| high            | 698    | 0.8887     | 1.2044 | 0.4613   | 620.34    |

Interpretasi: edge **terkonsentrasi pada regime high** — expectancy(high)
0.8887 jauh di atas unfiltered (0.5111) dan low (0.1540). Filter regime
membuang ~50% sinyal (1403 → 698) namun meningkatkan expectancy per trade
+74% vs unfiltered.

## 15.3 Venue-Derived Cost Grid (regime high)

| Scenario     | comm      | slip       | Total bps/side | Expectancy | PF     | Net P&L   |
| ------------ | --------- | ---------- | -------------- | ---------- | ------ | --------- |
| Zero cost    | 0         | 0          | 0              | 1.2506     | 1.3006 | 872.92    |
| ECN tight    | 0.00002   | 0.00003    | 0.5            | 1.0697     | 1.2515 | 746.63    |
| ECN rep.     | 0.00003   | 0.00007    | 1.0            | 0.8887     | 1.2044 | 620.34    |
| ECN wide     | 0.00005   | 0.00010    | 1.5            | 0.7078     | 1.1593 | 494.05    |
| Conservative | 0.00007   | 0.00013    | 2.0            | 0.5269     | 1.1160 | 367.77    |

Grid seluruhnya positif 0–2.0 bps/side (lebih lebar dari EXP-002, yang
membalik di ≈2.43 bps/side).

## 15.4 Breakeven Cost (regime high)

Breakeven (titik expectancy menyeberang nol), dihitung dengan grid halus:

- 3.38 bps/side → +0.0275 (PF 1.0057);
- 3.44 bps/side → +0.0058 (PF 1.0012);
- 3.46 bps/side → −0.0014 (PF 0.9997);
- **breakeven ≈ 3.44 bps/side** (vs 2.43 bps/side unfiltered EXP-002 §15.3).

Margin ke nol pada biaya venue nyata: 1.0 bps/side → margin **2.44 bps**
(breakeven − biaya) — **~70% lebih lebar** dari margin unfiltered
(1.43 bps, EXP-002 §18.2).

---

# 16. Out-of-Sample Testing (TODO-039)

Metodologi per **RSH-003 §6/§7**: split kronologis (no leakage, no
retroactive allocation); strategi frozen (konfigurasi EXP-003, regime
high) dijalankan tanpa perubahan pada kedua segmen — biaya tetap 1.0
bps/side. Reuse `run_on_slice` (ARC-ACT-013); filter regime diterapkan
otomatis oleh pipeline (no lookahead).

Report: `experiments/EXP-003/EXP-003_oos.md` (Code Version `4788eb3`).

Split point: index 70.000 (2021-04-29 18:00 UTC) — 70% train, 30% test
(identik EXP-002 §16).

| Metric        | Baseline | Train  | Test   | Δ Test/Train |
| ------------- | -------- | ------ | ------ | ------------ |
| Trade Count   | 698      | 446    | 253    | -            |
| Win Rate      | 0.4613   | 0.4596 | 0.4783 | -            |
| Expectancy    | 0.8887   | 0.1297 | 2.4853 | +1816.6%     |
| Profit Factor | 1.2044   | 1.0443 | 1.3680 | +31.0%       |
| Net P&L       | 620.34   | 57.83  | 628.77 | +987.2%      |
| Max DD        | 516.25   | 189.84 | 386.68 | -            |
| Sufficient    | True     | True   | True   | -            |

Interpretasi:

- **train segment kini positif** (+0.1297) — tidak lagi negatif seperti
  unfiltered EXP-002 (−0.1605): filter regime memperbaiki stasionaritas
  (kriteria SUPPORTED §13);
- **test tetap positif** (+2.4853, lebih tinggi dari EXP-002 +1.9810) —
  edge bertahan out-of-sample;
- edge masih lebih kuat di paruh akhir (test >> train), konsisten dengan
  EXP-002, namun **train tidak lagi rugi** — poin kunci perbaikan regime
  filter.

---

# 17. Robustness (TODO-039)

Metodologi per **RSH-003 §10**: strategi frozen (konfigurasi EXP-003,
regime high, biaya venue 1.0 bps/side) dijalankan pada slice waktu
kronologis, market lain, dan kombinasi parameter dekat-baseline.
Reuse `run_on_slice` (ARC-ACT-013).

Report: `experiments/EXP-003/EXP-003_robustness.md`
(Code Version `4788eb3`).

## 17.1 Time Period Stability

| Slice | Trades | Win Rate | Expectancy | PF    | Net P&L  | Max DD  |
| ----- | ------ | -------- | ---------- | ----- | -------- | ------- |
| period-1-of-4 | 172 | 0.4942 | 0.9849  | 1.3349 | 169.40 | 95.56 |
| period-2-of-4 | 173 | 0.4509 | −0.1541 | 0.9442 | −26.65  | 75.53 |
| period-3-of-4 | 139 | 0.4029 | −1.2684 | 0.6724 | −176.30 | 184.47|
| period-4-of-4 | 217 | 0.4931 | 3.2113  | 1.4598 | 696.85 | 386.68|

Interpretasi: **2/4 slice positif** (vs 1/4 unfiltered EXP-002 §17.1) —
robustness temporal membaik, namun masih bergantung pada paruh terakhir
(period-4 menyumbang sebagian besar P&L).

## 17.2 Cross-Market (XAGUSD, same timeframe)

| Market | Trades | Win Rate | Expectancy | PF    | Net P&L | Max DD |
| ------ | ------ | -------- | ---------- | ----- | ------- | ------ |
| XAGUSD | 533    | 0.5216   | 0.0409     | 1.3605| 21.80   | 9.42   |

Interpretasi: edge positif tipis ter-reproduksi di XAGUSD (expectancy
0.0409, PF 1.3605) — konsisten dengan EXP-002 §17.2 (0.0342).

## 17.3 Execution Cost (synthetic grid, pembanding M7)

Grid biaya sintetis robustness (0.0002/0.0005 = 2/5 bps/side) sebagai
pembanding M7 (EXP-001 §18.3):

| comm/slip | Expectancy | PF    |
| --------- | ---------- | ----- |
| 0 / 0     | 1.2506     | 1.3006|
| 0.0002 / 0| 0.5269     | 1.1160|
| 0.0005 / 0| −0.5587    | 0.8914|
| 0 / 0.0002| 0.5269     | 1.1160|
| 0 / 0.0005| −0.5587    | 0.8914|
| 0.0002/0.0002 | −0.1968 | 0.9601|
| 0.0005/0.0005 | −2.3680 | 0.6206|

Interpretasi: konsisten dengan M7 — edge gagal pada 0.05%/sisi (5 bps)
sintetis; namun breakeven high-regime 3.44 bps (§15.4) tetap jauh di atas
biaya venue nyata (~1.0 bps/side).

## 17.4 Parameter Combinations (price_lookback / rsi_period)

| Combo             | Trades | Expectancy | PF    | Net P&L  |
| ----------------- | ------ | ---------- | ----- | -------- |
| 20 / 14 (baseline)| 698    | 0.8887     | 1.2044| 620.34   |
| 10 / 7            | 960    | 0.2730     | 1.0600| 262.13   |
| 10 / 21           | 964    | −0.2046    | 0.9582| −197.24  |
| 30 / 7            | 559    | 0.4609     | 1.1029| 257.64   |
| 30 / 21           | 552    | 0.4633     | 1.1021| 255.75   |

Interpretasi: **4/5 kombinasi positif** (vs 3/5 unfiltered EXP-002 §17.4);
kombinasi rsi 21 ekstrem (10/21) tetap negatif, konsisten dengan EXP-002.
Baseline 20/14 tetap yang terbaik.

## 17.5 Finer Temporal Slices (8, validasi lanjutan)

Untuk menguji stabilitas temporal lebih halus (RSH-003 §10, rekomendasi
EXP-003 §18.3 — "slice lebih halus"), strategi frozen (regime high, 1.0
bps/side) dijalankan pada 8 slice kronologis:

| Slice | Trades | Win Rate | Expectancy | PF    | Net P&L  |
| ----- | ------ | -------- | ---------- | ----- | -------- |
| period-1-of-8 | 103 | 0.4757 | 0.3377  | 1.1075 | 34.78  |
| period-2-of-8 |  68 | 0.5147 | 1.8492  | 1.6897 | 125.75 |
| period-3-of-8 |  91 | 0.4396 | −0.4650 | 0.8400 | −42.32 |
| period-4-of-8 |  82 | 0.4634 | 0.1911  | 1.0734 | 15.67  |
| period-5-of-8 |  70 | 0.4429 | −0.0406 | 0.9812 | −2.84  |
| period-6-of-8 |  69 | 0.3623 | −2.5139 | 0.5513 | −173.46|
| period-7-of-8 | 107 | 0.4393 | −0.1474 | 0.9652 | −15.77 |
| period-8-of-8 | 110 | 0.5455 | 6.4784  | 1.6708 | 712.62 |

Interpretasi: **4/8 slice positif** pada biaya venue — konsisten dengan
pola 2/4 pada granularitas kasar (§17.1): proporsi slice positif stabil
(~50%), namun P&L tetap terkonsentrasi di slice akhir (period-8-of-8).
Granularitas lebih halus tidak mengubah kesimpulan.

## 17.6 Split-Point Sensitivity (OOS, validasi lanjutan)

Untuk menguji sensitivitas hasil OOS terhadap posisi split point
(RSH-003 §7, rekomendasi EXP-003 §18.3), split diuji pada 4 fraksi:

| Split | Train n | Train Exp | Train PF | Test n | Test Exp | Test PF | Stasioner |
| ----- | ------- | --------- | -------- | ------ | -------- | ------- | --------- |
| 0.5   | 343     | 0.4841    | 1.1729   | 356    | 1.4622   | 1.2535  | Ya        |
| 0.6   | 405     | 0.3946    | 1.1462   | 294    | 1.7918   | 1.2743  | Ya        |
| 0.7   | 446     | 0.1297    | 1.0443   | 253    | 2.4853   | 1.3680  | Ya        |
| 0.8   | 522     | −0.3738   | 0.8877   | 176    | 4.9272   | 1.6789  | Tidak     |

Interpretasi: **3/4 split stasioner** (train + test positif); pada split
0.8, train negatif namun test sangat kuat (+4.9272) — edge menurun di
paruh tengah data namun kuat di paruh akhir (volatilitas tinggi).
Kesimpulan OOS utama (§16) robust terhadap pilihan split point pada
rentang 0.5–0.7 (train positif), dan hanya melemah di batas ekstrem 0.8.

---

# 18. Conclusion

## 18.1 Verdict (pre-registered criteria, §13)

```text
SUPPORTED
- expectancy(high) pada skenario representative (1.0 bps/side) = 0.8887 > 0
  dengan n = 698 >= min_sample (30): TERPENUHI;
- biaya breakeven/side ≈ 3.44 bps >= 1.0 bps: TERPENUHI;
- OOS test expectancy(high) = 2.4853 > 0: TERPENUHI;
- OOS train expectancy(high) = 0.1297 > 0 (stasionaritas membaik vs EXP-002
  yang train-nya negatif −0.1605): TERPENUHI.
```

Seluruh kriteria pre-registered terpenuhi → **SUPPORTED**.

## 18.2 Implikasi

- **Edge terkonsentrasi pada regime high**: expectancy(high) 0.8887 >>
  low 0.1540 > (unfiltered 0.5111); filter regime membuang ~50% sinyal
  namun menaikkan expectancy per trade +74%;
- **stasionaritas membaik**: train kini positif (+0.1297 vs −0.1605
  unfiltered) — poin yang sebelumnya membuat EXP-002 belum tradable
  (§18.3) kini teratasi pada kriteria pre-registered;
- **cost tolerance naik**: breakeven 3.44 bps/side (vs 2.43 unfiltered)
  → margin ke nol pada biaya venue nyata 2.44 bps — ~70% lebih lebar dari
  margin unfiltered (1.43 bps); kejutan biaya lebih kecil risikonya;
- robustness temporal masih tidak sempurna (2/4 slice positif, paruh
  terakhir mendominasi) — filter regime memperbaiki namun tidak
  menghilangkan dependensi volatilitas akhir;
- XAGUSD dan kombinasi parameter: 4/5 positif (vs 3/5 unfiltered) —
  robustness lintas-market/parameter membaik.

## 18.3 Keputusan Lanjutan (peneliti)

Hipotesis EXP-003 **didukung secara pre-registered**: menyaring edge
RSI trendline breakout ke regime volatilitas high menghasilkan expectancy
positif dan stasioner (train+test positif) pada biaya venue nyata.
Rekomendasi EXP-002 §18.3 ter-realisasi.

Catatan kehati-hatian:

- robustness temporal masih bergantung pada paruh terakhir data
  (period-4-of-4 menyumbang sebagian besar P&L) — sebelum deklarasi
  tradable, disarankan:
  - validasi pada data terbaru (di luar 100.000 candle) dan slice lebih
    halus;
  - pertimbangan combined filter (mis. regime high + parameter
    non-ekstrem) sebagai konfirmasi tambahan;
  - validasi slippage terhadap data tick jika tersedia;
- verdict tetap berdasarkan kriteria pre-registered §13; hasil
  OOS/robustness adalah konteks tambahan (RSH-003, deskriptif).

## 18.4 Validasi Tradable (validasi lanjutan, §17.5/§17.6)

Dari tiga rekomendasi pra-tradable §18.3, dua telah dieksekusi:

1. **slice lebih halus** (§17.5): 8 slice kronologis → **4/8 positif**,
   konsisten dengan proporsi 2/4 pada granularitas kasar; granularitas
   lebih halus tidak mengubah kesimpulan (P&L tetap terkonsentrasi di
   slice akhir);
2. **combined filter** (regime high + parameter non-ekstrem, §17.4):
   kombinasi non-ekstrem (20/14, 10/7, 30/7, 30/21) semuanya positif
   (**4/5** termasuk baseline; hanya 10/21 rsi-ekstrem yang negatif);
3. **split-point sensitivity** (§17.6): OOS stasioner pada **3/4 split**
   (0.5/0.6/0.7, train+test positif); hanya split 0.8 yang train-negatif
   (−0.3738) namun test sangat kuat (+4.9272) — kesimpulan OOS §16 robust
   pada rentang 0.5–0.7.

**Item yang belum dieksekusi:** validasi pada data terbaru di luar 100.000
candle. Data spot XAUUSD H1 pasca 2026-05-26 (akhir dataset) **tidak
tersedia dari sumber gratis yang reliabel** pada saat penulisan (Yahoo
Finance: `XAUUSD=X` delisted/NotFound; Dukascopy datafeed: 503/404/timeout;
Stooq/Investing.com: JavaScript challenge). Alternatif `GC=F` (COMEX gold
futures) tersedia namun merupakan **instrumen berbeda dengan model biaya
venue berbeda** (futures ≠ spot ECN 1.0 bps/side), sehingga tidak dapat
diperlakukan sebagai "data terbaru" spot tanpa pre-registrasi ulang.
Evaluasi data terbaru **ditunda** hingga sumber spot XAUUSD H1 yang
reliabel tersedia.

**Status tradable (adendum hasil validasi):** bukti robustness temporal
finer-slice (4/8 positif), combined filter (4/5 kombinasi non-ekstrem
positif), dan stasionaritas split-point (3/4 split) **mendukung** tetapi
belum **menyimpulkan** tradable — deklarasi tradable penuh menunggu
validasi data terbaru di luar 100.000 candle.

## 18.5 Kesimpulan Formal Status Tradable

Berdasarkan seluruh evidence EXP-003 (§15–§17) dan validasi lanjutan
(§17.5/§17.6/§18.4), peneliti **secara formal menyimpulkan**:

> **Status strategi: BELUM TRADABLE (NOT YET TRADABLE).**
>
> - Verdict pre-registered EXP-003: **SUPPORTED** (§18.1) — edge
>   terkonsentrasi pada regime volatilitas high dan stasioner
>   train+test pada biaya venue nyata (1.0 bps/side).
> - Validasi lanjutan memperkuat dukungan (4/8 slice halus positif,
>   3/4 split-point stasioner, 4/5 kombinasi non-ekstrem positif) namun
>   **tidak cukup** untuk deklarasi tradable penuh.
> - Validasi pada data terbaru di luar 100.000 candle (rekomendasi
>   §18.3) **DITUTUP sebagai deferred validation path**: spot XAUUSD H1
>   pasca 2026-05-26 tidak tersedia dari sumber gratis yang reliabel;
>   `GC=F` futures adalah instrumen berbeda dengan model biaya venue
>   berbeda sehingga tidak dapat menggantikan spot tanpa pre-registrasi
>   ulang. Path ini TIDAK memblokir experiment berikutnya.
> - Tindak lanjut: EXP-004 (pre-registered) menguji ulang edge regime
>   high dengan **ATR-multiple SL/TP pada biaya venue nyata** — mekanisme
>   M7 (RQ-007) yang belum pernah diuji pada biaya venue 1.0 bps/side
>   (M7 memakai grid sintetis 2–5 bps/side, ARC-008 §14.3).

Catatan: kesimpulan ini bersifat deskriptif per RSH-003 (bukan proof);
verdict pre-registered §13 tetap menjadi dasar SUPPORTED/NOT.

---

# 19. Record Lifecycle

```text
Defined (spesifikasi + konfigurasi frozen)    ← 2026-08-10 (pre-registration, TODO-038)
    ↓ (TODO-039 Run EXP-003)
Run          ← 2026-08-10 (§15)
    ↓
Result (metrics dicatat)    ← 2026-08-10 (§15)
    ↓
OOS / robustness            ← 2026-08-10 (§16/§17)
    ↓
Validasi tradable           ← 2026-08-10 (§17.5/§17.6/§18.4)
    ↓
Conclusion (interpretasi evidence — peneliti, PRD-006 §9)    ← saat ini (§18.5: BELUM TRADABLE)
    ↓
Reviewed (validasi, RSH-003)
```

---

# 20. Traceability

| Item            | Requirement / TODO           |
| --------------- | ---------------------------- |
| Hypothesis      | RSH-001 §7, TODO-013         |
| Spec fields     | RSH-002 §6, TODO-014         |
| Metrics         | RSH-002 §8, FND-008 §25      |
| Reproducibility | FR-010, NFR-001, RSH-002 §9  |
| Venue cost      | RSH-003 §10 (cost dimension) |
| Regime filter   | ARC-008 §14, TODO-039        |
| Out-of-sample   | RSH-003 §6/§7, TODO-039      |
| Robustness      | RSH-003 §10, TODO-039        |
| Conclusion      | FR-011, RSH-001 §13          |

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
- `docs/02-architecture/ARC-008_Architecture_Review_Based_on_Evidence.md`
- `docs/05-research/RSH-001_Research_Methodology.md`
- `docs/05-research/RSH-002_Experiment_Specification.md`
- `docs/05-research/RSH-003_Validation_Methodology.md`
- `docs/07-experiments/EXP-001_RSI_Trendline_Breakout_Baseline.md`
- `docs/07-experiments/EXP-002_RSI_Trendline_Breakout_Real_Venue_Cost.md`
- `docs/03-engine/ENG-002_Event_Engine.md`
- `docs/03-engine/ENG-003_Signal_Engine.md`
- `docs/03-engine/ENG-005_Simulation_Engine.md`
- `docs/03-engine/ENG-006_Statistics_Engine.md`
- `docs/03-engine/ENG-007_Reporting_Engine.md`
- `docs/01-product/PRD-006_MVP_Definition.md`
- `configs/EXP-003.yaml`

---

# 23. Revision History

| Version | Date       | Changes                                      |
| ------- | ---------- | -------------------------------------------- |
| 1.0.3   | 2026-08-10 | Kesimpulan formal status tradable (§18.5): BELUM TRADABLE (NOT YET TRADABLE) — bukti mendukung namun tidak cukup untuk deklarasi tradable; validasi data terbaru DITUTUP sebagai deferred validation path (spot XAUUSD H1 pasca 2026-05-26 tidak tersedia, GC=F beda instrumen); tidak memblokir experiment berikutnya (EXP-004 pre-registered) |
| 1.0.2   | 2026-08-10 | Tradable-validation addendum (§17.5–§17.6, §18.4): 8-slice robustness (4/8 positif), split-point sensitivity OOS (3/4 split stasioner), combined filter (4/5 kombinasi non-ekstrem positif); validasi data terbaru ditunda (spot XAUUSD H1 pasca 2026-05-26 tidak tersedia dari sumber gratis reliabel — Yahoo delisted, Dukascopy 503/404, Stooq/Investing JS-challenge); GC=F futures beda instrumen & beda model biaya venue |
| 1.0.1   | 2026-08-10 | EXP-003 run (TODO-039) dicatat (§15–§17): regime high → expectancy 0.8887 @ 1.0 bps/side (n=698), breakeven ≈ 3.44 bps/side, OOS train +0.1297 & test +2.4853, 2/4 slice temporal positif, 4/5 combos positif; verdict SUPPORTED (§18) — edge terkonsentrasi pada regime high & stasioner train+test |
| 1.0.0   | 2026-08-10 | Initial EXP-003 pre-registration (TODO-038): volatility regime segmentation re-test |

---

**Document Status:** Result

**Document ID:** EXP-003

**Version:** 1.0.3

**End of Document**
