## Repository
trustify-backend

## Target Branch
main

## Description
Add filter query parameters to the search endpoint, allowing users to narrow search results by entity type and date range. The current search endpoint returns all matching entities without the ability to filter by category or time window. This task adds structured filtering capabilities using the shared query builder pattern from `common/src/db/query.rs`.

**Assumptions pending clarification:**
- Filters will include: entity type (SBOM, advisory, package) and date range (created_after, created_before). The feature description says "some kind of filtering capability" without specifying which attributes should be filterable. These filters were chosen based on the entity model and common search use cases.
- Filters combine with AND logic (all specified filters must match). The feature does not specify whether filters should use AND or OR semantics.
- All filter parameters are optional. When no filters are specified, the endpoint behaves identically to the current implementation (backward compatible).
- Additional filters (e.g., severity for advisories, license for packages) can be added in follow-up work once the filtering infrastructure is in place and requirements are clarified.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` -- add filter query parameters (entity_type, created_after, created_before) to the search endpoint handler
- `modules/search/src/service/mod.rs` -- accept filter criteria in SearchService methods; build filtered queries using shared query helpers
- `tests/api/search.rs` -- add tests for each filter parameter individually and in combination

## API Changes
- `GET /api/v2/search` -- MODIFY: add optional query parameters `entity_type` (string, comma-separated list of: sbom, advisory, package), `created_after` (ISO 8601 date), `created_before` (ISO 8601 date)

## Implementation Notes
- Use `common/src/db/query.rs` query builder helpers for constructing filter predicates. Inspect the existing filter patterns in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` for established conventions on query parameter extraction and predicate construction.
- Define a `SearchFilters` struct to encapsulate filter parameters, deserializable from query string parameters via Axum's `Query<SearchFilters>` extractor.
- Entity type filter should accept a comma-separated list of types: `?entity_type=sbom,advisory`. Parse and validate against known entity types.
- Date range filters should accept ISO 8601 date strings: `?created_after=2024-01-01&created_before=2024-12-31`.
- Return 400 Bad Request with a descriptive `AppError` for invalid filter values (bad date format, unknown entity type).
- Per CONVENTIONS.md §Module pattern: maintain the model/ + service/ + endpoints/ structure; place the `SearchFilters` struct in the service module or a new model file within `modules/search/src/`.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` for filter validation errors (invalid date format, unknown entity type).
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` handler scope.
- Per CONVENTIONS.md §Query helpers: use shared filtering and pagination helpers from `common/src/db/query.rs` for filter predicate construction rather than building raw SQL.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's query helper scope.
- Per CONVENTIONS.md §Response types: filtered search results must continue to use `PaginatedResults<T>` for consistent API responses across all list/search endpoints.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint response scope.
- Per CONVENTIONS.md §Testing: add integration tests following the established pattern with `assert_eq!(resp.status(), StatusCode::OK)` and status code assertions for error cases.
  Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.

## Reuse Candidates
- `common/src/db/query.rs::QueryBuilder` -- shared query builder with filtering, pagination, and sorting; reuse for filter predicate construction
- `common/src/model/paginated.rs::PaginatedResults<T>` -- response wrapper already used by all list endpoints; reuse for filtered search results
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference implementation for list endpoints with query parameter filtering; follow the same Axum extractor pattern for SearchFilters

## Acceptance Criteria
- [ ] `entity_type` filter parameter accepts comma-separated values (sbom, advisory, package) and returns only matching entity types
- [ ] `created_after` filter parameter excludes results created before the specified date
- [ ] `created_before` filter parameter excludes results created after the specified date
- [ ] Filters combine with AND logic when multiple are specified simultaneously
- [ ] All filter parameters are optional; omitting them returns unfiltered results (backward compatible)
- [ ] Invalid filter values (bad date format, unknown entity type) return 400 Bad Request with a descriptive error message
- [ ] Filters work correctly in combination with text search queries and relevance sorting from Task 2

## Test Requirements
- [ ] Test entity type filter with a single type returns only results of that type
- [ ] Test entity type filter with multiple comma-separated types returns matching types
- [ ] Test date range filter with created_after excludes older results
- [ ] Test date range filter with created_before excludes newer results
- [ ] Test combined filters (entity_type + date range + text query)
- [ ] Test that omitting all filters returns the same results as before (backward compatibility)
- [ ] Test invalid date format returns 400 error with descriptive message
- [ ] Test unknown entity type returns 400 error with descriptive message

## Verification Commands
- `cargo test -p modules-search` -- search module unit tests pass
- `cargo test -p tests --test search` -- search integration tests pass

## Dependencies
- Depends on: Task 1 -- Add database indexes for search performance (indexes improve filter query performance on large datasets)
