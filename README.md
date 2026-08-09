# Market Research Engine (MRE)

> **A research engine for systematic, reproducible, and evidence-driven analysis of market behavior and trading hypotheses.**

Market Research Engine (**MRE**) adalah framework Python untuk melakukan **market research dan trading hypothesis testing** secara sistematis, reproducible, dan berbasis evidence.

MRE dirancang bukan sekadar sebagai *backtesting script*, tetapi sebagai **research engine** yang menghubungkan:

```text
Market Data
     ↓
Observation
     ↓
Indicator
     ↓
Event
     ↓
Signal
     ↓
Order
     ↓
Execution
     ↓
Position
     ↓
Trade
     ↓
Statistics
     ↓
Evidence
     ↓
Research Knowledge
```

Tujuan akhirnya bukan sekadar menjawab:

> "Strategi ini profit atau tidak?"

Tetapi:

> **"Apakah hypothesis tertentu menunjukkan evidence yang cukup kuat, robust, dan reproducible untuk dipertimbangkan lebih lanjut?"**

---

## Project Status

**Status:** Active Development  
**Current Stage:** Experimental / Research Iteration  
**Repository:** `jjaenal/market_research_engine`

MRE telah melewati fase Foundation dan kini berada pada fase **active engineering + research experimentation**.

Project saat ini mencakup:

- modular market-data processing;
- event-driven research architecture;
- signal and strategy components;
- backtesting and trade simulation;
- risk-management components;
- configurable experiment execution;
- out-of-sample analysis;
- robustness analysis;
- transaction/execution-cost modelling;
- experiment pre-registration;
- research documentation;
- automated testing.

> Project status dan development progress mengikuti repository, TODO documentation, experiment records, dan commit history sebagai source of truth.

---

# Why MRE Exists

Trading strategies sering kali diuji dengan workflow sederhana:

```text
Idea
 ↓
Code
 ↓
Backtest
 ↓
Profit
 ↓
"Strategy works"
```

Workflow tersebut terlalu mudah menghasilkan kesimpulan yang salah.

MRE menggunakan pendekatan yang lebih disciplined:

```text
Research Question
       ↓
Hypothesis
       ↓
Pre-registration
       ↓
Experiment
       ↓
Baseline
       ↓
Sensitivity
       ↓
Out-of-Sample
       ↓
Robustness
       ↓
Realistic Execution Costs
       ↓
Statistical Analysis
       ↓
Conclusion
       ↓
Accept / Reject
       ↓
Next Hypothesis
```

Dengan pendekatan tersebut, **hasil negatif tetap merupakan hasil penelitian yang bernilai**.

Sebuah hypothesis yang ditolak dapat mencegah kita menghabiskan waktu dan modal pada assumption yang tidak memiliki evidence cukup.

---

# Core Philosophy

MRE dibangun berdasarkan beberapa prinsip utama.

## 1. Data Over Opinion

Kesimpulan harus berasal dari data dan experiment yang dapat ditelusuri.

```text
Opinion
   ↓
Hypothesis
   ↓
Experiment
   ↓
Evidence
   ↓
Conclusion
```

---

## 2. Event Before Signal

Market behavior dianalisis melalui event dan observable conditions sebelum menghasilkan signal.

```text
Market Data
    ↓
Observation
    ↓
Event
    ↓
Signal
```

---

## 3. Signal Before Trade

Signal generation dipisahkan dari trade execution.

```text
Signal
  ↓
Order
  ↓
Execution
  ↓
Trade
```

Hal ini memungkinkan research engine menguji market behavior tanpa mencampurkan seluruh logic menjadi satu strategy function.

---

## 4. Reproducible Research

Experiment harus dapat direproduksi.

Secara konseptual:

```text
Experiment
   +
Dataset
   +
Configuration
   +
Code Version
   ↓
Reproducible Result
```

---

## 5. Backtest Is Evidence, Not Proof

MRE tidak menganggap hasil backtest sebagai bukti bahwa sebuah strategy pasti profitable di masa depan.

```text
Backtest
   ↓
Evidence
   ↓
Validation
   ↓
Research Conclusion
```

Bukan:

```text
Backtest
   ↓
Profit
   ↓
Guaranteed Edge
```

---

## 6. Rejection Is a Valid Result

MRE secara eksplisit memungkinkan sebuah hypothesis dinyatakan:

```text
SUPPORTED
```

atau:

```text
REJECTED
```

Hypothesis yang ditolak bukan kegagalan framework.

Justru:

> **A rejected hypothesis is useful research knowledge.**

---

# Research Lifecycle

Research workflow MRE dirancang untuk mendukung iterative experimentation.

```text
┌──────────────────────┐
│ Research Question    │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Hypothesis           │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Pre-registration     │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Experiment           │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Baseline             │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Sensitivity          │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Out-of-Sample        │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Robustness           │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Realistic Costs      │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Statistical Analysis │
└──────────┬───────────┘
           ↓
      ┌────┴────┐
      ↓         ↓
   ACCEPT     REJECT
      │         │
      └────┬────┘
           ↓
     New Knowledge
```

---

# Architecture

MRE follows a modular and event-driven architecture.

At a high level:

```text
                 ┌───────────────┐
                 │  Market Data  │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │   Research    │
                 │   Components  │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │ Event / Signal│
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │   Execution   │
                 │   Simulation  │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │ Trade / Risk  │
                 │   Management  │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │  Statistics   │
                 │  & Analysis   │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │   Evidence    │
                 └───────────────┘
```

The architecture intentionally separates:

- data;
- observations;
- indicators;
- events;
- signals;
- orders;
- execution;
- positions;
- trades;
- statistics;
- research evidence.

This separation allows individual components to be tested independently and combined into different research experiments.

---

# Repository Structure

Current repository structure:

```text
market_research_engine/
│
├── .agents/
│   └── skills/
│
├── configs/
│
├── docs/
│
├── src/
│   └── mre/
│
├── tests/
│
├── .gitignore
├── AGENTS.md
├── README.md
├── pyproject.toml
├── requirements.txt
└── skills-lock.json
```

### `src/mre/`

Core implementation of the Market Research Engine.

### `tests/`

Automated tests for validating individual components and system behavior.

### `configs/`

Experiment and runtime configuration.

### `docs/`

Project documentation, architecture decisions, research documentation, experiment records, development guidance, and project governance.

### `.agents/skills/`

Project-specific AI-assisted development skills and supporting automation.

### `AGENTS.md`

Repository-level instructions for AI-assisted development and engineering workflow.

---

# Testing Philosophy

Testing MRE occurs at multiple levels.

```text
Code
 ↓
Unit Tests
 ↓
Integration Tests
 ↓
Simulation Validation
 ↓
Research Validation
```

A passing unit test does not automatically mean that a trading hypothesis is valid.

Likewise:

```text
Software Correctness
        ≠
Research Validity
```

Both must be evaluated independently.

---

# Research Validation Layers

MRE separates several validation dimensions.

## Software Validation

Question:

> Does the implementation behave as designed?

Examples:

- parser correctness;
- indicator calculations;
- signal generation;
- order handling;
- trade simulation;
- statistics.

---

## Backtest Validation

Question:

> Does the simulation correctly represent the intended market mechanics?

Examples:

- execution timing;
- spread;
- slippage;
- transaction costs;
- position handling;
- stop-loss / take-profit behavior.

---

## Research Validation

Question:

> Does the hypothesis remain supported under appropriate validation?

Examples:

- out-of-sample testing;
- sensitivity analysis;
- robustness testing;
- execution-cost analysis;
- regime analysis;
- repeated experiments.

---

# Current Research Direction

The initial motivation for MRE came from testing trading strategies such as:

**RSI Trendline Breakout**

The original question was intentionally simple:

```text
What is the probability?

What RR is appropriate?

Does the behavior survive testing?
```

That question evolved into a broader research problem:

```text
Market Event
     ↓
Observed Behavior
     ↓
Hypothesis
     ↓
Experiment
     ↓
Probability Distribution
     ↓
Risk / Reward Analysis
     ↓
Robustness
     ↓
Evidence
```

The strategy itself is therefore treated as a **research hypothesis**, rather than an assumed profitable system.

---

# Experimental Research

MRE supports experiment-driven development.

An experiment should ideally have:

```text
Experiment ID
Hypothesis
Research Question
Dataset
Configuration
Assumptions
Method
Metrics
Validation Plan
Result
Conclusion
```

Where appropriate, experiments may be **pre-registered before execution** to reduce post-hoc decision making and preserve research integrity.

---

# Example Research Question

A research question may look like:

> Does event X produce a statistically meaningful directional outcome over horizon N under execution-cost assumption C?

The engine should allow that question to be transformed into a reproducible experiment.

For example:

```text
Event
 ↓
Entry Condition
 ↓
Holding Horizon
 ↓
Outcome
 ↓
Distribution
 ↓
Probability
 ↓
Expectancy
 ↓
Robustness
```

---

# Risk and Execution

Trading performance cannot be evaluated solely from signal accuracy.

MRE therefore considers components such as:

- stop-loss;
- take-profit;
- risk/reward;
- ATR-based risk parameters;
- spread;
- slippage;
- execution costs;
- position lifecycle;
- drawdown;
- trade distribution.

The objective is to progressively move from:

```text
Idealized Backtest
```

toward:

```text
More Realistic Execution Model
```

because a strategy that appears profitable before costs may not remain profitable after realistic execution assumptions.

---

# Research Integrity

MRE explicitly considers common sources of misleading backtest results:

- lookahead bias;
- data leakage;
- survivorship bias;
- selection bias;
- overfitting;
- curve fitting;
- data snooping;
- parameter mining;
- unrealistic execution assumptions.

The project therefore favors:

```text
Pre-registration
+
Explicit Configuration
+
Out-of-Sample Testing
+
Robustness Analysis
+
Realistic Costs
+
Reproducibility
```

---

# Development Workflow

Development follows the project TODO and documentation rather than ad-hoc feature creation.

General workflow:

```text
TODO
 ↓
Implementation
 ↓
Test
 ↓
Review
 ↓
Validation
 ↓
Documentation
 ↓
Commit
 ↓
Next TODO
```

For research work:

```text
Hypothesis
 ↓
Pre-register
 ↓
Implement
 ↓
Run Experiment
 ↓
Analyze
 ↓
Document
 ↓
Accept / Reject
```

---

# Project Documentation

The `docs/` directory is the primary documentation system.

Documentation is organized around project concerns such as:

```text
Foundation
Product
Architecture
Engine
Development
Research
ADR
Experiments
```

Start here:

**[`docs/README.md`](docs/README.md)**

The documentation contains the detailed project context, standards, architecture, development workflow, research methodology, TODOs, and experiment records.

---

# Development Principles

## Small Modules

Prefer focused modules with clear responsibilities.

## Explicit Interfaces

Components should communicate through explicit contracts.

## Deterministic Behavior

Where possible, identical inputs and configuration should produce reproducible outputs.

## Testable Components

Business and research logic should remain independently testable.

## Configuration Over Hardcoding

Experiment parameters should be explicit and reproducible.

## Evidence Over Assumption

Research conclusions should be supported by experiment results.

---

# What MRE Is Not

MRE is not intended to be:

- a guaranteed-profit trading system;
- a signal-selling service;
- a broker;
- an execution platform for live trading;
- a magic strategy optimizer;
- a tool designed to manufacture profitable backtests.

MRE is a **research and experimentation framework**.

---

# Research Mindset

The most important mindset behind MRE is:

> **The objective is not to prove that our strategy works. The objective is to discover whether the evidence supports the hypothesis.**

Therefore:

```text
Hypothesis Supported
        ↓
More Research

Hypothesis Rejected
        ↓
More Research
```

Both outcomes increase our knowledge.

---

# Project Evolution

MRE began from a relatively simple question:

```text
"How do we backtest a trading strategy
and find its probability and ideal RR?"
```

It evolved into:

```text
"How do we build a reusable research engine
that can systematically investigate market
behavior and trading hypotheses?"
```

The difference is fundamental.

The first question produces a backtest.

The second produces a **research system**.

---

# Current Development Model

The project follows an iterative engineering and research loop:

```text
┌─────────────────────────────┐
│          TODO                │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│       Implementation         │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│           Tests              │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│        Validation             │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│       Documentation          │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│           Commit             │
└──────────────┬──────────────┘
               ↓
             TODO
```

For experimental work, the loop extends into:

```text
Implementation
      ↓
Experiment
      ↓
Evidence
      ↓
Conclusion
      ↓
New Hypothesis
```

---

# Getting Started

## Requirements

MRE is a Python project.

Recommended setup:

```bash
git clone https://github.com/jjaenal/market_research_engine.git

cd market_research_engine

python -m venv .venv

source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

For development installation, use the project configuration defined in:

```text
pyproject.toml
```

---

# Running Tests

Run the test suite using the project's configured test runner.

Typical command:

```bash
pytest
```

For a focused test:

```bash
pytest tests/<test_file>.py
```

Refer to the project documentation and `pyproject.toml` for the current test configuration.

---

# Development Guidelines

Before modifying the codebase:

1. Read the relevant documentation.
2. Check the current TODO.
3. Understand the existing architecture.
4. Identify affected tests.
5. Make the smallest appropriate change.
6. Run relevant tests.
7. Update documentation if behavior changes.
8. Commit the change with a meaningful message.

Do not introduce new architecture or features solely because they appear useful.

The current TODO and research requirements are the primary drivers of development.

---

# Contributing

This project currently follows a controlled development workflow.

For changes:

```text
Understand
   ↓
Plan
   ↓
Implement
   ↓
Test
   ↓
Review
   ↓
Document
   ↓
Commit
```

Architecture-level changes should be documented through the project's architecture decision process where required.

---

# License

License information will be defined by the project before public release.

---

# Disclaimer

MRE is a research and software-engineering project.

Research results generated by MRE do not constitute financial advice and should not be interpreted as a guarantee of future trading performance.

Historical results do not guarantee future results.

---

# Project Vision

The long-term vision of Market Research Engine is to provide a disciplined environment where market hypotheses can move through a complete lifecycle:

```text
Idea
 ↓
Question
 ↓
Hypothesis
 ↓
Experiment
 ↓
Simulation
 ↓
Validation
 ↓
Evidence
 ↓
Knowledge
```

The ultimate objective is not to create the most complicated trading system.

It is to create a system that helps us answer:

> **"What does the evidence actually tell us?"**

---

**Market Research Engine (MRE)**  
*Research the market. Test the hypothesis. Follow the evidence.*