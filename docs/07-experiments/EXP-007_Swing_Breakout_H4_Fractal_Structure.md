---
title: Swing Breakout (Fractal Structure) — H4 Timeframe
document_id: EXP-007
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

purpose: Pre-register EXP-007 (TODO-046) and record the run (TODO-047) — test a NEW strategy line, Swing Breakout (Fractal Structure), on XAUUSD H4 after the Price Breakout line was formally closed (H1 EXP-005 and H4 EXP-006 both REJECTED — structural failure, negative even at zero cost); a structural-fractal breakout complement distinct from pure price-momentum breakout. Result (1.0.1): REJECTED per pre-registered criteria — baseline expectancy +0.1170 @ 1.0 bps/side (n=425), breakeven ≈ 1.32 bps/side ≥ 1.0 bps, OOS test +4.2421 (positive) but OOS train −1.8114 (negative, NOT stationary); 1/4 slices positive, 3/5 combos positive, XAGUSD +0.0056 (thin positive); first line with a gross edge at zero cost (+0.4775) but temporally non-stationary (EXP-007 §15–§18)
---

# Swing Breakout (Fractal Structure) — H4 Timeframe

> Measure the Market. Discover the Edge.

---

# 1. Purpose

EXP-007 adalah **experiment ketujuh** MRE (RSH-002 §10 lifecycle — state
sekarang `Result`, pre-registration + hasil run). Line Price Breakout
(EXP-005 H1, EXP-006 H4, plugin `price_breakout`) telah **DITUTUP** per
EXP-006 §18.3: pada kedua timeframe expectancy negatif bahkan di biaya nol
(H1 −3.1186, H4 −7.9576), breakeven < 0 bps/side, OOS train/test keduanya
negatif, 0/4 slice temporal, 0/5 combos, XAGUSD negatif — kegagalan
struktural, bukan artefak biaya (EXP-005 §18.2, EXP-006 §18.2).

Keputusan peneliti (EXP-006 §18.3 kandidat 2): lanjutkan dengan **eksplorasi
berbeda** — bukan parameter mining otomatis, melainkan **kelas strategi baru**
yang secara struktural berbeda dari momentum murni yang telah dua kali gagal.

EXP-007 menguji **Swing Breakout (Fractal Structure)**: sinyal LONG muncul
ketika sebuah **swing-high fractal** menetapkan level resistensi struktural
(detektor swing, left/right = 2, ADR-003) dan kemudian **price confirmation**
(close > highest high N-bar, ENG-002 §7.3) **menembus level tersebut** dalam
window konfirmasi. Candle keputusan = candle breakout (price confirmation);
fill terjadi di open bar berikutnya setelah seluruh konstituen knowable
(E-1, SPEC-003, E-10).

Perbedaan struktural vs Price Breakout (EXP-005/006):

| Aspek      | Price Breakout (EXP-005/006)      | Swing Breakout (EXP-007)            |
| ---------- | --------------------------------- | ----------------------------------- |
| Urutan     | breakout Donchian dulu, fractal   | fractal swing-high dulu, breakout   |
|            | swing-high konfirmasi setelahnya  | menembus level setelahnya           |
| Trigger    | PRICE_CONFIRMATION                | SWING_HIGH                          |
| Confirmation | SWING_HIGH                       | PRICE_CONFIRMATION                  |
| Candle keputusan | candle fractal swing-high    | candle breakout (price confirmation)|
| Filosofi   | momentum murni (Donchian channel) | struktur fractal (level resistance) |

Hasil (TODO-047, doc 1.0.1): **REJECTED** per kriteria pre-registered §13 —
expectancy **+0.1170** @ 1.0 bps/side (n=425 >= 30) dan breakeven ≈ 1.32
bps/side >= 1.0 bps terpenuhi (3/4 kriteria), namun OOS **train −1.8114**
(negatif, tidak stasioner) walau OOS test +4.2421 (positif); robustness
1/4 slice positif, 3/5 combos positif, XAGUSD +0.0056 (tipis positif).
Temuan kunci: line ini adalah yang **pertama dengan gross edge** (positif di
biaya nol, +0.4775) — berbeda dari EXP-005/006 — namun edge **tidak
stasioner temporal** (terkonsentrasi di periode akhir) (§15–§18).

---

# 2. Scope

Scope EXP-007:

- pre-registration hypothesis (RSH-001 §7.2);
- dataset: XAUUSD **H4** (`datasets/XAUUSD_H4.csv`, immutable — Article 13),
  identik EXP-006 §7;
- configuration frozen: **identik dengan EXP-006 §9** (venue cost 1.0
  bps/side, tanpa regime filter, tanpa SL/TP) kecuali strategy → swing_breakout;
- strategi **Swing Breakout (Fractal Structure)** (§8) sebagai objek uji —
  plugin baru `swing_breakout` (`src/mre/strategies/exp007.py`, ARC-ACT-010,
  tanpa perubahan arsitektur);
- OOS dan robustness (RSH-003 §6/§7/§10) sebagai kriteria stasionaritas.

Di luar scope EXP-007:

- optimasi parameter (sensitivity/robustness, bukan objek uji baseline);
- regime filter, SL/TP, cooldown (mitigasi — evaluasi lanjutan hanya jika
  baseline SUPPORTED);
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
- EXP-005 (line Price Breakout, H1): REJECTED — expectancy negatif bahkan di
  biaya nol (−3.1186), breakeven < 0 bps, OOS train/test negatif, 0/4 slice
  temporal, 0/5 combos, XAGUSD negatif; kegagalan **struktural** (EXP-005
  §18.2).
- EXP-006 (line Price Breakout, H4): REJECTED — expectancy negatif bahkan di
  biaya nol (−7.9576), OOS train −5.0451 & test −14.2008, 0/4 slice, 0/5
  combos; hipotesis "edge spesifik H4" TIDAK terdukung; line DITUTUP
  (EXP-006 §18.2/§18.3).
- Kesimpulan lintas line + lintas timeframe: strategi berbasis harga (momentum
  breakout) gagal pada H1 dan H4 — XAUUSD tidak menunjukkan edge tradable
  untuk kelas strategi ini pada biaya realistis (EXP-005 §18.2, EXP-006 §18.2).

Pertanyaan EXP-007: apakah **kelas strategi yang berbeda secara struktural**
(level resistance fractal + breakout) menghasilkan edge yang tidak dimiliki
momentum murni? H1 dan H4 telah menolak momentum breakout; struktur fractal
adalah mekanisme entry yang berbeda — bukan varian parameter dari kelas yang
sama. Jika EXP-007 gagal (negatif bahkan di biaya nol), bukti memperkuat
kesimpulan bahwa **XAUUSD H4 tidak tradable untuk strategi berbasis harga**
(dua kelas strategi, dua timeframe, semua gagal).

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
| bps/side       | Basis point biaya per sisi (1 bps = 0.01%)            |
| Timeframe      | Periode candle (H1, H4, …) — RSH-002 §6              |

---

# 6. Hypothesis

Per RSH-001 §7.1:

> Kondisi **X** (deteksi/Event) menghasilkan
> edge pada **Symbol** (Y) timeframe (**Z**).

Hipotesis EXP-007 (pre-registered):

> **Breakout struktur fractal (swing-high fractal menetapkan level resistensi,
> kemudian close menembus level tersebut — dikonfirmasi price confirmation
> dalam window) pada XAUUSD H4 menghasilkan expectancy positif setelah biaya
> eksekusi venue nyata (1.0 bps/side) — kelas strategi struktur-fractal
> berbeda dari momentum murni yang telah gagal pada H1 dan H4 (EXP-005/006).**

Kriteria (RSH-001 §7.2):

- falsifiable: keputusan ditentukan oleh kriteria terukur (§13);
- terikat dataset dan konfigurasi spesifik (§7, §9);
- dinyatakan sebelum experiment dijalankan (dokumen ini).

Catatan: hipotesis ini **tidak** mengasumsikan struktur fractal pasti bekerja —
EXP-005/006 menunjukkan momentum breakout gagal. Pertanyaan terukur adalah
apakah mekanisme entry berbasis level struktural menghasilkan profil berbeda.
Jika SUPPORTED, arah riset lanjutan terbuka (regime/SL/TP/cooldown filter
pada H4, atau uji lintas instrument). Jika REJECTED (negatif bahkan di biaya
nol), bukti menunjukkan kegagalan **lintas kelas strategi** pada XAUUSD H4 —
memperkuat kesimpulan bahwa XAUUSD tidak tradable pada biaya realistis untuk
strategi berbasis harga (EXP-006 §18.2).

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

# 8. Strategy — Swing Breakout (Fractal Structure)

Plugin baru `swing_breakout` (`src/mre/strategies/exp007.py`, ARC-ACT-010).
Tidak ada perubahan pada detector, signal engine, atau engine lain —
strategi hanya mengonsumsi Event yang sudah ada:

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
(price confirmation — Event konstituen terbaru, FND-009 §13.5); **fill**
terjadi di open bar berikutnya setelah seluruh konstituen knowable (E-1,
SPEC-003 — "entry pada candle breakout" merujuk candle keputusan, bukan
fill, E-10). Parameter diukur per-bar: pada H4, price_lookback 20 ≈ 5 hari
kalender dan hold_bars 10 ≈ 2.5 hari — horizon identik EXP-006.

Perbedaan vs Price Breakout (EXP-005/006): di sana Donchian breakout
(PRICE_CONFIRMATION) terjadi dulu dan fractal swing-high (SWING_HIGH)
mengonfirmasi setelahnya; di sini fractal swing-high menetapkan level dulu
dan price confirmation menembusnya. Urutan trigger/confirmation terbalik —
entry pada fase berbeda dari episode breakout.

Catatan arsitektur: EventEngine tetap menghitung RSI (kontrak pipeline) namun
strategi `swing_breakout` **tidak mengkonsumsi** Event berbasis RSI.

---

# 9. Configuration (Frozen)

Konfigurasi dikunci (frozen) sebelum run (RSH-002 §9). Seluruh parameter
**menyamai EXP-006 §9** (venue cost 1.0 bps/side, tanpa regime filter, tanpa
SL/TP, dataset H4) kecuali `strategy_id` → `swing_breakout`.

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
identik EXP-002/005/006 §9.

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

Identik EXP-006 §10 (semantik terinci di SPEC-003/SPEC-004, E-9/E-10):

- Entry: **open bar berikutnya** setelah Signal **knowable** — "entry di
  candle breakout" merujuk candle keputusan, bukan fill (E-10);
- Exit: hold 10 bar (**close** bar `entry_bar + hold_bars`, net of costs);
- tanpa SL/TP absolut atau ATR-multiple;
- biaya per sisi: commission 3e-05 + slippage 7e-05 (1.0 bps/side total).

---

# 11. Variables

- **Independent**: kelas strategi (Swing Breakout fractal-structure — satu
  nilai, frozen, bukan grid);
- **Dependent**: metrics §12 (expectancy, PF, net P&L, win rate, dll.);
- **Controlled/frozen**: seluruh parameter §9, dataset §7, biaya venue.

---

# 12. Baseline Reference

- **EXP-006 kontrol** (Price Breakout, H4, 1.0 bps/side — EXP-006 §15.1):
  expectancy −8.3297, PF 0.429, win rate 0.370, n=1188; sebagai konteks:
  strategi baru dikatakan memberikan nilai riset tambahan jika expectancy
  **> 0** pada 1.0 bps/side dengan n >= 30 (kriteria pre-registered §13).
- **Konteks lintas line**: dua kelas strategi terdahulu (RSI Trendline
  Breakout H1, Price Breakout H1+H4) semuanya REJECTED — expectancy negatif
  bahkan di biaya nol.

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

- jika SUPPORTED, kelas strategi struktur-fractal layak dilanjutkan pada H4
  (evaluasi regime/SL/TP/cooldown sebagai mitigasi lanjutan);
- jika REJECTED, khususnya jika expectancy negatif pada biaya nol, bukti
  menunjukkan kegagalan **lintas kelas strategi** pada XAUUSD H4 — dua kelas
  strategi (momentum breakout + struktur fractal) gagal; memperkuat
  kesimpulan bahwa XAUUSD tidak tradable pada biaya realistis untuk strategi
  berbasis harga (EXP-006 §18.2).

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

Note: EXP-007 dijalankan sebelum standar E-8; blok ini dokumentasi
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

# 15. Run (TODO-047)

Report: `experiments/EXP-007/EXP-007_report.md` (Code Version `2abd670`).
Strategi frozen (konfigurasi EXP-007, Swing Breakout fractal-structure pada
XAUUSD H4, biaya venue 1.0 bps/side, tanpa regime filter, tanpa SL/TP)
dijalankan tanpa modifikasi.

## 15.1 Representative Scenario (1.0 bps/side)

| Metric        | Value |
| ------------- | ----- |
| Trade Count   | 425   |
| Win Rate      | 0.508235 |
| Loss Rate     | 0.491765 |
| Average Win   | 17.3268 |
| Average Loss  | 17.6691 |
| Risk/Reward   | 0.980624 |
| Expectancy    | +0.117027 |
| Profit Factor | 1.01347 |
| Gross Profit  | 3742.58 |
| Gross Loss    | 3692.84 |
| Net P&L       | +49.7363 |
| Max Drawdown  | 923.062 |
| Winning Streak| 8     |
| Losing Streak | 8     |

Perbandingan vs kontrol EXP-006 (Price Breakout H4, 1.0 bps/side, EXP-006
§15.1):

| Metric        | EXP-006 Price Breakout | EXP-007 Swing Breakout | Δ      |
| ------------- | ---------------------- | ---------------------- | ------ |
| Expectancy    | −8.3297                | +0.1170                | > 0    |
| Profit Factor | 0.4295                 | 1.0135                 | > 1    |
| Net P&L       | −9895.63               | +49.74                 | > 0    |
| Win Rate      | 0.3695                 | 0.5082                 | +37.5% |
| Trade Count   | 1188                   | 425                    | −64.2% |

Interpretasi: strategi struktur-fractal **profit** pada biaya venue nyata —
expectancy positif (+0.117), PF > 1, win rate 50.8% (naik drastis dari 36.9%
Price Breakout). Namun margin tipis: net P&L hanya +49.74 dari 425 trade
(≈ 0.117 per trade), avg win hampir sama dengan avg loss (RR 0.98) — kinerja
nyaris netral, didorong oleh periode akhir dataset (lihat §17.1).

## 15.2 Zero-Cost Context (grid biaya, variabel bebas §14)

| Scenario     | comm      | slip      | Total bps/side | Expectancy | PF     | Net P&L    |
| ------------ | --------- | --------- | -------------- | ---------- | ------ | ---------- |
| Zero cost    | 0         | 0         | 0              | +0.4775    | 1.0561 | +202.95    |
| ECN rep.     | 0.00003   | 0.00007   | 1.0            | +0.1170    | 1.0135 | +49.74     |
| Sintetis 2+2 | 0.0002    | 0.0002    | 4.0            | −0.9645    | 0.8954 | −409.90    |
| Sintetis 5+5 | 0.0005    | 0.0005    | 10             | −3.1274    | 0.6978 | −1329.16   |

Temuan kunci: **gross edge ADA** — expectancy positif pada biaya nol
(+0.4775), berbeda dari EXP-005/006 yang sudah negatif di 0 bps/side. Namun
expectancy turun cepat seiring biaya: breakeven ≈ 1.32 bps/side, hanya
sedikit di atas ambang kriteria 1.0 bps (§13).

## 15.3 Breakeven Cost

Interpolasi grid biaya: pada 0 bps/side expectancy +0.4775, pada 2 bps/side
(comm=0.0002) −0.2435 → slope ≈ −0.36/bps → **breakeven ≈ 1.32 bps/side**.
Kriteria "breakeven >= 1.0 bps" (§13) **TERPENUHI** (tipis). Sebagai konteks:
margin toleransi biaya kecil — hanya ~0.32 bps di atas biaya venue 1.0 bps.

---

# 16. Out-of-Sample Testing (TODO-047)

Metodologi per **RSH-003 §6/§7**: split kronologis (no leakage, no
retroactive allocation); strategi frozen (konfigurasi EXP-007, 1.0 bps/side)
dijalankan tanpa perubahan pada kedua segmen. Reuse `run_on_slice`
(ARC-ACT-013).

Report: `experiments/EXP-007/EXP-007_oos.md` (Code Version `2abd670`).

Split point: index 18.771 (2021-04-01 08:00 UTC) — 70% train, 30% test
(mekanisme identik EXP-006 §16).

| Metric        | Baseline | Train  | Test   | Δ Test/Train |
| ------------- | -------- | ------ | ------ | ------------ |
| Trade Count   | 425      | 289    | 134    | -            |
| Win Rate      | 0.5082   | 0.4983 | 0.5299 | -            |
| Expectancy    | +0.1170  | −1.8114 | +4.2421 | −334.2%    |
| Profit Factor | 1.0135   | 0.7527 | 1.3619 | +80.9%       |
| Net P&L       | +49.74   | −523.49 | +568.44 | −208.6%   |
| Max DD        | 923.06   | 612.71 | 327.94 | -            |
| Sufficient    | True     | True   | True   | -            |

Interpretasi:

- **test positif** (+4.2421) — edge bertahan out-of-sample pada segmen akhir;
- **train negatif** (−1.8114) — edge TIDAK stasioner; paruh awal dataset
  merugi, keuntungan terkonsentrasi di paruh akhir (konsisten §17.1
  period-4-of-4 +5.90);
- kriteria §13 (OOS test & train > 0) **TIDAK TERPENUHI** karena train negatif.

---

# 17. Robustness (TODO-047)

Metodologi per **RSH-003 §10**: strategi frozen (konfigurasi EXP-007, 1.0
bps/side) dijalankan tanpa perubahan. Descriptive only; thresholds per
RSH-004.

Report: `experiments/EXP-007/EXP-007_robustness.md` (Code Version `2abd670`).

## 17.1 Time Period Stability (4 slices)

| Slice          | Trades | Win Rate | Expectancy | PF     | Net P&L   | Max DD   |
| -------------- | ------ | -------- | ---------- | ------ | --------- | -------- |
| period-1-of-4  | 115    | 0.4870   | −2.1451    | 0.7022 | −246.69   | 340.34   |
| period-2-of-4  | 92     | 0.4891   | −1.1392    | 0.8089 | −104.81   | 150.86   |
| period-3-of-4  | 101    | 0.4653   | −2.7930    | 0.6752 | −282.10   | 439.96   |
| period-4-of-4  | 115    | 0.5826   | +5.9003    | 1.4705 | +678.54   | 306.59   |

Interpretasi: **1/4 slice positif** — hanya periode terakhir (period-4-of-4)
yang profit; tiga slice pertama semuanya merugi. Konsisten dengan OOS train
negatif: edge terkonsentrasi di periode akhir (≈ 2022-2026).

## 17.2 Cross-Market (XAGUSD)

| Market | Trades | Win Rate | Expectancy | PF     | Net P&L | Max DD |
| ------ | ------ | -------- | ---------- | ------ | ------- | ------ |
| XAGUSD | 1116   | 0.4830   | +0.0056    | 1.0396 | +6.20   | 19.13  |

Interpretasi: XAGUSD **tipis positif** (+0.0056, n=1116) — edge ter-reproduksi
lemah di market lain (catatan: XAGUSD diuji pada timeframe H1, dataset XAGUSD
H4 tidak tersedia). Ini berbeda dari EXP-005/006 yang XAGUSD-nya negatif.

## 17.3 Execution Cost (synthetic grid)

| comm/slip     | Expectancy | PF    |
| ------------- | ---------- | ----- |
| 0 / 0         | +0.4775    | 1.0561|
| 0.0002 / 0    | −0.2435    | 0.9725|
| 0.0005 / 0    | −1.3250    | 0.8591|
| 0 / 0.0002    | −0.2435    | 0.9725|
| 0 / 0.0005    | −1.3250    | 0.8591|
| 0.0002/0.0002 | −0.9645    | 0.8954|
| 0.0005/0.0005 | −3.1274    | 0.6978|

Interpretasi: **gross edge ada** (0/0 positif +0.4775) namun margin tipis —
negatif pada ≥ 2 bps/side; breakeven ≈ 1.32 bps/side. Bukan kegagalan
struktural seperti EXP-005/006, tapi toleransi biaya yang sempit.

## 17.4 Parameter Combinations (price_lookback / rsi_period)

| Combo             | Trades | Expectancy | PF    | Net P&L   |
| ----------------- | ------ | ---------- | ----- | --------- |
| 20 / 14 (baseline)| 425    | +0.1170    | 1.0135| +49.74    |
| 10 / 7            | 614    | +0.9026    | 1.1154| +554.19   |
| 10 / 21           | 614    | +0.9026    | 1.1154| +554.19   |
| 30 / 7            | 362    | −0.1209    | 0.9867| −43.76    |
| 30 / 21           | 362    | −0.1209    | 0.9867| −43.76    |

Interpretasi: **3/5 kombinasi positif** — lookback lebih pendek (10)
memberikan hasil lebih baik (+0.90), baseline 20 tipis positif, lookback 30
negatif. Varian positif menunjukkan sensitivitas terhadap parameter namun
bukan kegagalan seragam.

---

# 18. Conclusion

## 18.1 Verdict (pre-registered criteria, §13)

```text
REJECTED
- expectancy pada skenario representative (1.0 bps/side) = +0.1170 > 0
  dengan n = 425 >= min_sample (30): TERPENUHI;
- biaya breakeven/side ≈ 1.32 bps >= 1.0 bps: TERPENUHI (tipis);
- OOS test expectancy = +4.2421 > 0: TERPENUHI;
- OOS train expectancy = −1.8114 > 0 (stasioner): TIDAK TERPENUHI.
```

**3/4 kriteria pre-registered terpenuhi; OOS train (stasionaritas) tidak →
verdict pre-registered REJECTED.**

## 18.2 Implikasi

- **pertama kalinya sebuah line memiliki gross edge** — expectancy positif di
  biaya nol (+0.4775), berbeda dari EXP-005/006 yang sudah negatif di 0 bps/side;
- **namun edge tidak stasioner temporal**: OOS train negatif (−1.8114), 1/4
  slice temporal positif (hanya period-4-of-4 +5.90) — keuntungan
  terkonsentrasi di periode akhir (≈ 2022-2026);
- **toleransi biaya sempit**: breakeven ≈ 1.32 bps/side, hanya ~0.32 bps di
  atas biaya venue 1.0 bps — margin tipis yang mudah terhapus oleh variasi
  eksekusi;
- robustness campuran: 3/5 combos positif (lookback 10 terbaik +0.90),
  XAGUSD tipis positif (+0.0056) — sinyal positif lemah, tidak konsisten kuat;
- dibanding EXP-006 (Price Breakout H4): kelas strategi struktur-fractal
  jelas lebih baik dari momentum murni pada H4 (expectancy +0.117 vs −8.33,
  win rate 50.8% vs 37.0%), namun belum cukup untuk verdict SUPPORTED.

## 18.3 Keputusan Lanjutan (peneliti)

Hasil EXP-007: baseline & breakeven terpenuhi, OOS test positif, namun OOS
train negatif (tidak stasioner) dan 1/4 slice temporal positif. Catatan
kehati-hatian:

- verdict berdasarkan kriteria pre-registered §13; hasil OOS/robustness
  adalah konteks tambahan (RSH-003, deskriptif);
- gross edge (positif di biaya nol) adalah temuan baru yang tidak dimiliki
  line sebelumnya — sinyal bahwa kelas strategi ini layak dieksplorasi lebih
  lanjut walau baseline tidak lolos kriteria stasionaritas;
- kandidat langkah berikutnya (bukan parameter mining otomatis):
  1) pre-register evaluasi lanjutan pada Swing Breakout dengan mitigasi
     stasionaritas: regime filter (volatility regime, machinery EXP-003),
     SL/TP ATR-multiple (RQ-007 machinery), atau cooldown untuk mengurangi
     over-trading di periode non-stasioner, atau
  2) uji ulang Swing Breakout pada timeframe/instrument lain dengan
     pre-registration terpisah, atau
  3) menutup line Swing Breakout juga dan menghentikan riset edge XAUUSD.

---

# 19. Record Lifecycle

```text
Defined (spesifikasi + konfigurasi frozen)    <- 2026-08-11 (TODO-046)
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
| Hypothesis      | RSH-001 §7, TODO-046         |
| Spec fields     | RSH-002 §6, TODO-014         |
| Metrics         | RSH-002 §8, FND-008 §25      |
| Reproducibility | FR-010, NFR-001, RSH-002 §9  |
| Venue cost      | RSH-003 §10 (cost dimension) |
| Timeframe       | RSH-002 §6 (timeframe field) |
| Line closure    | EXP-006 §18.3                |
| Strategy plugin | ARC-005 §6, ARC-008 ARC-ACT-010 |
| Out-of-sample   | RSH-003 §6/§7, TODO-047      |
| Robustness      | RSH-003 §10, TODO-047        |
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
- `docs/07-experiments/EXP-006_Price_Breakout_H4_Timeframe.md`
- `docs/03-engine/ENG-002_Event_Engine.md`
- `docs/03-engine/ENG-003_Signal_Engine.md`
- `docs/03-engine/ENG-005_Simulation_Engine.md`
- `docs/03-engine/ENG-006_Statistics_Engine.md`
- `docs/03-engine/ENG-007_Reporting_Engine.md`
- `docs/01-product/PRD-006_MVP_Definition.md`
- `configs/EXP-007.yaml`

---

# 23. Revision History

| Version | Date       | Changes                                      |
| ------- | ---------- | -------------------------------------------- |
| 1.0.0   | 2026-08-11 | Initial EXP-007 pre-registration (TODO-046): Swing Breakout (Fractal Structure) diuji pada XAUUSD H4 setelah line Price Breakout DITUTUP (EXP-006 §18.3); keputusan peneliti — kelas strategi baru secara struktural berbeda dari momentum murni; config frozen identik EXP-006 §9 kecuali strategy → swing_breakout; plugin `swing_breakout` (ARC-ACT-010) |
| 1.0.1   | 2026-08-11 | Result (TODO-047): REJECTED per kriteria pre-registered §13 — expectancy +0.1170 @ 1.0 bps/side (n=425 >= 30) dan breakeven ≈ 1.32 bps/side (keduanya terpenuhi), OOS test +4.2421 positif namun OOS train −1.8114 negatif (tidak stasioner); 1/4 slice temporal positif, 3/5 combos positif, XAGUSD +0.0056 (tipis); gross edge pertama di line XAUUSD (positif di biaya nol +0.4775) namun toleransi biaya sempit dan edge tidak stasioner temporal (§15–§18) |

---

**Document Status:** Result

**Document ID:** EXP-007

**Version:** 1.0.1
