---
title: Documentation Home
project: Market Research Engine
version: 1.0.0
status: Active
owner: Project Team
last_updated: 2026-08-04
---

# 📚 Market Research Engine Documentation

> **Measure the Market. Discover the Edge.**

Selamat datang di dokumentasi resmi **Market Research Engine (MRE)**.

Dokumentasi ini merupakan sumber informasi utama mengenai visi, filosofi, arsitektur, desain, implementasi, metodologi riset, dan proses pengembangan framework.

> **Apabila terjadi perbedaan antara isi source code dan dokumentasi, dokumentasi menjadi referensi utama hingga dilakukan pembaruan resmi.**

---

# Purpose

Dokumentasi ini dibuat untuk memastikan bahwa:

- Seluruh keputusan arsitektur terdokumentasi.
- Seluruh proses pengembangan dapat ditelusuri.
- Framework dapat dikembangkan oleh siapa pun dengan cara yang konsisten.
- Pengetahuan proyek tidak bergantung pada individu tertentu.

---

# Documentation Philosophy

Framework ini menggunakan pendekatan:

> **Documentation Driven Development (DDD)**

Artinya:

```
Idea
    │
    ▼
Documentation
    │
    ▼
Review
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

Dokumentasi selalu dibuat sebelum implementasi.

---

# Documentation Structure

```
docs/

├── README.md

├── 00-foundation/

├── 01-product/

├── 02-architecture/

├── 03-engine/

├── 04-development/

├── 05-research/

└── adr/
```

---

# Reading Order

Bagi developer baru, urutan membaca dokumentasi adalah sebagai berikut:

## Phase 1 — Foundation

1. Project Charter
2. Project Context
3. Project Status
4. Roadmap
5. Glossary

---

## Phase 2 — Product

6. Product Vision

7. PRD

---

## Phase 3 — Architecture

8. System Architecture

9. Domain Model

10. Event Driven Architecture

11. Module Responsibilities

12. Plugin Architecture

---

## Phase 4 — Engine

13. Loader

14. Validator

15. Indicator Framework

16. Detector Framework

17. Event Engine

18. Probability Engine

19. Statistics Engine

20. Report Engine

---

## Phase 5 — Development

21. Coding Standards

22. Testing Strategy

23. Git Workflow

24. Logging

25. Error Handling

---

## Phase 6 — Research

26. Research Methodology

27. Experiment Playbook

28. Strategy Template

29. Roadmap

30. ADR

---

# Documentation Categories

## Foundation

Berisi dokumen yang mendefinisikan identitas proyek.

Contoh:

- Charter
- Project Context
- Roadmap

---

## Product

Menjelaskan kebutuhan bisnis.

---

## Architecture

Menjelaskan desain sistem.

---

## Engine

Menjelaskan implementasi setiap engine.

---

## Development

Menjelaskan standar engineering.

---

## Research

Menjelaskan metodologi riset.

---

## ADR

Architecture Decision Records.

Semua keputusan besar harus terdokumentasi.

---

# Guiding Principles

Semua dokumen dalam repository ini mengikuti prinsip berikut.

## 1. Data over Opinion

Keputusan harus berdasarkan data.

---

## 2. Event before Signal

Signal adalah hasil dari Event.

---

## 3. Signal before Trade

Trade adalah hasil evaluasi Signal.

---

## 4. Pure Functions

Business logic harus deterministic.

---

## 5. Reproducible Research

Eksperimen harus dapat diulang.

---

## 6. Small Independent Modules

Setiap modul memiliki satu tanggung jawab.

---

# Documentation Rules

Setiap dokumen wajib memiliki:

- Metadata
- Purpose
- Scope
- Dependencies
- References
- Changelog

---

# Naming Convention

Gunakan format:

```
NN_Document_Name.md
```

Contoh:

```
00_Project_Charter.md

01_Product_Vision.md

02_PRD.md
```

---

# Versioning

Status dokumen:

Draft

↓

Review

↓

Approved

↓

Deprecated

---

# Architecture Decision Records

Seluruh keputusan arsitektur dicatat pada folder:

```
docs/adr/
```

Tidak diperbolehkan mengambil keputusan arsitektur besar tanpa ADR.

---

# Contribution Workflow

```
Idea

↓

Discussion

↓

Documentation

↓

Review

↓

Implementation

↓

Testing

↓

Merge
```

---

# Project Motto

> Measure.

> Research.

> Validate.

> Then Trade.

---

# Closing Statement

Market Research Engine bukan hanya software.

Framework ini merupakan laboratorium riset yang dibangun dengan prinsip engineering, reproducibility, dan scientific thinking.

Seluruh pengembangan framework harus selalu mengacu pada dokumentasi ini.
