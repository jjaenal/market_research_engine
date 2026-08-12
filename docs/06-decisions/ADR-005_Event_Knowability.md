---
title: Event Knowability (Fact vs Confirmable Time)
document_id: ADR-005
version: 1.0.0
status: Accepted
category: Decision
owner: Market Research Engine Core Team
created: 2026-08-11
last_updated: 2026-08-11

depends_on:
  - FND-001
  - FND-009
  - ARC-003
  - SPEC-001
  - SPEC-003

referenced_by:
  - ENG-002
  - ENG-003
  - ENG-005
  - SPEC-001
  - SPEC-003

purpose: Record the decision that Event facts carry a separate confirmable/knowable time, binding signal execution to information availability (audit E-1)
---

# ADR-005 — Event Knowability (Fact vs Confirmable Time)

> Measure the Market. Discover the Edge.

---

# 1. Status

**Accepted** (2026-08-11)

---

# 2. Context

Audit E-1 menemukan **lookahead sistemik** pada semua strategi berbasis
swing/fractal: event swing di-stamp di candle puncak (`i`) yang hanya
bisa diketahui **`right` candle kemudian**. Sinyal berbasis swing
dapat dieksekusi 1–2 candle terlalu awal; pada kasus tertentu entry
mengkonsumsi close candle entry sendiri (same-bar leak). Klaim "no
lookahead" di EXP-002 §4, EXP-004 §10, EXP-007 §8/§16 hanyalah
**kira-kira benar**.

Alternatif yang dipertimbangkan:

1. **Waktu fakta vs waktu dapat-diketahui (dipilih)** — Event membawa
   `timestamp` (fakta) dan `confirmable_at`/`confirmable_ref`
   (kapan bisa diketahui); konsumen dilarang bertindak sebelum waktu
   dapat-diketahui.
2. **Timestamp diset langsung di bar konfirmasi** — puncak tidak lagi
   dilacak; informasi "nilai puncak" hilang dari model.
3. **Retensi referensi tanpa guard** — mempertahankan perilaku legacy;
   lookahead tetap ada.

---

# 3. Decision

Setiap `Event` yang fakta-nya baru dapat diketahui setelah beberapa bar
membawa dua waktu:

```text
timestamp         = waktu fakta (mis. candle puncak i)
confirmable_ref   = index bar pertama saat fakta dapat diketahui (i + right)
confirmable_at    = timestamp bar tersebut
```

- Detektor yang dapat diketahui di bar yang sama (mis.
  `PRICE_CONFIRMATION` di close bar-nya) membiarkan
  `confirmable_*` = `None` (fallback ke fakta).
- `Signal.timestamp` = waktu knowable terakhir di antara seluruh
  konstituen (SPEC-003 §4.2).
- `simulate()` entry di open bar setelah **signal knowable**:
  `entry_bar = max(signal_bar + 1, max(confirmable_ref) + 1)`.
- Detail teknis dicatat dalam **SPEC-001 §4.4** dan **SPEC-003 §4**.

---

# 4. Consequences

Positif:

- eliminasi lookahead swing/fractal (E-1) — signal timing menjadi
  benar-benar kausal;
- evidence OOS/train/test menjadi dapat dipercaya;
- konsisten dengan prinsip "backtest adalah evidence, bukan bukti"
  (FND-009) — information availability eksplisit;
- detektor tanpa delay (PRICE_CONFIRMATION) tidak terpenalized.

Negatif:

- Event model lebih kaya (dua waktu per event);
- entry dapat tertunda `right` bar untuk strategi berbasis swing
  (biaya latency — sudah melekat pada definisi fractal);
- angka historis (EXP-001..008) tidak setara dengan angka hasil
  pipeline baru; hasil lama TIDAK ditulis ulang (Rule 2 audit),
  harus di-re-run sebagai evidence baru.

---

# 5. Alternatives Considered

| Opsi                             | Dipilih | Alasan tidak dipilih                      |
| -------------------------------- | ------- | ----------------------------------------- |
| Fact vs confirmable time         | ✓       | Kausal, mempertahankan info puncak         |
| Timestamp di bar konfirmasi      | —       | Kehilangan nilai/posisi puncak            |
| Tanpa guard                      | —       | Lookahead tetap ada (audit E-1)           |

---

# 6. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/02-architecture/ARC-003_Event_Architecture.md`
- `docs/05-research/SPEC-001_Swing_Detection.md`
- `docs/05-research/SPEC-003_Signal_Timing_Execution.md`
- `src/mre/models/event.py`
- `src/mre/engines/signal_engine.py`
- `src/mre/engines/simulation_engine.py`

---

# 7. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-08-11 | Initial ADR (event knowability, E-1) |

---

**Document Status:** Accepted

**Document ID:** ADR-005

**Version:** 1.0.0

**End of Document