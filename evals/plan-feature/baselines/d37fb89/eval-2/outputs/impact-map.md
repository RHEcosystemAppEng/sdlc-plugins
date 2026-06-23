# Repository Impact Map: TC-9002 — Improve Search Experience

## Feature Summary

TC-9002 requests improvements to the search experience: faster search, more relevant results, and filtering capabilities. The feature description is intentionally vague and requires significant clarification before definitive implementation decisions can be made.

## Workflow Mode Decision

**Mode:** direct-to-main

**Rationale:** The MVP scope involves modifications confined to a single repository (trustify-backend). The changes are incremental improvements to an existing search module — adding query optimization, relevance tuning, and filtering — rather than a cross-cutting architectural change requiring coordinated multi-repo deployment. Direct-to-main is appropriate for this scope.

## Ambiguities and Gaps

The following ambiguities have been identified in the feature description and must be clarified with the product owner before implementation details can be finalized:

### Ambiguity 1: No Performance Targets for "Faster" Search
The requirement states "Search should be faster" and "Currently too slow" but provides no quantified targets. What is the current search latency? What is the acceptable target latency (e.g., p95 < 200ms)? Without measurable targets, we cannot validate that the improvement meets expectations.
**Assumption pending clarification:** Tasks will focus on adding database indexing and query optimization as generally applicable performance improvements, but acceptance criteria cannot include specific latency thresholds until targets are defined.

### Ambiguity 2: No Definition of "More Relevant" Results
The requirement states "Results should be more relevant" and "Users complain about irrelevant results" but does not define what relevance means. Should results be ranked by text-match quality? Should certain entity types (advisories vs. SBOMs vs. packages) be prioritized? Should recency matter? Are there specific user complaints or examples of poor results to reference?
**Assumption pending clarification:** Tasks will implement PostgreSQL full-text search with ts_rank scoring as a baseline relevance improvement, but the ranking weights and field priorities are assumptions that need product validation.

### Ambiguity 3: No Specification of Which Filters to Add
The requirement states "Add filters — Some kind of filtering capability" without specifying which filters. The backend manages SBOMs, advisories, and packages — possible filters include entity type, date range, severity (advisories), license (packages), or supplier. No user research or requirements detail is provided.
**Assumption pending clarification:** Tasks will implement filtering by entity type as a minimal, broadly useful filter. Additional filters (severity, date range, etc.) should be specified by the product owner.

### Ambiguity 4: No Quantified Non-Functional Requirements
"Should be fast enough" is not a measurable requirement. No targets for response time, throughput, concurrent users, or resource consumption are given.
**Assumption pending clarification:** Tasks will ensure search queries use indexes and avoid full table scans, but no specific performance benchmarks can be asserted.

### Ambiguity 5: No Existing Performance Baseline
"Don't break existing functionality" implies backward compatibility but no existing test coverage baseline is mentioned. It is unclear which specific behaviors must be preserved (e.g., existing query parameter contracts, response shapes, pagination behavior).
**Assumption pending clarification:** Tasks will preserve the existing GET /api/v2/search endpoint contract and add new query parameters as optional additions, maintaining backward compatibility.

## Scope Exclusions

### "Better UI" (Non-MVP) — Excluded
The "Better UI" requirement is marked as non-MVP and cannot be planned:
- No frontend repository is available in the project configuration
- No design mockups or UI specifications have been provided
- Search UI improvements require frontend work that is out of scope for trustify-backend

This requirement is excluded entirely from the implementation plan.

## Impacted Repository

### trustify-backend

**Modules affected:**

| Module / Path | Impact | Reason |
|---|---|---|
| `modules/search/src/service/mod.rs` | Modify | Add full-text search ranking, optimize query execution |
| `modules/search/src/endpoints/mod.rs` | Modify | Add filter query parameters, update response structure |
| `common/src/db/query.rs` | Modify | Add full-text search query helpers and filter combinators |
| `entity/src/` | Potentially modify | Add search-related indexes if needed by migration |
| `migration/src/` | New migration | Add PostgreSQL full-text search indexes (tsvector columns, GIN indexes) |
| `tests/api/search.rs` | Modify | Add integration tests for new search features |

## Task Breakdown

| Task | Title | Dependencies |
|---|---|---|
| Task 1 | Add full-text search indexes via database migration | None |
| Task 2 | Implement relevance-ranked search in SearchService | Task 1 |
| Task 3 | Add search filter support (entity type filter) | Task 2 |
| Task 4 | Add integration tests for improved search | Task 3 |
