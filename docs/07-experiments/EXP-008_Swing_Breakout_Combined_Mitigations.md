---
title: Swing Breakout (Fractal Structure) — Combined Stationarity Mitigations
document_id: EXP-008
version: 1.0.2
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

purpose: Pre-register EXP-008 (TODO-048) and record the run (TODO-049) — re-test the EXP-007 edge (Swing Breakout fractal-structure on XAUUSD H4) with COMBINED stationarity mitigations after EXP-007 was REJECTED per pre-registered criteria (EXP-007 §15–§18): expectancy +0.1170 @ 1.0 bps/side (n=425) and breakeven ≈ 1.32 bps/side both met, OOS test +4.2421 positive, but OOS train −1.8114 negative → NOT stationary. Researcher decision (EXP-007 §18.3 candidate 1): stationarity mitigations, not parameter mining — regime filter (EXP-003 machinery) + ATR-multiple SL/TP (RQ-007 machinery) + cooldown combined in one frozen config. Result (1.0.1): REJECTED per pre-registered criteria — expectancy +2.6211 @ 1.0 bps/side (n=167 ≥ 30) and breakeven ≈ 8.8 bps/side ≥ 1.0 bps both met, OOS test +9.5649 (positive) but OOS train −0.6073 (negative, NOT stationary); robustness improved strongly (2/4 slices, 5/5 combos, XAGUSD +0.0216, negative only at 10 bps) yet the edge remains temporally non-stationary (EXP-008 §15–§18)
---

# Swing Breakout (Fractal Structure) — Combined Stationarity Mitigations

> Measure the Market. Discover the Edge.

---

# 1. Purpose

EXP-008 adalah **experiment kedelapan** MRE (RSH-002 §10 lifecycle — state
sekarang `Result`, pre-registration + hasil run). EXP-007 (Swing Breakout fractal-structure,
XAUUSD H4, plugin `swing_breakout`) telah dijalankan (TODO-047) dan **REJECTED**
per kriteria pre-registered §13 (EXP-007 §15–§18): baseline expectancy
**+0.1170** @ 1.0 bps/side (n=425 >= 30) dan breakeven ≈ 1.32 bps/side >= 1.0 bps
terpenuhi, OOS test **+4.2421** positif, **namun OOS train −1.8114 negatif**
(tidak stasioner); robustness 1/4 slice temporal positif, 3/5 combos positif,
XAGUSD +0.0056 (tipis). Temuan kunci EXP-007: line ini yang **pertama dengan
gross edge** di line XAUUSD (positif di biaya nol, +0.4775), namun edge
**tidak stasioner temporal** — keuntungan terkonsentrasi di periode akhir
(≈ 2022–2026).

Keputusan peneliti (EXP-007 §18.3 kandidat 1): lanjutkan dengan **mitigasi
stasionaritas** — bukan parameter mining otomatis. EXP-008 menerapkan **tiga
mitigasi sekaligus** (semua machinery yang sudah ada, tidak ada perubahan
arsitektur) untuk menstabilkan edge di seluruh periode dataset:

1. **Regime filter** (volatility regime `high`, machinery EXP-003, ARC-008 §14):
   karena edge terkonsentrasi di periode ber-volatilitas tinggi, menyaring
   sinyal ke regime HIGH (ATR short >= ATR long) langsung menargetkan
   non-stasionaritas temporal.
2. **SL/TP ATR-multiple** (SL 1.0 / TP 4.0, machinery RQ-007, pola EXP-004):
   kontrol risiko lebih ketat — memotong kerugian pada periode non-stasioner
   yang merugi (paruh awal dataset, EXP-007 §16).
3. **Cooldown** (10, ENG-003 §8.1, ARC-008 ARC-ACT-012): satu keputusan per
   episode — mengurangi over-trading / overlap sinyal di periode yang sama.

Hasil (TODO-049, doc 1.0.1): **REJECTED** per kriteria pre-registered §13 —
expectancy **+2.6211** @ 1.0 bps/side (n=167 >= 30) dan breakeven ≈ 8.8
bps/side >= 1.0 bps terpenuhi, OOS test **+9.5649** positif, **namun OOS
train −0.6073 negatif** (tidak stasioner); robustness membaik drastis — 2/4
slice temporal positif, **5/5 combos positif**, XAGUSD +0.0216 (tipis
positif), negatif hanya di 10 bps/side (vs 2 bps di EXP-007). Temuan kunci:
mitigasi gabungan **memperbaiki seluruh dimensi** (expectancy 22×, breakeven
1.32 → 8.8 bps, Max DD −78%, combos 3/5 → 5/5) **kecuali stasionaritas** —
edge masih terkonsentrasi di periode akhir (period-4-of-4 +11.69, §15–§18).

---

# 2. Scope

Scope EXP-008:

- pre-registration hypothesis (RSH-001 §7.2);
- dataset: XAUUSD **H4** (`datasets/XAUUSD_H4.csv`, immutable — Article 13),
  identik EXP-006/EXP-007 §7;
- configuration frozen: **identik dengan EXP-007 §9** (venue cost 1.0 bps/side,
  dataset H4, event/indicator/statistics sections) **kecuali tiga mitigasi
  stasionaritas** (§9.3–§9.5): regime `high`, SL/TP ATR 1.0/4.0, cooldown 10;
- strategi **Swing Breakout (Fractal Structure)** (§8) — plugin `swing_breakout`
  yang sama (`src/mre/strategies/exp007.py`, ARC-ACT-010), tidak diubah;
- OOS dan robustness (RSH-003 §6/§7/§10) sebagai kriteria stasionaritas.

Di luar scope EXP-008:

- optimasi parameter (sensitivity/robustness, bukan objek uji baseline);
- menambah/mengubah mitigasi di luar tiga yang di-frozen (§9) — perubahan
  tambahan memerlukan pre-registration terpisah;
- modifikasi strategi/detector/engine (seluruhnya reusable);
- data terbaru di luar rentang dataset H4 (deferred path, EXP-003 §18.5 —
  tidak memblokir experiment ini);
- arah short (strategi hanya LONG — konsisten line sebelumnya);
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
- EXP-005/EXP-006 (line Price Breakout, H1 + H4): REJECTED — expectancy
  negatif bahkan di biaya nol (H1 −3.1186, H4 −7.9576); kegagalan
  **struktural** dan **lintas timeframe**; line DITUTUP (EXP-005 §18.2,
  EXP-006 §18.2/§18.3).
- EXP-007 (Swing Breakout, H4): REJECTED per kriteria §13 (3/4 terpenuhi;
  OOS train negatif → tidak stasioner), namun **gross edge pertama di line
  XAUUSD** — positif di biaya nol (+0.4775), berbeda dari EXP-005/006 yang
  sudah negatif di 0 bps/side (EXP-007 §18.2).

Pertanyaan EXP-008: apakah **mitigasi stasionaritas gabungan** (regime high
+ SL/TP ATR-multiple + cooldown) dapat menstabilkan gross edge Swing
Breakout sehingga bertahan positif di seluruh periode dataset (OOS train &
test) pada biaya venue nyata (1.0 bps/side)? Ini bukan parameter mining —
ketiga mitigasi adalah **mekanisme risk/regime yang sudah teruji** (EXP-003,
EXP-004, EXP-001 §19.6) yang diterapkan sebagai satu konfigurasi frozen.

Jika EXP-008 gagal (kombinasi mitigasi tidak menstabilkan edge), bukti
menunjukkan gross edge Swing Breakout tidak dapat dijadikan tradable oleh
mitigasi yang tersedia pada biaya realistis — arah lanjutan adalah
timeframe/instrument lain atau menutup line (EXP-007 §18.3).

Hasil EXP-008 (§15–§18): mitigasi gabungan **memperbaiki seluruh dimensi
profil edge** — expectancy naik 22× (+0.117 → +2.621), breakeven 1.32 → ≈ 8.8
bps/side (6.7×), Max DD −78%, combos 3/5 → 5/5, XAGUSD tetap positif (tipis),
negatif pada grid biaya hanya di 10 bps/side (vs 2 bps di EXP-007). **Namun
stasionaritas tetap gagal**: OOS train −0.6073 (negatif), 2/4 slice temporal
positif — edge masih terkonsentrasi di periode akhir (period-4-of-4 +11.69).

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
| Swing high fractal | Puncak lokal (fractal) dengan left/right candle di kedua sisi (ADR-003, ENG-002 §7.1) |
| SWING_HIGH     | Event: fractal swing high terdeteksi (ADR-003)        |
| PRICE_CONFIRMATION | Event: close > highest high N-bar sebelumnya (ENG-002 §7.3) |
| Breakout       | Penembusan level (di sini: level swing-high fractal) |
| Regime         | Label volatilitas per candle (ATR short vs long, ARC-008 §14) |
| bps/side       | Basis point biaya per sisi (1 bps = 0.01%)            |
| Cooldown       | Jeda minimum antar sinyal (ENG-003 §8.1)              |
| Timeframe      | Periode candle (H1, H4, …) — RSH-002 §6              |

---

# 6. Hypothesis

Per RSH-001 §7.1:

> Kondisi **X** (deteksi/Event) menghasilkan
> edge pada **Symbol** (Y) timeframe (**Z**).

Hipotesis EXP-008 (pre-registered):

> **Menerapkan mitigasi stasionaritas gabungan (regime volatilitas HIGH —
> ATR short >= ATR long; SL/TP ATR-multiple SL 1.0 / TP 4.0; cooldown 10)
> pada edge Swing Breakout fractal-structure XAUUSD H4 (EXP-007 — gross edge
> positif di biaya nol namun tidak stasioner temporal) menghasilkan expectancy
> positif DAN stasioner (OOS train & test positif) setelah biaya eksekusi
> venue nyata (1.0 bps/side).**

Kriteria (RSH-001 §7.2):

- falsifiable: keputusan ditentukan oleh kriteria terukur (§13);
- terikat dataset dan konfigurasi spesifik (§7, §9);
- dinyatakan sebelum experiment dijalankan (dokumen ini).

Catatan: hipotesis ini **tidak** mengasumsikan mitigasi pasti bekerja —
EXP-003 (regime) dan EXP-004 (SL/TP) sudah diuji pada line RSI Trendline
Breakout yang berbeda strategi; EXP-008 menguji ketiganya **sekaligus** pada
Swing Breakout. Pertanyaan terukur adalah apakah kombinasi ini menstabilkan
edge yang ada. Jika SUPPORTED, arah riset lanjutan terbuka (pemisahan
kontribusi tiap mitigasi, atau lanjut ke uji tradable). Jika REJECTED
(bahkan dengan mitigasi gabungan edge tidak stasioner/negatif), bukti
menunjukkan gross edge Swing Breakout tidak dapat distabilkan oleh mekanisme
risk/regime yang tersedia (EXP-007 §18.3).

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
2026-04-14, lebih pendek dari H1 2026-05-26). Dataset immutable (Article 13,
ARC-004). Identik EXP-006/EXP-007 §7.

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
| Provenance                | Export terpisah (bukan agregasi H1); identik EXP-006/EXP-007 §7 |

Aturan tertera konsisten dengan ARC-004 §7/§8 dan `validator.py`.

---

# 8. Strategy — Swing Breakout (Fractal Structure)

Strategi yang diuji **identik dengan EXP-007** — plugin `swing_breakout`
(`src/mre/strategies/exp007.py`, ARC-ACT-010), **tidak diubah** untuk
EXP-008. Perbedaan hanya pada konfigurasi (mitigasi, §9), bukan pada
definisi sinyal:

```text
TRIGGER:       SWING_HIGH           (fractal swing high — level resistensi
                                     struktural, ADR-003)
CONFIRMATION:  PRICE_CONFIRMATION   (close > highest high N-bar — penembusan
                                     level dalam window, ENG-002 §7.3)
SIGNAL:        LONG
```

Semantik: sinyal LONG muncul ketika sebuah swing-high fractal terbentuk
(menetapkan level struktural) dan, dalam `window` (5) candle setelahnya,
sebuah price confirmation menembus level tersebut (close > highest high
N-bar, yang mencakup level swing-high). Candle keputusan = candle breakout
(price confirmation); fill terjadi di open bar berikutnya setelah seluruh
konstituen knowable (E-1, SPEC-003 — "entry pada candle breakout" merujuk
candle keputusan, bukan fill, E-10). Detail lengkap: EXP-007 §8.

Catatan arsitektur: EventEngine tetap menghitung RSI (kontrak pipeline) namun
strategi `swing_breakout` **tidak mengkonsumsi** Event berbasis RSI.

---

# 9. Configuration (Frozen)

Konfigurasi dikunci (frozen) sebelum run (RSH-002 §9). Seluruh parameter
**menyamai EXP-007 §9** (venue cost 1.0 bps/side, dataset H4, tanpa perubahan
event/indicator/statistics) **kecuali tiga mitigasi stasionaritas** yang
ditandai (M):

- §9.3 Signal: `cooldown` 0 → **10** (M);
- §9.4 Execution: tambah `stop_loss_atr` 1.0 / `take_profit_atr` 4.0 (M);
- §9.5 Regime: `selected_regime` (none) → **"high"** (M).

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
| cooldown      | **10** (M) |

## 9.4 Execution

| Parameter     | Value |
| ------------- | ----- |
| position_size | 1.0   |
| commission_rate | 0.00003 |
| slippage_rate | 0.00007 |
| hold_bars     | 10    |
| stop_loss     | -     |
| take_profit   | -     |
| stop_loss_atr | **1.0** (M) |
| take_profit_atr | **4.0** (M) |
| atr_period    | 14    |

Venue cost model: 1.0 bps/side total (commission 0.3 bps + slippage 0.7 bps),
identik EXP-002/005/006/007 §9.

## 9.5 Regime

| Parameter     | Value |
| ------------- | ----- |
| atr_short_period | 14 |
| atr_long_period | 100 |
| selected_regime | **"high"** (M) |

## 9.6 Statistics

| Parameter     | Value |
| ------------- | ----- |
| min_sample    | 30    |

---

# 10. Execution Assumptions

Identik EXP-007 §10 (semantik terinci di SPEC-003/SPEC-004, E-9/E-10),
dengan tambahan SL/TP ATR-multiple:

- Entry: **open bar berikutnya** setelah Signal **knowable** — "entry di
  candle breakout" merujuk candle keputusan, bukan fill (E-10);
- Exit: SL/TP ATR-multiple dievaluasi per bar (level SL = entry − 1.0 × ATR,
  TP = entry + 4.0 × ATR, ATR period 14; di-resolve pada entry dari ATR
  `entry_bar − 1` — bar terakhir yang telah ditutup, E-2/SPEC-004 §4.1 —
  tanpa lookahead — `_resolve_stop_take`, RQ-007); SL diprioritaskan atas
  TP dalam bar yang sama (konservatif, SPEC-004 §4.3); gap-through-open →
  exit di open (SPEC-004 §4.4); jika tidak ter-trigger, exit hold 10 bar
  (**close** bar `entry_bar + hold_bars`, net of costs);
- biaya per sisi: commission 3e-05 + slippage 7e-05 (1.0 bps/side total);
- regime filter: hanya sinyal yang dikonfirmasi pada candle berlabel regime
  HIGH (ATR short 14 >= ATR long 100) yang ditradingkan (`select_regime`).

---

# 11. Variables

- **Independent**: mitigasi stasionaritas gabungan (regime high + SL/TP
  ATR-multiple + cooldown — satu nilai, frozen, bukan grid);
- **Dependent**: metrics §12 (expectancy, PF, net P&L, win rate, dll.);
- **Controlled/frozen**: seluruh parameter §9 (kecuali mitigasi §9.3–§9.5),
  dataset §7, biaya venue.

---

# 12. Baseline Reference

- **EXP-007 kontrol** (Swing Breakout, H4, 1.0 bps/side, tanpa mitigasi —
  EXP-007 §15.1): expectancy +0.1170, PF 1.013, win rate 0.508, n=425;
  breakeven ≈ 1.32 bps/side; OOS train −1.8114 / test +4.2421; 1/4 slice
  positif, 3/5 combos positif.
- **Konteks mitigasi per line**: EXP-003 (regime high pada RSI line) —
  expectancy 0.8887 @ 1.0 bps/side (n=698), breakeven 3.44 bps, OOS train
  +0.1297 & test +2.4853 (stasioner); EXP-004 (SL/TP 1.0/4.0 pada RSI line) —
  breakeven 3.31 bps, OOS stasioner, robustness membaik, namun breakeven <
  3.44 kontrol. Mitigasi ini belum pernah diuji pada Swing Breakout.

Kriteria keberhasilan pre-registered (§13) bersifat **absolut** terhadap
ekspektasi peneliti, bukan relatif terhadap EXP-007: mitigasi dikatakan
sukses jika expectancy > 0 DAN OOS train & test > 0 pada 1.0 bps/side.

---

# 13. Decision Criteria (pre-registered)

```text
SUPPORTED
Jika pada skenario representative (1.0 bps/side, konfigurasi frozen §9):
  - expectancy > 0 dengan n >= min_sample (30);
  - biaya breakeven/side >= 1.0 bps (setidaknya menutup biaya venue);
  - OOS test expectancy > 0 (edge bertahan out-of-sample);
  - OOS train expectancy > 0 (stasionaritas — kriteria yang GAGAL di
    EXP-007, target utama mitigasi).

REJECTED
Jika salah satu kriteria SUPPORTED tidak terpenuhi.
```

Interpretasi tambahan (bukan keputusan, untuk konteks):

- jika SUPPORTED, mitigasi gabungan menstabilkan gross edge Swing Breakout —
  langkah lanjutan: pisahkan kontribusi tiap mitigasi (regime/SL-TP/cooldown)
  atau lanjut ke evaluasi tradable (seperti EXP-003 §17.5);
- jika REJECTED, khususnya jika OOS train masih negatif, kombinasi mitigasi
  tidak menstabilkan edge — kandidat berikutnya (EXP-007 §18.3): uji
  timeframe/instrument lain, atau menutup line Swing Breakout.

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

Note: EXP-008 dijalankan sebelum standar E-8; blok ini dokumentasi
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

# 15. Run (TODO-049)

Report: `experiments/EXP-008/EXP-008_report.md` (Code Version `5ea484e`).
Konfigurasi frozen EXP-008 (Swing Breakout fractal-structure pada XAUUSD H4,
venue cost 1.0 bps/side, regime high + SL/TP ATR 1.0/4.0 + cooldown 10)
dijalankan tanpa modifikasi.

## 15.1 Representative Scenario (1.0 bps/side)

| Metric        | Value |
| ------------- | ----- |
| Trade Count   | 167   |
| Win Rate      | 0.359281 |
| Loss Rate     | 0.640719 |
| Average Win   | 25.4145 |
| Average Loss  | 10.1603 |
| Risk/Reward   | 2.50135 |
| Expectancy    | +2.62105 |
| Profit Factor | 1.40262 |
| Gross Profit  | 1524.87 |
| Gross Loss    | 1087.15 |
| Net P&L       | +437.715 |
| Max Drawdown  | 207.468 |
| Winning Streak| 3     |
| Losing Streak | 8     |

Perbandingan vs kontrol EXP-007 (Swing Breakout, H4, 1.0 bps/side, tanpa
mitigasi — EXP-007 §15.1):

| Metric        | EXP-007 (tanpa mitigasi) | EXP-008 (mitigasi gabungan) | Δ     |
| ------------- | ----------------------- | --------------------------- | ----- |
| Expectancy    | +0.1170                 | +2.6211                     | +22.4×|
| Profit Factor | 1.0135                  | 1.4026                      | +38.4%|
| Net P&L       | +49.74                  | +437.72                     | +8.8× |
| Win Rate      | 0.5082                  | 0.3593                      | −29.3%|
| Max DD        | 923.06                  | 207.47                      | −77.5%|
| Trade Count   | 425                     | 167                         | −60.7%|

Interpretasi: mitigasi gabungan **mengubah profil trade secara radikal** —
win rate turun (0.508 → 0.359) namun Risk/Reward naik drastis (0.98 → 2.50)
karena SL/TP ATR 1.0/4.0 memotong kerugian lebih dini (avg loss 17.67 →
10.16) sementara avg win naik (17.33 → 25.41). Expectancy naik 22× dan Max
DD turun 77.5%. Regime high + cooldown mengurangi trade count (425 → 167) —
memfilter sinyal ke periode ber-volatilitas tinggi yang memang tempat edge
berada (EXP-007 §17.1).

## 15.2 Zero-Cost Context (grid biaya, variabel bebas §14)

| Scenario     | comm      | slip      | Total bps/side | Expectancy | PF     | Net P&L    |
| ------------ | --------- | --------- | -------------- | ---------- | ------ | ---------- |
| Zero cost    | 0         | 0         | 0              | +2.9039    | 1.4567 | +484.95    |
| ECN rep.     | 0.00003   | 0.00007   | 1.0            | +2.6211    | 1.4026 | +437.72    |
| Sintetis 2+2 | 0.0002    | 0.0002    | 4.0            | +1.4755    | 1.2045 | +246.41    |
| Sintetis 5+5 | 0.0005    | 0.0005    | 10             | −0.3561    | 0.9572 | −59.47     |

Temuan kunci: **toleransi biaya jauh lebih besar** — breakeven ≈ 8.8 bps/side
(vs ≈ 1.32 bps di EXP-007); expectancy tetap positif bahkan di 4 bps/side
(sintetis grid M7) dan hanya negatif di 10 bps/side (vs negatif mulai 2 bps
di EXP-007).

## 15.3 Breakeven Cost

Interpolasi grid biaya: pada 4 bps/side (comm=0.0002) +1.4755, pada 10
bps/side (comm=0.0005) −0.3561 → slope ≈ −0.31/bps → **breakeven ≈ 8.8
bps/side**. Kriteria "breakeven >= 1.0 bps" (§13) **TERPENUHI** (lebar).
Sebagai konteks: ini breakeven **tertinggi di seluruh line XAUUSD** — 8.8×
di atas biaya venue 1.0 bps (vs EXP-007 yang hanya ~0.32 bps margin).

---

# 16. Out-of-Sample Testing (TODO-049)

Metodologi per **RSH-003 §6/§7**: split kronologis (no leakage, no
retroactive allocation); strategi frozen (konfigurasi EXP-008, 1.0 bps/side)
dijalankan tanpa perubahan pada kedua segmen. Reuse `run_on_slice`
(ARC-ACT-013).

Report: `experiments/EXP-008/EXP-008_oos.md` (Code Version `5ea484e`).

Split point: index 18.771 (2021-04-01 08:00 UTC) — 70% train, 30% test
(mekanisme identik EXP-007 §16).

| Metric        | Baseline | Train  | Test   | Δ Test/Train |
| ------------- | -------- | ------ | ------ | ------------ |
| Trade Count   | 167      | 114    | 53     | -            |
| Win Rate      | 0.3593   | 0.3421 | 0.3962 | -            |
| Expectancy    | +2.6211  | −0.6073 | +9.5649 | −1674.9%   |
| Profit Factor | 1.4026   | 0.8857 | 2.0526 | +131.8%      |
| Net P&L       | +437.72  | −69.23 | +506.94 | −832.2%   |
| Max DD        | 207.47   | 189.11 | 87.59  | -            |
| Sufficient    | True     | True   | True   | -            |

Interpretasi:

- **test positif** (+9.5649, PF 2.05) — edge sangat kuat out-of-sample pada
  segmen akhir;
- **train negatif** (−0.6073) — edge TIDAK stasioner; paruh awal dataset
  merugi, keuntungan terkonsentrasi di paruh akhir (konsisten §17.1
  period-4-of-4 +11.69);
- kriteria §13 (OOS test & train > 0) **TIDAK TERPENUHI** karena train negatif.

Catatan: dibanding EXP-007 (train −1.8114 / test +4.2421), mitigasi
**memperbaiki kedua segmen** (train −1.81 → −0.61, test +4.24 → +9.56) namun
train masih negatif — perbaikan, bukan stasionaritas.

---

# 17. Robustness (TODO-049)

Metodologi per **RSH-003 §10**: strategi frozen (konfigurasi EXP-008, 1.0
bps/side) dijalankan tanpa perubahan. Descriptive only; thresholds per
RSH-004.

Report: `experiments/EXP-008/EXP-008_robustness.md` (Code Version `5ea484e`).

## 17.1 Time Period Stability (4 slices)

| Slice          | Trades | Win Rate | Expectancy | PF     | Net P&L   | Max DD   |
| -------------- | ------ | -------- | ---------- | ------ | --------- | -------- |
| period-1-of-4  | 45     | 0.4667   | +0.8363    | 1.1725 | +37.63    | 57.33    |
| period-2-of-4  | 38     | 0.2895   | −2.8154    | 0.4780 | −106.99   | 110.78   |
| period-3-of-4  | 36     | 0.2222   | −0.4656    | 0.9198 | −16.76    | 73.43    |
| period-4-of-4  | 46     | 0.4348   | +11.6854   | 2.2182 | +537.53   | 87.59    |

Interpretasi: **2/4 slice positif** (naik dari 1/4 di EXP-007) — periode
terakhir (period-4-of-4) sangat kuat (+11.69, PF 2.22), periode pertama
(period-1-of-4) kini tipis positif (+0.84, naik dari −2.15 di EXP-007),
namun dua slice tengah (period-2/3) masih merugi. Konsisten dengan OOS train
negatif: edge tetap terkonsentrasi di periode akhir, walau tidak se-ekstrem
EXP-007 (slice pertama sudah membaik).

## 17.2 Cross-Market (XAGUSD)

| Market | Trades | Win Rate | Expectancy | PF     | Net P&L | Max DD |
| ------ | ------ | -------- | ---------- | ------ | ------- | ------ |
| XAGUSD | 469    | 0.3710   | +0.0216    | 1.2153 | +10.15  | 4.80   |

Interpretasi: XAGUSD **tipis positif** (+0.0216, n=469, PF 1.22) — edge
ter-reproduksi lemah di market lain (catatan: XAGUSD diuji pada timeframe H1,
dataset XAGUSD H4 tidak tersedia). Konsisten dengan EXP-007 (+0.0056).

## 17.3 Execution Cost (synthetic grid)

| comm/slip     | Expectancy | PF    |
| ------------- | ---------- | ----- |
| 0 / 0         | +2.9039    | 1.4567|
| 0.0002 / 0    | +2.1823    | 1.3208|
| 0.0005 / 0    | +1.1000    | 1.1470|
| 0 / 0.0002    | +2.1971    | 1.3252|
| 0 / 0.0005    | +1.4480    | 1.2026|
| 0.0002/0.0002 | +1.4755    | 1.2045|
| 0.0005/0.0005 | −0.3561    | 0.9572|

Interpretasi: **seluruh grid non-10bps positif** — negatif hanya pada 10
bps/side (0.0005/0.0005); dibanding EXP-007 yang sudah negatif di 2 bps/side,
toleransi biaya naik drastis (breakeven 1.32 → ≈ 8.8 bps/side).

## 17.4 Parameter Combinations (price_lookback / rsi_period)

| Combo             | Trades | Expectancy | PF    | Net P&L   |
| ----------------- | ------ | ---------- | ----- | --------- |
| 20 / 14 (baseline)| 167    | +2.6211    | 1.4026| +437.72   |
| 10 / 7            | 229    | +2.5475    | 1.3993| +583.37   |
| 10 / 21           | 229    | +2.5475    | 1.3993| +583.37   |
| 30 / 7            | 141    | +3.3358    | 1.5085| +470.34   |
| 30 / 21           | 141    | +3.3358    | 1.5085| +470.34   |

Interpretasi: **5/5 kombinasi positif** (vs 3/5 di EXP-007) — seluruh
kombinasi near-baseline profit, termasuk lookback 30 yang di EXP-007 negatif
(−0.12). Sensitivitas parameter rendah — profil robust terhadap variasi
parameter.

---

# 18. Conclusion

## 18.1 Verdict (pre-registered criteria, §13)

```text
REJECTED
- expectancy pada skenario representative (1.0 bps/side) = +2.6211 > 0
  dengan n = 167 >= min_sample (30): TERPENUHI;
- biaya breakeven/side ≈ 8.8 bps >= 1.0 bps: TERPENUHI (lebar);
- OOS test expectancy = +9.5649 > 0: TERPENUHI;
- OOS train expectancy = −0.6073 > 0 (stasioner): TIDAK TERPENUHI.
```

**3/4 kriteria pre-registered terpenuhi; OOS train (stasionaritas) tidak →
verdict pre-registered REJECTED.**

## 18.2 Implikasi

- **mitigasi gabungan memperbaiki seluruh dimensi profil edge**: expectancy
  +0.117 → +2.621 (22×), breakeven 1.32 → ≈ 8.8 bps/side (6.7×), Max DD
  923 → 207 (−78%), combos 3/5 → 5/5, slices 1/4 → 2/4, XAGUSD tetap positif
  (+0.0056 → +0.0216), negatif pada grid biaya hanya di 10 bps/side (vs 2
  bps di EXP-007);
- **namun stasionaritas tetap gagal**: OOS train −0.6073 (vs −1.8114 di
  EXP-007 — membaik namun masih negatif), 2/4 slice temporal positif —
  keuntungan tetap terkonsentrasi di periode akhir (period-4-of-4 +11.69);
- **mekanisme perbaikan**: SL/TP ATR 1.0/4.0 mengubah profil (win rate turun,
  RR 0.98 → 2.50, avg loss dipotong 43%) + regime high memfilter ke periode
  ber-volatilitas tinggi; ini memperbaiki risk/cost-tolerance secara drastis
  namun tidak menciptakan stasionaritas — edge di periode tengah (2016–2022)
  tidak muncul walau sudah difilter regime high;
- **kesimpulan**: mitigasi stasionaritas gabungan **gagal sebagai mekanisme
  stasionaritas** (kriteria pre-registered §13) walau berhasil sebagai
  **mekanisme risk/cost-tolerance**. Edge Swing Breakout H4 tetap non-
  stasioner temporal — bukan karena biaya, bukan karena over-trading, bukan
  karena volatilitas, melainkan karena struktur tren XAUUSD berubah antar
  periode (2022–2026 bullish) yang tidak dapat "dipaksa stasioner" oleh
  filter.

## 18.3 Keputusan Lanjutan (peneliti)

Hasil EXP-008: baseline, breakeven, dan OOS test terpenuhi (3/4 kriteria),
namun OOS train masih negatif (tidak stasioner). Catatan kehati-hatian:

- verdict berdasarkan kriteria pre-registered §13; hasil OOS/robustness
  adalah konteks tambahan (RSH-003, deskriptif);
- mitigasi gabungan adalah **mekanisme risk/cost-tolerance yang sangat
  efektif** (breakeven 8.8 bps/side — tertinggi di line XAUUSD) namun
  **bukan mekanisme stasionaritas** — ini temuan riset yang berguna untuk
  eksperimen strategi lain;
- kandidat langkah berikutnya (bukan parameter mining otomatis):
  1) tutup line Swing Breakout dan akhiri riset edge XAUUSD berbasis harga
     (dua kelas strategi — momentum + struktur — gagal pada H1 dan H4 di
     kriteria stasionaritas; EXP-007 §18.3 kandidat 3), atau
  2) pre-register evaluasi pada timeframe/instrument lain dengan
     pre-registration terpisah (EXP-007 §18.3 kandidat 2), atau
  3) jika line dilanjutkan: mitigasi stasionaritas yang berbeda (mis. regime
     LOW untuk period-2/3, atau filter tren jangka panjang) — memerlukan
     pre-registration terpisah, bukan mining pada EXP-008.

## 18.4 Keputusan Akhir (researcher)

**Line Swing Breakout DITUTUP.** Keputusan peneliti (post-EXP-008): menutup
line Swing Breakout dan **menghentikan riset edge XAUUSD berbasis harga**
untuk sementara. Alasan:

- dua kelas strategi (momentum Price Breakout EXP-005/006 + struktur Swing
  Breakout EXP-007/008) keduanya REJECTED per kriteria pre-registered di
  kriteria **stasionaritas** — kegagalan **lintas kelas strategi** pada H1
  dan H4;
- EXP-008 membuktikan mitigasi (regime/SL-TP/cooldown) memperbaiki
  risk/cost-tolerance namun **tidak dapat menstabilkan edge secara
  temporal** — non-stasionaritas adalah properti struktural dari hubungan
  price-action XAUUSD yang diuji, bukan artefak biaya/eksekusi;
- langkah berikutnya: **audit forensik metodologi & spesifikasi eksperimen**
  (EXP-001..EXP-008) — verifikasi bahwa rejections valid secara metodologis
  dan spesifikasi strategi deterministik sebelum eksperimen baru (dokumen
  audit terpisah).

---

# 19. Record Lifecycle

```text
Defined (spesifikasi + konfigurasi frozen)    <- 2026-08-11 (TODO-048)
    |
Run          <- 2026-08-11 (§15)
    |
Result (metrics dicatat)    <- 2026-08-11 (§15)
    |
OOS / robustness            <- 2026-08-11 (§16/§17)
    |
Conclusion (interpretasi evidence — peneliti, PRD-006 §9)    <- 2026-08-11 (§18)
    |
Reviewed (validasi, RSH-003)
    |
CLOSED (keputusan peneliti — line Swing Breakout ditutup, §18.4)    <- saat ini
```

---

# 20. Traceability

| Item            | Requirement / TODO           |
| --------------- | ---------------------------- |
| Hypothesis      | RSH-001 §7, TODO-048         |
| Spec fields     | RSH-002 §6, TODO-014         |
| Metrics         | RSH-002 §8, FND-008 §25      |
| Reproducibility | FR-010, NFR-001, RSH-002 §9  |
| Venue cost      | RSH-003 §10 (cost dimension) |
| Timeframe       | RSH-002 §6 (timeframe field) |
| Line continuation | EXP-007 §18.3             |
| Strategy plugin | ARC-005 §6, ARC-008 ARC-ACT-010 |
| Regime machinery | ARC-008 §14, EXP-003        |
| SL/TP machinery | RQ-007, EXP-004              |
| Cooldown        | ENG-003 §8.1, ARC-008 ARC-ACT-012 |
| Out-of-sample   | RSH-003 §6/§7, TODO-048      |
| Robustness      | RSH-003 §10, TODO-048        |
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
- `docs/07-experiments/EXP-003_RSI_Trendline_Breakout_Volatility_Regime.md`
- `docs/07-experiments/EXP-004_RSI_Trendline_Breakout_SL_TP_Venue_Cost.md`
- `docs/07-experiments/EXP-007_Swing_Breakout_H4_Fractal_Structure.md`
- `docs/03-engine/ENG-002_Event_Engine.md`
- `docs/03-engine/ENG-003_Signal_Engine.md`
- `docs/03-engine/ENG-005_Simulation_Engine.md`
- `docs/03-engine/ENG-006_Statistics_Engine.md`
- `docs/03-engine/ENG-007_Reporting_Engine.md`
- `docs/01-product/PRD-006_MVP_Definition.md`
- `configs/EXP-008.yaml`

---

# 23. Revision History

| Version | Date       | Changes                                      |
| ------- | ---------- | -------------------------------------------- |
| 1.0.0   | 2026-08-11 | Initial EXP-008 pre-registration (TODO-048): re-test Swing Breakout (EXP-007 REJECTED — 3/4 criteria, OOS train negatif) dengan mitigasi stasionaritas GABUNGAN — regime high (EXP-003 machinery), SL/TP ATR 1.0/4.0 (RQ-007 machinery), cooldown 10 (ENG-003 §8.1); config frozen identik EXP-007 §9 kecuali tiga mitigasi §9.3–§9.5; keputusan peneliti (EXP-007 §18.3 kandidat 1) |
| 1.0.1   | 2026-08-11 | Result (TODO-049): REJECTED per kriteria pre-registered §13 — expectancy +2.6211 @ 1.0 bps/side (n=167 >= 30), breakeven ≈ 8.8 bps/side (keduanya terpenuhi), OOS test +9.5649 positif namun OOS train −0.6073 negatif (tidak stasioner); robustness membaik drastis — 2/4 slice positif, 5/5 combos positif, XAGUSD +0.0216 (tipis), negatif hanya di 10 bps/side; mitigasi = mekanisme risk/cost-tolerance yang sangat efektif namun BUKAN mekanisme stasionaritas (§15–§18) |
| 1.0.2   | 2026-08-11 | Line Swing Breakout DITUTUP (§18.4) — keputusan peneliti: dua kelas strategi (momentum + struktur) keduanya REJECTED di kriteria stasionaritas (H1 + H4); mitigasi tidak dapat menstabilkan edge temporal; langkah berikutnya = audit forensik metodologi & spesifikasi eksperimen (EXP-001..EXP-008) |

---

**Document Status:** Result

**Document ID:** EXP-008

**Version:** 1.0.2
