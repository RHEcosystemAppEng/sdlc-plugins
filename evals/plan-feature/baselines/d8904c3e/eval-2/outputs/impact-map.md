# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities Identified

The following ambiguities in the feature description prevent fully deterministic planning. Assumptions are documented inline per task; these require clarification from the product owner before implementation begins.

1. **"Search should be faster" — no performance baseline or target.** The requirement states "currently too slow" but provides no current latency measurements, target latency thresholds (e.g., p95 < 200ms), or definition of which search operations are slow (query execution, indexing, network). **Assumption pending clarification:** the bottleneck is database query execution time, and adding PostgreSQL full-text search indexes will address the issue.

2. **"Results should be more relevant" — no relevance criteria defined.** No definition of what constitutes a "relevant" vs "irrelevant" result. No ranking algorithm requirements, no examples of bad results, no specification of which entity fields should influence ranking. **Assumption pending clarification:** relevance means PostgreSQL full-text search ranking (ts_rank) across searchable text fields, with results ordered by match quality.

3. **"Add filters" — filter types and behavior unspecified.** "Some kind of filtering capability" does not specify which fields should be filterable, whether filters combine with AND or OR semantics, whether filters apply to all entity types or specific ones, or how filter values are validated. **Assumption pending clarification:** filters are query parameters on the existing search endpoint, supporting entity type, severity, and date range filters with AND semantics.

4. **"Should be fast enough" (NFR) — no quantifiable target.** No latency SLA, throughput requirements, or percentile targets (p50, p95, p99). Cannot validate this NFR without measurable criteria.

5. **"Don't break existing functionality" (NFR) — no backward compatibility specification.** No definition of what constitutes "breaking" — API contract stability? Response shape preservation? Existing query parameter behavior? **Assumption pending clarification:** existing GET /api/v2/search endpoint contract (request parameters and response shape) must remain backward-compatible; new parameters are additive only.

## Impact Map

```
trustify-backend:
  changes:
    - Add database migration for full-text search indexes on searchable entity columns (sbom, advisory, package)
    - Enhance SearchService to use PostgreSQL full-text search with relevance ranking (ts_rank)
    - Add filter query parameters (entity type, severity, date range) to GET /api/v2/search endpoint
    - Update search integration tests to cover ranking and filtering behavior
```

## Excluded Requirements

| Requirement | MVP? | Reason for Exclusion |
|---|---|---|
| Better UI — "Make it look nicer" | No | No design mockups available and no frontend repository in the Repository Registry. Cannot decompose into actionable tasks without visual specifications and a target frontend codebase. |

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:
- All changes are within a single repository (trustify-backend) — no cross-repo coordination needed
- The three MVP requirements (performance, relevance, filters) can be implemented and merged independently without leaving main in a broken state
- Each task adds additive functionality to the existing search module — no breaking API changes between tasks
- No coordinated schema migrations — the index migration (Task 1) is independent of the service-level changes (Tasks 2 and 3)

## Field Inheritance

- **Priority:** Normal (inherited from TC-9002, will be propagated to all tasks)
- **Fix Versions:** RHTPA 1.6.0 (inherited from TC-9002, will be propagated to all tasks — no fixVersion scope restriction configured, defaulting to "both")
