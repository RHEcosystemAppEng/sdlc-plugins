## Repository
trustify-backend

## Target Branch
main

## Description
Add entity-type and field-value filtering capability to the search API endpoint (`GET /api/v2/search`). Currently, the search endpoint returns unfiltered full-text search results across all entity types (SBOMs, advisories, packages). This task adds query parameters that allow callers to narrow search results by entity type and by specific field values (e.g., severity for advisories, license for packages).

This addresses the Feature TC-9002 MVP requirement "Add filters — some kind of filtering capability." The Feature description does not specify which fields should be filterable; this task implements entity-type filtering and field-value filtering for the fields exposed in existing entity summary structs as a reasonable baseline. The feature owner should confirm the filterable field set before implementation begins.

## Files to Modify
- `modules/search/endpoints/mod.rs` — Add filter query parameters (entity_type, severity, license, date_range) to the GET /api/v2/search handler; extract and pass filter values to SearchService
- `modules/search/service/mod.rs` — Implement filter application logic in SearchService using common query builder helpers; apply filters as WHERE clauses on the search query
- `tests/api/search.rs` — Add integration tests for filtered search: filter by entity type, filter by field value, combined filters, empty filter results

## Files to Create
- `migration/src/m0002_search_filter_indexes/mod.rs` — Database migration to add B-tree indexes on columns used for filtering (e.g., advisory severity, package license, SBOM created_at) to ensure filter queries perform well

## Implementation Notes
- Use the existing shared query builder helpers in `common/src/db/query.rs` for constructing filter predicates. The module already provides filtering, pagination, and sorting utilities — extend or compose them rather than writing custom SQL filter logic.
- Follow the module pattern established in the codebase: model/ + service/ + endpoints/. The filter parameter struct should be defined in or near the endpoints module, similar to how list endpoints in `modules/fundamental/src/sbom/endpoints/list.rs` handle query parameters.
- All handler functions must return `Result<T, AppError>` with `.context()` wrapping per the codebase error handling convention.
- Search results with filters applied must still use `PaginatedResults<T>` from `common/src/model/paginated.rs` for the response wrapper.
- Register any new routes in `modules/search/endpoints/mod.rs` and ensure they are mounted via `server/src/main.rs`.
- For the migration, follow the existing pattern in `migration/src/m0001_initial/mod.rs`. Register the new migration in `migration/src/lib.rs`.
- Integration tests must follow the pattern in `tests/api/` — hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)`.
- **Ambiguity note**: The Feature does not specify which fields should be filterable. This task plans filtering on entity_type (SBOM, advisory, package), advisory severity, package license, and date range as a baseline. Confirm with the feature owner before implementation.

## Reuse Candidates
- `common/src/db/query.rs::query` — Shared query builder helpers for filtering, pagination, and sorting. Reuse these helpers to construct filter WHERE clauses rather than writing custom SQL predicates.
- `common/src/model/paginated.rs::PaginatedResults` — Paginated response wrapper. Reuse for filtered search result responses.
- `modules/fundamental/src/sbom/endpoints/list.rs` — GET /api/v2/sbom list endpoint. Reference as a pattern for extracting query parameters and constructing filtered, paginated responses.
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Includes severity field. Reference to confirm the filterable field name and type for advisory severity filtering.
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Includes license field. Reference to confirm the filterable field name and type for package license filtering.

## Acceptance Criteria
- [ ] GET /api/v2/search accepts an `entity_type` query parameter that filters results to a specific entity type (sbom, advisory, package)
- [ ] GET /api/v2/search accepts field-value filter parameters (severity, license, date_range) that narrow results by field value
- [ ] Multiple filters can be combined in a single request (e.g., entity_type=advisory&severity=critical)
- [ ] Filtered results are returned using the existing PaginatedResults<T> wrapper with correct total counts
- [ ] Filtering with no matching results returns an empty result set (not an error)
- [ ] Existing search behavior (no filters) is unchanged — backward compatible
- [ ] B-tree indexes are created for all filterable columns via database migration

## Test Requirements
- [ ] Integration test: search with entity_type=sbom returns only SBOM results
- [ ] Integration test: search with entity_type=advisory returns only advisory results
- [ ] Integration test: search with severity=critical returns only advisories with critical severity
- [ ] Integration test: search with combined filters (entity_type + severity) returns correctly narrowed results
- [ ] Integration test: search with no filters returns all results (backward compatibility)
- [ ] Integration test: search with filters matching no results returns empty PaginatedResults with total=0

## Verification Commands
- `cargo test --test search -- --test-threads=1` — Run search integration tests; all tests should pass
- `cargo build` — Verify the project compiles without errors after changes

## Dependencies
- No dependencies on other tasks
