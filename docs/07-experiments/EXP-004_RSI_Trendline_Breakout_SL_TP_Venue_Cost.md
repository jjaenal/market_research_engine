---
title: RSI Trendline Breakout - ATR-multiple SL/TP at Venue Cost
document_id: EXP-004
version: 1.0.1
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

purpose: Record EXP-004 run (TODO-041) — re-test the high-regime edge with ATR-multiple SL/TP (SL 1.0/TP 4.0) at real venue execution costs (1.0 bps/side), which M7 tested only on the synthetic 2–5 bps/side grid; verdict REJECTED per pre-registered criteria (breakeven 3.31 < 3.44 bps control) but expectancy/drawdown/robustness all improved (EXP-004 §15–§18)
---

# RSI Trendline Breakout - ATR-multiple SL/TP at Venue Cost

> Measure the Market. Discover the Edge.

---

# 1. Purpose

EXP-004 adalah **experiment keempat** MRE (RSH-002 §10 lifecycle - state
sekarang `Result`, run selesai TODO-041). EXP-003 (SUPPORTED) menunjukkan
edge RSI trendline breakout terkonsentrasi pada regime volatilitas high
dan stasioner train+test pada biaya venue nyata (1.0 bps/side), namun
belum cukup bukti untuk deklarasi tradable (EXP-003 §18.4/§18.5).

M7 sudah menguji **risk management SL/TP ATR-multiple** (RQ-007, ARC-008
§14.2/§14.3, EXP-001 §19.7) pada grid biaya **sintetis** 2-5 bps/side dan
menjawab TIDAK: SL/TP menaikkan breakeven cost namun tidak memulihkan
edge pada 0.05%/side. Yang BELUM pernah diuji: SL/TP ATR-multiple pada
**biaya venue nyata (1.0 bps/side)** di mana edge sudah terbukti positif
(EXP-002 0.5111, EXP-003 high 0.8887).

EXP-004 mengisi celah tersebut: re-test SL/TP ATR-multiple pada edge
regime high (konfigurasi EXP-003) dengan biaya venue nyata.

---

# 2. Scope

Scope EXP-004:

- pre-registration hypothesis (RSH-001 §7.2);
- dataset tetap (immutable, Article 13) - identik dengan EXP-001/002/003;
- configuration frozen: **identik dengan EXP-003** (regime high, biaya
  venue 1.0 bps/side), hanya menambah SL/TP ATR-multiple di §9.4;
- SL/TP ATR-multiple sebagai variabel bebas (grid pre-defined, M7 §19.7);
- OOS dan robustness (RSH-003 §6/§7/§10) sebagai kriteria stasionaritas.

Di luar scope EXP-004:

- optimasi parameter (tetap sensitivity-style, bukan objek uji);
- modifikasi strategi/detector/engine (seluruhnya reusable dari M7);
- data terbaru di luar 100.000 candle (deferred path, EXP-003 §18.5 -
  tidak memblokir experiment ini);
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

- EXP-002: edge bertahan pada biaya venue nyata (expectancy 0.5111 @ 1.0
  bps/side) namun tidak stasioner (train negatif, EXP-002 §16/§18.3).
- EXP-003: filter regime high memperbaiki stasionaritas (train +0.1297 &
  test +2.4853) dan menaikkan breakeven ke ~3.44 bps/side; verdict
  SUPPORTED namun belum cukup untuk deklarasi tradable (EXP-003 §18.5).
- M7 RQ-007 (ARC-008 §14.2/§14.3): SL/TP ATR-multiple **menaikkan
  breakeven cost** (all 26 -> 30 bps; high 36 -> 42 bps) dan memperbaiki
  expectancy pada 0.02% (0.34 vs 0.15), tetapi **tidak memulihkan edge
  pada grid sintetis 0.05%/side** - kombinasi terkuat (cooldown 10 +
  regime high + SL 1.0/TP 4.0) tetap negatif (-0.51).

Implikasi: SL/TP adalah **exit rule dini** yang memperbaiki tolerance
biaya. Karena EXP-003 sudah positif pada biaya venue 1.0 bps/side dengan
breakeven 3.44 bps, pertanyaannya bukan "apakah SL/TP memulihkan edge"
(menguji pada grid sintetis) melainkan "apakah SL/TP **memperbaiki**
expectancy dan menaikkan breakeven lebih jauh" pada biaya venue nyata.

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
| Regime high    | ATR short (14) >= ATR long (100) - volatilitas mengembang |
| SL/TP ATR      | Exit rule dini: level dari entry +/- N x ATR bar terakhir yang ditutup (SPEC-004 §4.1) |
| bps/side       | Basis point biaya per sisi (1 bps = 0.01%)            |

---

# 6. Hypothesis

Per RSH-001 §7.1:

> Kondisi **X** (deteksi/Event) menghasilkan
> edge pada **Symbol** (Y) timeframe (**Z**).

Hipotesis EXP-004 (pre-registered):

> **Menambahkan SL/TP ATR-multiple (SL 1.0 / TP 4.0, ATR period 14) pada
> edge RSI trendline breakout regime volatilitas HIGH (EXP-003 SUPPORTED)
> mempertahankan atau memperbaiki expectancy positif DAN menaikkan
> tolerance biaya (breakeven/side) setelah biaya eksekusi venue nyata
> (1.0 bps/side) - berbeda dari M7 (RQ-007 TIDAK) yang diuji pada grid
> sintetis 2-5 bps/side.**

Kriteria (RSH-001 §7.2):

- falsifiable: keputusan ditentukan oleh kriteria terukur (§13);
- terikat dataset dan konfigurasi spesifik (§7, §9);
- dinyatakan sebelum experiment dijalankan (dokumen ini).

Catatan: hipotesis ini **menambahkan exit rule** pada hipotesis EXP-003
(EXP-003 §6). Jika SL/TP memang menaikkan tolerance biaya (temuan M7
§14.3), maka pada biaya venue 1.0 bps/side (jauh di bawah breakeven
kontrol 3.44 bps) SL/TP seharusnya tidak menurunkan expectancy dan bisa
menaikkan breakeven lebih jauh - memperkuat kandidat tradable.

---

# 7. Dataset

| Field          | Value                                      |
| -------------- | ------------------------------------------ |
| File           | `datasets/XAUUSD_H1.csv`                   |
| Symbol         | XAUUSD                                     |
| Timeframe      | H1                                         |
| Source         | CSV (kolom: timestamp, open, high, low, close, volume) |
| Date Range     | 2009-09-11 18:00 -> 2026-05-26 23:00       |
| Candle Count   | 100.000                                    |
| Integrity      | valid (validasi inti PRD-006 §8.2)         |

Dataset bersifat **immutable** (Article 13, ARC-004) dan identik dengan
EXP-001/EXP-002/EXP-003 §7 (kontrol).

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
| Provenance                | CSV lokal; immutable (Article 13); identik EXP-001..003 §7 |

Aturan tertera konsisten dengan ARC-004 §7/§8 dan `validator.py`.

---

# 8. Strategy - RSI Trendline Breakout

Strategi **identik** dengan EXP-001 §8 / EXP-002 §8 / EXP-003 §8 (plugin
`rsi_trendline_breakout`, LONG-only, deteksi melalui pipeline yang sama).
Tidak ada perubahan pada detector, signal definition, atau engine.

---

# 9. Configuration (Frozen)

Konfigurasi dikunci (frozen) sebelum run (RSH-002 §9). Seluruh parameter
**menyamai EXP-003 §9** (termasuk biaya venue dan regime filter)
**kecuali** §9.4 yang menambahkan SL/TP ATR-multiple.

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
| stop_loss_atr   | 1.0   |
| take_profit_atr | 4.0   |
| atr_period      | 14    |

SL/TP ATR-multiple di-resolve pada entry dari ATR `entry_bar − 1` (bar
terakhir yang telah ditutup — E-2, SPEC-004 §4.1; period 14) dengan
no lookahead (`_resolve_stop_take()` di `simulation_engine.py`, RQ-007
machinery, ARC-008 §14.2). SL 1.0 / TP 4.0 adalah kombinasi terkuat M7
(EXP-001 §19.7, ARC-008 §14.3).

## 9.5 Venue Cost Model (frozen, identik EXP-003 §9.5)

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
berlabel regime `high` (identik EXP-003 §9.7).

---

# 10. Execution Assumptions

Per RSH-001 §14 (semantik terinci di SPEC-003/SPEC-004, E-9/E-10):

- **Entry**: open bar berikutnya setelah Signal **knowable**
  (`max(signal_bar + 1, max(confirmable_ref) + 1)` — seluruh constituent
  Event sudah dapat diketahui; E-1);
- **Exit**: SL diresolusi **lebih dulu** dari TP dalam bar yang sama
  (konservatif); jika tidak ada SL/TP tersentuh, exit setelah `hold_bars`
  (10) bar di **close** bar scheduled;
- **Sizing**: `position_size = 1.0` (fixed);
- **Transaction cost**: model venue §9.5 (identik EXP-003);
- **Slippage**: `slippage_rate` pada entry dan exit (conservative);
- **Regime label**: candle pada timestamp konfirmasi sinyal (no lookahead);
- **SL/TP level**: dari ATR di `entry_bar − 1` (bar terakhir yang telah
  ditutup — E-2, SPEC-004 §4.1); gap-through-open → exit di open;
  SL/TP eligible sejak entry bar (SPEC-004 §4.5);
- Eksekusi adalah simulasi, bukan live (PRD-006 §9).

Catatan E-9: revisi §10 ini merekonsiliasi dokumentasi dengan kode
(`simulation_engine.py`, SPEC-004). Angka §15–§18 dihasilkan oleh kode
yang sama; kalimat lama ("mana yang tersentuh lebih dulu", "ATR di entry
bar") adalah deskripsi yang keliru dan **tidak** mengubah hasil yang
dicatat.

---

# 11. Variables

## 11.1 Control Variables

- dataset (XAUUSD H1, rentang penuh);
- strategy/indicator/event/signal config (§9.1-§9.3);
- biaya venue 1.0 bps/side (§9.5);
- regime filter high (§9.7);
- hold_bars, sizing, min_sample.

## 11.2 Independent Variables

SL/TP ATR-multiple (grid pre-defined, konsisten M7 §19.7):

| Skenario        | stop_loss_atr | take_profit_atr | Catatan                           |
| --------------- | ------------- | --------------- | --------------------------------- |
| None (kontrol)  | -             | -               | = EXP-003 (0.8887 @ 1.0 bps/side) |
| SL 1.0          | 1.0           | -               | SL saja                          |
| SL 1.0 / TP 4.0 | 1.0           | 4.0             | primary (config frozen §9.4)      |
| SL 2.0 / TP 4.0 | 2.0           | 4.0             | SL lebih lebar                    |

## 11.3 Dependent Variables

- metrik minimum (RSH-002 §8);
- OOS train/test expectancy (stasionaritas, §12/§16);
- robustness temporal slices (RSH-003 §10);
- breakeven cost per skenario;
- equity curve;
- trade log.

---

# 12. Baseline Reference

Per RSH-001 §9:

- **No Trade** - reference tanpa aktivitas (equity 0);
- **EXP-003 representative** (regime high, no SL/TP, 1.0 bps/side ->
  expectancy 0.8887, n=698, breakeven ~3.44 bps/side, EXP-003 §15) sebagai
  kontrol: SL/TP dikatakan menambah nilai jika expectancy(SL/TP) >= 0
  DAN breakeven(SL/TP) >= 3.44 bps/side.

---

# 13. Decision Criteria (pre-registered)

```text
SUPPORTED
Jika pada skenario representative (1.0 bps/side, selected_regime="high",
SL 1.0 / TP 4.0 ATR-multiple):
  - expectancy(SL/TP) > 0 dengan n >= min_sample (30);
  - biaya breakeven/side >= 3.44 bps (breakeven kontrol EXP-003) - SL/TP
    tidak menurunkan tolerance biaya;
  - OOS test expectancy(SL/TP) > 0 (edge bertahan out-of-sample);
  - OOS train expectancy(SL/TP) > 0 (stasionaritas, seperti EXP-003).

REJECTED
Jika salah satu kriteria SUPPORTED tidak terpenuhi.
```

Interpretasi tambahan (bukan keputusan, untuk konteks):

- perbandingan SL/TP grid (§11.2) menunjukkan sensitivitas terhadap
  lebar SL/TP;
- jika SUPPORTED dan breakeven(SL/TP) > 3.44 bps, SL/TP **menambah**
  tolerance biaya pada edge high regime (temuan M7 §14.3 terkonfirmasi
  pada biaya venue nyata) - memperkuat kandidat tradable;
- jika REJECTED, SL/TP tidak memperbaiki edge high regime pada biaya
  venue nyata (kontrol EXP-003 tetap lebih baik).

Catatan multiple-testing (RSH-004 §8.2, E-8):

```text
- jumlah kriteria keputusan:            4 (expectancy > 0, breakeven >= 3.44 bps,
                                         OOS test > 0, OOS train > 0);
- jumlah kombinasi parameter (combo):   5 (price_lookback × rsi_period — EXP-001 legacy grid);
- jumlah slice temporal / split point:  4 slice (+ 8 fine slice, 4 split point);
- jumlah dimensi robustness:            4 (periods, markets, costs, combos);
- koreksi / penalty:                    none — risiko data-snooping dinyatakan eksplisit.
```

Note: EXP-004 dijalankan sebelum standar E-8; blok ini dokumentasi
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

Dihitung per skenario SL/TP (§11.2) plus OOS dan robustness (RSH-003).

---

# 15. Run (TODO-041)

Report: `experiments/EXP-004/EXP-004_report.md` (Code Version `0afabbc`).
Strategi frozen (konfigurasi EXP-004, regime high, biaya venue 1.0 bps/side,
SL 1.0 / TP 4.0 ATR-multiple) dijalankan tanpa modifikasi.

## 15.1 Representative Scenario (1.0 bps/side, regime high, SL 1.0/TP 4.0)

| Metric        | Value |
| ------------- | ----- |
| Trade Count   | 698   |
| Win Rate      | 0.3696 |
| Loss Rate     | 0.6304 |
| Average Win   | 12.2766 |
| Average Loss  | 5.3498 |
| Risk/Reward   | 2.2948 |
| Expectancy    | 1.1654 |
| Profit Factor | 1.3456 |
| Gross Profit  | 3167.36 |
| Gross Loss    | 2353.93 |
| Net P&L       | 813.43 |
| Max Drawdown  | 201.82 |
| Winning Streak| 10    |
| Losing Streak | 13    |

Perbandingan vs kontrol EXP-003 (regime high, tanpa SL/TP, EXP-003 §15.1):

| Metric      | EXP-003 kontrol | EXP-004 (SL 1.0/TP 4.0) | Δ       |
| ----------- | --------------- | ----------------------- | ------- |
| Expectancy  | 0.8887          | 1.1654                  | +31.1%  |
| Profit Factor | 1.2044        | 1.3456                  | +11.7%  |
| Net P&L     | 620.34          | 813.43                  | +31.1%  |
| Max Drawdown| 516.25          | 201.82                  | −60.9%  |
| Win Rate    | 0.4613          | 0.3696                  | −19.9%  |

Interpretasi: SL/TP ATR-multiple **memperbaiki expectancy, PF, net P&L, dan
menurunkan Max Drawdown secara drastis** (−61%), namun menurunkan win rate
(TP membatasi winner). Expectancy tetap positif dengan n = 698 ≥ 30.

## 15.2 SL/TP Grid (1.0 bps/side, regime high, variabel bebas §11.2)

| Skenario        | Trades | Win Rate | Expectancy | PF     | Net P&L  | Max DD  |
| --------------- | ------ | -------- | ---------- | ------ | -------- | ------- |
| None (kontrol)  | 698    | 0.4613   | 0.8887     | 1.2044 | 620.34   | 516.25  |
| SL 1.0          | 698    | 0.3639   | 1.0186     | 1.2994 | 711.01   | 306.38  |
| SL 1.0 / TP 4.0 | 698    | 0.3696   | 1.1654     | 1.3456 | 813.43   | 201.82  |
| SL 2.0 / TP 4.0 | 698    | 0.4484   | 1.1653     | 1.2867 | 813.36   | 388.10  |

Interpretasi: **4/4 skenario positif** pada biaya venue; SL 1.0/TP 4.0
terbaik (expectancy tertinggi + Max DD terendah). SL/TP memperbaiki
expectancy pada semua varian vs kontrol (0.8887 → ≥ 1.0186).

## 15.3 Venue-Derived Cost Grid (regime high, SL 1.0/TP 4.0)

| Scenario     | comm      | slip       | Total bps/side | Expectancy | PF     | Net P&L   |
| ------------ | --------- | ---------- | -------------- | ---------- | ------ | --------- |
| Zero cost    | 0         | 0          | 0              | 1.4852     | 1.4655 | 1036.67   |
| ECN tight    | 0.00002   | 0.00003    | 0.5            | 1.3080     | 1.3967 | 912.95    |
| ECN rep.     | 0.00003   | 0.00007    | 1.0            | 1.1654     | 1.3456 | 813.43    |
| ECN wide     | 0.00005   | 0.00010    | 1.5            | 0.9617     | 1.2768 | 671.25    |
| Conservative | 0.00007   | 0.00013    | 2.0            | 0.5656     | 1.1526 | 394.75    |

Grid seluruhnya positif 0–2.0 bps/side; pada setiap titik grid expectancy
SL/TP **lebih tinggi** dari kontrol EXP-003 §15.3.

## 15.4 Breakeven Cost (regime high, SL 1.0/TP 4.0)

Breakeven (titik expectancy menyeberang nol), grid halus:

- 3.28 bps/side → +0.0401 (PF 1.0100);
- 3.30 bps/side → +0.0341 (PF 1.0085);
- 3.31 bps/side → −0.0303 (PF 0.9925);
- **breakeven ≈ 3.31 bps/side** (vs 3.44 bps/side kontrol EXP-003 §15.4).

Margin ke nol pada biaya venue nyata: 1.0 bps/side → margin **2.31 bps**
(breakeven − biaya) — sedikit **lebih tipis** dari kontrol (2.44 bps).

Catatan penting: SL/TP memperbaiki expectancy pada biaya venue dan
menurunkan Max DD secara drastis, namun breakeven sedikit **LEBIH RENDAH**
dari kontrol (3.31 vs 3.44 bps) — SL/TP **tidak menaikkan** tolerance
biaya pada margin. Ini berbeda dari klaim M7 (ARC-008 §14.3 "breakeven naik
~4–6 bps") yang diukur pada grid sintetis.

---

# 16. Out-of-Sample Testing (TODO-041)

Metodologi per **RSH-003 §6/§7**: split kronologis (no leakage, no
retroactive allocation); strategi frozen (konfigurasi EXP-004, regime high,
SL/TP) dijalankan tanpa perubahan pada kedua segmen — biaya tetap 1.0
bps/side. Reuse `run_on_slice` (ARC-ACT-013).

Report: `experiments/EXP-004/EXP-004_oos.md` (Code Version `0afabbc`).

Split point: index 70.000 (2021-04-29 18:00 UTC) — 70% train, 30% test
(identik EXP-002 §16 / EXP-003 §16).

| Metric        | Baseline | Train  | Test   | Δ Test/Train |
| ------------- | -------- | ------ | ------ | ------------ |
| Trade Count   | 698      | 446    | 253    | -            |
| Win Rate      | 0.3696   | 0.3700 | 0.3755 | -            |
| Expectancy    | 1.1654   | 0.2026 | 2.9515 | +1356.6%     |
| Profit Factor | 1.3456   | 1.0846 | 1.5901 | +46.6%       |
| Net P&L       | 813.43   | 90.37  | 746.72 | +726.3%      |
| Max DD        | 201.82   | 95.84  | 201.81 | -            |
| Sufficient    | True     | True   | True   | -            |

Interpretasi:

- **train positif** (+0.2026) dan **test positif** (+2.9515) — stasioner,
  memenuhi kriteria SUPPORTED §13 (OOS test & train > 0);
- dibanding EXP-003: train membaik (+0.1297 → +0.2026) dan test membaik
  (+2.4853 → +2.9515);
- edge masih lebih kuat di paruh akhir (test >> train), konsisten dengan
  EXP-002/EXP-003.

---

# 17. Robustness (TODO-041)

Metodologi per **RSH-003 §10**: strategi frozen (konfigurasi EXP-004,
regime high, SL 1.0/TP 4.0, 1.0 bps/side) dijalankan tanpa perubahan.
Descriptive only; thresholds per RSH-004.

Report: `experiments/EXP-004/EXP-004_robustness.md` (Code Version `0afabbc`).

## 17.1 Time Period Stability (4 slices)

| Slice          | Trades | Win Rate | Expectancy | PF     | Net P&L  | Max DD  |
| -------------- | ------ | -------- | ---------- | ------ | -------- | ------- |
| period-1-of-4  | 172    | 0.4128   | 0.7276     | 1.2943 | 125.14   | 48.25   |
| period-2-of-4  | 173    | 0.3526   | 0.0773     | 1.0356 | 13.37    | 51.50   |
| period-3-of-4  | 139    | 0.3381   | −0.3034    | 0.8896 | −42.17   | 107.81  |
| period-4-of-4  | 217    | 0.3733   | 3.3717     | 1.6307 | 731.66   | 201.81  |

Interpretasi: **3/4 slice positif** (vs 2/4 kontrol EXP-003 §17.1) —
robustness temporal membaik; P&L tetap terkonsentrasi di slice akhir.

## 17.2 Finer Temporal Slices (8, validasi lanjutan)

| Slice          | Trades | Win Rate | Expectancy | PF     | Net P&L  | Max DD  |
| -------------- | ------ | -------- | ---------- | ------ | -------- | ------- |
| period-1-of-8  | 103    | 0.3883   | 0.3631     | 1.1523 | 37.40    | 48.25   |
| period-2-of-8  |  68    | 0.4412   | 1.1600     | 1.4393 | 78.88    | 48.09   |
| period-3-of-8  |  91    | 0.3846   | −0.2141    | 0.9013 | −19.48   | 48.25   |
| period-4-of-8  |  82    | 0.3171   | 0.4006     | 1.1848 | 32.85    | 49.41   |
| period-5-of-8  |  70    | 0.3714   | 0.2939     | 1.1630 | 20.57    | 62.12   |
| period-6-of-8  |  69    | 0.3043   | −0.9093    | 0.7546 | −62.74   | 107.81  |
| period-7-of-8  | 107    | 0.3271   | 0.0970     | 1.0282 | 10.38    | 117.72  |
| period-8-of-8  | 110    | 0.4182   | 6.5571     | 1.9115 | 721.28   | 201.81  |

Interpretasi: **6/8 slice positif** (vs 4/8 kontrol EXP-003 §17.5) —
SL/TP memperbaiki proporsi slice temporal positif; P&L tetap terkonsentrasi
di period-8-of-8.

## 17.3 Cross-Market (XAGUSD, same timeframe)

| Market | Trades | Win Rate | Expectancy | PF     | Net P&L | Max DD |
| ------ | ------ | -------- | ---------- | ------ | ------- | ------ |
| XAGUSD | 533    | 0.3659   | 0.0417     | 1.4300 | 22.25   | 8.02   |

Interpretasi: edge positif tipis ter-reproduksi di XAGUSD (expectancy
0.0417, PF 1.4300) — konsisten dengan EXP-002 (0.0342) / EXP-003 (0.0409).

## 17.4 Execution Cost (synthetic grid, pembanding M7)

| comm/slip     | Expectancy | PF    |
| ------------- | ---------- | ----- |
| 0 / 0         | 1.4852     | 1.4655|
| 0.0002 / 0    | 0.7614     | 1.2095|
| 0.0005 / 0    | −0.3242    | 0.9249|
| 0 / 0.0002    | 0.5523     | 1.1497|
| 0 / 0.0005    | −0.8352    | 0.8081|
| 0.0002/0.0002 | −0.1715    | 0.9587|
| 0.0005/0.0005 | −2.6444    | 0.5301|

Interpretasi: konsisten dengan M7 — edge gagal pada 0.05%/sisi (5 bps)
sintetis; namun pada biaya venue nyata (1.0 bps/side) expectancy tetap
positif dengan margin 2.31 bps.

## 17.5 Parameter Combinations (price_lookback / rsi_period)

| Combo             | Trades | Expectancy | PF    | Net P&L  |
| ----------------- | ------ | ---------- | ----- | -------- |
| 20 / 14 (baseline)| 698    | 1.1654     | 1.3456| 813.43   |
| 10 / 7            | 960    | 0.0752     | 1.0191| 72.15    |
| 10 / 21           | 964    | 0.0213     | 1.0053| 20.55    |
| 30 / 7            | 559    | 0.9079     | 1.2673| 507.53   |
| 30 / 21           | 552    | 1.4564     | 1.4488| 803.92   |

Interpretasi: **5/5 kombinasi positif** (vs 4/5 kontrol EXP-003 §17.4) —
SL/TP memperbaiki robustness parameter; kombinasi 10/21 (yang negatif pada
EXP-002/EXP-003) kini positif tipis.

## 17.6 Split-Point Sensitivity (OOS, validasi lanjutan)

| Split | Train n | Train Exp | Train PF | Test n | Test Exp | Test PF | Stasioner |
| ----- | ------- | --------- | -------- | ------ | -------- | ------- | --------- |
| 0.5   | 343     | 0.4303    | 1.1866   | 356    | 1.9368   | 1.4472  | Ya        |
| 0.6   | 405     | 0.3648    | 1.1637   | 294    | 2.3447   | 1.4819  | Ya        |
| 0.7   | 446     | 0.2026    | 1.0846   | 253    | 2.9515   | 1.5901  | Ya        |
| 0.8   | 522     | 0.0415    | 1.0162   | 176    | 4.5506   | 1.8037  | Ya        |

Interpretasi: **4/4 split stasioner** (train+test positif) — membaik vs
kontrol EXP-003 §17.6 (3/4; split 0.8 train negatif). SL/TP memperbaiki
stasionaritas split-point.

---

# 18. Conclusion

## 18.1 Verdict (pre-registered criteria, §13)

```text
REJECTED
- expectancy(SL/TP) pada skenario representative (1.0 bps/side) = 1.1654 > 0
  dengan n = 698 >= min_sample (30): TERPENUHI;
- biaya breakeven/side ≈ 3.31 bps >= 3.44 bps (kontrol EXP-003): TIDAK
  TERPENUHI (SL/TP menurunkan breakeven sedikit, 3.44 -> 3.31 bps);
- OOS test expectancy(SL/TP) = 2.9515 > 0: TERPENUHI;
- OOS train expectancy(SL/TP) = 0.2026 > 0 (stasioner): TERPENUHI.
```

**3/4 kriteria pre-registered terpenuhi; kriteria breakeven (>= 3.44 bps)
tidak terpenuhi → verdict pre-registered REJECTED** (hipotesis "SL/TP
menaikkan tolerance biaya" tidak didukung pada margin).

## 18.2 Implikasi

- **SL/TP sangat memperbaiki profil risiko**: expectancy naik +31% (0.8887
  → 1.1654), PF naik, net P&L naik, dan Max Drawdown turun −61% (516 → 202);
- **namun tolerance biaya sedikit menurun**: breakeven 3.31 vs 3.44 bps
  kontrol — SL/TP memperbaiki edge pada biaya venue namun tidak menaikkan
  titik impas pada margin (berbeda dari klaim M7 yang diukur pada grid
  sintetis);
- **stasionaritas & robustness membaik**: OOS train+test positif (meningkat
  vs EXP-003), 3/4 slice (vs 2/4), 6/8 fine slice (vs 4/8), 5/5 combos (vs
  4/5), 4/4 split-point stasioner (vs 3/4);
- **verdict**: hipotesis spesifik EXP-004 (SL/TP menaikkan tolerance biaya)
  **REJECTED**, namun SL/TP terbukti memperbaiki expectancy, drawdown, dan
  robustness pada biaya venue nyata — nilai sebagai exit rule, bukan sebagai
  penambah cost tolerance.

## 18.3 Keputusan Lanjutan (peneliti)

SL/TP ATR-multiple **tidak** memenuhi kriteria breakeven pre-registered
(3.31 < 3.44 bps) sehingga hipotesis EXP-004 ditolak pada kriteria tersebut,
meskipun memperbaiki hampir semua metrik lain. Catatan kehati-hatian:

- verdict berdasarkan kriteria pre-registered §13; hasil OOS/robustness
  adalah konteks tambahan (RSH-003, deskriptif);
- M7 mencatat breakeven SL/TP "naik 4–6 bps" (ARC-008 §14.3) — tidak
  ter-reproduksi pada grid venue halus; perlu verifikasi basis perhitungan
  M7 sebelum dipakai sebagai referensi lanjutan;
- data terbaru di luar 100.000 candle tetap deferred path (EXP-003 §18.5);
- arah selanjutnya (kandidat): validasi SL/TP lain (SL lebih sempit, TP
  bervariasi), atau deklinasi strategi ini dan beralih ke strategi lain
  (EXP-001 §19.8, ARC-008 §14.4).

---

# 19. Record Lifecycle

```text
Defined (spesifikasi + konfigurasi frozen)    ← 2026-08-10 (pre-registration, TODO-040)
    ↓ (TODO-041 Run EXP-004)
Run          ← 2026-08-10 (§15)
    ↓
Result (metrics dicatat)    ← 2026-08-10 (§15)
    ↓
OOS / robustness            ← 2026-08-10 (§16/§17)
    ↓
Conclusion (interpretasi evidence — peneliti, PRD-006 §9)    ← saat ini (§18)
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
| SL/TP           | ARC-008 §14.2, RQ-007        |
| Regime filter   | ARC-008 §14, EXP-003 §9.7    |
| Out-of-sample   | RSH-003 §6/§7, TODO-041      |
| Robustness      | RSH-003 §10, TODO-041        |
| Conclusion      | FR-011, RSH-001 §13          |

---

# 21. Compliance

| Document / Rule          | Experiment requirement             |
| ------------------------ | ---------------------------------- |
| FND-003                  | ID immutable, sekuensial           |
| FND-005 §37              | Research Evidence priority         |
| FND-009                  | Backtest =/= Proof                 |
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
- `docs/07-experiments/EXP-003_RSI_Trendline_Breakout_Volatility_Regime.md`
- `docs/03-engine/ENG-002_Event_Engine.md`
- `docs/03-engine/ENG-003_Signal_Engine.md`
- `docs/03-engine/ENG-005_Simulation_Engine.md`
- `docs/03-engine/ENG-006_Statistics_Engine.md`
- `docs/03-engine/ENG-007_Reporting_Engine.md`
- `docs/01-product/PRD-006_MVP_Definition.md`
- `configs/EXP-004.yaml`

---

# 23. Revision History

| Version | Date       | Changes                                      |
| ------- | ---------- | -------------------------------------------- |
| 1.0.1   | 2026-08-10 | EXP-004 run (TODO-041) dicatat (§15–§17): SL 1.0/TP 4.0 @ 1.0 bps/side → expectancy 1.1654 (n=698), breakeven ≈ 3.31 bps/side, OOS train +0.2026 & test +2.9515, 3/4 slice positif, 6/8 fine slice, 5/5 combos, 4/4 split-point stasioner; verdict REJECTED (§18) — breakeven < 3.44 bps kontrol, meski expectancy/drawdown/robustness membaik |
| 1.0.0   | 2026-08-10 | Initial EXP-004 pre-registration (TODO-040): ATR-multiple SL/TP re-test at real venue costs (1.0 bps/side) on the EXP-003 high-regime edge; config frozen identik EXP-003 + SL 1.0 / TP 4.0 |

---

**Document Status:** Result

**Document ID:** EXP-004

**Version:** 1.0.1

**End of Document**
