---
title: Swing Breakout (Fractal Structure) — H4 Timeframe
document_id: EXP-007
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

purpose: Pre-register EXP-007 (TODO-046) — test a NEW strategy line, Swing Breakout (Fractal Structure), on XAUUSD H4 after the Price Breakout line was formally closed (H1 EXP-005 and H4 EXP-006 both REJECTED — structural failure, negative even at zero cost); a structural-fractal breakout complement distinct from pure price-momentum breakout
---

# Swing Breakout (Fractal Structure) — H4 Timeframe

> Measure the Market. Discover the Edge.

---

# 1. Purpose

EXP-007 adalah **experiment ketujuh** MRE (RSH-002 §10 lifecycle — state
sekarang `Defined`, pre-registration). Line Price Breakout (EXP-005 H1,
EXP-006 H4, plugin `price_breakout`) telah **DITUTUP** per EXP-006 §18.3:
pada kedua timeframe expectancy negatif bahkan di biaya nol (H1 −3.1186,
H4 −7.9576), breakeven < 0 bps/side, OOS train/test keduanya negatif,
0/4 slice temporal, 0/5 combos, XAGUSD negatif — kegagalan struktural,
bukan artefak biaya (EXP-005 §18.2, EXP-006 §18.2).

Keputusan peneliti (EXP-006 §18.3 kandidat 2): lanjutkan dengan **eksplorasi
berbeda** — bukan parameter mining otomatis, melainkan **kelas strategi baru**
yang secara struktural berbeda dari momentum murni yang telah dua kali gagal.

EXP-007 menguji **Swing Breakout (Fractal Structure)**: sinyal LONG muncul
ketika sebuah **swing-high fractal** menetapkan level resistensi struktural
(detektor swing, left/right = 2, ADR-003) dan kemudian **price confirmation**
(close > highest high N-bar, ENG-002 §7.3) **menembus level tersebut** dalam
window konfirmasi. Entry pada candle breakout (price confirmation).

Perbedaan struktural vs Price Breakout (EXP-005/006):

| Aspek      | Price Breakout (EXP-005/006)      | Swing Breakout (EXP-007)            |
| ---------- | --------------------------------- | ----------------------------------- |
| Urutan     | breakout Donchian dulu, fractal   | fractal swing-high dulu, breakout   |
|            | swing-high konfirmasi setelahnya  | menembus level setelahnya           |
| Trigger    | PRICE_CONFIRMATION                | SWING_HIGH                          |
| Confirmation | SWING_HIGH                       | PRICE_CONFIRMATION                  |
| Entry      | candle fractal swing-high         | candle breakout (price confirmation)|
| Filosofi   | momentum murni (Donchian channel) | struktur fractal (level resistance) |

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
N-bar, yang mencakup level swing-high). Entry pada candle breakout (price
confirmation — Event konstituen terbaru, FND-009 §13.5). Parameter diukur
per-bar: pada H4, price_lookback 20 ≈ 5 hari kalender dan hold_bars 10 ≈
2.5 hari — horizon identik EXP-006.

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

Identik EXP-006 §10:

- Entry: next bar open setelah sinyal;
- Exit: hold 10 bar (harga exit = open bar ke-hold_bars, net of costs);
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
Defined (spesifikasi + konfigurasi frozen)    <- saat ini (2026-08-11, TODO-046)
    |
Run (TODO-047, belum dijalankan)
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
- `docs/07-experiments/EXP-006_Price_Breakout_H4_Timeframe.md`
- `docs/03-engine/ENG-002_Event_Engine.md`
- `docs/03-engine/ENG-003_Signal_Engine.md`
- `docs/03-engine/ENG-005_Simulation_Engine.md`
- `docs/03-engine/ENG-006_Statistics_Engine.md`
- `docs/03-engine/ENG-007_Reporting_Engine.md`
- `docs/01-product/PRD-006_MVP_Definition.md`
- `configs/EXP-007.yaml`

---

# 19. Revision History

| Version | Date       | Changes                                      |
| ------- | ---------- | -------------------------------------------- |
| 1.0.0   | 2026-08-11 | Initial EXP-007 pre-registration (TODO-046): Swing Breakout (Fractal Structure) diuji pada XAUUSD H4 setelah line Price Breakout DITUTUP (EXP-006 §18.3); keputusan peneliti — kelas strategi baru secara struktural berbeda dari momentum murni; config frozen identik EXP-006 §9 kecuali strategy → swing_breakout; plugin `swing_breakout` (ARC-ACT-010) |

---

**Document Status:** Defined

**Document ID:** EXP-007

**Version:** 1.0.0
