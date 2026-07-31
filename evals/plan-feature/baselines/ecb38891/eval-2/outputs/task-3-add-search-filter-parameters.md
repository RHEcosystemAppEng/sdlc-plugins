## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capability to the search endpoint so users can narrow search results by entity type, date range, and severity. The feature requirement states "some kind of filtering capability" (TC-9002) without specifying exact filter fields. This task implements filters based on the entity model analysis: the search spans SBOMs, advisories, and packages, so filtering by entity type, temporal range, and advisory severity provides the most useful initial filter set.

**Note:** The filter field set (entity type, date range, severity) is derived from repository analysis of the searchable entities. The product owner should confirm these filters are the right ones and whether additional filters are needed (e.g., package license, SBOM source).

## Files to Modify
- `modules/search/src/service/mod.rs` — Add filter parameters to the SearchService search method (entity_type, date_from, date_to, severity); construct conditional WHERE clauses based on provided filters
- `modules/search/src/endpoints/mod.rs` — Accept filter query parameters on `GET /api/v2/search`; parse and validate filter values; pass validated filters to SearchService
- `common/src/db/query.rs` — Extend shared query builder helpers with filter predicate construction if reusable filter patterns emerge (e.g., date range filtering across modules)
- `tests/api/search.rs` — Add integration tests for each filter type and filter combinations

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters:
  - `entity_type` (string, enum: `sbom`, `advisory`, `package`) — filter results to a single entity type
  - `date_from` (ISO 8601 date string) — filter results to entities created/updated on or after this date
  - `date_to` (ISO 8601 date string) — filter results to entities created/updated on or before this date
  - `severity` (string, enum: `low`, `medium`, `high`, `critical`) — filter advisory results by severity level (ignored for non-advisory entity types)

## Implementation Notes
- Per CONVENTIONS.md (Key Conventions) - Query helpers: use the shared filtering and pagination utilities from `common/src/db/query.rs` to build filter predicates. Applies: task modifies `common/src/db/query.rs` matching the convention's query builder scope.
- Per CONVENTIONS.md (Key Conventions) - Error handling: filter validation errors should return appropriate HTTP error responses using `AppError`. Invalid filter values (e.g., malformed dates, unknown entity types) should return 400 Bad Request. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust error handling scope.
- Per CONVENTIONS.md (Key Conventions) - Response types: filtered results must still return `PaginatedResults<T>` with accurate `total` count reflecting the filtered result set. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint response scope.
- Per CONVENTIONS.md (Key Conventions) - Testing: integration tests go in `tests/api/` and hit a real PostgreSQL test database. Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.
- Build filter predicates using SeaORM's `Condition::all()` chaining pattern. Each filter is optional — when omitted, no constraint is added for that field.
- The `entity_type` filter determines which entity tables are included in the search query. When specified, only search the specified entity's table(s).
- The `severity` filter is only meaningful for advisory entities. When `entity_type` is set to a non-advisory type and `severity` is provided, either ignore the filter silently or return a validation error — document the chosen behavior.
- Date range filtering should use the entity's `created_at` or `updated_at` timestamp field. Use `>=` for `date_from` and `<=` for `date_to`.
- See `modules/fundamental/src/sbom/endpoints/list.rs` for an example of an endpoint that accepts query parameters for filtering.
- See `modules/fundamental/src/advisory/model/summary.rs` for the `severity` field on AdvisorySummary.

## Reuse Candidates
- `common/src/db/query.rs::filtering helpers` — shared filtering utilities for constructing WHERE clause predicates; extend rather than duplicate for date range and enum filters
- `common/src/db/query.rs::pagination helpers` — shared pagination utilities that filters must integrate with (filtered total count must be accurate)
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the `severity` field definition used for severity filtering
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference implementation of a list endpoint with query parameter handling
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains the `license` field if license filtering is added in the future

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?entity_type=package` returns only package results
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` returns only results within the specified date range
- [ ] `GET /api/v2/search?severity=critical` returns only advisory results with critical severity
- [ ] Multiple filters can be combined (e.g., `entity_type=advisory&severity=high&date_from=2024-06-01`)
- [ ] Invalid filter values (malformed dates, unknown entity types) return HTTP 400 with a descriptive error message
- [ ] Omitting all filters returns all results (backward compatible with current behavior)
- [ ] Filtered results include accurate `total` count in the `PaginatedResults` response
- [ ] Existing search functionality is not broken (all existing tests continue to pass)

## Test Requirements
- [ ] Integration test: verify `entity_type=sbom` filter returns only SBOM entities
- [ ] Integration test: verify `entity_type=advisory` filter returns only advisory entities
- [ ] Integration test: verify `entity_type=package` filter returns only package entities
- [ ] Integration test: verify `date_from` and `date_to` filters correctly constrain results by date
- [ ] Integration test: verify `severity` filter returns only advisories matching the specified severity
- [ ] Integration test: verify combining multiple filters narrows results correctly (AND semantics)
- [ ] Integration test: verify invalid `entity_type` value returns HTTP 400
- [ ] Integration test: verify malformed `date_from` value returns HTTP 400
- [ ] Integration test: verify omitting all filters returns all results (no regression)

## Verification Commands
- `cargo test -p tests --test search` — all search integration tests pass

## Documentation Updates
- `README.md` — Add documentation for the new filter query parameters on the search endpoint (entity_type, date_from, date_to, severity) with usage examples

## Dependencies
- Depends on: Task 1 — Add search indexes and optimize query performance (requires the optimized search query foundation)
