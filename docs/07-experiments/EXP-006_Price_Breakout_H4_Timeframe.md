---
title: Price Breakout (Donchian-style) — H4 Timeframe
document_id: EXP-006
version: 1.0.1
status: Result
category: Experiment
owner: Market Research Engine Core Team
created: 2026-08-11
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

purpose: Pre-register EXP-006 (TODO-044) and record the run (TODO-045) — re-test the Price Breakout (Donchian-style) strategy on XAUUSD H4 after the H1 baseline (EXP-005) was REJECTED per pre-registered criteria (expectancy negative even at zero cost, breakeven < 0 bps, OOS train/test negative); tests whether the Price Breakout edge is timeframe-specific. Result (1.0.1): REJECTED per pre-registered criteria — expectancy −8.3297 @ 1.0 bps/side (n=1188), negative even at zero cost (−7.9576), breakeven < 0 bps, OOS train −5.0451 & test −14.2008, 0/4 slices, 0/5 combos, XAGUSD negative (EXP-006 §15–§18)
---

# Price Breakout (Donchian-style) — H4 Timeframe

> Measure the Market. Discover the Edge.

---

# 1. Purpose

EXP-006 adalah **experiment keenam** MRE (RSH-002 §10 lifecycle — state
sekarang `Result`, pre-registration + hasil run). Line Price Breakout
(EXP-005, plugin `price_breakout`) pada H1 telah **REJECTED** per kriteria
pre-registered: expectancy −3.4848 @ 1.0 bps/side (n=3882), bahkan negatif di
biaya nol (−3.1186), OOS train −2.6301 & test −5.2396, 0/4 slice temporal,
0/5 combos, XAGUSD negatif (EXP-005 §15–§18). Keputusan peneliti (EXP-005
§18.3 kandidat 2): lanjutkan dengan **eksplorasi berbeda pada sumbu berbeda**
— bukan parameter mining otomatis, melainkan uji spesifik apakah edge
strategi bersifat **spesifik timeframe**.

EXP-006 menguji strategi yang **identik** (definisi sinyal, konfigurasi
frozen, biaya venue) pada **timeframe berbeda**: XAUUSD **H4** (bukan H1).
Hipotesis: kegagalan Price Breakout pada H1 mungkin spesifik horizon;
lookback/swing/hold yang sama mengekspresikan horizon waktu ~4× lebih panjang
pada H4 (price_lookback 20 H4-bar ≈ 5 hari kalender vs ~1 hari pada H1;
hold_bars 10 H4-bar ≈ 2.5 hari vs ~10 jam pada H1).

Hasil (TODO-045, doc 1.0.1): **REJECTED** per kriteria pre-registered §13 —
expectancy −8.3297 @ 1.0 bps/side (n=1188 >= 30), negatif bahkan pada biaya
nol (−7.9576), breakeven < 0 bps/side, OOS train −5.0451 & test −14.2008
(keduanya negatif), 0/4 slice temporal, 0/5 combos, XAGUSD negatif
(§15–§18). Edge Price Breakout TIDAK bersifat spesifik H4 — kegagalan
**lintas timeframe** (H1 dan H4) memperkuat kesimpulan bahwa XAUUSD tidak
menunjukkan edge tradable pada biaya realistis untuk kelas strategi ini.

---

# 2. Scope

Scope EXP-006:

- pre-registration hypothesis (RSH-001 §7.2);
- dataset baru: XAUUSD **H4** (`datasets/XAUUSD_H4.csv`, immutable — Article 13);
- configuration frozen: **identik dengan EXP-005 §9** (venue cost 1.0 bps/side,
  tanpa regime filter, tanpa SL/TP) kecuali dataset/timeframe → H4;
- strategi **Price Breakout (Donchian-style)** (§8) sebagai objek uji —
  plugin `price_breakout` yang sama, tanpa modifikasi;
- OOS dan robustness (RSH-003 §6/§7/§10) sebagai kriteria stasionaritas.

Di luar scope EXP-006:

- optimasi parameter (sensitivity/robustness, bukan objek uji baseline);
- regime filter, SL/TP, cooldown (mitigasi — evaluasi lanjutan hanya jika
  baseline SUPPORTED);
- modifikasi strategi/detector/engine (seluruhnya reusable);
- data terbaru di luar rentang dataset H4 (deferred path, EXP-003 §18.5 —
  tidak memblokir experiment ini);
- market lain (XAGUSD robustness cross-market hanya jika tersedia H4;
  saat ini hanya XAGUSD_H1 tersedia — cross-market memakai H1 dengan
  catatan perbedaan timeframe).

---

# 3. Audience

- tim MRE;
- peneliti;
- quant analyst;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Per FND-005 §37, Research Evidence adalah sumber prioritas keputusan.

- EXP-001..EXP-004 (line RSI Trendline Breakout, H1): seluruhnya selesai —
  edge tidak menunjukkan profil tradable pada biaya venue realistis; line
  ditutup formal (EXP-004 §18.3).
- EXP-005 (line Price Breakout, H1): REJECTED — expectancy negatif bahkan di
  biaya nol, breakeven < 0 bps, OOS train/test negatif, 0/4 slice temporal,
  0/5 combos, XAGUSD negatif; kegagalan **struktural** (rugi sebelum biaya),
  bukan artefak biaya venue (EXP-005 §18.2).
- Kesimpulan lintas line (EXP-005 §18.2): dua kelas strategi berbeda pada
  XAUUSD **H1** sama-sama gagal.

Pertanyaan EXP-006: apakah kegagalan tersebut **spesifik H1** atau **universal
untuk XAUUSD**? Timeframe adalah dimensi yang belum pernah diuji (M7 hanya
menguji H1, ARC-008). Jika H4 menghasilkan edge gross positif (expectancy > 0
pada biaya nol) dan net positif pada 1.0 bps/side, maka edge strategi adalah
spesifik horizon — membuka arah riset yang baru. Jika H4 juga gagal (negatif
bahkan di biaya nol), bukti memperkuat kesimpulan bahwa XAUUSD tidak tradable
pada strategi kelas ini di berbagai timeframe.

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
| Timeframe      | Periode candle (H1, H4, …) — RSH-002 §6              |

---

# 6. Hypothesis

Per RSH-001 §7.1:

> Kondisi **X** (deteksi/Event) menghasilkan
> edge pada **Symbol** (Y) timeframe (**Z**).

Hipotesis EXP-006 (pre-registered):

> **Breakout harga Donchian-style (close menembus highest high N-bar,
> dikonfirmasi swing-high fractal) pada XAUUSD H4 menghasilkan expectancy
> positif setelah biaya eksekusi venue nyata (1.0 bps/side) — edge strategi
> Price Breakout bersifat spesifik timeframe, tidak ada pada H1 (EXP-005
> REJECTED) namun mungkin ada pada H4.**

Kriteria (RSH-001 §7.2):

- falsifiable: keputusan ditentukan oleh kriteria terukur (§13);
- terikat dataset dan konfigurasi spesifik (§7, §9);
- dinyatakan sebelum experiment dijalankan (dokumen ini).

Catatan: hipotesis ini **tidak** mengasumsikan momentum murni pasti bekerja —
EXP-005 menunjukkan sebaliknya pada H1. Pertanyaan terukur adalah apakah
horizon waktu mengubah hasil. Jika SUPPORTED, arah riset lanjutan terbuka
(regime/SL/TP/cooldown filter pada H4). Jika REJECTED (negatif bahkan di
biaya nol), bukti menunjukkan kegagalan lintas timeframe pada kelas strategi
ini — memperkuat kesimpulan XAUUSD tidak tradable pada biaya realistis
(EXP-005 §18.2).

---

# 7. Dataset

| Field          | Value                                      |
| -------------- | ------------------------------------------ |
| File           | `datasets/XAUUSD_H4.csv`                   |
| Symbol         | XAUUSD                                     |
| Timeframe      | H4                                         |
| Source         | CSV (kolom: timestamp, open, high, low, close, volume) |
| Date Range     | 2009-07-13 20:00 -> 2026-04-14 04:00       |
| Candle Count   | 26.816                                     |
| Integrity      | valid (validasi inti PRD-006 §8.2)         |

Catatan provenance: file H4 **bukan** agregasi dari `datasets/XAUUSD_H1.csv`
lokal — rentangnya berbeda (mulai 2009-07-13, lebih awal dari H1; berakhir
2026-04-14, lebih pendek dari H1 2026-05-26). Verifikasi silang 22.356 bar
H4 vs agregasi 4×H1 pada rentang overlap cocok kecuali 1 bar tail (bar
terakhir H4). Dataset immutable (Article 13, ARC-004).

## Market Definition (RSH-002 §6.1, E-5)

| Field                     | Value                                   |
| ------------------------- | --------------------------------------- |
| Instrument                | XAUUSD (spot gold)                      |
| Origin / Vendor           | Export terpisah; vendor tidak terdokumentasi |
| Session / Hours           | Tanpa filter session (seluruh bar tersedia) |
| Timezone                  | UTC (ISO 8601 `Z`)                      |
| Ordering                  | Strictly increasing timestamp           |
| Missing Data Handling     | Tidak diimputasi; ambang → ditolak      |
| Duplicate Handling        | Timestamp duplikat ditolak              |
| Gap Handling              | Tidak di-resample / tidak di-fill       |
| OHLC Rules                | open/close > 0; high ≥ max(o,c); low ≤ min(o,c) |
| Provenance                | Export terpisah (bukan agregasi H1); cross-check 4×H1 22.356 bar cocok kecuali 1 bar tail |

Aturan tertera konsisten dengan ARC-004 §7/§8 dan `validator.py`.

---

# 8. Strategy — Price Breakout (Donchian-style)

Identik dengan EXP-005 §8 — strategi yang sama, plugin `price_breakout`
(`src/mre/strategies/exp005.py`, ARC-ACT-010). Tidak ada perubahan pada
detector, signal definition, atau engine:

```text
TRIGGER:       PRICE_CONFIRMATION   (close > highest high N-bar — Donchian
                                     upper channel break, ENG-002 §7.3)
CONFIRMATION:  SWING_HIGH           (fractal swing high setelah breakout,
                                     ADR-003)
SIGNAL:        LONG
```

Semantik: sinyal LONG muncul ketika harga menembus highest high dari `lookback`
candle terakhir dan, dalam `window` (5) candle setelahnya, sebuah fractal
swing-high terkonfirmasi. Parameter diukur per-bar: pada H4, price_lookback
20 ≈ 5 hari kalender (vs ~1 hari pada H1) dan hold_bars 10 ≈ 2.5 hari (vs
~10 jam pada H1) — horizon strategi ~4× lebih panjang.

Catatan arsitektur: EventEngine tetap menghitung RSI (kontrak pipeline) namun
strategi `price_breakout` **tidak mengkonsumsi** Event berbasis RSI.

---

# 9. Configuration (Frozen)

Konfigurasi dikunci (frozen) sebelum run (RSH-002 §9). Seluruh parameter
**menyamai EXP-005 §9** (venue cost 1.0 bps/side, tanpa regime filter, tanpa
SL/TP) kecuali dataset/timeframe → H4.

## 9.1 Indicators

| Parameter     | Value |
| ------------- | ----- |
| rsi_period    | 14    |

Catatan: RSI tetap dihitung pipeline namun tidak dikonsumsi oleh strategi.

## 9.2 Event Engine

| Parameter     | Value |
| ------------- | ----- |
| swing_left    | 2     |
| swing_right   | 2     |
| price_lookback| 20    |

## 9.3 Signal

| Parameter     | Value |
| ------------- | ----- |
| window        | 5     |
| cooldown      | 0     |

## 9.4 Execution

| Parameter     | Value |
| ------------- | ----- |
| position_size | 1.0   |
| commission_rate | 0.00003 |
| slippage_rate | 0.00007 |
| hold_bars     | 10    |
| stop_loss     | -     |
| take_profit   | -     |
| stop_loss_atr | -     |
| take_profit_atr | -   |
| atr_period    | 14    |

Venue cost model: 1.0 bps/side total (commission 0.3 bps + slippage 0.7 bps),
identik EXP-002/005 §9.

## 9.5 Regime

| Parameter     | Value |
| ------------- | ----- |
| atr_short_period | 14 |
| atr_long_period | 100 |
| selected_regime | (none) |

## 9.6 Statistics

| Parameter     | Value |
| ------------- | ----- |
| min_sample    | 30    |

---

# 10. Execution Assumptions

Identik EXP-005 §10 (semantik terinci di SPEC-003/SPEC-004, E-9/E-10):

- Entry: **open bar berikutnya** setelah Signal **knowable** — "entry di
  candle breakout" merujuk candle keputusan, bukan fill (E-10);
- Exit: hold 10 bar (**close** bar `entry_bar + hold_bars`, net of costs);
- tanpa SL/TP absolut atau ATR-multiple;
- biaya per sisi: commission 3e-05 + slippage 7e-05 (1.0 bps/side total).

---

# 11. Variables

- **Independent**: timeframe (H4, satu nilai — frozen, bukan grid);
- **Dependent**: metrics §12 (expectancy, PF, net P&L, win rate, dll.);
- **Controlled/frozen**: seluruh parameter §9, dataset §7, biaya venue.

---

# 12. Baseline Reference

- **EXP-005 kontrol** (Price Breakout, H1, 1.0 bps/side — EXP-005 §15.1):
  expectancy −3.4848, PF 0.428, win rate 0.337, n=3882; sebagai konteks:
  strategi H4 dikatakan memberikan nilai riset tambahan jika expectancy
  **> 0** pada 1.0 bps/side dengan n >= 30 (kriteria pre-registered §13).

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

- jika SUPPORTED, edge Price Breakout bersifat spesifik H4 — layak dilanjutkan
  (evaluasi regime/SL/TP/cooldown pada H4 sebagai mitigasi lanjutan);
- jika REJECTED, khususnya jika expectancy negatif pada biaya nol, bukti
  menunjukkan kegagalan **lintas timeframe** pada kelas strategi ini —
  memperkuat kesimpulan bahwa XAUUSD tidak tradable pada biaya realistis
  (EXP-005 §18.2).

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

Note: EXP-006 dijalankan sebelum standar E-8; blok ini dokumentasi
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
- robustness temporal slices, cross-market (XAGUSD H1 dengan catatan
  perbedaan timeframe), cost grid, parameter combinations;
- breakeven cost.

---

# 15. Run (TODO-045)

Report: `experiments/EXP-006/EXP-006_report.md` (Code Version `e4e72bd`).
Strategi frozen (konfigurasi EXP-006, Price Breakout Donchian-style pada
XAUUSD H4, biaya venue 1.0 bps/side, tanpa regime filter, tanpa SL/TP)
dijalankan tanpa modifikasi.

## 15.1 Representative Scenario (1.0 bps/side)

| Metric        | Value |
| ------------- | ----- |
| Trade Count   | 1188  |
| Win Rate      | 0.369529 |
| Loss Rate     | 0.630471 |
| Average Win   | 16.9689 |
| Average Loss  | 23.1575 |
| Risk/Reward   | 0.732759 |
| Expectancy    | −8.3297 |
| Profit Factor | 0.429481 |
| Gross Profit  | 7449.33 |
| Gross Loss    | 17345   |
| Net P&L       | −9895.63 |
| Max Drawdown  | 10003.2 |
| Winning Streak| 13    |
| Losing Streak | 19    |

Perbandingan vs kontrol EXP-005 (Price Breakout H1, 1.0 bps/side, EXP-005
§15.1):

| Metric        | EXP-005 H1 | EXP-006 H4 | Δ        |
| ------------- | ---------- | ---------- | -------- |
| Expectancy    | −3.4848    | −8.3297    | < 0      |
| Profit Factor | 0.4280     | 0.4295     | ~        |
| Net P&L       | −13528     | −9895.63   | < 0      |
| Win Rate      | 0.33694    | 0.3695     | +9.7%    |
| Trade Count   | 3882       | 1188       | −69.4%   |

Interpretasi: strategi momentum murni Price Breakout (Donchian-style)
**rugi** pada H4 dengan besaran expectancy bahkan lebih negatif daripada H1
(−8.33 vs −3.48) meskipun trade count lebih sedikit. Win rate H4 lebih tinggi
(36.95%) namun average loss (23.16) jauh lebih besar dari average win
(16.97) — kombinasi risk/reward 0.73 yang merugikan secara gross maupun net.

## 15.2 Zero-Cost Context (grid biaya, variabel bebas §14)

| Scenario     | comm      | slip      | Total bps/side | Expectancy | PF     | Net P&L    |
| ------------ | --------- | --------- | -------------- | ---------- | ------ | ---------- |
| Zero cost    | 0         | 0         | 0              | −7.9576    | 0.4463 | −9453.64   |
| ECN rep.     | 0.00003   | 0.00007   | 1.0            | −8.3297    | 0.4295 | −9895.63   |
| Sintetis 5+5 | 0.0005    | 0.0005    | 10             | −11.6781   | 0.3043 | −13873.57  |

Temuan kunci: **bahkan pada biaya nol (comm=0/slip=0) expectancy tetap
negatif (−7.9576)** — strategi tidak menghasilkan edge sama sekali pada H4
(gross expectancy sudah negatif). Breakeven cost berada **di bawah 0
bps/side**, jauh di bawah ambang kriteria 1.0 bps (§13).

## 15.3 Breakeven Cost

Karena gross expectancy sudah negatif (avg win 16.9689 × 0.369529 vs avg loss
23.1575 × 0.630471), **tidak ada biaya positif yang menghasilkan breakeven**:
expectancy negatif pada 0 bps/side (−7.9576) dan semakin negatif seiring
biaya naik. Breakeven < 0 bps/side → kriteria "breakeven >= 1.0 bps"
(§13) **TIDAK TERPENUHI** tanpa perlu interpolasi grid.

---

# 16. Out-of-Sample Testing (TODO-045)

Metodologi per **RSH-003 §6/§7**: split kronologis (no leakage, no
retroactive allocation); strategi frozen (konfigurasi EXP-006, 1.0 bps/side)
dijalankan tanpa perubahan pada kedua segmen. Reuse `run_on_slice`
(ARC-ACT-013).

Report: `experiments/EXP-006/EXP-006_oos.md` (Code Version `e4e72bd`).

Split point: index 18.771 (2021-04-01 08:00 UTC) — 70% train, 30% test
(mekanisme identik EXP-002 §16 / EXP-003 §16 / EXP-004 §16 / EXP-005 §16).

| Metric        | Baseline | Train  | Test   | Δ Test/Train |
| ------------- | -------- | ------ | ------ | ------------ |
| Trade Count   | 1188     | 760    | 418    | -            |
| Win Rate      | 0.3695   | 0.3697 | 0.3804 | -            |
| Expectancy    | −8.3297  | −5.0451 | −14.2008 | +181.5%  |
| Profit Factor | 0.4295   | 0.4265 | 0.4361 | +2.3%       |
| Net P&L       | −9895.63 | −3834.29 | −5935.95 | +54.8% |
| Max DD        | 10003.17 | 3941.80 | 5935.95 | -            |
| Sufficient    | True     | True   | True   | -            |

Interpretasi:

- **train negatif** (−5.0451) dan **test negatif** (−14.2008) — edge TIDAK
  ter-reproduksi out-of-sample; kedua segmen merugi;
- test jauh lebih buruk dari train (−14.20 vs −5.05) — degradasi +181.5%
  in-sample → OOS;
- dibanding EXP-005 H1 (train −2.6301 / test −5.2396): keduanya merugi di
  kedua segmen, H4 lebih buruk secara absolut;
- kriteria §13 (OOS test & train > 0) **TIDAK terpenuhi** (keduanya negatif).

---

# 17. Robustness (TODO-045)

Metodologi per **RSH-003 §10**: strategi frozen (konfigurasi EXP-006, 1.0
bps/side) dijalankan tanpa perubahan. Descriptive only; thresholds per
RSH-004.

Report: `experiments/EXP-006/EXP-006_robustness.md` (Code Version `e4e72bd`).

## 17.1 Time Period Stability (4 slices)

| Slice          | Trades | Win Rate | Expectancy | PF     | Net P&L   | Max DD   |
| -------------- | ------ | -------- | ---------- | ------ | --------- | -------- |
| period-1-of-4  | 305    | 0.3902   | −4.8820    | 0.4809 | −1489.00  | 1596.51  |
| period-2-of-4  | 225    | 0.3422   | −4.3200    | 0.3896 | −972.00   | 972.00   |
| period-3-of-4  | 278    | 0.3525   | −5.9749    | 0.3738 | −1661.01  | 1691.34  |
| period-4-of-4  | 370    | 0.3946   | −15.2655   | 0.4407 | −5648.24  | 5782.25  |

Interpretasi: **0/4 slice positif** — semua periode temporal merugi;
konsisten dengan baseline negatif.

## 17.2 Cross-Market (XAGUSD)

| Market | Trades | Win Rate | Expectancy | PF     | Net P&L | Max DD |
| ------ | ------ | -------- | ---------- | ------ | ------- | ------ |
| XAGUSD | 3049   | 0.3214   | −0.1232    | 0.4045 | −375.50 | 377.51 |

Interpretasi: XAGUSD juga negatif (−0.1232) — edge momentum TIDAK
ter-reproduksi cross-market (catatan: XAGUSD diuji pada timeframe H1,
dataset XAGUSD H4 tidak tersedia).

## 17.3 Execution Cost (synthetic grid)

| comm/slip     | Expectancy | PF    |
| ------------- | ---------- | ----- |
| 0 / 0         | −7.9576    | 0.4463|
| 0.0002 / 0    | −8.7017    | 0.4134|
| 0.0005 / 0    | −9.8178    | 0.3686|
| 0 / 0.0002    | −8.7017    | 0.4134|
| 0 / 0.0005    | −9.8178    | 0.3686|
| 0.0002/0.0002 | −9.4458    | 0.3830|
| 0.0005/0.0005 | −11.6781   | 0.3043|

Interpretasi: **seluruh grid negatif, termasuk 0/0** — bukan masalah biaya;
edge tidak ada bahkan sebelum biaya (gross expectancy negatif).

## 17.4 Parameter Combinations (price_lookback / rsi_period)

| Combo             | Trades | Expectancy | PF    | Net P&L   |
| ----------------- | ------ | ---------- | ----- | --------- |
| 20 / 14 (baseline)| 1188   | −8.3297    | 0.4295| −9895.63  |
| 10 / 7            | 1644   | −7.0815    | 0.4692| −11642.00 |
| 10 / 21           | 1644   | −7.0815    | 0.4692| −11642.00 |
| 30 / 7            | 997    | −8.3826    | 0.4501| −8357.47  |
| 30 / 21           | 997    | −8.3826    | 0.4501| −8357.47  |

Interpretasi: **0/5 kombinasi positif** — semua varian parameter merugi
dengan besaran serupa; kegagalan bukan artefak pemilihan parameter tunggal.

---

# 18. Conclusion

## 18.1 Verdict (pre-registered criteria, §13)

```text
REJECTED
- expectancy pada skenario representative (1.0 bps/side) = −8.3297 < 0
  dengan n = 1188 >= min_sample (30): TIDAK TERPENUHI;
- biaya breakeven/side < 0 bps (expectancy negatif bahkan pada biaya nol,
  −7.9576) >= 1.0 bps: TIDAK TERPENUHI;
- OOS test expectancy = −14.2008 > 0: TIDAK TERPENUHI;
- OOS train expectancy = −5.0451 > 0 (stasioner): TIDAK TERPENUHI.
```

**0/4 kriteria pre-registered terpenuhi → verdict pre-registered REJECTED.**

## 18.2 Implikasi

- **Price Breakout (Donchian-style) merugi di semua dimensi pada H4**:
  baseline −8.3297, OOS train −5.0451 & test −14.2008, 0/4 slice temporal,
  0/5 parameter combos, XAGUSD negatif, dan seluruh grid biaya negatif
  termasuk nol biaya;
- **edge tidak ada secara gross**: strategi rugi bahkan tanpa biaya
  (expectancy −7.9576 @ 0 bps/side) — kegagalan struktural, bukan biaya
  venue;
- **edge TIDAK spesifik H4** — hipotesis §6 TIDAK terdukung: strategi gagal
  dengan besaran serupa (bahkan lebih negatif) pada kedua timeframe;
- **memperkuat kesimpulan lintas line dan lintas timeframe**: tiga kelas
  pengujian berbeda (RSI Trendline Breakout H1 EXP-001..004, Price Breakout
  H1 EXP-005, Price Breakout H4 EXP-006) semuanya gagal menunjukkan edge
  tradable pada biaya venue realistis;
- per interpretasi §13: bukti menolak kelas momentum breakout pada H1 dan H4
  — konsisten dengan kesimpulan bahwa XAUUSD tidak tradable pada biaya
  realistis untuk strategi berbasis harga (EXP-005 §18.2).

## 18.3 Keputusan Lanjutan (peneliti)

Hasil EXP-006 konsisten negatif di semua dimensi (baseline, OOS, temporal,
cross-market, cost grid, parameter). Catatan kehati-hatian:

- verdict berdasarkan kriteria pre-registered §13; hasil OOS/robustness
  adalah konteks tambahan (RSH-003, deskriptif);
- strategi hanya LONG (SignalRule LONG, trigger PRICE_CONFIRMATION + SWING_HIGH
  window 5) — tidak menguji arah short; pertimbangan lanjutan opsional;
- dataset H4 adalah export terpisah (bukan agregasi H1) — bukan artefak
  data; hasil menggambarkan perilaku strategi pada horizon yang lebih panjang;
- kandidat langkah berikutnya (bukan parameter mining otomatis):
  1) menutup line Price Breakout juga (konsisten dgn bukti dua timeframe
     gagal), atau
  2) pre-register eksplorasi berbeda (instrumen/konteks pasar lain, mis.
     indeks/forex non-XAU, atau entry-filter berbeda) dengan keputusan
     terpisah, atau
  3) menghentikan riset edge XAUUSD dan beralih konteks pasar lain.

---

# 19. Record Lifecycle

```text
Defined (spesifikasi + konfigurasi frozen)    <- 2026-08-11 (TODO-044)
    |
Run          <- 2026-08-11 (§15)
    |
Result (metrics dicatat)    <- 2026-08-11 (§15)
    |
OOS / robustness            <- 2026-08-11 (§16/§17)
    |
Conclusion (interpretasi evidence — peneliti, PRD-006 §9)    <- saat ini (§18)
    |
Reviewed (validasi, RSH-003)
```

---

# 20. Traceability

| Item            | Requirement / TODO           |
| --------------- | ---------------------------- |
| Hypothesis      | RSH-001 §7, TODO-044         |
| Spec fields     | RSH-002 §6, TODO-014         |
| Metrics         | RSH-002 §8, FND-008 §25      |
| Reproducibility | FR-010, NFR-001, RSH-002 §9  |
| Venue cost      | RSH-003 §10 (cost dimension) |
| Timeframe       | RSH-002 §6 (timeframe field) |
| Line closure    | EXP-005 §18.3                |
| Strategy plugin | ARC-005 §6, ARC-008 ARC-ACT-010 |
| Out-of-sample   | RSH-003 §6/§7, TODO-045      |
| Robustness      | RSH-003 §10, TODO-045        |
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
- `docs/07-experiments/EXP-005_Price_Breakout_Baseline.md`
- `docs/03-engine/ENG-002_Event_Engine.md`
- `docs/03-engine/ENG-003_Signal_Engine.md`
- `docs/03-engine/ENG-005_Simulation_Engine.md`
- `docs/03-engine/ENG-006_Statistics_Engine.md`
- `docs/03-engine/ENG-007_Reporting_Engine.md`
- `docs/01-product/PRD-006_MVP_Definition.md`
- `configs/EXP-006.yaml`

---

# 23. Revision History

| Version | Date       | Changes                                      |
| ------- | ---------- | -------------------------------------------- |
| 1.0.0   | 2026-08-11 | Initial EXP-006 pre-registration (TODO-044): Price Breakout (Donchian-style) diuji ulang pada XAUUSD H4 setelah line H1 REJECTED (EXP-005 §15–§18); keputusan peneliti (EXP-005 §18.3) — uji spesifik apakah edge bersifat spesifik timeframe; config frozen identik EXP-005 §9 kecuali dataset/timeframe → H4 |
| 1.0.1   | 2026-08-11 | Result (TODO-045): REJECTED per kriteria pre-registered §13 — expectancy −8.3297 @ 1.0 bps/side (n=1188 >= 30), negatif bahkan pada biaya nol (−7.9576), breakeven < 0 bps; OOS train −5.0451 & test −14.2008 (keduanya negatif); 0/4 slice temporal, 0/5 combos, XAGUSD −0.1232; 0/4 kriteria terpenuhi (§15–§18); hipotesis "edge spesifik H4" TIDAK terdukung — kegagalan lintas timeframe memperkuat kesimpulan XAUUSD tidak tradable |

---

**Document Status:** Result

**Document ID:** EXP-006

**Version:** 1.0.1

**End of Document**
