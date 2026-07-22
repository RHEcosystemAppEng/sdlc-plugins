# Impact Map: TC-9002 — Improve search experience

## Feature Summary

**Jira Key**: TC-9002
**Priority**: Normal (inherited by all tasks)
**Fix Versions**: RHTPA 1.6.0 (inherited by all tasks — no fixVersion scope config, defaults to "both")

## Scope

Only MVP requirements are in scope. The "Better UI" requirement is explicitly excluded — it is marked non-MVP and cannot be planned without design mockups or a frontend repository in the Repository Registry.

## Flagged Ambiguities

1. **No performance baseline or target**: The requirement "search should be faster" and the NFR "should be fast enough" provide no quantifiable metrics. There is no baseline latency measurement, no target SLA (e.g., p95 < 200ms), and no specification of dataset size for benchmarking. Without these, "faster" is unmeasurable.

2. **No definition of relevance**: "Results should be more relevant" does not specify what makes a result relevant. There is no ranking algorithm preference (e.g., BM25, tf-idf, exact-match boosting), no description of what "irrelevant results" look like (wrong entity types? stale data? partial matches returning too broadly?), and no example queries with expected vs. actual results.

3. **No filter specification**: "Add filters — some kind of filtering capability" does not specify which entity fields should be filterable (e.g., entity type, severity, date range, license, package name), what filter operators are needed (exact match, range, multi-select, free-text), or whether filters combine with AND, OR, or both.

4. **No search scope definition**: The feature does not clarify whether "search" refers to the existing full-text search endpoint (`GET /api/v2/search`) only, or also includes the per-entity list endpoints (SBOM, advisory, package) which have their own query capabilities via `common/src/db/query.rs`.

5. **No data volume context**: "Currently too slow" provides no information about data volume (number of SBOMs, advisories, packages), whether slowness is in query execution or response serialization, or whether the issue is under normal load or concurrent access.

## Assumptions (Pending Clarification)

- **ASSUMPTION-1**: Performance optimization targets the `GET /api/v2/search` endpoint served by `modules/search/src/service/mod.rs`. PostgreSQL GIN indexes on text columns used by full-text search will provide the primary optimization.
- **ASSUMPTION-2**: Relevance ranking will use PostgreSQL `ts_rank` over `tsvector` columns, which is the standard approach for full-text search ranking in PostgreSQL-backed Rust services using SeaORM.
- **ASSUMPTION-3**: Filters will support entity type (SBOM, advisory, package) and common fields available on existing entity models: severity (advisory), license (package). Filters combine with AND logic.
- **ASSUMPTION-4**: The existing `PaginatedResults<T>` response wrapper from `common/src/model/paginated.rs` will be extended or composed to include relevance scores rather than replaced.
- **ASSUMPTION-5**: Performance improvements are measured via integration tests with timing assertions, not a separate benchmarking framework, since no performance testing infrastructure is described.

## Excluded from Scope

| Requirement | Reason |
|---|---|
| Better UI | Non-MVP. No design mockups provided. No frontend repository in the Repository Registry. Cannot be planned. |

## Impacted Repository

**trustify-backend** — all tasks target this single repository.

## Impacted Modules and Files

| Module / Path | Impact | Task(s) |
|---|---|---|
| `migration/src/` | New migration for GIN indexes and tsvector columns | Task 1 |
| `entity/src/sbom.rs` | No schema change; index is database-level only | Task 1 |
| `entity/src/advisory.rs` | No schema change; index is database-level only | Task 1 |
| `entity/src/package.rs` | No schema change; index is database-level only | Task 1 |
| `modules/search/src/service/mod.rs` | Add ts_rank scoring to search queries | Task 2 |
| `modules/search/src/lib.rs` | Re-export new model types if added | Task 2 |
| `modules/search/src/endpoints/mod.rs` | Add filter query parameters, return ranked results | Task 2, Task 3 |
| `common/src/db/query.rs` | Extend query helpers for search filter predicates | Task 3 |
| `tests/api/search.rs` | New integration tests for ranking and filtering | Task 2, Task 3 |

## Task Dependency Graph

```
Task 1: Add full-text search indexes (no dependencies)
   |
   v
Task 2: Implement relevance-ranked search results (depends on Task 1)
   |
   v
Task 3: Add filtering to search endpoint (depends on Task 2)
```

## Task Summary

| Task | Title | Repository | Dependencies |
|---|---|---|---|
| 1 | Add PostgreSQL full-text search indexes for search optimization | trustify-backend | None |
| 2 | Implement relevance-ranked search results | trustify-backend | Task 1 |
| 3 | Add entity-type and field filtering to search endpoint | trustify-backend | Task 2 |

## Field Inheritance

All tasks inherit from parent Feature TC-9002:

| Field | Value | Inheritance Rule |
|---|---|---|
| Priority | Normal | Inherited by all tasks (parent Feature priority is not "Undefined") |
| Fix Versions | RHTPA 1.6.0 | Inherited by all tasks (no fixVersion scope configured — defaults to "both") |
| Labels | ai-generated-jira | Applied per constraint 4.8 |

## Workflow Mode

**direct-to-main** — single repository, all tasks target `main` branch.

## additional_fields on Created Issues

Each created Jira task would include:

```json
{
  "priority": { "name": "Normal" },
  "fixVersions": [{ "name": "RHTPA 1.6.0" }],
  "labels": ["ai-generated-jira"]
}
```
