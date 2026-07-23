## Repository
trustify-backend

## Target Branch
main

## Description
Extend the GET /api/v2/search endpoint to accept filter query parameters for entity type and date range, enabling users to narrow search results to specific entity types or time windows. This addresses TC-9002 requirement: "Add filters -- some kind of filtering capability." Currently, the search endpoint returns all matching entities across all types (SBOMs, advisories, packages) without any filtering options. This task adds three optional query parameters: `entity_type` (to filter by entity kind), `created_after`, and `created_before` (to filter by creation date range). All parameters are optional and backward-compatible -- omitting them returns unfiltered results identical to the current behavior.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` -- add filter query parameter parsing and validation to the GET /api/v2/search handler
- `modules/search/src/service/mod.rs` -- add filter application logic (WHERE clauses) to the SearchService's query builder
- `tests/api/search.rs` -- add integration tests for filter parameter combinations and validation errors

## API Changes
- `GET /api/v2/search` -- MODIFY: add optional query parameters:
  - `entity_type` (string, optional) -- filter results to a single entity type. Valid values: `sbom`, `advisory`, `package`. Returns HTTP 400 for unknown values.
  - `created_after` (ISO 8601 datetime string, optional) -- return only entities created on or after this timestamp.
  - `created_before` (ISO 8601 datetime string, optional) -- return only entities created before this timestamp.
  - When both `created_after` and `created_before` are specified, `created_after` must be earlier than `created_before`; otherwise returns HTTP 400.
  - All filter parameters combine with the search query using AND semantics: results must match the search term AND all specified filters.
  - Response shape (`PaginatedResults<T>`) is unchanged.

## Implementation Notes
- Inspect `modules/search/src/endpoints/mod.rs` to understand the current handler signature and query parameter parsing before adding new parameters
- Inspect `modules/fundamental/src/sbom/endpoints/list.rs` as a reference for how existing list endpoints parse query parameters using Axum's `Query<T>` extractor
- Define a `SearchFilter` struct (or extend the existing query parameter struct) with optional fields:
  ```
  entity_type: Option<String>
  created_after: Option<chrono::DateTime<Utc>>
  created_before: Option<chrono::DateTime<Utc>>
  ```
- Derive `Deserialize` on the struct for automatic query parameter parsing via `Query<SearchFilter>`
- Validate filter parameters before passing to the service layer:
  - `entity_type` must be one of the known entity type values (`sbom`, `advisory`, `package`); return `AppError` with HTTP 400 for unknown values
  - If both `created_after` and `created_before` are present, validate that `created_after < created_before`; return `AppError` with HTTP 400 on invalid range
- In the SearchService, apply filters as additional `WHERE` clauses to the existing search query using the query builder from `common/src/db/query.rs`
- For entity type filtering, add a condition on the entity discriminator column or filter by source table join
- For date range filtering, add `>= created_after` and `< created_before` conditions on the entity's creation timestamp column
- Per CONVENTIONS.md section "Endpoint Registration": register the updated query parameter struct in the endpoint's route handler following the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md section "Response Types": continue returning `PaginatedResults<T>` from filtered search queries -- do not change the response wrapper. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md section "Error Handling": return `Result<T, AppError>` with `.context()` wrapping for filter validation errors and any new error paths. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md section "Query Helpers": use shared filtering, pagination, and sorting from `common/src/db/query.rs` for constructing filter WHERE clauses rather than writing raw SQL. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust service/query file scope.
- Per CONVENTIONS.md section "Testing": add integration tests in `tests/api/search.rs` using a real PostgreSQL test database and `assert_eq!(resp.status(), StatusCode::OK)` / `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` patterns. Applies: task modifies `tests/api/search.rs` matching the convention's Rust test file scope.

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers (filtering, pagination, sorting) -- reuse existing filter construction patterns rather than writing custom WHERE clause builders
- `modules/fundamental/src/sbom/endpoints/list.rs` -- GET /api/v2/sbom list endpoint with Axum `Query<>` extractor pattern for query parameter parsing -- follow this pattern for the new filter parameter struct
- `modules/fundamental/src/advisory/service/advisory.rs` -- AdvisoryService may have date-range or severity filtering patterns that can be adapted for search filters
- `common/src/error.rs` -- `AppError` enum with `IntoResponse` implementation for returning structured HTTP 400 validation errors
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` wrapper for the filtered response

## Acceptance Criteria
- [ ] GET /api/v2/search accepts optional `entity_type` query parameter and returns only entities of the specified type when provided
- [ ] GET /api/v2/search accepts optional `created_after` and `created_before` query parameters and returns only entities within the date range
- [ ] Omitting all filter parameters returns unfiltered results identical to current behavior (backward-compatible)
- [ ] Filters combine with the search query term using AND semantics (results match both the query and all filters)
- [ ] Invalid `entity_type` value returns HTTP 400 with a descriptive error message listing valid values
- [ ] Invalid date range (`created_after` >= `created_before`) returns HTTP 400 with a descriptive error message
- [ ] Malformed date strings in `created_after` or `created_before` return HTTP 400
- [ ] The `PaginatedResults<T>` response structure is unchanged -- `total` count reflects the filtered result count

## Test Requirements
- [ ] Test filtering by `entity_type=sbom` returns only SBOM entities
- [ ] Test filtering by `entity_type=advisory` returns only advisory entities
- [ ] Test filtering by `entity_type=package` returns only package entities
- [ ] Test filtering by date range with both `created_after` and `created_before` returns only entities within the range
- [ ] Test filtering with only `created_after` returns entities created on or after the specified date
- [ ] Test filtering with only `created_before` returns entities created before the specified date
- [ ] Test combining `entity_type` and date range filters returns correctly narrowed results
- [ ] Test that omitting all filters returns the same results as an unfiltered search (backward compatibility)
- [ ] Test invalid `entity_type` value (e.g., `entity_type=unknown`) returns HTTP 400
- [ ] Test invalid date range (`created_after` later than `created_before`) returns HTTP 400
- [ ] Test with no search query but with filters only (filter-only mode, if supported)
- [ ] All existing search integration tests continue to pass

## Verification Commands
- `cargo test -p tests --test search` -- run all search integration tests including new filter tests
- `cargo build` -- verify the project compiles without errors after adding the new parameter struct and filter logic

## Dependencies
- None
