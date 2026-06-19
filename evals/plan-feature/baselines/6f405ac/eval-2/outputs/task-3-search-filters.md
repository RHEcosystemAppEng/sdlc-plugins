## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint (`GET /api/v2/search`) so users can narrow search results by entity type, severity, and date range. This addresses the "add filters" MVP requirement from TC-9002.

**Ambiguity note:** The feature specifies "some kind of filtering capability" with no detail on which fields, which entities, filter combination logic, or API contract. This task assumes the following filter parameters, pending clarification:
- `entity_type` — filter by result type (sbom, advisory, package); optional, multi-value
- `severity` — filter advisories by severity level; optional, multi-value (relevant to advisory entities per `modules/fundamental/src/advisory/model/summary.rs` which includes a severity field)
- `created_after` / `created_before` — date range filter; optional
- Filters are combined with AND semantics
- All filter parameters are optional; omitting them preserves existing unfiltered behavior (backward compatible)

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add query parameter structs for filter parameters on `GET /api/v2/search`; pass parsed filters to the SearchService
- `modules/search/src/service/mod.rs` — Accept filter parameters and apply them as WHERE clauses in the search query alongside full-text search
- `common/src/db/query.rs` — Add shared filter builder helpers for entity type, severity, and date range predicates if not already covered by existing filtering utilities

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `entity_type` (string, multi-value), `severity` (string, multi-value), `created_after` (ISO 8601 date), `created_before` (ISO 8601 date)

## Implementation Notes
Inspect `modules/search/src/endpoints/mod.rs` to understand the current route definition and query parameter handling. Add a `SearchFilters` struct (or extend the existing query params struct) with the new filter fields using Axum's `Query<T>` extractor.

In `modules/search/src/service/mod.rs`, modify the search query to apply filters as additional WHERE clauses. Use the existing query builder patterns from `common/src/db/query.rs` for constructing filter predicates.

For the `entity_type` filter, the search service likely queries across multiple entity tables (SBOM, advisory, package). The filter should control which tables are included in the search union/join.

For the `severity` filter, reference `modules/fundamental/src/advisory/model/summary.rs` which defines the `AdvisorySummary` struct with a severity field — use the same severity type/enum for the filter parameter.

For date range filters, use standard SeaORM column comparison operators.

Per CONVENTIONS.md §Framework: use Axum `Query<T>` extractor for query parameters. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Invalid filter values should produce appropriate AppError variants. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Query helpers: extend shared filtering utilities in `common/src/db/query.rs`. Applies: task modifies `common/src/db/query.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Endpoint registration: if any new sub-routes are added, register them in `modules/search/src/endpoints/mod.rs`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `common/src/db/query.rs` — existing shared filtering, pagination, and sorting helpers; extend rather than duplicate
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity field type/enum to reuse for the severity filter parameter
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for how list endpoints handle query parameter extraction with Axum
- `modules/fundamental/src/advisory/endpoints/list.rs` — reference for how advisory list handles filtering

## Acceptance Criteria
- [ ] `GET /api/v2/search` accepts optional `entity_type`, `severity`, `created_after`, and `created_before` query parameters
- [ ] Omitting all filter parameters returns the same results as before (backward compatible)
- [ ] `entity_type` filter restricts results to the specified entity type(s)
- [ ] `severity` filter restricts advisory results to the specified severity level(s)
- [ ] Date range filters restrict results to the specified time window
- [ ] Invalid filter values return a clear error response via AppError
- [ ] Filters combine with AND semantics

## Test Requirements
- [ ] Search with `entity_type=sbom` returns only SBOM results
- [ ] Search with `severity=critical` returns only advisories with critical severity
- [ ] Search with `created_after` and `created_before` returns only results in the date range
- [ ] Search with multiple filters returns results matching all criteria
- [ ] Search with no filters returns all results (backward compatibility)
- [ ] Search with invalid filter values returns an appropriate error status

## Dependencies
- Depends on: Task 2 — Relevance scoring (filters are applied alongside the updated search logic)
