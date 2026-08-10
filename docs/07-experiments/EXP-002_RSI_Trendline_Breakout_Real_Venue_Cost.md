---
title: RSI Trendline Breakout — Real Venue Execution Cost
document_id: EXP-002
version: 1.0.1
status: Result
category: Experiment
owner: Market Research Engine Core Team
created: 2026-08-09
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

referenced_by:
  - FND-006
  - FND-008

purpose: Record EXP-002 run (TODO-036) — re-test the EXP-001 edge under real retail XAUUSD venue execution costs (spread + commission + slippage); verdict SUPPORTED per pre-registered criteria
---

# RSI Trendline Breakout — Real Venue Execution Cost

> Measure the Market. Discover the Edge.

---

# 1. Purpose

EXP-002 adalah **experiment kedua** MRE (RSH-002 §10 lifecycle — state
sekarang `Result`, pre-registration `Defined`).

Dokumen ini berawal sebagai **pre-registration** (RSH-001 §7.2):
hipotesis, variabel, dan kriteria keputusan dinyatakan **sebelum**
experiment dijalankan; run dan conclusion dicatat kemudian (§15, §16).

Motivasi (evidence input dari M7, ARC-008 §14.4):

- M7 menjawab seluruh research question baseline dengan **cost grid
  sintetis 0.02%–0.05% per sisi** (2–5 bps/side, ARC-008 §14.1/§14.3);
- biaya eksekusi nyata retail XAUUSD (spread + komisi + slippage ECN)
  berada jauh **di bawah** grid tersebut (~0.4–1.2 bps/side);
- oleh karena itu verdict M7 ("rejected pada biaya realistis") bergantung
  pada definisi "realistis" yang belum diukur dari venue nyata.

Tujuan EXP-002:

> Menguji kembali edge EXP-001 terhadap **biaya eksekusi venue nyata**
> (spread + komisi + slippage retail XAUUSD), bukan grid sintetis.

---

# 2. Scope

Scope EXP-002:

- pre-registration hypothesis (RSH-001 §7.2);
- dataset tetap (immutable, Article 13) — sama dengan EXP-001;
- configuration frozen: strategi identik dengan EXP-001 §9, hanya
  `execution` (biaya) yang berubah;
- expected outputs (metrik minimum, RSH-002 §8);
- cost grid venue-derived sebagai variabel bebas.

Di luar scope EXP-002:

- optimasi parameter (tetap TODO-024-style, bukan objek uji);
- strategi baru (EXP-003+);
- market lain (TODO-030).

---

# 3. Audience

- tim MRE;
- peneliti;
- quant analyst;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Per FND-005 §37, Research Evidence adalah sumber prioritas keputusan.

M7 menghasilkan verdict: hipotesis EXP-001 **ditolak** pada biaya realistis
(ARC-008 §14.4, EXP-001 §19.8). Namun basis biayanya adalah **grid sintetis**
(0.02%–0.05%/sisi) yang diambil dari RSH-003 §10, bukan pengukuran venue.

EXP-002 menutup gap tersebut: memodelkan biaya eksekusi dari data venue
retail nyata, lalu menjalankan pipeline yang sama (deterministik, no
lookahead) untuk menguji apakah edge bertahan pada biaya yang sebenarnya
dibayar trader retail.

---

# 5. Definitions

Terminologi mengikuti **FND-009** (One Concept, One Name).

| Term        | Definition                                            |
| ----------- | ----------------------------------------------------- |
| Experiment  | Unit penelitian terikat konfigurasi (RSH-002 §5)      |
| Event       | Fakta terdeteksi dari data (FND-001 Article 5)        |
| Signal      | Agregasi evidence dari Events (FND-009 §13)           |
| Trade       | Transaksi terukur dari simulasi (FND-009)             |
| Result      | Output terukur (metrics) dari experiment              |
| Venue       | Tempat eksekusi nyata (broker/pasar) yang memungut biaya |
| bps/side    | Basis point biaya per sisi (1 bps = 0.01%)            |

---

# 6. Hypothesis

Per RSH-001 §7.1:

> Kondisi **X** (deteksi/Event) menghasilkan
> edge pada **Symbol** (Y) timeframe (**Z**).

Hipotesis EXP-002 (pre-registered):

> **Breakout RSI trendline yang dikonfirmasi harga (Price Confirmation)
> pada XAUUSD H1 menghasilkan expectancy positif setelah biaya eksekusi
> venue nyata (spread + komisi + slippage retail ECN).**

Kriteria (RSH-001 §7.2):

- falsifiable: keputusan ditentukan oleh kriteria terukur (§13);
- terikat dataset dan konfigurasi spesifik (§7, §9);
- dinyatakan sebelum experiment dijalankan (dokumen ini).

Catatan: hipotesis ini identik dengan EXP-001 §6; yang diubah adalah
**definisi biaya** dari "0.02%–0.05%/sisi sintetis" menjadi "venue-derived".

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
EXP-001 §7 (kontrol).

---

# 8. Strategy — RSI Trendline Breakout

Strategi **identik** dengan EXP-001 §8 (plugin `rsi_trendline_breakout`,
LONG-only, deteksi melalui pipeline yang sama). Tidak ada perubahan pada
detector, signal definition, atau engine.

---

# 9. Configuration (Frozen)

Konfigurasi dikunci (frozen) sebelum run (RSH-002 §9). Seluruh parameter
menyamai EXP-001 §9 **kecuali** §9.4 (execution costs).

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

## 9.5 Venue Cost Model (pre-registered)

Representative retail ECN XAUUSD, standard lot = 100 oz
(notional 1 lot = 100 × harga spot).

| Komponen       | Per sisi/lot | Catatan                                       |
| -------------- | ------------ | --------------------------------------------- |
| Spread (half)  | ~$6.00       | raw ECN ~12 points round-trip ($0.12/oz)      |
| Commission     | $3.50        | umum $3.00–$7.00/lot/side (ECN raw)           |
| Slippage       | ~$2.00       | typical entry slippage 1–3 pips              |

Total per sisi ≈ **$11.50** pada notional ~$180,000/lot
(gold ~$1,800/oz) → **~0.64 bps/side**.

Karena rentang harga gold dataset lebar ($700–$2,700), biaya fraksional
dibekukan secara konservatif di **1.0 bps/side total**, terpecah:

- `commission_rate = 0.00003` (0.3 bps/side, dikenakan pada notional
  round-trip — ENG-005);
- `slippage_rate = 0.00007` (0.7 bps/side, dikenakan pada harga per sisi).

## 9.6 Statistics (ENG-006)

| Parameter  | Value |
| ---------- | ----- |
| min_sample | 30    |

---

# 10. Execution Assumptions

Per RSH-001 §14:

- **Entry**: open bar berikutnya setelah Signal (next bar open);
- **Exit**: setelah `hold_bars` (10) bar;
- **Sizing**: `position_size = 1.0` (fixed);
- **Transaction cost**: model venue §9.5 (bukan 0, bukan grid sintetis);
- **Slippage**: `slippage_rate` pada entry dan exit (conservative);
- Eksekusi adalah simulasi, bukan live (PRD-006 §9).

---

# 11. Variables

## 11.1 Control Variables

- dataset (XAUUSD H1, rentang penuh);
- strategy/indicator/event/signal config (§9.1–§9.3);
- hold_bars, sizing, SL/TP (off);
- min_sample.

## 11.2 Independent Variables

Biaya eksekusi (venue-derived cost grid):

| Skenario          | commission_rate | slippage_rate | Total/side |
| ----------------- | --------------- | ------------- | ---------- |
| Baseline (0)      | 0.0             | 0.0           | 0          |
| ECN tight         | 0.00002         | 0.00003       | 0.5 bps    |
| ECN representative | 0.00003        | 0.00007       | 1.0 bps    |
| ECN wide          | 0.00005         | 0.00010       | 1.5 bps    |
| Conservative      | 0.00007         | 0.00013       | 2.0 bps    |

`configs/EXP-002.yaml` membekukan skenario **representative** sebagai run
utama; grid di atas adalah sensitivity untuk menilai margin ke nol.

## 11.3 Dependent Variables

- metrik minimum (RSH-002 §8);
- equity curve;
- trade log.

---

# 12. Baseline Reference

Per RSH-001 §9:

- **No Trade** — reference tanpa aktivitas (equity 0);
- **EXP-001 baseline** — hasil M5 pada biaya 0 (EXP-001 §15) sebagai
  pembanding dengan biaya model venue.

---

# 13. Decision Criteria (pre-registered)

```text
SUPPORTED
Jika expectancy > 0 pada skenario representative (1.0 bps/side) dengan
n >= min_sample (30), dan biaya breakeven/side >= 1.0 bps.

REJECTED
Jika expectancy <= 0 pada skenario representative (1.0 bps/side)
atau n < min_sample.
```

Interpretasi tambahan (bukan keputusan, untuk konteks):

- grid 0.5/1.5/2.0 bps/side memberi kurva expectancy → biaya dan margin;
- jika SUPPORTED, verdict M7 diperhalus: edge bertahan pada biaya venue
  nyata meski gagal pada grid sintetis 0.05%/side;
- jika REJECTED, konklusi M7 diperkuat (edge tidak bertahan bahkan pada
  biaya venue nyata).

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

# 15. Run (TODO-036)

Strategi dijalankan **frozen** (config `configs/EXP-002.yaml` = `EXP-002`),
tanpa perubahan pada parameter strategi — hanya biaya eksekusi yang
bervariasi pada grid venue-derived (§11.2). Determinisme diverifikasi:
grid point zero-cost (0.8683) identik dengan baseline EXP-001 §15 (0.868)
— kontrol determinisme (FR-010, NFR-001).

Report: `experiments/EXP-002/EXP-002_report.md` (Code Version `c0ce79e`).

## 15.1 Representative Scenario (1.0 bps/side, config frozen)

| Metric             | Value   |
| ------------------ | ------- |
| Trade Count        | 1403    |
| Win Count          | 671     |
| Loss Count         | 732     |
| Win Rate           | 0.4783  |
| Loss Rate          | 0.5217  |
| Average Win        | 10.1465 |
| Average Loss       | 8.32137 |
| Risk/Reward        | 1.21934 |
| Expectancy         | 0.5111  |
| Profit Factor      | 1.1177  |
| Gross Profit       | 6808.33 |
| Gross Loss         | 6091.24 |
| Net P&L            | 717.095 |
| Maximum Drawdown   | 643.884 |
| Winning Streak     | 11      |
| Losing Streak      | 12      |
| Evidence Sufficient| True (n=1403 ≥ 30) |

## 15.2 Venue-Derived Cost Grid

| Scenario     | comm      | slip       | Total bps/side | Expectancy | PF     | Win Rate | n    | Net P&L   |
| ------------ | --------- | ---------- | -------------- | ---------- | ------ | -------- | ---- | --------- |
| Zero cost    | 0         | 0          | 0              | 0.8683     | 1.2087 | 0.4954   | 1403 | 1218.23   |
| ECN tight    | 0.00002   | 0.00003    | 0.5            | 0.6897     | 1.1623 | 0.4847   | 1403 | 967.66    |
| ECN rep.     | 0.00003   | 0.00007    | 1.0            | 0.5111     | 1.1177 | 0.4783   | 1403 | 717.09    |
| ECN wide     | 0.00005   | 0.00010    | 1.5            | 0.3325     | 1.0750 | 0.4647   | 1403 | 466.53    |
| Conservative | 0.00007   | 0.00013    | 2.0            | 0.1539     | 1.0340 | 0.4547   | 1403 | 215.96    |

## 15.3 Breakeven Cost

Breakeven (titik expectancy menyeberang nol), dihitung dengan grid halus
di sekitar titik nol:

- 2.40 bps/side → expectancy +0.0111 (PF 1.0024);
- 2.45 bps/side → expectancy −0.0068 (PF 0.9985);
- verifikasi halus: 2.43 bps/side → expectancy +0.0003 (PF 1.0001);
  2.44 bps/side → expectancy −0.0032 (PF 0.9993);
- **breakeven ≈ 2.43 bps/side**.

---

# 16. Conclusion

## 16.1 Verdict (pre-registered criteria, §13)

```text
SUPPORTED
- expectancy pada skenario representative (1.0 bps/side) = 0.5111 > 0
  dengan n = 1403 >= min_sample (30): TERPENUHI;
- biaya breakeven/side ≈ 2.43 bps >= 1.0 bps: TERPENUHI.
```

Verdict M7 diperhalus (sesuai interpretasi tambahan §13): **edge bertahan
pada biaya venue nyata** (0.5–2.0 bps/side seluruhnya expectancy positif)
meski gagal pada grid sintetis 0.05%/side (ARC-008 §14.4, EXP-001 §19.8).

## 16.2 Implikasi

- Definisi "biaya realistis" M7 (2–5 bps/side sintetis) **konservatif
  terhadap venue nyata**: real retail XAUUSD ECN ~0.4–1.2 bps/side (§9.5)
  berada jauh di bawah grid tempat edge gagal;
- edge RSI trendline breakout memiliki **cost tolerance ≈ 2.43 bps/side**
  — konsisten dengan interpolasi linier grid M7 (EXP-001 §19.7 / ARC-008
  §14.3: 0.1539 @ 0.02% → −0.9176 @ 0.05% ≈ 2.43 bps/side; catatan: angka
  breakeven "26 bps" pada tabel M7 tidak konsisten dengan grid-nya dan
  tidak ter-reproduksi di sini);
- margin ke nol pada biaya venue nyata: 1.0 bps/side → margin 1.43 bps
  (breakeven − biaya) — **tipis**; kejutan biaya (news/illiquidity) atau
  biaya non-ECN (markup spread broker markup) dapat menghapusnya;
- tetap berlaku prinsip FND-009 (backtest ≠ proof): hasil ini
  **in-sample + venue-cost model**, belum divalidasi OOS/robustness untuk
  EXP-002 (bisa menjadi EXP-002 lanjutan atau EXP-003).

## 16.3 Keputusan Lanjutan (peneliti)

Hipotesis EXP-002 **didukung secara pre-registered**. Sebelum
memperlakukan edge sebagai tradable, evidence berikut direkomendasikan:

- EXP-002 OOS/robustness pada venue cost grid (reuse `run_on_slice`,
  ARC-ACT-013);
- validasi slippage model terhadap data tick (jika tersedia);
- pertimbangan margin biaya tipis (1.43 bps) terhadap akurasi model biaya.

---

# 17. Record Lifecycle

```text
Defined (spesifikasi + konfigurasi frozen)    ← 2026-08-09 (pre-registration)
    ↓ (TODO-035 Run EXP-002)
Run          ← 2026-08-10 (TODO-036, §15)
    ↓
Result (metrics dicatat)    ← saat ini (§15.1)
    ↓
Conclusion (interpretasi evidence — peneliti, PRD-006 §9)    ← saat ini (§16)
    ↓
Reviewed (validasi, RSH-003)
```

---

# 18. Traceability

| Item            | Requirement / TODO           |
| --------------- | ---------------------------- |
| Hypothesis      | RSH-001 §7, TODO-013         |
| Spec fields     | RSH-002 §6, TODO-014         |
| Metrics         | RSH-002 §8, FND-008 §25      |
| Reproducibility | FR-010, NFR-001, RSH-002 §9  |
| Venue cost      | RSH-003 §10 (cost dimension) |
| Conclusion      | FR-011, RSH-001 §13          |

---

# 19. Compliance

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

# 20. References

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
- `docs/03-engine/ENG-002_Event_Engine.md`
- `docs/03-engine/ENG-003_Signal_Engine.md`
- `docs/03-engine/ENG-005_Simulation_Engine.md`
- `docs/03-engine/ENG-006_Statistics_Engine.md`
- `docs/03-engine/ENG-007_Reporting_Engine.md`
- `docs/01-product/PRD-006_MVP_Definition.md`
- `configs/EXP-002.yaml`

Venue cost basis (eksternal, dikompilasi saat pre-registration):

- IC Markets / Pepperstone / Tickmill raw ECN XAUUSD spread + commission
  (sumber publik broker review, 2025–2026);
- typical retail slippage XAUUSD 1–3 pips (sumber publik).

---

# 21. Revision History

| Version | Date       | Changes                                      |
| ------- | ---------- | -------------------------------------------- |
| 1.0.1   | 2026-08-10 | EXP-002 run (TODO-036) dicatat (§15): venue cost grid + breakeven ≈ 2.43 bps/side; verdict SUPPORTED (§16.1) — edge bertahan pada biaya venue nyata, verdict M7 diperhalus |
| 1.0.0   | 2026-08-09 | Initial EXP-002 pre-registration (TODO-035): real venue execution cost re-test |

---

**Document Status:** Result

**Document ID:** EXP-002

**Version:** 1.0.1

**End of Document**
