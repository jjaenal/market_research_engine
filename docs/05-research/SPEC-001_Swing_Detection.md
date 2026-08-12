---
title: Swing Detection
document_id: SPEC-001
version: 1.0.0
status: Draft
category: Research
owner: Market Research Engine Core Team
created: 2026-08-11
last_updated: 2026-08-11

depends_on:
  - FND-009
  - RSH-001
  - RSH-002
  - ENG-002

referenced_by:
  - EXP-001
  - EXP-005
  - EXP-006
  - EXP-007
  - EXP-008

purpose: Deterministic, lookahead-safe fractal swing detection used by every swing-based strategy (audit E-1)
---

# SPEC-001 — Swing Detection

> Measure the Market. Discover the Edge.

---

# 1. Purpose

SPEC-001 mendefinisikan **definisi swing high / swing low yang
deterministik** dan **bebas lookahead**, sebagai dasar semua strategi
berbasis fractal/swing.

Dokumen ini menjawab temuan audit E-1: event swing sebelumnya di-stamp
pada candle puncak (`i`) yang belum bisa diketahui saat itu juga —
baru *knowable* setelah window konfirmasi kanan (`right`) ditutup.
Pendekatan `confirmable_at`/`confirmable_ref` (ADR-005) memisahkan
**waktu fakta** (timestamp puncak) dari **waktu dapat-diketahui**
(timestamp bar `i + right`); konsumen dilarang bertindak sebelum waktu
dapat-diketahui (SPEC-003).

---

# 2. Scope

Scope SPEC-001:

- swing high / swing low pada seri harga **atau** seri indikator (mis. RSI);
- parameter `left` / `right`;
- tie handling (equal values);
- multiple simultaneous structures;
- confirmation timing (kapan swing *knowable*).

Di luar scope SPEC-001:

- structure invalidation / replacement (tidak digunakan strategi saat ini);
- penentuan sinyal / entry (SPEC-003);
- penentuan level breakout (SPEC-002).

---

# 3. Inputs

| Input        | Deskripsi                                        |
| ------------ | ------------------------------------------------ |
| `values`     | Seri numerik terurut (closes atau nilai indikator) |
| `timestamps` | Seri datetime sejajar dengan `values`            |
| `left`       | Jumlah bar di kiri puncak (default 2)            |
| `right`      | Jumlah bar di kanan puncak (default 2)           |

---

# 4. Deterministic Rules

## 4.1 Fraktal Ekstremum

- `swing_high` pada index `i` berlaku jika dan hanya jika
  `values[i] > values[j]` untuk **semua** `j ∈ [i−left, i+right]`,
  `j ≠ i` (strict).
- `swing_low` simetris: `values[i] < values[j]` untuk semua `j` pada
  window yang sama (strict).

## 4.2 Tie Handling

- **Tie mendiskualifikasi**: jika ada neighbor dengan nilai **sama**
  (`values[i] == values[j]`), maka index `i` **bukan** swing high dan
  **bukan** swing low.
- Plateau (baris nilai sama berurutan) tidak menghasilkan swing.
- Tidak ada swing ganda (high dan low) pada satu index pada data bersih.

## 4.3 Window Penuh

- Hanya index `i ∈ [left, n−right)` yang dievaluasi (window lengkap di
  kedua sisi).
- Window di tepi seri yang tidak lengkap **tidak** menghasilkan swing.

## 4.4 Confirmation Timing (E-1, ADR-005)

- `timestamp` event = bar puncak `i` (waktu fakta).
- `confirmable_at` = `timestamps[i + right]` (waktu dapat-diketahui).
- `confirmable_ref` = `i + right` (bar dapat-diketahui).
- Konsumen (SPEC-003) tidak boleh mengeksekusi sebelum seluruh konstituen
  knowable.

## 4.5 NaN (Warm-Up)

- Nilai `NaN` **tidak boleh** menghasilkan event swing (warm-up region).
- Aturan ini adalah bagian dari spec; lihat Catatan Implementasi §7.

---

# 5. Edge Cases

| Kasus                                   | Perilaku deterministik       |
| --------------------------------------- | ---------------------------- |
| NaN / warm-up region                    | Tidak menghasilkan event     |
| Plateau / equal highs atau lows         | Tie → tidak menghasilkan event |
| Window tepi tidak lengkap               | Tidak menghasilkan event     |
| Seri berakhir tepat di window kanan     | Index terakhir yang valid adalah `n−right−1` |

---

# 6. Non-Goals

- structure invalidation / replacement;
- penentuan sinyal / entry (SPEC-003);
- penentuan level breakout (SPEC-002);
- konfirmasi harga (PRICE_CONFIRMATION, SPEC-002).

---

# 7. Traceability

| Item                   | Code / Doc                                 |
| ---------------------- | ------------------------------------------ |
| `detect_swings`        | `src/mre/detectors/swing.py`               |
| Event model            | `src/mre/models/event.py` (`confirmable_at`/`confirmable_ref`) |
| Pemanggil              | `src/mre/engines/event_engine.py` (closes) dan `src/mre/detectors/rsi_trendline.py` (RSI) |
| ADR-003                  | Semantik fractal (window `left`/`right`, strict) |
| ADR-005                  | Knowability — fakt timestamp vs confirmable time |
| E-1                      | Audit findings (lookahead swing/fractal)   |

**Catatan Implementasi:** `swing.py` mengimplementasikan aturan §4.5:
seluruh window `[i−left, i+right]` yang mengandung NaN **tidak**
menghasilkan event di index `i` (baik NaN di puncak maupun di neighbor
mendiskualifikasi kandidat). Sebelumnya region NaN pada warm-up RSI
dapat menghasilkan swing high dan low spurios (dual event); guard ini
tidak mengubah sinyal/trade (garis trendline berslope NaN tidak pernah
ter-break), hanya menghilangkan event sampah.

---

# 8. Compliance

| Document / Rule  | Requirement                    |
| ---------------- | ------------------------------ |
| FND-009          | Backtest ≠ Proof               |
| RSH-001 §7.2     | Pre-registration               |
| Article 7        | Deterministic                  |
| Article 13       | Immutable data                 |

---

# 9. References

- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/03-engine/ENG-002_Event_Engine.md`
- `docs/06-decisions/ADR-003_Swing_Algorithm.md`
- `docs/06-decisions/ADR-005_Event_Knowability.md`
- `src/mre/detectors/swing.py`

---

# 10. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-08-11 | Initial Swing Detection spec (E-1) |

---

**Document Status:** Draft

**Document ID:** SPEC-001

**Version:** 1.0.0

**End of Document**
