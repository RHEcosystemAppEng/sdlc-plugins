# Plan Summary — TC-9002: Improve search experience

## Tasks Created

| # | Task Title | Repository | Dependencies |
|---|---|---|---|
| 1 | Add PostgreSQL full-text search indexes for search optimization | trustify-backend | None |
| 2 | Implement relevance-ranked search results | trustify-backend | Task 1 |
| 3 | Add entity-type and field filtering to search endpoint | trustify-backend | Task 2 |

**Total tasks**: 3
**Workflow mode**: direct-to-main

## Repositories Affected

- **trustify-backend** — all 3 tasks target this repository

## Field Inheritance

All tasks inherit the following fields from parent Feature TC-9002:

| Field | Value | Rule |
|---|---|---|
| Priority | Normal | Inherited — parent Feature priority is set and not "Undefined" (constraint 1.74) |
| Fix Versions | RHTPA 1.6.0 | Inherited — no fixVersion scope configured, defaults to "both" (constraint 1.75) |
| Labels | ai-generated-jira | Applied per constraint 4.8 |

## Flagged Ambiguities

The feature description TC-9002 is underspecified. The following ambiguities were identified and must be clarified with stakeholders before implementation begins:

1. **No performance baseline or target**: "Search should be faster" and "should be fast enough" are not measurable. No current latency data, target SLA, or dataset size is provided.

2. **No definition of relevance**: "Results should be more relevant" does not define what constitutes a relevant result. No ranking algorithm preference, no example queries with expected results, and no description of what "irrelevant" results look like.

3. **No filter specification**: "Add filters — some kind of filtering capability" does not specify which fields to filter on, what filter operators are needed, or how filters should combine.

4. **No search scope definition**: It is unclear whether "search" refers only to `GET /api/v2/search` or also encompasses per-entity list endpoints.

5. **No data volume context**: "Currently too slow" provides no information about dataset size, concurrent load, or whether the bottleneck is in query execution vs. response handling.

## Assumptions Made (Pending Clarification)

| ID | Assumption | Affects Task(s) |
|---|---|---|
| ASSUMPTION-1 | Optimization targets `GET /api/v2/search` via PostgreSQL GIN indexes on tsvector columns | Task 1 |
| ASSUMPTION-2 | Relevance ranking uses PostgreSQL `ts_rank` over tsvector columns | Task 2 |
| ASSUMPTION-3 | Filters support entity type (sbom/advisory/package), severity, and license with AND combination logic | Task 3 |
| ASSUMPTION-4 | Existing `PaginatedResults<T>` is composed with a new `SearchResult` type rather than replaced | Task 2 |
| ASSUMPTION-5 | Performance is validated via integration tests, not a separate benchmarking framework | Task 1 |

## Excluded from Scope

- **Better UI** (non-MVP): Cannot be planned without design mockups or a frontend repository. No frontend repository exists in the Repository Registry.

## Documentation Task

Not generated — the feature description does not contain a Documentation Considerations section (constraint 1.84).

## Testing Tasks

Not generated — no testing readiness template exists at `docs/testing-readiness.md` in the target repository (constraint 1.86).
