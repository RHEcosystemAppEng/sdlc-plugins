## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint so users can narrow search results by entity type, date range, and severity. The current search endpoint (GET /api/v2/search) accepts only a query string with no filtering options. This task extends the endpoint to accept filter query parameters and applies them in the SearchService query pipeline.

**Assumption (pending clarification):** The feature description says "some kind of filtering capability" without specifying which filters. This task assumes the following filter set based on the existing entity models: entity type (sbom, advisory, package), date range (created_after, created_before), and severity (for advisories). The product owner should confirm which filters are needed and whether additional filters (e.g., license type, package ecosystem) should be included.

**Assumption (pending clarification):** The feature description does not specify whether filters should be combined with AND or OR logic. This task assumes AND semantics (all specified filters must match) following the convention established by the existing query builder in `common/src/db/query.rs`.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` -- Add filter query parameters (entity_type, created_after, created_before, severity) to the GET /api/v2/search handler
- `modules/search/src/service/mod.rs` -- Extend SearchService to apply filter conditions to search queries
- `common/src/db/query.rs` -- Extend shared query builder helpers with filter predicate composition if not already supported
- `tests/api/search.rs` -- Add integration tests for filtered search queries

## API Changes
- `GET /api/v2/search` -- MODIFY: accepts new optional query parameters: `entity_type` (enum: sbom, advisory, package), `created_after` (ISO 8601 date), `created_before` (ISO 8601 date), `severity` (string, applies to advisory results only)

## Implementation Notes
- Follow the existing list endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` for accepting query parameters via Axum extractors. Use `axum::extract::Query<T>` with a dedicated filter struct.
- Extend the shared query builder in `common/src/db/query.rs` to support filter predicate composition. Review the existing filtering helpers to determine whether new filter types can be added as extensions or require new helper functions.
- For entity type filtering, use the existing entity models in `entity/src/` (sbom.rs, advisory.rs, package.rs) to determine the correct table/column references for conditional joins or UNION partitioning.
- For severity filtering on advisories, reference the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` which includes a severity field.
- For date range filtering, use standard SeaORM column comparison expressions against created/modified timestamp columns.
- Per CONVENTIONS.md §Error handling: wrap all filter parsing and query construction with `.context()` for descriptive error messages. Return appropriate HTTP 400 errors for invalid filter values. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust handler scope.
- Per CONVENTIONS.md §Query helpers: extend the shared filtering utilities in `common/src/db/query.rs` following established patterns rather than building custom filter logic in the search service. Applies: task modifies `common/src/db/query.rs` matching the convention's query helper scope.
- Per CONVENTIONS.md §Endpoint registration: ensure the updated search route in `modules/search/src/endpoints/mod.rs` correctly handles the new query parameters. See `modules/fundamental/src/sbom/endpoints/mod.rs` for route registration with query extractors. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Response types: filtered results should continue to use `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint list scope.
- Per CONVENTIONS.md §Testing: add filter-specific integration tests in `tests/api/search.rs` using the established test database pattern with `assert_eq!(resp.status(), StatusCode::OK)`. See `tests/api/sbom.rs` for examples. Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `common/src/db/query.rs` -- Shared query builder helpers for filtering, pagination, and sorting; extend these rather than writing custom filter logic
- `modules/fundamental/src/sbom/endpoints/list.rs` -- List endpoint example showing how to accept and validate query parameters via Axum extractors
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- Contains severity field definition useful for severity filter validation
- `common/src/model/paginated.rs::PaginatedResults` -- Response wrapper for filtered and paginated results

## Acceptance Criteria
- [ ] GET /api/v2/search accepts optional entity_type query parameter and returns only matching entity types
- [ ] GET /api/v2/search accepts optional created_after and created_before query parameters and returns only results within the date range
- [ ] GET /api/v2/search accepts optional severity query parameter and filters advisory results by severity
- [ ] Multiple filters can be combined (AND semantics)
- [ ] Omitting all filters returns unfiltered results (backward compatible)
- [ ] Invalid filter values return HTTP 400 with a descriptive error message
- [ ] Filtered results are still paginated using PaginatedResults<T>

## Test Requirements
- [ ] Integration test: filter by entity_type=sbom returns only SBOM results
- [ ] Integration test: filter by entity_type=advisory returns only advisory results
- [ ] Integration test: filter by entity_type=package returns only package results
- [ ] Integration test: filter by date range returns only results within the specified range
- [ ] Integration test: filter by severity returns only advisories matching the severity
- [ ] Integration test: combining entity_type and date range filters returns the intersection
- [ ] Integration test: omitting all filters returns the same results as the unfiltered endpoint
- [ ] Integration test: invalid entity_type value returns HTTP 400

## Verification Commands
- `cargo test -p tests --test search` -- verify all search integration tests pass including filter tests
- `cargo build -p search` -- verify search module compiles with new filter types

## Dependencies
- Depends on: Task 1 -- Optimize search query performance (indexes should be in place before adding filtered queries)
