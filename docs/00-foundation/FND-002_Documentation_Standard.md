---
title: Documentation Standard
document_id: FND-002
version: 1.0.2
status: Approved
category: Foundation
owner: Market Research Engine
created: 2026-08-07
last_updated: 2026-08-08

depends_on:
  - README.md
  - FND-001_Project_Charter.md

referenced_by:
  - All Documentation

purpose: Govern the structure, metadata, and writing standards for all project documentation
---

# Documentation Standard

> "Good software starts with good documentation."

---

# 1. Purpose

Dokumen ini mendefinisikan standar penulisan dokumentasi untuk seluruh
Market Research Engine (MRE).

Seluruh dokumen dalam repository wajib mengikuti standar ini.

Tujuannya adalah menjaga:

- Konsistensi
- Keterbacaan
- Kemudahan review
- Kemudahan maintenance
- Kemudahan onboarding developer baru

---

# 2. Objectives

Standar dokumentasi dibuat agar seluruh informasi memiliki struktur yang sama.

Developer tidak perlu belajar format baru setiap membuka dokumen.

AI Assistant juga dapat memahami struktur dokumen dengan mudah.

---

# 3. Documentation Philosophy

MRE menggunakan pendekatan:

## Documentation Driven Development (DDD)

Seluruh implementasi harus diawali dengan dokumentasi.

```
Idea
    │
    ▼
Documentation
    │
    ▼
Architecture Review
    │
    ▼
Implementation
    │
    ▼
Testing
    │
    ▼
Release
```

Implementasi tanpa dokumentasi dianggap belum siap dikerjakan.

---

# 4. Documentation Principles

## Principle 1

Single Source of Truth

Setiap informasi hanya memiliki satu lokasi resmi.

Tidak boleh ada informasi yang saling bertentangan.

---

## Principle 2

Documentation Before Code

Dokumentasi harus selesai sebelum implementasi dimulai.

---

## Principle 3

Living Documentation

Dokumentasi harus selalu diperbarui ketika implementasi berubah.

---

## Principle 4

Engineering First

Dokumentasi ditulis sebagai spesifikasi teknis.

Bukan catatan pribadi.

---

## Principle 5

Reproducibility

Seluruh eksperimen dan keputusan harus dapat ditelusuri kembali.

---

# 5. Document Categories

Repository dokumentasi dibagi menjadi beberapa kategori.

## Foundation

Dokumen yang mendefinisikan identitas proyek.

Contoh:

- Project Charter
- Documentation Standard
- Glossary

---

## Product

Menjelaskan kebutuhan produk.

---

## Architecture

Menjelaskan desain sistem.

---

## Engine

Menjelaskan implementasi engine.

---

## Development

Menjelaskan standar engineering.

---

## Research

Menjelaskan metodologi penelitian.

---

## ADR

Architecture Decision Records.

---

## Context

Dokumen dinamis.

Misalnya:

- Project Status
- Session Log
- Decision Log

---

# 6. Required Metadata

Seluruh dokumen wajib memiliki metadata.

Template:

```yaml
---
title:
document_id:
version:
status:
category:
owner:
created:
last_updated:

depends_on:

referenced_by:
---
```

---

# 7. Document Status

Status yang diperbolehkan.

| Status     | Meaning         |
| ---------- | --------------- |
| Draft      | Sedang ditulis  |
| Review     | Sedang direview |
| Approved   | Resmi           |
| Deprecated | Tidak digunakan |

---

# 8. Document Structure

Seluruh dokumen menggunakan struktur berikut.

```
Metadata

Purpose

Scope

Audience

Background

Definitions

Main Content

Examples

References

Revision History
```

Semakin besar dokumen,
semakin lengkap strukturnya.

---

# 9. Naming Convention

Nama file menggunakan PascalCase.

Contoh:

```
Project_Charter.md

System_Architecture.md

Probability_Engine.md
```

Kategori menggunakan folder.

```
architecture/

engine/

development/
```

---

# 10. Markdown Rules

Gunakan heading secara konsisten.

```
#

##

###
```

Jangan melompati level heading.

---

Gunakan bullet list.

```
-

-
```

Gunakan numbering bila urutan penting.

```
1.

2.

3.
```

---

Gunakan code block.

````text
```python
```
````

---

**Document Status:** Approved

**Document ID:** FND-002

**Version:** 1.0.2

**End of Document**
