---
title: Adopt Event-Driven Architecture
document_id: ADR-001
version: 1.0.0
status: Accepted
category: Decision
owner: Market Research Engine Core Team
created: 2026-08-08
last_updated: 2026-08-08

depends_on:
  - FND-001
  - FND-005
  - ARC-001
  - ARC-003

referenced_by:
  - ARC-003

purpose: Record the decision to adopt event-driven architecture for MRE
---

# ADR-001 — Adopt Event-Driven Architecture

> Measure the Market. Discover the Edge.

---

# 1. Status

**Accepted** (2026-08-08)

---

# 2. Context

MRE menguji hipotesis trading secara ilmiah (PRD-001 §7).

Per **Article 1**, Event adalah unit atomik sistem:
Signal mengagregasi Event; Trade lahir dari evaluasi Signal.
Per **Article 3**, detektor menghasilkan fakta (Event), bukan rekomendasi.

Model alternatif yang dipertimbangkan:

1. **Event-driven (dipilih)** — detektor memancarkan fakta atomik;
   Signal adalah agregasi; seluruh aliran data berbentuk timeline Event.
2. **Procedural pipeline** — transformasi berurutan tanpa unit atomik;
   fleksibilitas rendah, integrasi antar detektor sulit.
3. **Object-centric (stateful)** — objek global menyimpan state;
   melanggar Article 6 (stateless) dan Article 13 (immutability).

---

# 3. Decision

MRE mengadopsi **event-driven architecture**:

- Event adalah unit atomik (Article 1);
- detektor memancarkan Event sebagai fakta (Article 2, Article 3);
- Signal adalah agregasi Event yang dapat dijelaskan (Article 4, Article 5);
- aliran data sistem berbentuk timeline Event;
- Event immutable dan deterministic (Article 7, Article 13).

Detail teknis dicatat dalam **ARC-003** (Event Architecture).

---

# 4. Consequences

Positif:

- keputusan selalu dapat dijelaskan (Article 5);
- detektor independen dan dapat diuji (Article 2);
- reproducibility experiment terjaga (determinism);
- integrasi antar detektor melalui Signal.

Negatif:

- overhead desain model Event;
- semua integrasi melewati timeline Event (tambahan abstraksi);
- warm-up / data tidak cukup harus ditangani eksplisit (PRD-003 §7.4).

---

# 5. Alternatives Considered

| Opsi               | Dipilih | Alasan tidak dipilih                          |
| ------------------ | ------- | --------------------------------------------- |
| Event-driven       | ✓       | Sesuai Articles 1–5, 7, 13                    |
| Procedural pipeline| —       | Fleksibilitas rendah; tidak ada unit atomik   |
| Object-centric     | —       | Melanggar Article 6, Article 13               |

---

# 6. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/02-architecture/ARC-001_System_Architecture.md`
- `docs/02-architecture/ARC-003_Event_Architecture.md`
- `docs/01-product/PRD-001_Product_Vision.md`

---

# 7. Revision History

| Version | Date       | Changes                          |
| ------- | ---------- | -------------------------------- |
| 1.0.0   | 2026-08-08 | Initial ADR (event-driven)       |

---

**Document Status:** Accepted

**Document ID:** ADR-001

**Version:** 1.0.0

**End of Document**
