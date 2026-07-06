## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capability to the search endpoint GET /api/v2/search so users can narrow search results by specific criteria. The feature description states "Add filters — Some kind of filtering capability" but does not specify which filter dimensions, operators, or interaction patterns are needed.

**Assumption (pending clarification):** The minimum viable filter set includes:
- **Entity type filter** (`type`): filter results by entity type (sbom, advisory, package) since the search spans multiple entity types
- **Date range filter** (`from_date`, `to_date`): filter results by creation or modification date

These are assumed as the minimum useful filters. Stakeholders should confirm the desired filter dimensions. Additional filters (e.g., severity for advisories, license for packages, supplier for SBOMs) may be added in follow-up work once the filtering framework is in place.

**Assumption (pending clarification):** Filters combine with AND semantics (all specified filters must match). If OR semantics or complex filter expressions are needed, the query builder approach will need to be extended.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add filter query parameters (type, from_date, to_date) to the GET /api/v2/search handler. Parse and validate filter parameters from the request query string.
- `modules/search/src/service/mod.rs` — Implement filter logic in SearchService: accept filter parameters, build filtered queries using the shared query builder helpers, apply filters as WHERE clauses on the search query

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `type` (string, one of: sbom, advisory, package), `from_date` (ISO 8601 date string), `to_date` (ISO 8601 date string). When provided, results are filtered to match all specified criteria. Existing parameters (query text, pagination) remain unchanged.

## Implementation Notes
- Leverage the shared filtering helpers in `common/src/db/query.rs` to build filter predicates. The query.rs module already supports filtering and pagination — extend it to accept the new filter parameters rather than implementing custom filter logic in the search service.
- For the entity type filter, add a discriminator column or use the existing entity source to filter results by type. If the search currently unions results from multiple entity queries, add a conditional branch to query only the specified entity type.
- For date range filters, use standard SQL date comparison operators. Ensure the date columns are indexed (Task 1 may have already added relevant indexes).
- Validate filter parameter values at the endpoint level before passing them to the service. Return 400 Bad Request with a descriptive error for invalid filter values (e.g., invalid date format, unknown entity type).
- Ensure filters work correctly with pagination — the total count in `PaginatedResults<T>` must reflect the filtered result count, not the unfiltered total.

Per CONVENTIONS.md §Error handling: ensure all new or modified handler functions return `Result<T, AppError>` with `.context()` wrapping for meaningful error messages, including filter validation errors.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting helpers from `common/src/db/query.rs` for building filter predicates.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust service file scope.

Per CONVENTIONS.md §Response types: filtered search results must continue to return `PaginatedResults<T>` with accurate total counts reflecting the filtered set.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

Per CONVENTIONS.md §Endpoint registration: register any new routes or modified route parameters in `modules/search/src/endpoints/mod.rs`.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

Per CONVENTIONS.md §Testing: add integration tests in `tests/api/` using a real PostgreSQL test database with the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

## Reuse Candidates
- `common/src/db/query.rs::query` — Shared query builder helpers for filtering, pagination, and sorting. This is the primary reuse target — extend these helpers to support the new filter parameters rather than building custom filter logic.
- `common/src/model/paginated.rs::PaginatedResults` — Response wrapper. Ensure filtered results correctly populate the total count field.
- `common/src/error.rs::AppError` — Error enum with IntoResponse. Use for 400 Bad Request responses on invalid filter parameters.

## Acceptance Criteria
- [ ] GET /api/v2/search accepts optional `type` filter parameter and returns only results matching the specified entity type
- [ ] GET /api/v2/search accepts optional `from_date` and `to_date` filter parameters and returns only results within the specified date range
- [ ] Multiple filters can be combined (AND semantics) — e.g., filtering by type=advisory AND from_date=2024-01-01
- [ ] Invalid filter values return 400 Bad Request with a descriptive error message
- [ ] PaginatedResults total count reflects the filtered result count
- [ ] Existing search behavior without filters is unchanged (backward compatible)

## Test Requirements
- [ ] Integration test verifying filtering by entity type returns only results of that type
- [ ] Integration test verifying filtering by date range returns only results within the range
- [ ] Integration test verifying combined filters (type + date range) return the correct intersection
- [ ] Integration test verifying invalid filter values (bad date format, unknown type) return 400 status
- [ ] Integration test verifying unfiltered search still works identically to pre-filter behavior
- [ ] Integration test verifying pagination total count is correct when filters are applied

## Verification Commands
- `cargo test -p tests --test search` — verify all search integration tests pass

## Dependencies
- Depends on: Task 1 — Optimize search query performance (date column indexes should be in place for efficient date range filtering)
