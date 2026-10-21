# Task 3 — Add filtering capabilities to search endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the GET /api/v2/search endpoint, allowing users to narrow search results by specific criteria. The feature TC-9002 requires "some kind of filtering capability" but does not specify which fields, entity types, or filter operators should be supported.

**Assumption:** Filters will support the following fields based on existing entity model attributes discoverable in the codebase:
- **Entity type filter** — filter by entity kind (SBOM, advisory, package) since SearchService searches across all entities
- **Date range filter** — filter by creation/modification date, a common filtering need for document-oriented data
- **Severity filter** — filter by severity level, based on the `severity` field present in `AdvisorySummary`

**Assumption:** Filter parameters are passed as optional query parameters to GET /api/v2/search (e.g., `?type=advisory&severity=high&date_from=2024-01-01`). Omitted filters impose no constraint (all results returned).

**Assumption:** The filter operators are exact match for entity type and severity, and range (from/to) for date fields. Multi-select is not required for MVP.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameters to GET /api/v2/search route handler
- `modules/search/src/service/mod.rs` — implement filter logic in SearchService, applying filter predicates to search queries
- `tests/api/search.rs` — add integration tests for filtered search

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `type` (string: "sbom", "advisory", "package"), `severity` (string), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date)

## Implementation Notes
- Use the existing query builder filtering helpers in `common/src/db/query.rs` for constructing filter predicates — this module already provides shared filtering, pagination, and sorting patterns used by other endpoints.
- Follow the pattern established by list endpoints (e.g., `modules/fundamental/src/sbom/endpoints/list.rs`, `modules/fundamental/src/advisory/endpoints/list.rs`) for accepting and parsing query parameters.
- Define a `SearchFilter` struct to hold the optional filter parameters, following the pattern of existing filter/query structs in the codebase.
- Ensure filtered search results still use `PaginatedResults<T>` from `common/src/model/paginated.rs` as the response wrapper, consistent with all other list endpoints.
- Ensure filter parameters are optional — when omitted, the endpoint behaves identically to the current unfiltered search.
- Per CONVENTIONS.md §Module pattern: maintain the model/ + service/ + endpoints/ structure for search module changes.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Error handling: use `Result<T, AppError>` with `.context()` wrapping for all error paths in the filter parsing and query execution.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` handler scope.
- Per CONVENTIONS.md §Endpoint registration: register the updated search route with filter parameters in `modules/search/src/endpoints/mod.rs`, following the route registration pattern used by other modules.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Response types: return `PaginatedResults<T>` from the search endpoint, consistent with all list endpoints.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint `.rs` scope.
- Per CONVENTIONS.md §Query helpers: use shared filtering and pagination from `common/src/db/query.rs` for filter predicate construction.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` service file scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/` using real PostgreSQL and the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `common/src/db/query.rs::filtering helpers` — shared filtering utilities used by all list endpoints; reuse for filter predicate construction
- `common/src/model/paginated.rs::PaginatedResults<T>` — response wrapper for paginated results; already used by search endpoint
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference implementation showing query parameter extraction and filter application pattern
- `modules/fundamental/src/advisory/endpoints/list.rs` — another reference for query parameter handling with severity-based filtering

## Acceptance Criteria
- [ ] GET /api/v2/search accepts optional `type` query parameter to filter by entity type (sbom, advisory, package)
- [ ] GET /api/v2/search accepts optional `severity` query parameter to filter advisories by severity
- [ ] GET /api/v2/search accepts optional `date_from` and `date_to` query parameters for date range filtering
- [ ] Omitting all filter parameters returns the same results as the current unfiltered search (backward compatible)
- [ ] Combining multiple filters applies AND logic (all filters must match)
- [ ] Invalid filter values return appropriate error responses (400 Bad Request)
- [ ] Filtered results are still returned in the `PaginatedResults<T>` wrapper

## Test Requirements
- [ ] Integration test: search with `type=advisory` returns only advisory results
- [ ] Integration test: search with `severity=high` returns only high-severity advisories
- [ ] Integration test: search with `date_from` and `date_to` returns only results within the date range
- [ ] Integration test: search with no filters returns same results as before (backward compatibility)
- [ ] Integration test: search with invalid filter value returns 400 status
- [ ] Existing search integration tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test --test search` — verify all search integration tests pass
- `curl "http://localhost:8080/api/v2/search?q=test&type=advisory"` — manual verification of filtered search

## Dependencies
- None (can be implemented independently of Task 1 and Task 2)
