## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capability to the search endpoint (GET /api/v2/search). Users need to narrow search results by entity type, date range, or other relevant fields. Extend the search endpoint to accept filter query parameters and pass them through to the SearchService for query filtering.

Note: The Feature description specifies "Some kind of filtering capability" without defining specific filter fields. Implementers should start with entity type filtering (SBOM, advisory, package) as the minimum viable filter, and consider additional filters (date range, severity) based on the entity models.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameters to the GET /api/v2/search handler using Axum query parameter extraction
- `modules/search/src/service/mod.rs` — implement filter application logic in SearchService, translating filter parameters into query predicates
- `common/src/db/query.rs` — extend shared query builder with filter predicate support if the existing helpers do not cover the needed filter types

## Files to Create
- `modules/search/src/model/mod.rs` — search filter parameter types (e.g., `SearchFilter` struct defining available filter fields and their types)

## API Changes
- `GET /api/v2/search` — MODIFY: accept new query parameters for filtering (e.g., `?type=sbom`, `?severity=high`, `?from=2024-01-01&to=2024-12-31`); invalid filter values return 400 Bad Request with descriptive error

## Implementation Notes
- Follow the filtering pattern used by existing list endpoints: `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` for query parameter handling
- Reuse shared filtering helpers from `common/src/db/query.rs` — check existing filter predicates before adding new ones
- Define filter parameter types using Axum's `Query<T>` extractor with serde deserialization
- Return filtered results using `PaginatedResults<T>` from `common/src/model/paginated.rs`
- For entity type filtering, filter at the query level (WHERE clause) rather than post-query to maintain performance
- Per CONVENTIONS.md §Endpoint Registration: register filter-enabled search routes in `modules/search/src/endpoints/mod.rs`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for invalid filter parameter errors. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's .rs file scope.
- Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`. Applies: task modifies `common/src/db/query.rs` matching the convention's query builder scope.
- Per CONVENTIONS.md §Response Types: return `PaginatedResults<T>` from filtered search results. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's response type scope.
- Per CONVENTIONS.md §Module Pattern: follow model/ + service/ + endpoints/ structure for new filter model types. Applies: task creates `modules/search/src/model/mod.rs` matching the convention's module structure scope.

## Reuse Candidates
- `common/src/db/query.rs::query` — shared query builder helpers including existing filtering logic; extend for search-specific filters
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper for consistent paginated responses
- `modules/fundamental/src/sbom/endpoints/list.rs` — example of list endpoint with query parameter extraction and filtering
- `modules/fundamental/src/advisory/endpoints/list.rs` — another list endpoint example demonstrating filter patterns

## Acceptance Criteria
- [ ] Search endpoint accepts filter query parameters (at minimum: entity type filter)
- [ ] Filters correctly narrow search results to matching entities only
- [ ] Invalid filter values return 400 Bad Request with a descriptive error message
- [ ] Unfiltered searches (no filter parameters) continue to work identically to current behavior
- [ ] Multiple filters can be combined (AND semantics)

## Test Requirements
- [ ] Add integration tests to `tests/api/search.rs` for each supported filter type (entity type, and any additional filters)
- [ ] Test combining multiple filters in a single request
- [ ] Test invalid filter parameter handling (invalid type value, malformed date range)
- [ ] Verify unfiltered search behavior is unchanged from pre-filter implementation

## Verification Commands
- `cargo test --test search` — run search integration tests and verify all pass

## Dependencies
- None
