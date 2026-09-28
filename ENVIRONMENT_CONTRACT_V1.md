# Environment Contract v1

## Purpose

Environment Contract v1 defines the cross-system identity, provenance, trust, lifecycle, and handoff vocabulary for the four-project autonomous decision environment:

```text
NEXUS  -> learn / infer / optimize / policy lifecycle
ARGUS  -> test / falsify / evaluate / evidence
AEGIS  -> assure / govern / authorize / approve
ORION  -> execute / observe / persist outcomes
```

The contract is a wire-level agreement. It does not create a fifth runtime, policy engine, evaluator, governance engine, or executor.

## 1. Common identity context

Every cross-service request, artifact handoff, and event should preserve the following identifiers when applicable:

| Field | Meaning | Owner |
|---|---|---|
| `tenant_id` | Isolation/security boundary | AEGIS, enforced by ORION |
| `service_id` | Producing/consuming service identity | Runtime |
| `request_id` | Individual API/request identity | Caller/runtime |
| `trace_id` | Distributed trace identity | Runtime/observability |
| `correlation_id` | Business workflow identity | Workflow owner |
| `decision_id` | Immutable decision identity | AEGIS/ORION |
| `policy_artifact_hash` | Exact policy artifact identity | NEXUS |
| `action_fingerprint` | Exact action identity | AEGIS |
| `authorization_ref` | Exact authorization identity | AEGIS |
| `execution_id` | Execution lifecycle identity | ORION |
| `idempotency_key` | Duplicate-side-effect control | ORION |
| `event_id` | Immutable event identity | ORION/event backbone |

Identifiers must not be silently substituted across domains. A reference is valid only when its producer can prove the referenced object and its consumer can validate the expected binding.

## 2. Provenance chain

The minimum provenance chain is:

```text
Dataset
  -> ResearchManifest
  -> PolicyArtifact
  -> NEXUS evaluation evidence
  -> ARGUS Benchmark / EvidencePacket
  -> ARGUS EvidenceEnvelope
  -> AEGIS Decision
  -> AEGIS GovernanceResult
  -> AEGIS Authorization
  -> ORION ExecutionRequest
  -> ORION ExecutionRecord
  -> OutcomeEvent
  -> NEXUS OutcomeObservation
```

Each transition must preserve enough identity to answer:

1. What exact artifact or decision was involved?
2. Which version/environment produced it?
3. Which evidence supported the transition?
4. Which authorization allowed the transition?
5. Which execution produced the observed outcome?

## 3. Policy identity

NEXUS owns policy and research identity.

A policy handoff should carry at least:

```json
{
  "policy_id": "policy-...",
  "policy_version": "v...",
  "policy_artifact_hash": "sha256:...",
  "research_manifest_ref": "manifest-...",
  "dataset_hash": "sha256:...",
  "environment_ref": "env-..."
}
```

A policy artifact hash identifies the exact artifact. A policy name/version alone is not sufficient for execution authorization.

## 4. Evaluation identity

ARGUS owns scientific evaluation identity.

A downstream evidence handoff should identify:

```json
{
  "benchmark_id": "argus-...",
  "benchmark_version": "0.3.0",
  "environment_id": "env-...",
  "environment_version": "v...",
  "evidence_packet_id": "packet-...",
  "immutable_manifest_hash": "sha256:...",
  "evidence_identity": "sha256:..."
}
```

When evidence evaluates a concrete decision or action, the evidence may additionally bind:

```text
decision_id
action_fingerprint
policy_artifact_hash
```

Evidence is not authorization.

## 5. EvidenceEnvelope

The canonical future ARGUS-to-AEGIS handoff is an `EvidenceEnvelope`:

```json
{
  "schema_version": "evidence-envelope-v1",
  "envelope_id": "evidence-env-...",
  "issuer": "argus",
  "issued_at": "...",
  "tenant_id": "...",
  "benchmark": {
    "benchmark_id": "...",
    "benchmark_version": "...",
    "environment_id": "...",
    "environment_version": "..."
  },
  "evidence": {
    "packet_id": "...",
    "immutable_manifest_hash": "sha256:...",
    "evidence_identity": "sha256:..."
  },
  "subject": {
    "decision_id": "...",
    "action_fingerprint": "...",
    "policy_artifact_hash": "sha256:..."
  },
  "integrity": {
    "algorithm": "sha256",
    "signature": null,
    "key_id": null
  }
}
```

Cryptographic signing is a later implementation seam. Until signing is enabled, an evidence digest must still be deterministic and verifiable. An unsigned envelope must not be treated as cryptographically authenticated.

## 6. AEGIS authorization identity

AEGIS owns authorization.

An authorization must bind at minimum:

```text
tenant_id
decision_id
action_fingerprint
policy identity
assurance/evidence references
governance result
approval lineage when required
issued_at
expires_at
authorization_ref
```

The following must be rejected:

```text
valid authorization_ref + different action
valid authorization_ref + different decision
valid decision + missing authorization
valid evidence + inferred authorization
expired authorization + execution request
```

A human approval is also an authorization event only when AEGIS records the exact decision and action identity it approved.

## 7. ORION execution identity

ORION owns execution identity and side-effect controls.

The execution request should preserve:

```text
execution_id
decision_id
action_fingerprint
authorization_ref
governance_ref
idempotency_key
tenant_id
trace_id
correlation_id
policy_artifact_hash
```

ORION may validate authorization bindings, but it must not invent governance or authorization decisions.

The executor must remain idempotent for the same `idempotency_key` and must not silently reuse a key for a materially different action.

## 8. Outcome semantics

ORION owns operational outcome capture.

An execution completion does not automatically mean business success. The environment distinguishes:

```text
execution status
  !=
business outcome
```

An `OutcomeEvent` may contain:

```text
event_id
execution_id
decision_id
tenant_id
entity identity
success
actual reward
actual cost
state snapshot
decision digest
action identity
execution identity
source event references
```

NEXUS decides whether a resulting observation is scientifically eligible for OPE, FQE, causal estimation, or policy learning.

Production outcome data is not automatically trusted training data.

## 9. Event lifecycle

The canonical event vocabulary is:

```text
decision.created
evaluation.completed
evidence.issued
governance.completed
approval.requested
approval.completed
authorization.issued
execution.requested
execution.started
execution.completed
execution.failed
outcome.observed
incident.detected
policy.updated
```

ORION owns the operational event infrastructure. Other repositories publish domain events through defined adapters rather than creating competing event stores.

## 10. Trust rules

The following implications are forbidden:

```text
Evidence        -> Authorization
Authorization  -> Execution by implication
Outcome         -> Training Data
Model Output   -> Executable Command
Identifier     -> Validity without object lookup/binding
```

The correct pattern is:

```text
propose
  -> evaluate
  -> authorize
  -> validate exact identity
  -> execute
  -> observe
  -> qualify
```

## 11. Replay and integrity

Every state-changing object should be reproducible from immutable identifiers and persisted evidence where practical.

Consumers should reject:

- malformed schema versions;
- tenant mismatches;
- decision/action fingerprint mismatches;
- invalid digests;
- expired authorizations;
- unsupported contract versions;
- replayed requests with incompatible payloads.

Generated timestamps and runtime latency are observational metadata and must not alter content-derived identity hashes.

## 12. Compatibility

This document defines **Environment Contract v1**.

Repository package versions and wire/schema versions remain separate concepts. For example:

```text
package/release: 0.4.0
wire schema:      v1
environment:      v1
```

A package upgrade does not silently change a wire schema. A wire-schema change requires an explicit compatibility decision.

## 13. Ownership matrix

| Concern | NEXUS | ARGUS | AEGIS | ORION |
|---|---:|---:|---:|---:|
| Policy learning | owner | | | |
| Research provenance | owner | | | |
| Scientific evaluation | | owner | | |
| Benchmark/environment | | owner | | |
| Evidence integrity | | owner | consumes | |
| Governance | | | owner | |
| Authorization | | | owner | validates |
| Human approval | | | owner | |
| Execution | | | | owner |
| Idempotency | | | | owner |
| Operational events | | | | owner |
| Outcome capture | | | | owner |
| Scientific outcome eligibility | owner | evidence source | | |
| Distributed tracing | participates | participates | participates | runtime owner |
| Emergency execution stop | | | policy owner | enforcement owner |

## 14. Acceptance path

Environment v1 is considered integrated only when one test can demonstrate:

```text
NEXUS policy artifact
  -> ARGUS evaluates exact candidate
  -> ARGUS produces immutable evidence
  -> AEGIS verifies and binds evidence
  -> AEGIS authorizes exact action fingerprint
  -> ORION accepts only the authorized request
  -> ORION executes idempotently
  -> ORION emits outcome
  -> NEXUS receives the outcome observation
  -> NEXUS refuses scientific use when required fields are missing
```

A failure at any trust boundary must fail closed for the affected operation while preserving the audit trail.

## 15. Implementation order

1. Define and test common identity fields.
2. Add ARGUS EvidenceEnvelope with deterministic integrity.
3. Add AEGIS authorization binding to decision/action/evidence identity.
4. Add ORION enforcement of the authorization binding.
5. Propagate trace/correlation identifiers through events.
6. Add local distributed deployment and observability.
7. Add cryptographic signing/key management.
8. Run the complete acceptance path above.

This contract is deliberately incremental. Existing native repository contracts remain authoritative inside each repository until an explicit adapter implements the Environment Contract.
