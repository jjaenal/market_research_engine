---
title: Swing Detection Algorithm (Fractal Window)
document_id: ADR-003
version: 1.0.0
status: Accepted
category: Decision
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-08

depends_on:
  - FND-001
  - FND-005
  - FND-009
  - ARC-003

referenced_by:
  - ENG-002
  - ENG-003

purpose: Record the swing detection algorithm used by the Event Engine (RSH-ACT-003, ARC-ACT-004)
---

# ADR-003 — Swing Detection Algorithm (Fractal Window)

> Measure the Market. Discover the Edge.

---

# 1. Status

**Accepted** (2026-08-08)

---

# 2. Context

Per **FND-009 §11**, Swing High / Swing Low adalah market point
yang memenuhi aturan tertentu. Aturan tersebut belum final
(section 10.8, 11.1–11.3). Detektor swing (ENG-002 §7.1)
membutuhkan definisi algoritmik yang deterministic (Article 7).

Alternatif yang dipertimbangkan:

1. **Fractal window (dipilih)** — titik adalah swing
   bila strictly extrema dalam window `left`+`right` di sekitarnya.
2. **Percentage reversal (zigzag)** — swing bila perubahan
   nilai melebihi threshold persen; sensitif terhadap skala/volatilitas.
3. **Percentile/rolling rank** — swing berdasarkan rangking
   dalam window; tergantung distribusi dan window.

---

# 3. Decision

MRE menggunakan **fractal window** untuk swing detection:

```text
swing_high di i:
    series[i] > series[j] untuk semua j di [i-left, i+right], j ≠ i
swing_low di i:
    series[i] < series[j] untuk semua j di [i-left, i+right], j ≠ i
```

- `left` dan `right` dikonfigurasi (default 2);
- window tidak penuh di tepi → tidak ada swing (no partial window);
- perbandingan strictly → area flat menghasilkan tanpa swing;
- operasi murni pada satu series (independen, Article 2).

Detail teknis dicatat dalam **ENG-002 §7.1**.

---

# 4. Consequences

Positif:

- deterministic dan reproducible (Article 7);
- independen terhadap skala/volatilitas harga;
- parameter konfigurasi sederhana (`left`, `right`);
- konsisten dengan konfigurasi legacy `fractal` (PRD Sprint 1).

Negatif:

- latency deteksi (butuh konfirmasi `right` candle setelahnya);
- perbandingan strict membuat flat region tanpa swing;
- tidak mendeteksi swing di `left`/`right` candle pertama/terakhir.

---

# 5. Alternatives Considered

| Opsi                 | Dipilih | Alasan tidak dipilih                       |
| -------------------- | ------- | ------------------------------------------ |
| Fractal window       | ✓       | Deterministic, scale-invariant             |
| Percentage reversal  | —       | Sensitif terhadap skala/volatilitas        |
| Percentile/rank      | —       | Tergantung distribusi dan window           |

---

# 6. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/02-architecture/ARC-003_Event_Architecture.md`
- `docs/03-engine/ENG-002_Event_Engine.md`

---

# 7. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-08-08 | Initial ADR (fractal algorithm)  |

---

**Document Status:** Accepted

**Document ID:** ADR-003

**Version:** 1.0.0

**End of Document**
