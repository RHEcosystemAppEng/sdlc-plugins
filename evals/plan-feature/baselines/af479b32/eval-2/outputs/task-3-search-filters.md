# Task 3: Add filtering capabilities to search endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add optional filter query parameters to the search endpoint so users can narrow search results by entity type, date range, and severity. Currently, the search endpoint returns all matching results across all entity types with no filtering options. This task adds filter parameters that combine with text search using AND semantics: all specified filters must match for a result to be included.

This addresses the MVP requirement "Add filters" from TC-9002. Note: the feature specified "Some kind of filtering capability" without details. The chosen filters (entity_type, date_from, date_to, severity) are based on the available data model fields across SBOM, advisory, and package entities.

## Files to Modify
- `modules/search/src/service/mod.rs` -- add filter predicate construction to the search query builder, applying entity type, date range, and severity conditions
- `modules/search/src/endpoints/mod.rs` -- add optional query parameters (`entity_type`, `date_from`, `date_to`, `severity`) to the search endpoint handler and pass them to SearchService
- `tests/api/search.rs` -- add integration tests for each filter type, filter combinations, and backward compatibility with no filters

## API Changes
- `GET /api/v2/search` -- MODIFY: add optional query parameters:
  - `entity_type` (string, optional): filter by entity type; values: `sbom`, `advisory`, `package`
  - `date_from` (string, optional): ISO 8601 date; include only results created on or after this date
  - `date_to` (string, optional): ISO 8601 date; include only results created on or before this date
  - `severity` (string, optional): filter advisory results by severity level (e.g., `critical`, `high`, `medium`, `low`)
  - All parameters are optional; omitting all returns unfiltered results (backward-compatible)
  - Multiple filters combine with AND semantics

## Implementation Notes
- Define a `SearchFilters` struct to encapsulate the optional filter parameters. Deserialize from query string using Axum's `Query` extractor.
- For `entity_type` filter: add a WHERE clause that restricts results to the specified entity type. If omitted, return all entity types.
- For `date_from` / `date_to` filters: add date range predicates on the entity's creation timestamp. Handle edge cases (only `date_from`, only `date_to`, both).
- For `severity` filter: apply to advisory results only. When searching across entity types, severity-filtered results exclude non-advisory entities unless `entity_type` is also set to `advisory`.
- Per CONVENTIONS.md §Query helpers: reuse shared filtering helpers from `common/src/db/query.rs` for filter predicate construction. See the existing filtering patterns for pagination and sorting as a reference. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's service query file scope.
- Per CONVENTIONS.md §Module pattern: follow `model/ + service/ + endpoints/` structure. Place the `SearchFilters` struct in the service module or a dedicated model file within `modules/search/src/`. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Validate filter parameter values and return appropriate error responses for invalid inputs (e.g., malformed dates, unknown entity types). Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's handler file scope.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Filtered results maintain the same response wrapper. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint file scope.
- Per CONVENTIONS.md §Caching: filter parameters affect cache key composition. Ensure that different filter combinations produce different cache keys to avoid returning stale results. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint route builder scope.
- Per CONVENTIONS.md §Testing: integration tests use a real PostgreSQL test database. Insert test data with varying entity types, dates, and severities to verify filter behavior. Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.
- **Ambiguity note**: Confirm the chosen filter set (entity_type, date_from, date_to, severity) with the team before implementing. The feature requirement did not specify which filters to add.

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, sorting; primary reuse target for building filter predicates
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- example of existing service with filtering patterns; reference for severity-based filtering
- `modules/fundamental/src/sbom/endpoints/list.rs` -- example of list endpoint with query parameters; reference for Axum Query extractor usage
- `common/src/model/paginated.rs::PaginatedResults` -- response wrapper to maintain for filtered result sets

## Acceptance Criteria
- [ ] Search endpoint accepts optional `entity_type`, `date_from`, `date_to`, and `severity` query parameters
- [ ] Entity type filter returns only results matching the specified type (sbom, advisory, or package)
- [ ] Date range filter (date_from, date_to) excludes results outside the specified range
- [ ] Severity filter returns only advisory results with the matching severity level
- [ ] Multiple filters combine with AND semantics (all conditions must match)
- [ ] Omitting all filter parameters returns unfiltered results (backward-compatible with existing behavior)
- [ ] Invalid filter values (malformed dates, unknown entity types) return appropriate error responses

## Test Requirements
- [ ] Verify entity_type filter returns only matching entity types (test each: sbom, advisory, package)
- [ ] Verify date_from filter excludes results created before the specified date
- [ ] Verify date_to filter excludes results created after the specified date
- [ ] Verify combined date_from + date_to returns only results within the date range
- [ ] Verify severity filter returns only advisories with matching severity
- [ ] Verify multiple filters combine correctly (e.g., entity_type=advisory + severity=high)
- [ ] Verify omitting all filters returns the same results as the unfiltered endpoint
- [ ] Verify invalid filter values return 400 Bad Request with descriptive error messages
- [ ] Existing search integration tests continue to pass without modification

## Verification Commands
- `cargo test --test api search` -- verify all search integration tests pass

## Dependencies
- Depends on: Task 1 -- Add full-text search indexes (indexed columns support efficient filtered + text search queries)
