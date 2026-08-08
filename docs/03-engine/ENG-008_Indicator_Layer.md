---
title: Indicator Layer
document_id: ENG-008
version: 1.0.0
status: Draft
category: Engine
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-08

depends_on:
  - FND-001
  - FND-005
  - FND-009
  - FND-010
  - ARC-001
  - ARC-002
  - ARC-003
  - ARC-004
  - ARC-006
  - ARC-007
  - PRD-003
  - PRD-004
  - DEV-002
  - ENG-001

referenced_by:
  - FND-006
  - FND-008

purpose: Define the Indicator Layer implementation spec — EMA, RSI, ATR formulas, no-lookahead, and warm-up handling (TODO-016)
---

# Indicator Layer

> Measure the Market. Discover the Edge.

---

# 1. Purpose

ENG-008 mendefinisikan **Indicator Layer** — spesifikasi implementasi
untuk TODO-016 (Build Indicator Layer).

Dokumen ini menetapkan:

- kontrak interface indikator;
- formula EMA, RSI, ATR;
- persyaratan no-lookahead;
- penanganan warm-up;
- pengujian terhadap nilai referensi.

---

# 2. Scope

Scope ENG-008:

- indikator awal: EMA, RSI, ATR;
- kontrak pure function;
- no-lookahead dan determinism.

Di luar scope ENG-008:

- detektor (ENG-002/ARC-003);
- event/signal (ARC-003);
- indikator tambahan di masa depan.

---

# 3. Audience

Pembaca utama dokumen ini:

- tim MRE;
- software engineer;
- AI assistant yang bekerja pada repository ini.

---

# 4. Background

Per FND-001 Article 8, indikator tidak pernah mengeksekusi Trade.
Indikator menghasilkan data (IndicatorSeries), bukan rekomendasi.

Per ARC-006 §7.2:

```text
IndicatorEngine: compute(dataset, indicator_params) → IndicatorSeries
```

---

# 5. Definitions

Terminologi mengikuti **FND-009** (One Concept, One Name).

Istilah kunci:

| Term           | Definition                                |
| -------------- | ----------------------------------------- |
| Indicator      | Transformasi data → series (FND-009)      |
| IndicatorSeries | Output terukur dari indikator             |
| Warm-up        | Periode awal tanpa nilai valid            |
| Lookahead      | Penggunaan candle masa depan (dilarang)   |

---

# 6. Interface

Setiap indikator adalah **pure function** (Article 6, Article 7):

| Indicator | Signature                                |
| --------- | ---------------------------------------- |
| EMA       | `ema(closes, period) → list[float]`      |
| RSI       | `rsi(closes, period) → list[float]`      |
| ATR       | `atr(candles, period) → list[float]`     |

Kontrak:

- input dan output sama panjang dengan data;
- nilai warm-up pertama `period - 1` = NaN;
- tidak ada penggunaan candle masa depan (critical requirement).

---

# 7. Indicator Formulas

## 7.1 EMA (Exponential Moving Average)

```text
alpha = 2 / (period + 1)
EMA[t] = alpha * close[t] + (1 - alpha) * EMA[t-1]
seed  = SMA(closes[:period])  # pada indeks period-1
```

- `EMA[0..period-2]` = NaN;
- `EMA[period-1]` = SMA awal;
- tanpa lookahead.

## 7.2 RSI (Relative Strength Index, Wilder)

```text
delta[t] = close[t] - close[t-1]
gain[t]  = max(delta[t], 0)
loss[t]  = max(-delta[t], 0)

avg_gain[period] = mean(gain[1..period])
avg_loss[period] = mean(loss[1..period])

avg_gain[t] = (avg_gain[t-1] * (period - 1) + gain[t]) / period
avg_loss[t] = (avg_loss[t-1] * (period - 1) + loss[t]) / period

RS = avg_gain / avg_loss
RSI = 100 - 100 / (1 + RS)       # avg_loss == 0 → RSI = 100
```

- nilai RSI pertama pada indeks `period` (memerlukan `period` delta);
- tanpa lookahead.

## 7.3 ATR (Average True Range, Wilder)

```text
TR[0] = high[0] - low[0]
TR[t] = max(high[t] - low[t],
            |high[t] - close[t-1]|,
            |low[t] - close[t-1]|)

ATR[period] = mean(TR[1..period])
ATR[t] = (ATR[t-1] * (period - 1) + TR[t]) / period
```

- nilai ATR pertama pada indeks `period` (memerlukan `period` TR);
- tanpa lookahead.

---

# 8. No-Lookahead (Critical Requirement)

Per FND-007 §16 dan TODO-016:

> Indicator calculations must not use future candles.

Konsekuensi:

- nilai pada indeks `i` hanya bergantung pada candles[0..i];
- deterministik (Article 7);
- diuji secara eksplisit (perbandingan nilai saat `i` sebelum candle berikutnya tersedia).

---

# 9. Warm-Up Handling

- nilai sebelum cukup data = NaN;
- konsumen (detektor/engine) harus menangani NaN (PRD-003 §7.4 warm-up);
- panjang output = panjang input.

---

# 10. Testing (DEV-002)

- unit test terhadap **nilai referensi yang diketahui** (known-good literal);
- test no-lookahead: nilai pada `i` tidak berubah saat data dipotong;
- test warm-up: NaN pada `period - 1` elemen pertama;
- test determinism: run yang sama → output sama.

---

# 11. Traceability

| Item              | Requirement / Feature     |
| ----------------- | ------------------------- |
| EMA/RSI/ATR       | TODO-016                  |
| No-lookahead      | TODO-016 critical requirement, FND-007 §16 |
| Indicator data only | Article 8               |
| Determinism       | Article 7, NFR-001        |

---

# 12. Compliance

| Constitution Article | Indicator requirement     |
| -------------------- | ------------------------- |
| Article 6            | Pure function, stateless  |
| Article 7            | Deterministic             |
| Article 8            | Indicator never trades    |
| Article 13           | Data immutable            |

---

# 13. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/00-foundation/FND-010_Foundation_Review.md`
- `docs/02-architecture/ARC-001_System_Architecture.md`
- `docs/02-architecture/ARC-002_Domain_Model.md`
- `docs/02-architecture/ARC-003_Event_Architecture.md`
- `docs/02-architecture/ARC-004_Data_Architecture.md`
- `docs/02-architecture/ARC-006_Module_Architecture.md`
- `docs/02-architecture/ARC-007_Architecture_Review.md`
- `docs/01-product/PRD-003_Core_Workflow.md`
- `docs/01-product/PRD-004_Functional_Requirements.md`
- `docs/04-development/DEV-002_Testing_Strategy.md`
- `docs/03-engine/ENG-001_Data_Engine.md`

---

# 14. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-08-08 | Initial indicator layer spec     |

---

**Document Status:** Draft

**Document ID:** ENG-008

**Version:** 1.0.0

**End of Document**
