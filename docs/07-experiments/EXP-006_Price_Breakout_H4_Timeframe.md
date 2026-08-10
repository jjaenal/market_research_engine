---
title: Price Breakout (Donchian-style) — H4 Timeframe
document_id: EXP-006
version: 1.0.0
status: Defined
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

purpose: Pre-register EXP-006 (TODO-044) — re-test the Price Breakout (Donchian-style) strategy on XAUUSD H4 after the H1 baseline (EXP-005) was REJECTED per pre-registered criteria (expectancy negative even at zero cost, breakeven < 0 bps, OOS train/test negative); tests whether the Price Breakout edge is timeframe-specific
---

# Price Breakout (Donchian-style) — H4 Timeframe

> Measure the Market. Discover the Edge.

---

# 1. Purpose

EXP-006 adalah **experiment keenam** MRE (RSH-002 §10 lifecycle — state
sekarang `Defined`, pre-registration). Line Price Breakout (EXP-005, plugin
`price_breakout`) pada H1 telah **REJECTED** per kriteria pre-registered:
expectancy −3.4848 @ 1.0 bps/side (n=3882), bahkan negatif di biaya nol
(−3.1186), OOS train −2.6301 & test −5.2396, 0/4 slice temporal, 0/5 combos,
XAGUSD negatif (EXP-005 §15–§18). Keputusan peneliti (EXP-005 §18.3 kandidat
2): lanjutkan dengan **eksplorasi berbeda pada sumbu berbeda** — bukan
parameter mining otomatis, melainkan uji spesifik apakah edge strategi
bersifat **spesifik timeframe**.

EXP-006 menguji strategi yang **identik** (definisi sinyal, konfigurasi
frozen, biaya venue) pada **timeframe berbeda**: XAUUSD **H4** (bukan H1).
Hipotesis: kegagalan Price Breakout pada H1 mungkin spesifik horizon;
lookback/swing/hold yang sama mengekspresikan horizon waktu ~4× lebih panjang
pada H4 (price_lookback 20 H4-bar ≈ 5 hari kalender vs ~1 hari pada H1;
hold_bars 10 H4-bar ≈ 2.5 hari vs ~10 jam pada H1).

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

Identik EXP-005 §10:

- Entry: next bar open setelah sinyal;
- Exit: hold 10 bar (harga exit = open bar ke-hold_bars, net of costs);
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

# 15. Record Lifecycle

```text
Defined (spesifikasi + konfigurasi frozen)    <- saat ini (2026-08-11, TODO-044)
    |
Run (TODO-045, belum dijalankan)
    |
Result (metrics dicatat)
    |
OOS / robustness
    |
Conclusion (interpretasi evidence — peneliti, PRD-006 §9)
    |
Reviewed (validasi, RSH-003)
```

---

# 16. Traceability

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

# 17. Compliance

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

# 18. References

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

# 19. Revision History

| Version | Date       | Changes                                      |
| ------- | ---------- | -------------------------------------------- |
| 1.0.0   | 2026-08-11 | Initial EXP-006 pre-registration (TODO-044): Price Breakout (Donchian-style) diuji ulang pada XAUUSD H4 setelah line H1 REJECTED (EXP-005 §15–§18); keputusan peneliti (EXP-005 §18.3) — uji spesifik apakah edge bersifat spesifik timeframe; config frozen identik EXP-005 §9 kecuali dataset/timeframe → H4 |

---

**Document Status:** Defined

**Document ID:** EXP-006

**Version:** 1.0.0

**End of Document**
