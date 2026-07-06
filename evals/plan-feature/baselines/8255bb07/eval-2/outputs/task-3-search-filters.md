# Task 3 — Add filter parameters to search endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint so users can narrow search results by entity type and date range. The feature requirement states "add filters — some kind of filtering capability" without specifying which filters to implement.

This task adds optional filter query parameters to the `GET /api/v2/search` endpoint and updates the `SearchService` to apply filter predicates using the existing query builder helpers in `common/src/db/query.rs`.

**Assumption:** "Some kind of filtering capability" is interpreted as a minimum viable set of filters: entity type (sbom, advisory, package) and date range (created_after, created_before). These filters are additive optional parameters. No specific filter fields, operators, or interaction model (AND/OR) were defined in the feature description (see TC-9002 ambiguity #3).

**Assumption:** Filters are combined with AND semantics (all specified filters must match). This is the standard behavior for the existing query builder helpers in `common/src/db/query.rs`.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add optional filter query parameters: `entity_type` (enum: sbom, advisory, package), `created_after` (ISO 8601 date), `created_before` (ISO 8601 date)
- `modules/search/src/service/mod.rs` — Accept filter parameters and apply them as query predicates, using the shared filtering helpers from `common/src/db/query.rs`
- `tests/api/search.rs` — Add integration tests for filtering behavior

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `entity_type` (string enum: `sbom`, `advisory`, `package`), `created_after` (ISO 8601 date string), `created_before` (ISO 8601 date string). All parameters are optional. When omitted, no filtering is applied (existing behavior preserved).

## Implementation Notes
- Define a `SearchFilter` struct in `modules/search/src/service/mod.rs` (or a new `modules/search/src/model/` directory if the struct grows complex) to hold the typed filter parameters. Use Axum's `Query<SearchFilter>` extractor in the endpoint handler.
- Leverage `common/src/db/query.rs` for building filter predicates. The existing query builder already supports filtering and pagination patterns — extend the search query to accept the same predicate types rather than implementing custom filter logic.
- The `entity_type` filter should restrict the search to a single entity table (sbom, advisory, or package). When omitted, search across all entities as before.
- The `created_after` and `created_before` filters should apply to the entity's creation timestamp column. Use SeaORM's column filtering with `ColumnTrait::gt()` and `ColumnTrait::lt()` or equivalent operators.
- The entity tables are defined in `entity/src/` — `sbom.rs`, `advisory.rs`, `package.rs`. Reference these for the column names and types when building filter predicates.
- Per CONVENTIONS.md §Error Handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping. Invalid filter parameter values (e.g., malformed dates, unknown entity types) must return structured error responses.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md §Query Helpers: use the shared filtering utilities from `common/src/db/query.rs` rather than implementing custom predicate logic. Follow the filtering patterns established in other list endpoints.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust service file scope.
- Per CONVENTIONS.md §Response Types: filtered search results must use `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md §Endpoint Registration: if new route segments are needed for filter-specific endpoints, register them in `modules/search/src/endpoints/mod.rs` following the existing route registration pattern.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/search.rs` using the established test database pattern with `assert_eq!(resp.status(), StatusCode::OK)`.
  Applies: task modifies `tests/api/search.rs` matching the convention's integration test file scope.
- Relevant constraints from `docs/constraints.md`: commit messages must follow Conventional Commits (§2.2), every commit must reference TC-9002 in the footer (§2.1), and changes must be scoped to the files listed above (§5.1).

## Reuse Candidates
- `common/src/db/query.rs::query` — Shared query builder helpers for filtering, pagination, and sorting. This is the primary reuse candidate: the search filter implementation should use these existing helpers rather than writing new filter logic.
- `common/src/model/paginated.rs::PaginatedResults` — Response wrapper for paginated list results. Filtered search results must use this type.
- `common/src/error.rs::AppError` — Error enum implementing `IntoResponse`. Use for filter validation errors (invalid date format, unknown entity type).
- `modules/fundamental/src/sbom/endpoints/list.rs` — Example of a list endpoint with query parameters. Follow this pattern for the filter parameter extraction.
- `modules/fundamental/src/advisory/endpoints/list.rs` — Another example of a list endpoint with filtering. Reference for consistent filter parameter naming.

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?entity_type=package` returns only package results
- [ ] `GET /api/v2/search?created_after=2024-01-01` returns only results created after the specified date
- [ ] `GET /api/v2/search?created_before=2024-12-31` returns only results created before the specified date
- [ ] Multiple filters can be combined (AND semantics): `entity_type=sbom&created_after=2024-01-01` returns SBOMs created after Jan 1
- [ ] Omitting all filter parameters returns all results (existing behavior preserved)
- [ ] Invalid filter values return a 400 error with a descriptive message
- [ ] All existing integration tests continue to pass

## Test Requirements
- [ ] Integration test: verify `entity_type=sbom` returns only SBOM entities
- [ ] Integration test: verify `entity_type=advisory` returns only advisory entities
- [ ] Integration test: verify `entity_type=package` returns only package entities
- [ ] Integration test: verify `created_after` filter excludes results before the specified date
- [ ] Integration test: verify `created_before` filter excludes results after the specified date
- [ ] Integration test: verify combined filters apply AND semantics
- [ ] Integration test: verify omitting filters returns unfiltered results (backward compatibility)
- [ ] Integration test: verify invalid `entity_type` value returns 400 status
- [ ] Integration test: verify malformed date in `created_after` returns 400 status

## Verification Commands
- `cargo test -p search` — verify search module compiles with filter parameters
- `cargo test --test search` — run search integration tests against the test database

## Dependencies
- None (independent task; can be implemented in parallel with Tasks 1 and 2)
