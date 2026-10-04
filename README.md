# Ambhara

**AI engineering · decision intelligence · research engineering**

I build AI and applied-ML systems where the important question is not only **"does it run?"** but **"can the result be evaluated, traced, reproduced, and governed?"**

My current work sits at the intersection of:

- agentic AI and evaluation
- causal and probabilistic decision systems
- forecasting, ranking, and optimization
- data-intensive systems and research engineering
- reliability, security, provenance, and bounded autonomy

## Flagship architecture

```text
                 NEXUS
          learning / policy
                 │
                 ▼
                ARGUS
        evaluation / evidence
                 │
                 ▼
                AEGIS
    assurance / governance / control
                 │
                 ▼
                ORION
       execution / observation
```

The boundaries are deliberate:

**NEXUS** learns and proposes.  
**ARGUS** evaluates and produces evidence.  
**AEGIS** assures, governs, and authorizes.  
**ORION** executes, observes, and attributes outcomes.

These flagship repositories are currently being hardened and remain private while the architecture evolves. Their public-facing documentation is kept explicit about implemented scope, evidence, and limitations rather than presenting synthetic results as real-world claims.

## Selected work

### AI and agentic systems

**EnterpriseAgentic** — production-oriented agentic RAG with hybrid retrieval, reranking, bounded self-correction, guardrails, telemetry, real SEC EDGAR ingestion, and evaluation.

**RAG Eval Harness** — deterministic evaluation infrastructure that measures retrieval and generation separately, including abstention behavior and explicit "not run" states for unavailable providers.

### Applied decision intelligence

**Retail Demand & Inventory** — M5-based forecasting, leakage-safe temporal evaluation, conformal uncertainty, and inventory-policy simulation.

**Bayesian MMM & Budgeting** — Bayesian marketing-mix modeling with known-ground-truth validation, parameter recovery, response curves, and constrained budget optimization.

**Quantitative Research** — leakage-safe quantitative research with walk-forward validation, locked protocols, holdout controls, artifact provenance, and independent evidence verification.

**Neural Search & LTR** — retrieval and ranking experiments spanning lexical retrieval, dense retrieval, fusion, reranking, LambdaMART, and statistical evaluation.

### Research engineering

**Entity Resolution** — deterministic blocking and similarity matching with ambiguity routing, calibration caveats, and evaluation that distinguishes abstention from incorrect matching.

**Cache Audit** — static analysis for prompt-caching failure modes, evaluated as a classifier so precision/recall and known limitations are visible.

**Repository Docs QA** — retrieval and grounded-Q&A evaluation over changing GitHub README corpora, with corpus-size sensitivity and abstention testing.

## Engineering principles

**Evidence before claims.**  
**Evaluation is part of the system, not a final screenshot.**  
**Data leakage and provenance are first-class concerns.**  
**Uncertainty and limitations are explicit.**  
**Security boundaries are tested, not assumed.**  
**Research evidence is separated from production capability.**  
**Reproducibility matters more than notebook-only demos.**  
**Prefer coherent systems over multiplying repositories.**

## What I optimize for

I care about systems that can survive scrutiny from three directions:

```text
                 correctness
                     ▲
                     │
        ┌────────────┼────────────┐
        │            │            │
     scientific   engineering   operational
       rigor        quality       safety
```

That means temporal validation, meaningful baselines, failure analysis, regression tests, provenance, CI, bounded execution, and honest reporting of what has **not** been proven.

## Stack

Python · PyTorch · scikit-learn · LightGBM · PyMC · FastAPI · Polars · DuckDB · PostgreSQL · Docker · GitHub Actions · TypeScript · React

<!-- PROJECTS:START -->

_Public project index is generated automatically from repositories explicitly tagged for it._

<!-- PROJECTS:END -->
