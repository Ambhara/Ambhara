# Ambhara

AI engineering, decision systems, and data-intensive research.

I build systems where the important question is not only **"does it run?"** but **"can the result be evaluated, traced, and explained?"**

## Flagship work

### Decision & AI systems

- **[NEXUS](https://github.com/Ambhara/Nexus)** — canonical learning and policy layer for the NEXUS → AEGIS → ORION architecture.
- **[AEGIS](https://github.com/Ambhara/Aegis)** — assurance and control-plane layer covering governance, authorization, and execution boundaries.
- **[EnterpriseAgentic](https://github.com/Ambhara/EnterpriseAgentic)** — enterprise-oriented agentic systems work.
- **[paparan-ai-z.ai](https://github.com/Ambhara/paparan-ai-z.ai)** — AI application work with portfolio verification and an explicitly documented current implementation.

### Applied decision science

- **[RetailDemandInv](https://github.com/Ambhara/RetailDemandInv)** — demand forecasting and inventory decision research.
- **[NeuralSearchLeraningRank](https://github.com/Ambhara/NeuralSearchLeraningRank)** — neural search / learning-to-rank work.
- **[CausalDecision](https://github.com/Ambhara/CausalDecision)** — causal decision research artifact.
- **[IndustrialHealthAsset](https://github.com/Ambhara/IndustrialHealthAsset)** — industrial health / asset decision systems.
- **[UrbanOPS](https://github.com/Ambhara/UrbanOPS)** — urban operations and decision-support work.
- **[BayesianMMMBudgeting](https://github.com/Ambhara/BayesianMMMBudgeting)** — Bayesian marketing-mix and budget allocation research.
- **[Marketplace Intelligence](https://github.com/Ambhara/Marketplace-Intelligence-Delivery-Risk-Decision-Science)** — marketplace delivery-risk and decision-science work.
- **[EntityResolution](https://github.com/Ambhara/EntityResolution)** — entity-resolution research and implementation.

### Research & evaluation

- **[paper](https://github.com/Ambhara/paper)** — research manuscript and experimental artifacts.
- **[rag-eval-harness](https://github.com/Ambhara/rag-eval-harness)** — evaluation infrastructure for retrieval-augmented generation systems.
- **[QuantitativeResearch](https://github.com/Ambhara/QuantitativeResearch)** — quantitative research and modeling work.

## Architecture

The current platform direction separates concerns rather than turning every repository into another platform:

```
                    NEXUS
              learning / policy
                    │
                    ▼
                  AEGIS
        assurance / governance /
          authorization / control
                    │
                    ▼
                  ORION
          execution / observation
```

Domain projects remain domain projects. They can provide research, models, evaluation evidence, and decision artifacts without being forced into the platform layer.

## Engineering principles

- **Measure before claiming.** Evaluation belongs alongside the system, not after it.
- **Keep boundaries explicit.** Learning, assurance, governance, and execution have different responsibilities.
- **Prefer additive migration.** Existing research and domain implementations remain usable while canonical interfaces are introduced.
- **Make reproducibility visible.** Tests, CI, manifests, checkpoints, and provenance should support the claims made by a repository.
- **Don't multiply repositories without a reason.** The portfolio is being consolidated around a smaller set of coherent projects.

## Research interests

Decision systems · agentic AI · retrieval and ranking · forecasting · causal inference · Bayesian modeling · optimization · evaluation · data-intensive systems

## Stack

Python · PyTorch · Polars · DuckDB · Docker · GitHub Actions · TypeScript/React

---

The repositories above are the source of truth for implementation details, experiments, and evidence. This profile is intentionally an index rather than a second copy of every project's documentation.
