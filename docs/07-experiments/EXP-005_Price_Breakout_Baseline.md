---
title: Price Breakout (Donchian-style) — Baseline
document_id: EXP-005
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

purpose: Pre-register EXP-005 (TODO-042) — first experiment of a NEW strategy line (Price Breakout, Donchian-style) after the RSI Trendline Breakout research line (EXP-001..EXP-004) was formally closed as not demonstrating sufficient tradable edge under realistic venue execution costs
---

# Price Breakout (Donchian-style) — Baseline

> Measure the Market. Discover the Edge.

---

# 1. Purpose

EXP-005 adalah **experiment kelima** MRE (RSH-002 §10 lifecycle — state
sekarang `Defined`, pre-registration). Line research RSI Trendline Breakout
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

Per RSH-001 §14:

- **Entry**: open bar berikutnya setelah Signal (next bar open);
- **Exit**: setelah `hold_bars` (10) bar (tanpa SL/TP pada baseline);
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

# 15. Record Lifecycle

```text
Defined (spesifikasi + konfigurasi frozen)    <- saat ini (2026-08-10, TODO-042)
    |
Run (TODO-043, belum dijalankan)
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
- `docs/07-experiments/EXP-004_RSI_Trendline_Breakout_SL_TP_Venue_Cost.md`
- `docs/03-engine/ENG-002_Event_Engine.md`
- `docs/03-engine/ENG-003_Signal_Engine.md`
- `docs/03-engine/ENG-005_Simulation_Engine.md`
- `docs/03-engine/ENG-006_Statistics_Engine.md`
- `docs/03-engine/ENG-007_Reporting_Engine.md`
- `docs/01-product/PRD-006_MVP_Definition.md`
- `configs/EXP-005.yaml`

---

# 19. Revision History

| Version | Date       | Changes                                      |
| ------- | ---------- | -------------------------------------------- |
| 1.0.0   | 2026-08-10 | Initial EXP-005 pre-registration (TODO-042): Price Breakout (Donchian-style) baseline; line RSI Trendline Breakout ditutup (EXP-001..EXP-004), strategi momentum murni terdaftar sebagai plugin `price_breakout`; config frozen identik EXP-002 (venue cost 1.0 bps/side) |

---

**Document Status:** Defined

**Document ID:** EXP-005

**Version:** 1.0.0

**End of Document**
