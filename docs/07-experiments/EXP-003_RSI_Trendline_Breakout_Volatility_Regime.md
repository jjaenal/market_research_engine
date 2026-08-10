---
title: RSI Trendline Breakout — Volatility Regime Segmentation
document_id: EXP-003
version: 1.0.0
status: Defined
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

purpose: Pre-register EXP-003 (TODO-038) — test whether the EXP-002 edge (SUPPORTED at venue costs but non-stationary) is concentrated in the HIGH volatility regime and becomes stationary when filtered via the M7 regime machinery
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

Per RSH-001 §14:

- **Entry**: open bar berikutnya setelah Signal (next bar open);
- **Exit**: setelah `hold_bars` (10) bar;
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

# 15. Record Lifecycle

```text
Defined (spesifikasi + konfigurasi frozen)    ← saat ini (pre-registration)
    ↓ (TODO-038 Create EXP-003)
Run          ← TODO-039 Run EXP-003
    ↓
Result (metrics dicatat)
    ↓
Conclusion (interpretasi evidence — peneliti, PRD-006 §9)
    ↓
Reviewed (validasi, RSH-003)
```

---

# 16. Traceability

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

# 17. Compliance

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

# 19. Revision History

| Version | Date       | Changes                                      |
| ------- | ---------- | -------------------------------------------- |
| 1.0.0   | 2026-08-10 | Initial EXP-003 pre-registration (TODO-038): volatility regime segmentation re-test |

---

**Document Status:** Defined

**Document ID:** EXP-003

**Version:** 1.0.0

**End of Document**
