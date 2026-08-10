---
title: RSI Trendline Breakout - ATR-multiple SL/TP at Venue Cost
document_id: EXP-004
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

purpose: Pre-register EXP-004 (TODO-040) - re-test the high-regime edge with ATR-multiple SL/TP (RQ-007 machinery) at real venue execution costs (1.0 bps/side), which M7 tested only on the synthetic 2-5 bps/side grid
---

# RSI Trendline Breakout - ATR-multiple SL/TP at Venue Cost

> Measure the Market. Discover the Edge.

---

# 1. Purpose

EXP-004 adalah **experiment keempat** MRE (RSH-002 §10 lifecycle - state
sekarang `Defined`, pre-registration). EXP-003 (SUPPORTED) menunjukkan
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
| SL/TP ATR      | Exit rule dini: level dari entry +/- N x ATR entry bar (RQ-007) |
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

SL/TP ATR-multiple di-resolve di entry bar dari ATR (period 14) dengan
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

Per RSH-001 §14:

- **Entry**: open bar berikutnya setelah Signal (next bar open);
- **Exit**: SL/TP ATR-multiple diprioritaskan (mana yang tersentuh lebih
  dulu); jika tidak, exit setelah `hold_bars` (10) bar;
- **Sizing**: `position_size = 1.0` (fixed);
- **Transaction cost**: model venue §9.5 (identik EXP-003);
- **Slippage**: `slippage_rate` pada entry dan exit (conservative);
- **Regime label**: candle pada timestamp konfirmasi sinyal (no lookahead);
- **SL/TP level**: dari ATR di entry bar (no lookahead, ARC-008 §14.2);
- Eksekusi adalah simulasi, bukan live (PRD-006 §9).

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

# 15. Record Lifecycle

```text
Defined (spesifikasi + konfigurasi frozen)    <- 2026-08-10 (pre-registration, TODO-040)
    |
Run (TODO-041, belum dijalankan)
    |
Result (metrics dicatat)
    |
OOS / robustness
    |
Conclusion (interpretasi evidence - peneliti, PRD-006 §9)
    |
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
| SL/TP           | ARC-008 §14.2, RQ-007        |
| Regime filter   | ARC-008 §14, EXP-003 §9.7    |
| Out-of-sample   | RSH-003 §6/§7, TODO-041      |
| Robustness      | RSH-003 §10, TODO-041        |
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

# 19. Revision History

| Version | Date       | Changes                                      |
| ------- | ---------- | -------------------------------------------- |
| 1.0.0   | 2026-08-10 | Initial EXP-004 pre-registration (TODO-040): ATR-multiple SL/TP re-test at real venue costs (1.0 bps/side) on the EXP-003 high-regime edge; config frozen identik EXP-003 + SL 1.0 / TP 4.0 |

---

**Document Status:** Defined

**Document ID:** EXP-004

**Version:** 1.0.0

**End of Document**
