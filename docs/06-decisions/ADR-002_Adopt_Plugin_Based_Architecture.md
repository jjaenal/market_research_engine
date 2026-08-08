---
title: Adopt Plugin-Based Architecture
document_id: ADR-002
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
  - ARC-005

referenced_by:
  - ARC-005

purpose: Record the decision to adopt a plugin-based architecture for detectors, indicators, and strategies
---

# ADR-002 — Adopt Plugin-Based Architecture

> Measure the Market. Discover the Edge.

---

# 1. Status

**Accepted** (2026-08-08)

---

# 2. Context

Per **Article 11 (Plugin First)**, strategi dan detektor
ditambahkan sebagai plugin tanpa mengubah engine (NFR-006, FEAT-011).

Per **Article 12**, plugin dijalankan melalui konfigurasi (FR-012).

Model alternatif yang dipertimbangkan:

1. **Plugin-based (dipilih)** — indicator/detector/strategy
   terdaftar dan dimuat melalui konfigurasi; engine tetap stabil.
2. **Hardcoded strategy** — strategi tertanam di kode engine;
   setiap strategi baru mengubah engine; melanggar Article 11.
3. **Runtime script injection** — plugin berupa script yang diinjeksi
   saat runtime; keamanan dan determinisme sulit dijaga.

---

# 3. Decision

MRE mengadopsi **plugin-based architecture**:

- indicator, detector, dan strategy adalah plugin
  dengan kontrak inti (plugin_id, version, config_schema, run);
- plugin dimuat dari package yang dikenal melalui konfigurasi eksperimen;
- plugin bergantung hanya pada interface inti
  (Event, Signal, konfigurasi), bukan infrastructure;
- menambahkan strategi/detektor baru tidak mengubah engine.

Detail teknis dicatat dalam **ARC-005** (Plugin Architecture).

---

# 4. Consequences

Positif:

- ekstensibilitas (NFR-006);
- engine stabil saat plugin bertambah;
- sesuai Article 11, Article 12;
- strategi dapat dibagikan secara open-source.

Negatif:

- overhead kontrak/registrasi plugin;
- performa tambahan untuk validasi konfigurasi saat loading;
- perlu kebijakan isolasi yang konsisten.

---

# 5. Alternatives Considered

| Opsi                  | Dipilih | Alasan tidak dipilih                          |
| --------------------- | ------- | --------------------------------------------- |
| Plugin-based          | ✓       | Sesuai Article 11, NFR-006                    |
| Hardcoded strategy    | —       | Melanggar Article 11; engine sering berubah   |
| Runtime script inject | —       | Keamanan dan determinisme sulit dijaga        |

---

# 6. References

- `docs/00-foundation/FND-001_Project_Charter.md`
- `docs/00-foundation/FND-005_Project_Context.md`
- `docs/02-architecture/ARC-001_System_Architecture.md`
- `docs/02-architecture/ARC-005_Plugin_Architecture.md`
- `docs/01-product/PRD-005_Non_Functional_Requirements.md`
- `docs/01-product/PRD-007_Feature_Specification.md`

---

# 7. Revision History

| Version | Date       | Changes                    |
| ------- | ---------- | -------------------------- |
| 1.0.0   | 2026-08-08 | Initial ADR (plugin-based) |

---

**Document Status:** Accepted

**Document ID:** ADR-002

**Version:** 1.0.0

**End of Document**
