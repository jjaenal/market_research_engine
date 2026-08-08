---
title: RSI Trendline Algorithm (Two-Point Line)
document_id: ADR-004
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
  - ADR-003

referenced_by:
  - ENG-002
  - ENG-003

purpose: Record the RSI trendline build and break algorithm used by the Event Engine (RSH-ACT-003, ARC-ACT-004)
---

# ADR-004 — RSI Trendline Algorithm (Two-Point Line)

> Measure the Market. Discover the Edge.

---

# 1. Status

**Accepted** (2026-08-08)

---

# 2. Context

Per **FND-009 §10.6–10.8**, RSI Trendline dibangun berdasarkan
swing/pivot pada RSI, dan exact rules belum final hingga
strategy specification ditetapkan.

Per **FND-009 §10.7**, breakout harus memiliki
deterministic definition (Article 7).

Alternatif yang dipertimbangkan:

1. **Two-point line (dipilih)** — trendline dari dua swing
   terakhir; break saat nilai menembus garis.
2. **Least-squares regression** — trendline dari regresi
   seluruh swing; sensitif terhadap outliers dan perubahan struktur.
3. **Rolling extremum projection** — line dari level ekstrem
   terbaru; reaktif namun rawan false break.

---

# 3. Decision

MRE menggunakan **two-point line** untuk RSI trendline:

```text
Up-trendline dari dua swing low terakhir:
    point A = swing_low[-2], point B = swing_low[-1]
    slope = (rsi[B] - rsi[A]) / (iB - iA)
    line(t) = rsi[A] + slope * (t - iA)

RSI_TRENDLINE_CREATED  → saat B terkonfirmasi, bila slope > 0
RSI_TRENDLINE_BROKEN   → pertama kali rsi[t] < line(t), t > iB
```

- up-trendline hanya valid bila slope > 0;
- down-trendline simetris dari dua swing high terakhir (slope < 0);
- satu trendline aktif; break menonaktifkan garis tersebut;
- operasi murni pada RSI series (independen, Article 2).

Detail teknis dicatat dalam **ENG-002 §7.2**.

---

# 4. Consequences

Positif:

- deterministic dan reproducible (Article 7);
- konfigurasi minimal (bergantung pada swing detector);
- mudah diuji dan dijelaskan (Article 5).

Negatif:

- hanya dua titik — sensitif terhadap swing terakhir;
- break tunggal dapat memicu false signal (mitigasi di Signal Engine,
  ENG-003);
- slope flat (0) tidak membentuk trendline (bukan trend).

---

# 5. Alternatives Considered

| Opsi                    | Dipilih | Alasan tidak dipilih                       |
| ----------------------- | ------- | ------------------------------------------ |
| Two-point line          | ✓       | Deterministic, sederhana, explainable      |
| Least-squares regression| —       | Sensitif terhadap outliers                 |
| Rolling extremum        | —       | Rawan false break                          |

---

# 6. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/00-foundation/FND-009_Project_Glossary.md`
- `docs/02-architecture/ARC-003_Event_Architecture.md`
- `docs/06-decisions/ADR-003_Swing_Algorithm.md`
- `docs/03-engine/ENG-002_Event_Engine.md`

---

# 7. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-08-08 | Initial ADR (trendline algorithm) |

---

**Document Status:** Accepted

**Document ID:** ADR-004

**Version:** 1.0.0

**End of Document**
