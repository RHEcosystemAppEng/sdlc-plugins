## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capability to the search endpoint (`GET /api/v2/search`). The feature description requires "some kind of filtering capability" but does not specify which fields, filter operations, or UI integration (see Ambiguity A3 in the impact map). This task adds query parameter-based filters to the search endpoint, following the existing query helper patterns in `common/src/db/query.rs` for filtering, pagination, and sorting.

**Ambiguity note:** The specific filterable fields and filter operations are not defined in the feature description. This implementation assumes support for filtering by entity type (SBOM, advisory, package) and common fields (name, date range). Additional filter fields should be discussed with the product owner before implementation.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` -- add filter query parameter extraction and validation to GET /api/v2/search
- `modules/search/src/service/mod.rs` -- extend SearchService to accept and apply filter parameters to search queries
- `common/src/db/query.rs` -- extend shared query helpers if needed for search-specific filter operations

## Files to Create
- `modules/search/src/model/mod.rs` -- module entry point for search model types
- `modules/search/src/model/filter.rs` -- SearchFilter struct and related types (entity type enum, date range, field filter parameters)

## API Changes
- `GET /api/v2/search` -- MODIFY: add optional query parameters for filtering:
  - `entity_type` (string, optional) -- filter by entity type (sbom, advisory, package)
  - `name` (string, optional) -- filter by name substring match
  - `date_from` (ISO 8601 date, optional) -- filter results from this date
  - `date_to` (ISO 8601 date, optional) -- filter results up to this date
  - Note: additional filters TBD based on product owner input (see Ambiguity A3)

## Implementation Notes
- Follow the existing filter/pagination pattern in `common/src/db/query.rs` -- extend the shared query builder to support search-specific filters rather than building custom filter logic
- Define a `SearchFilter` struct in `modules/search/src/model/` to encapsulate filter parameters, following the module pattern (model/ + service/ + endpoints/)
- Parse filter query parameters in the endpoint handler using Axum's `Query` extractor
- Apply filters as WHERE clauses in the SearchService query, composing with the existing full-text search predicate
- Per CONVENTIONS.md §Module Pattern: each domain module follows `model/ + service/ + endpoints/` structure -- the new model directory follows this convention.
  Applies: task creates `modules/search/src/model/mod.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Error Handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping -- apply to new filter validation error paths.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's .rs handler/service scope.
- Per CONVENTIONS.md §Query Helpers: shared filtering, pagination, and sorting via `common/src/db/query.rs` -- integrate search filters with existing helpers rather than duplicating. See `modules/fundamental/src/sbom/endpoints/list.rs` for the established filter query parameter pattern.
  Applies: task modifies `common/src/db/query.rs` matching the convention's .rs query helper scope.
- Per CONVENTIONS.md §Endpoint Registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules -- ensure filter parameters are documented in route registration.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint .rs scope.
- Per CONVENTIONS.md §Response Types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs` -- filtered search results must use this wrapper.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's .rs endpoint scope.

**Constraints (docs/constraints.md):**
- §2 Commit Rules: every commit must reference the Jira task ID in the footer, follow Conventional Commits, and include `--trailer="Assisted-by: Claude Code"`
- §3 PR Rules: branch must be named after the Jira task ID; after opening PR, post link as Jira comment; `gh pr create` must specify `--base main`
- §5 Code Change Rules: changes scoped to listed files; inspect code before modifying; follow patterns in Implementation Notes; do not duplicate existing functionality

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting; extend for search-specific filters
- `modules/fundamental/src/sbom/endpoints/list.rs` -- example of list endpoint with filter parameters; demonstrates the established filter pattern
- `modules/fundamental/src/advisory/endpoints/list.rs` -- another example of filtered list endpoint; follow the same query parameter extraction approach
- `common/src/model/paginated.rs::PaginatedResults` -- response wrapper to use for filtered search results

## Acceptance Criteria
- [ ] GET /api/v2/search accepts `entity_type` query parameter to filter results by entity type
- [ ] GET /api/v2/search accepts `name` query parameter for name substring filtering
- [ ] GET /api/v2/search accepts `date_from` and `date_to` query parameters for date range filtering
- [ ] Filters compose correctly with full-text search (filters narrow search results, not replace them)
- [ ] Invalid filter values return appropriate error responses (400 Bad Request with descriptive message)
- [ ] Omitting all filter parameters returns unfiltered results (backward-compatible)
- [ ] Existing search integration tests in `tests/api/search.rs` continue to pass

## Test Requirements
- [ ] Add integration test for entity_type filter (verify only matching entity types are returned)
- [ ] Add integration test for name filter (verify substring matching works)
- [ ] Add integration test for date range filter (verify date boundaries are respected)
- [ ] Add integration test for combined filters (verify multiple filters compose correctly)
- [ ] Add integration test for invalid filter values (verify 400 error response)
- [ ] Verify existing unfiltered search tests pass unchanged

## Verification Commands
- `cargo test --test search` -- verify search integration tests pass
- `cargo build` -- verify compilation succeeds

## Dependencies
- Depends on: Task 1 -- Optimize search query performance (filters benefit from search indexes)
