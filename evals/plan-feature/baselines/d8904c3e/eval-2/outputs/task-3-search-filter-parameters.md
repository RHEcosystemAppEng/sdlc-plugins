## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering parameters to the search endpoint (`GET /api/v2/search`) to allow users to narrow search results by entity type, severity, and date range. The existing search implementation returns all matching entities without filtering capability.

This task addresses the TC-9002 requirement "Add filters — Some kind of filtering capability" by adding query parameter-based filters to the search endpoint and integrating filter logic into the SearchService.

**Assumption (pending clarification):** The feature description specifies "some kind of filtering capability" without defining which filters, their values, or their behavior. This task assumes the following minimum filter set based on the existing entity models:
- **Entity type filter** (`type`): filter by entity kind — `sbom`, `advisory`, or `package` (derived from the three searchable entity types in the search module)
- **Severity filter** (`severity`): filter advisories by severity level (derived from AdvisorySummary's severity field in `modules/fundamental/src/advisory/model/summary.rs`)
- **Date range filter** (`after`, `before`): filter results by creation or modification date

**Assumption (pending clarification):** Filters combine with AND semantics (all specified filters must match). If OR semantics or more complex filter expressions are needed, the query builder approach would need to be revised.

**Assumption (pending clarification):** Filters are additive query parameters on the existing `GET /api/v2/search` endpoint. No separate filter endpoint or filter configuration API is planned.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add filter query parameters to the search endpoint handler (`GET /api/v2/search`): `type`, `severity`, `after`, `before`
- `modules/search/src/service/mod.rs` — Extend SearchService to accept and apply filter criteria in search queries
- `tests/api/search.rs` — Add integration tests for filtered search results

## Implementation Notes
- Per CONVENTIONS.md §Endpoint registration: add filter query parameters to the existing route in `modules/search/src/endpoints/mod.rs`. Follow the endpoint parameter extraction pattern used in existing list endpoints (e.g., `modules/fundamental/src/sbom/endpoints/list.rs` for `GET /api/v2/sbom`).
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint .rs file scope.
- Per CONVENTIONS.md §Query helpers: use the shared filtering helpers in `common/src/db/query.rs` to build filter conditions. Inspect the existing filtering, pagination, and sorting patterns to ensure the new filter parameters integrate cleanly with the existing query builder infrastructure.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's .rs file scope.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` from all filter validation and query execution paths. Use `.context()` for error wrapping. Invalid filter values (e.g., unknown entity type, malformed date) should return appropriate HTTP 400 errors.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's .rs file scope.
- Per CONVENTIONS.md §Response types: filtered results must continue to use `PaginatedResults<T>` from `common/src/model/paginated.rs`. Filtering reduces the result set but does not change the response shape.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's .rs file scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/search.rs` following the existing pattern with a real PostgreSQL test database. Test each filter parameter individually and in combination.
  Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.
- Inspect `modules/fundamental/src/advisory/model/summary.rs` for the `AdvisorySummary` severity field values to define valid severity filter options.
- Inspect `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` for existing query parameter extraction patterns to follow.
- New query parameters must be optional — omitting a filter returns unfiltered results (backward compatible).
- Define a filter struct (e.g., `SearchFilters`) to pass filter criteria from the endpoint handler to the SearchService, keeping the endpoint layer thin.

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `type` (enum: sbom|advisory|package), `severity` (string), `after` (ISO 8601 date), `before` (ISO 8601 date). All parameters are optional; omitting them returns unfiltered results (backward compatible).

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting — the primary integration point for filter conditions
- `modules/fundamental/src/sbom/endpoints/list.rs` — Example of query parameter extraction in a list endpoint (pattern to follow for filter parameter parsing)
- `modules/fundamental/src/advisory/endpoints/list.rs` — Example of advisory-specific query parameter handling
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the severity field definition for severity filter validation
- `common/src/model/paginated.rs::PaginatedResults` — Response wrapper that filtered results must conform to
- `common/src/error.rs::AppError` — Error type for filter validation error handling

## Acceptance Criteria
- [ ] `GET /api/v2/search?type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?type=package` returns only package results
- [ ] `GET /api/v2/search?severity=critical` returns only advisories with critical severity
- [ ] `GET /api/v2/search?after=2024-01-01&before=2024-12-31` returns only results within the date range
- [ ] Multiple filters can be combined (e.g., `type=advisory&severity=high`) with AND semantics
- [ ] Omitting all filter parameters returns the same results as before (backward compatible)
- [ ] Invalid filter values return HTTP 400 with a descriptive error message
- [ ] Response shape remains `PaginatedResults<T>` — no breaking changes

## Test Requirements
- [ ] Integration test: filter by entity type returns only matching entity type
- [ ] Integration test: filter by severity returns only advisories with matching severity
- [ ] Integration test: filter by date range returns only results within the specified range
- [ ] Integration test: combining multiple filters applies AND semantics
- [ ] Integration test: omitting filters returns unfiltered results (backward compatibility)
- [ ] Integration test: invalid filter value returns HTTP 400 error
- [ ] Integration test: pagination works correctly with active filters

## Verification Commands
- `cargo test --test search` — search integration tests pass including new filter tests
- `cargo clippy --all-targets` — no new warnings introduced
- `curl "http://localhost:8080/api/v2/search?q=test&type=sbom"` — returns only SBOM results

## Dependencies
- Depends on: Task 1 — Add database indexes for search performance (indexes support efficient filtered queries)
