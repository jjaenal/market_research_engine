---
title: Price Breakout (Donchian-style) — Baseline
document_id: EXP-005
version: 1.0.1
status: Result
category: Experiment
owner: Market Research Engine Core Team
created: 2026-08-10
last_updated: 2026-08-11

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

purpose: Record EXP-005 run (TODO-043) — Price Breakout (Donchian-style) baseline, first experiment of a NEW strategy line after the RSI Trendline Breakout research line (EXP-001..EXP-004) was formally closed; verdict REJECTED per pre-registered criteria — expectancy -3.4848 @ 1.0 bps/side (n=3882) and even negative at ZERO cost (-3.1186), breakeven < 0 bps, OOS train -2.6301 & test -5.2396 (EXP-005 §15–§18)
---

# Price Breakout (Donchian-style) — Baseline

> Measure the Market. Discover the Edge.

---

# 1. Purpose

EXP-005 adalah **experiment kelima** MRE (RSH-002 §10 lifecycle — state
sekarang `Result`, run selesai TODO-043). Line research RSI Trendline Breakout
(EXP-001..EXP-004) telah **ditutup secara formal** sebagai research outcome
sukses namun negatif: edge tidak menunjukkan profil tradable yang cukup pada
biaya eksekusi venue realistis (EXP-001 §19.8, ARC-008 §14.4, EXP-004 §18.3 —
verdict terakhir REJECTED per kriteria pre-registered EXP-004 §13).

EXP-005 membuka line strategi baru yang **berbeda secara fundamental**:
**Price Breakout (Donchian-style)** — strategi momentum murni yang menembus
harga tertinggi N-bar (Donchian upper channel) dikonfirmasi fractal
swing-high, **tanpa input RSI** (berbeda dari line yang ditutup yang berbasis
oscillator RSI).

Pilihan strategi: momentum/breakout adalah kelas strategi yang arsitekturnya
sudah didukung penuh (detector `PRICE_CONFIRMATION` dan `SWING_HIGH` sudah ada
sejak M7, ARC-008 §14) sehingga **tidak ada perubahan arsitektur** — cukup
registrasi plugin baru (ARC-ACT-010). Ini mengikuti keputusan peneliti untuk
meninggalkan parameter mining pada RSI Trendline Breakout (EXP-004 §18.3).

---

# 2. Scope

Scope EXP-005:

- pre-registration hypothesis (RSH-001 §7.2);
- dataset tetap (immutable, Article 13) — identik dengan EXP-001..004;
- configuration frozen: **identik dengan EXP-002** (venue cost 1.0 bps/side,
  tanpa regime filter, tanpa SL/TP) — baseline murni strategi baru;
- strategi **Price Breakout (Donchian-style)** sebagai objek uji (§8);
- OOS dan robustness (RSH-003 §6/§7/§10) sebagai kriteria stasionaritas.

Di luar scope EXP-005:

- optimasi parameter (sensitivity/robustness, bukan objek uji baseline);
- regime filter, SL/TP, cooldown (mitigasi line lama — evaluasi lanjutan
  hanya jika baseline SUPPORTED);
- modifikasi strategi/detector/engine (seluruhnya reusable dari M7);
- data terbaru di luar 100.000 candle (deferred path, EXP-003 §18.5 —
  tidak memblokir experiment ini);
- market lain (XAGUSD robustness cross-market, RSH-003 §10).

---

# 3. Audience

- tim MRE;
- peneliti;
- quant analyst;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Per FND-005 §37, Research Evidence adalah sumber prioritas keputusan.

- EXP-001 baseline (M5): edge RSI trendline breakout positif pada zero cost
  namun gagal pada ≥ 0.05%/side — hipotesis REJECTED sebagai strategi
  tradable pada biaya realistis (EXP-001 §19.8).
- M7 (ARC-008 §14): seluruh mitigasi (dedup, regime, SL/TP) TIDAK memulihkan
  edge pada grid sintetis — **CORE HOLDS, PERIPHERY DRIFTS**; kesimpulan:
  yang diuji adalah strategi, bukan arsitektur.
- EXP-002 (venue cost 1.0 bps/side): SUPPORTED namun tidak stasioner
  (train negatif, 1/4 slice positif).
- EXP-003 (regime high): SUPPORTED, stasioner, breakeven ≈ 3.44 bps — namun
  BELUM TRADABLE (EXP-003 §18.5).
- EXP-004 (SL/TP ATR-multiple): REJECTED pada kriteria breakeven (3.31 < 3.44
  bps) — SL/TP tidak menaikkan tolerance biaya, meski memperbaiki profil
  risiko/robustness. Keputusan peneliti (EXP-004 §18.3): **tutup line RSI
  Trendline Breakout, pre-register strategi baru** (bukan lanjut parameter
  mining).

Implikasi: empat experiment pada line yang sama menghasilkan bukti yang
mendukung edge pada biaya rendah namun **tidak menyimpulkan tradable** pada
biaya venue nyata. Alih-alih mengorek parameter lebih jauh pada strategi yang
sama, EXP-005 menguji apakah **kelas momentum murni** (tanpa oscillator)
menghasilkan profil yang berbeda pada biaya venue yang sama.

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
| Donchian channel | Highest high / lowest low dari N candle terakhir (lookback) |
| PRICE_CONFIRMATION | Event: close > highest high N-bar sebelumnya (ENG-002 §7.3) |
| SWING_HIGH     | Event: fractal swing high (ADR-003, ENG-002 §7.1)    |
| bps/side       | Basis point biaya per sisi (1 bps = 0.01%)            |

---

# 6. Hypothesis

Per RSH-001 §7.1:

> Kondisi **X** (deteksi/Event) menghasilkan
> edge pada **Symbol** (Y) timeframe (**Z**).

Hipotesis EXP-005 (pre-registered):

> **Breakout harga Donchian-style (close menembus highest high N-bar,
> dikonfirmasi swing-high fractal) pada XAUUSD H1 menghasilkan expectancy
> positif setelah biaya eksekusi venue nyata (1.0 bps/side) — strategi
> momentum murni yang berbeda dari line RSI Trendline Breakout yang ditutup.**

Kriteria (RSH-001 §7.2):

- falsifiable: keputusan ditentukan oleh kriteria terukur (§13);
- terikat dataset dan konfigurasi spesifik (§7, §9);
- dinyatakan sebelum experiment dijalankan (dokumen ini).

Catatan: hipotesis ini **independen** dari line lama — tidak mengasumsikan
apapun tentang RSI trendline. Jika SUPPORTED, momentum murni adalah arah
riset yang layak dilanjutkan (regime/SL/TP filter sebagai langkah berikut).
Jika REJECTED, bukti kumulatif menolak kelas momentum breakout ini juga pada
biaya venue — memperkuat kesimpulan umum bahwa edge pada XAUUSD H1 tidak
bertahan pada biaya realistis.

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
EXP-001..004 §7 (kontrol).

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
| Provenance                | CSV lokal; immutable (Article 13); identik EXP-001..004 §7 |

Aturan tertera konsisten dengan ARC-004 §7/§8 dan `validator.py`.

---

# 8. Strategy — Price Breakout (Donchian-style)

Strategi baru yang terdaftar sebagai plugin `price_breakout`
(`src/mre/strategies/exp005.py`, ARC-ACT-010). Tidak ada perubahan pada
detector, signal definition, atau engine — hanya konsumsi Event yang sudah
ada:

```text
TRIGGER:       PRICE_CONFIRMATION   (close > highest high N-bar — Donchian
                                     upper channel break, ENG-002 §7.3)
CONFIRMATION:  SWING_HIGH           (fractal swing high setelah breakout,
                                     ADR-003)
SIGNAL:        LONG
```

Semantik: sinyal LONG muncul ketika harga menembus highest high dari `lookback`
candle terakhir dan, dalam `window` (5) candle setelahnya, sebuah fractal
swing-high terkonfirmasi — momentum breakout ditegaskan oleh struktur harga,
bukan oleh oscillator. Tidak ada `trigger_payload` (tidak ada filter arah
tambahan; PRICE_CONFIRMATION sudah selektif arah atas).

Catatan arsitektur: EventEngine tetap menghitung indikator RSI (kontrak
`compute_report` saat ini) namun strategi `price_breakout` **tidak mengkonsumsi**
Event berbasis RSI — RSI hanya dibutuhkan pipeline, bukan signal definition.

---

# 9. Configuration (Frozen)

Konfigurasi dikunci (frozen) sebelum run (RSH-002 §9). Seluruh parameter
**menyamai EXP-002 §9** (venue cost 1.0 bps/side, tanpa regime filter, tanpa
SL/TP) — baseline murni strategi baru.

## 9.1 Indicators

| Parameter     | Value |
| ------------- | ----- |
| rsi_period    | 14    |

(RSI dihitung pipeline namun tidak dikonsumsi strategi; lihat §8.)

## 9.2 Event Engine (ENG-002)

| Parameter      | Value |
| -------------- | ----- |
| swing_left     | 2     |
| swing_right    | 2     |
| price_lookback | 20    |

`price_lookback = 20` = N-bar Donchian channel (highest high window).

## 9.3 Signal Definition (ENG-003)

| Field           | Value                 |
| --------------- | --------------------- |
| signal_type     | LONG                  |
| trigger         | PRICE_CONFIRMATION    |
| trigger_payload | (none)                |
| confirmations   | (SWING_HIGH)          |
| window          | 5                     |
| source_strategy | price_breakout        |
| cooldown        | 0                     |

## 9.4 Execution (ENG-005)

| Parameter       | Value |
| --------------- | ----- |
| position_size   | 1.0   |
| commission_rate | 0.00003 |
| slippage_rate   | 0.00007 |
| hold_bars       | 10    |
| stop_loss       | None  |
| take_profit     | None  |
| stop_loss_atr   | None  |
| take_profit_atr | None  |
| atr_period      | 14    |

## 9.5 Venue Cost Model (frozen, identik EXP-002 §9.5)

- `commission_rate = 0.00003` (0.3 bps/side);
- `slippage_rate = 0.00007` (0.7 bps/side);
- total **1.0 bps/side** (representative retail ECN XAUUSD).

## 9.6 Statistics (ENG-006)

| Parameter  | Value |
| ---------- | ----- |
| min_sample | 30    |

## 9.7 Volatility Regime Filter (ARC-008 §14, M7 machinery)

| Parameter         | Value |
| ----------------- | ----- |
| atr_short_period  | 14    |
| atr_long_period   | 100   |
| selected_regime   | ""    |

Tidak ada regime filter pada baseline (identik EXP-002) — filter adalah
mitigasi line lama dan hanya dievaluasi lanjutan jika baseline SUPPORTED.

---

# 10. Execution Assumptions

Per RSH-001 §14 (semantik terinci di SPEC-003/SPEC-004, E-9/E-10):

- **Entry**: open bar berikutnya setelah Signal **knowable** (E-1);
- **Exit**: setelah `hold_bars` (10) bar di **close** bar scheduled
  (tanpa SL/TP pada baseline);
- **Sizing**: `position_size = 1.0` (fixed);
- **Transaction cost**: model venue §9.5 (identik EXP-002);
- **Slippage**: `slippage_rate` pada entry dan exit (conservative);
- Eksekusi adalah simulasi, bukan live (PRD-006 §9).

---

# 11. Variables

## 11.1 Control Variables

- dataset (XAUUSD H1, rentang penuh);
- strategy/indicator/event/signal config (§9.1-§9.3);
- biaya venue 1.0 bps/side (§9.5);
- hold_bars, sizing, min_sample.

## 11.2 Independent Variables

Untuk baseline EXP-005: **tidak ada variabel bebas** — satu konfigurasi
frozen (§9) dijalankan apa adanya. Grid parameter (price_lookback,
window, dll.) adalah bahan sensitivity/robustness lanjutan (RSH-003 §10)
yang hanya dieksekusi setelah baseline.

## 11.3 Dependent Variables

- metrik minimum (RSH-002 §8);
- OOS train/test expectancy (stasionaritas, §12/§16);
- robustness temporal slices (RSH-003 §10);
- breakeven cost;
- equity curve;
- trade log.

---

# 12. Baseline Reference

Per RSH-001 §9:

- **No Trade** — reference tanpa aktivitas (equity 0);
- **EXP-002 representative** (unfiltered, 1.0 bps/side -> expectancy 0.5111,
  n=1403, breakeven ≈ 2.43 bps/side, EXP-002 §15) sebagai konteks: strategi
  momentum dikatakan menambah nilai riset jika expectancy >= 0 pada 1.0
  bps/side dengan n >= 30 (kriteria pre-registered §13).

Catatan: perbandingan langsung dengan EXP-002 bukan apples-to-apples (strategi
berbeda); konteks di atas hanya menunjukkan bahwa biaya venue yang sama sudah
"lolos" untuk line lama.

---

# 13. Decision Criteria (pre-registered)

```text
SUPPORTED
Jika pada skenario representative (1.0 bps/side, konfigurasi frozen §9):
  - expectancy > 0 dengan n >= min_sample (30);
  - biaya breakeven/side >= 1.0 bps (setidaknya menutup biaya venue);
  - OOS test expectancy > 0 (edge bertahan out-of-sample);
  - OOS train expectancy > 0 (stasionaritas, seperti EXP-002/003).

REJECTED
Jika salah satu kriteria SUPPORTED tidak terpenuhi.
```

Interpretasi tambahan (bukan keputusan, untuk konteks):

- jika SUPPORTED, strategi momentum murni layak dilanjutkan (evaluasi
  regime/SL/TP/cooldown sebagai mitigasi lanjutan, RSH-003 §10);
- jika REJECTED, bukti menolak kelas momentum breakout ini juga pada biaya
  venue — memperkuat kesimpulan bahwa edge XAUUSD H1 tidak tradable pada
  biaya realistis (EXP-001 §19.8, ARC-008 §14.4).

Catatan multiple-testing (RSH-004 §8.2, E-8):

```text
- jumlah kriteria keputusan:            4 (expectancy > 0, breakeven >= 1.0 bps,
                                         OOS test > 0, OOS train > 0);
- jumlah kombinasi parameter (combo):   5 (price_lookback × rsi_period — grid degenerate
                                         legacy; rsi_period inert untuk strategi tanpa RSI);
- jumlah slice temporal / split point:  4 slice, 1 split point;
- jumlah dimensi robustness:            4 (periods, markets, costs, combos);
- koreksi / penalty:                    none — risiko data-snooping dinyatakan eksplisit.
```

Note: EXP-005 dijalankan sebelum standar E-8; blok ini dokumentasi
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
Max Drawdown
Winning Streak
Losing Streak
Sufficient Sample (n >= min_sample)
```

Serta (RSH-003):

- OOS train/test metrics;
- robustness temporal slices, cross-market (XAGUSD), cost grid, parameter
  combinations;
- breakeven cost.

---

# 15. Run (TODO-043)

Report: `experiments/EXP-005/EXP-005_report.md` (Code Version `60e7660`).
Strategi frozen (konfigurasi EXP-005, Price Breakout Donchian-style, biaya
venue 1.0 bps/side, tanpa regime filter, tanpa SL/TP) dijalankan tanpa
modifikasi.

## 15.1 Representative Scenario (1.0 bps/side)

| Metric        | Value |
| ------------- | ----- |
| Trade Count   | 3882  |
| Win Rate      | 0.33694 |
| Loss Rate     | 0.66306 |
| Average Win   | 7.7394 |
| Average Loss  | 9.18848 |
| Risk/Reward   | 0.842294 |
| Expectancy    | −3.4848 |
| Profit Factor | 0.428019 |
| Gross Profit  | 10123.1 |
| Gross Loss    | 23651.1 |
| Net P&L       | −13528 |
| Max Drawdown  | 13571.8 |
| Winning Streak| 15    |
| Losing Streak | 28    |

Perbandingan vs kontrol EXP-002 (RSI Trendline Breakout unfiltered, 1.0
bps/side, EXP-002 §15.1):

| Metric        | EXP-002 kontrol | EXP-005 | Δ      |
| ------------- | --------------- | ------- | ------ |
| Expectancy    | 0.5111          | −3.4848 | < 0    |
| Profit Factor | 1.1177          | 0.4280  | < 1    |
| Net P&L       | 717.09          | −13528  | < 0    |
| Win Rate      | 0.4783          | 0.33694 | −29.6% |
| Trade Count   | 1403            | 3882    | +176.7%|

Interpretasi: strategi momentum murni Price Breakout (Donchian-style)
**rugi** pada biaya venue nyata — expectancy negatif dan PF < 1. Win rate
rendah (33.7%) dengan risk/reward 0.84 — kombinasi yang merugikan secara
gross maupun net.

## 15.2 Zero-Cost Context (grid biaya, variabel bebas §14)

| Scenario     | comm      | slip      | Total bps/side | Expectancy | PF     | Net P&L    |
| ------------ | --------- | --------- | -------------- | ---------- | ------ | ---------- |
| Zero cost    | 0         | 0         | 0              | −3.1186    | 0.4674 | −12106.22  |
| ECN rep.     | 0.00003   | 0.00007   | 1.0            | −3.4848    | 0.4280 | −13528.01  |
| Sintetis 5+5 | 0.0005    | 0.0005    | 10             | −6.7811    | 0.1990 | −26324.09  |

Temuan kunci: **bahkan pada biaya nol (comm=0/slip=0) expectancy tetap
negatif (−3.1186)** — strategi tidak menghasilkan edge sama sekali
(gross expectancy sudah negatif). Breakeven cost berada **di bawah 0
bps/side**, jauh di bawah ambang kriteria 1.0 bps (§13).

## 15.3 Breakeven Cost

Karena gross expectancy sudah negatif (avg win 7.7394 × 0.33694 vs avg loss
9.18848 × 0.66306), **tidak ada biaya positif yang menghasilkan breakeven**:
expectancy negatif pada 0 bps/side (−3.1186) dan semakin negatif seiring
biaya naik. Breakeven < 0 bps/side → kriteria "breakeven >= 1.0 bps"
(§13) **TIDAK TERPENUHI** tanpa perlu interpolasi grid.

---

# 16. Out-of-Sample Testing (TODO-043)

Metodologi per **RSH-003 §6/§7**: split kronologis (no leakage, no
retroactive allocation); strategi frozen (konfigurasi EXP-005, 1.0 bps/side)
dijalankan tanpa perubahan pada kedua segmen. Reuse `run_on_slice`
(ARC-ACT-013).

Report: `experiments/EXP-005/EXP-005_oos.md` (Code Version `60e7660`).

Split point: index 70.000 (2021-04-29 18:00 UTC) — 70% train, 30% test
(identik EXP-002 §16 / EXP-003 §16 / EXP-004 §16).

| Metric        | Baseline | Train  | Test   | Δ Test/Train |
| ------------- | -------- | ------ | ------ | ------------ |
| Trade Count   | 3882     | 2560   | 1305   | -            |
| Win Rate      | 0.3369   | 0.3328 | 0.3425 | -            |
| Expectancy    | −3.4848  | −2.6301 | −5.2396 | −99.2%     |
| Profit Factor | 0.4280   | 0.3917 | 0.4559 | +16.4%      |
| Net P&L       | −13528.01| −6732.93 | −6837.65 | +1.6%    |
| Max DD        | 13571.75 | 6778.83 | 6940.14 | -            |
| Sufficient    | True     | True   | True   | -            |

Interpretasi:

- **train negatif** (−2.6301) dan **test negatif** (−5.2396) — edge TIDAK
  ter-reproduksi out-of-sample; kedua segmen merugi;
- dibanding EXP-002 (train −0.1605 / test +1.9810): jauh lebih buruk —
  momentum breakout tidak memiliki edge di paruh awal maupun akhir dataset;
- kriteria §13 (OOS test & train > 0) **TIDAK terpenuhi** (keduanya negatif).

---

# 17. Robustness (TODO-043)

Metodologi per **RSH-003 §10**: strategi frozen (konfigurasi EXP-005, 1.0
bps/side) dijalankan tanpa perubahan. Descriptive only; thresholds per
RSH-004.

Report: `experiments/EXP-005/EXP-005_robustness.md` (Code Version `60e7660`).

## 17.1 Time Period Stability (4 slices)

| Slice          | Trades | Win Rate | Expectancy | PF     | Net P&L   | Max DD   |
| -------------- | ------ | -------- | ---------- | ------ | --------- | -------- |
| period-1-of-4  | 1012   | 0.3370   | −2.8809    | 0.3828 | −2915.43  | 2961.42  |
| period-2-of-4  | 757    | 0.3118   | −2.4350    | 0.3582 | −1843.33  | 1843.33  |
| period-3-of-4  | 999    | 0.3303   | −2.8422    | 0.3936 | −2839.40  | 2883.04  |
| period-4-of-4  | 1093   | 0.3577   | −5.4558    | 0.4740 | −5963.16  | 5963.16  |

Interpretasi: **0/4 slice positif** — semua periode temporal merugi;
konsisten dengan baseline negatif.

## 17.2 Cross-Market (XAGUSD, same timeframe)

| Market | Trades | Win Rate | Expectancy | PF     | Net P&L | Max DD |
| ------ | ------ | -------- | ---------- | ------ | ------- | ------ |
| XAGUSD | 3049   | 0.3214   | −0.1232    | 0.4045 | −375.50 | 377.51 |

Interpretasi: XAGUSD juga negatif (−0.1232) — edge momentum TIDAK
ter-reproduksi cross-market.

## 17.3 Execution Cost (synthetic grid)

| comm/slip     | Expectancy | PF    |
| ------------- | ---------- | ----- |
| 0 / 0         | −3.1186    | 0.4674|
| 0.0002 / 0    | −3.8511    | 0.3922|
| 0.0005 / 0    | −4.9498    | 0.3028|
| 0 / 0.0002    | −3.8511    | 0.3922|
| 0 / 0.0005    | −4.9498    | 0.3028|
| 0.0002/0.0002 | −4.5836    | 0.3299|
| 0.0005/0.0005 | −6.7811    | 0.1990|

Interpretasi: **seluruh grid negatif, termasuk 0/0** — bukan masalah biaya;
edge tidak ada bahkan sebelum biaya (gross expectancy negatif).

## 17.4 Parameter Combinations (price_lookback / rsi_period)

| Combo             | Trades | Expectancy | PF    | Net P&L   |
| ----------------- | ------ | ---------- | ----- | --------- |
| 20 / 14 (baseline)| 3882   | −3.4848    | 0.4280| −13528.01 |
| 10 / 7            | 5606   | −3.4782    | 0.4235| −19498.76 |
| 10 / 21           | 5606   | −3.4782    | 0.4235| −19498.76 |
| 30 / 7            | 3203   | −3.5916    | 0.4267| −11503.88 |
| 30 / 21           | 3203   | −3.5916    | 0.4267| −11503.88 |

Interpretasi: **0/5 kombinasi positif** — semua varian parameter merugi
dengan besaran serupa; kegagalan bukan artefak pemilihan parameter tunggal.

---

# 18. Conclusion

## 18.1 Verdict (pre-registered criteria, §13)

```text
REJECTED
- expectancy pada skenario representative (1.0 bps/side) = −3.4848 < 0
  dengan n = 3882 >= min_sample (30): TIDAK TERPENUHI;
- biaya breakeven/side < 0 bps (expectancy negatif bahkan pada biaya nol,
  −3.1186) >= 1.0 bps: TIDAK TERPENUHI;
- OOS test expectancy = −5.2396 > 0: TIDAK TERPENUHI;
- OOS train expectancy = −2.6301 > 0 (stasioner): TIDAK TERPENUHI.
```

**0/4 kriteria pre-registered terpenuhi → verdict pre-registered REJECTED.**

## 18.2 Implikasi

- **Price Breakout (Donchian-style) baseline merugi di semua dimensi**:
  baseline −3.4848, OOS train −2.6301 & test −5.2396, 0/4 slice temporal,
  0/5 parameter combos, XAGUSD negatif, dan seluruh grid biaya negatif
  termasuk nol biaya;
- **edge tidak ada secara gross**: strategi rugi bahkan tanpa biaya
  (expectancy −3.1186 @ 0 bps/side) — kegagalan struktural, bukan biaya
  venue;
- **memperkuat kesimpulan lintas line**: dua kelas strategi berbeda pada
  XAUUSD H1 (RSI Trendline Breakout EXP-001..004 dan Price Breakout EXP-005)
  keduanya gagal menunjukkan edge tradable pada biaya venue realistis
  (EXP-001 §19.8, ARC-008 §14.4);
- per interpretasi §13: bukti menolak kelas momentum breakout ini juga pada
  biaya venue — konsisten dengan kesimpulan bahwa edge XAUUSD H1 tidak
  tradable pada biaya realistis.

## 18.3 Keputusan Lanjutan (peneliti)

Hasil EXP-005 konsisten negatif di semua dimensi (baseline, OOS, temporal,
cross-market, cost grid, parameter). Catatan kehati-hatian:

- verdict berdasarkan kriteria pre-registered §13; hasil OOS/robustness
  adalah konteks tambahan (RSH-003, deskriptif);
- strategi hanya LONG (SignalRule LONG, trigger PRICE_CONFIRMATION + SWING_HIGH
  window 5) — tidak menguji arah short; pertimbangan lanjutan opsional;
- kandidat langkah berikutnya (bukan parameter mining otomatis):
  1) menutup line Price Breakout juga (konsisten dgn bukti dua kelas strategi
     gagal), atau
  2) pre-register eksplorasi berbeda (timeframe/intrument/entry-filter lain)
     dengan keputusan terpisah, atau
  3) menghentikan riset edge XAUUSD H1 dan beralih konteks pasar lain.

---

# 19. Record Lifecycle

```text
Defined (spesifikasi + konfigurasi frozen)    ← 2026-08-10 (pre-registration, TODO-042)
    ↓ (TODO-043 Run EXP-005)
Run          ← 2026-08-11 (§15)
    ↓
Result (metrics dicatat)    ← 2026-08-11 (§15)
    ↓
OOS / robustness            ← 2026-08-11 (§16/§17)
    ↓
Conclusion (interpretasi evidence — peneliti, PRD-006 §9)    ← saat ini (§18)
    ↓
Reviewed (validasi, RSH-003)
```

---

# 20. Traceability

| Item            | Requirement / TODO           |
| --------------- | ---------------------------- |
| Hypothesis      | RSH-001 §7, TODO-042         |
| Spec fields     | RSH-002 §6, TODO-014         |
| Metrics         | RSH-002 §8, FND-008 §25      |
| Reproducibility | FR-010, NFR-001, RSH-002 §9  |
| Venue cost      | RSH-003 §10 (cost dimension) |
| Line closure    | EXP-001 §19.8, ARC-008 §14.4 |
| Strategy plugin | ARC-005 §6, ARC-008 ARC-ACT-010 |
| Out-of-sample   | RSH-003 §6/§7, TODO-043      |
| Robustness      | RSH-003 §10, TODO-043        |
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
- `docs/07-experiments/EXP-004_RSI_Trendline_Breakout_SL_TP_Venue_Cost.md`
- `docs/03-engine/ENG-002_Event_Engine.md`
- `docs/03-engine/ENG-003_Signal_Engine.md`
- `docs/03-engine/ENG-005_Simulation_Engine.md`
- `docs/03-engine/ENG-006_Statistics_Engine.md`
- `docs/03-engine/ENG-007_Reporting_Engine.md`
- `docs/01-product/PRD-006_MVP_Definition.md`
- `configs/EXP-005.yaml`

---

# 23. Revision History

| Version | Date       | Changes                                      |
| ------- | ---------- | -------------------------------------------- |
| 1.0.1   | 2026-08-11 | EXP-005 run (TODO-043) dicatat (§15–§17): Price Breakout baseline @ 1.0 bps/side → expectancy −3.4848 (n=3882), breakeven < 0 bps (negatif bahkan di biaya nol −3.1186), OOS train −2.6301 & test −5.2396, 0/4 slice positif, 0/5 combos, XAGUSD negatif; verdict REJECTED (§18) — 0/4 kriteria pre-registered |
| 1.0.0   | 2026-08-10 | Initial EXP-005 pre-registration (TODO-042): Price Breakout (Donchian-style) baseline; line RSI Trendline Breakout ditutup (EXP-001..EXP-004), strategi momentum murni terdaftar sebagai plugin `price_breakout`; config frozen identik EXP-002 (venue cost 1.0 bps/side) |

---

**Document Status:** Result

**Document ID:** EXP-005

**Version:** 1.0.1

**End of Document**
