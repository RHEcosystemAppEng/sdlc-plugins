## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capability to the search endpoint so that users can narrow search results by entity type and entity-specific fields. The current `GET /api/v2/search` endpoint in `modules/search/src/endpoints/mod.rs` returns unfiltered full-text search results with no way to constrain results by category or field value.

**Assumption (pending clarification):** In the absence of a filter specification, this task assumes the following filter parameters for `GET /api/v2/search`:
- `entity_type` — filter by entity type: `sbom`, `advisory`, `package` (or return all if omitted)
- `severity` — filter advisory results by severity level (e.g., `critical`, `high`, `medium`, `low`)
- `date_from` / `date_to` — filter by creation or modification date range

These assumed filters should be validated with the product owner. Additional filters may be needed based on user feedback.

**Assumption (pending clarification):** Filters are combined using AND logic (all specified filters must match). If OR logic or more complex filter expressions are needed, this requires further specification.

## Files to Modify
- `modules/search/src/service/mod.rs` — extend `SearchService` to accept and apply filter parameters when constructing search queries
- `modules/search/src/endpoints/mod.rs` — add query parameters for filters to the `GET /api/v2/search` endpoint handler
- `common/src/db/query.rs` — extend shared query builder helpers to support filter predicate construction for search

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `entity_type` (string enum: sbom|advisory|package), `severity` (string), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date). All parameters are optional; when omitted, no filtering is applied for that dimension. When multiple parameters are specified, they are combined with AND logic.

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Extend it to accept a filter struct/parameters and apply them as WHERE clause predicates in the search query.
- Use the shared query builder helpers in `common/src/db/query.rs` — the existing filtering utilities support pagination and sorting; extend them to support search-specific filter predicates rather than building filter logic from scratch.
- The search endpoint handler in `modules/search/src/endpoints/mod.rs` registers `GET /api/v2/search`. Add query parameter extraction using Axum's `Query` extractor for the new filter parameters.
- For entity type filtering, reference the entity definitions: `entity/src/sbom.rs` (SBOM entity), `entity/src/advisory.rs` (Advisory entity), `entity/src/package.rs` (Package entity).
- For severity filtering, reference the `severity` field on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`.
- The response must continue to use `PaginatedResults<T>` from `common/src/model/paginated.rs` — filters reduce the result set but do not change the response shape.
- Follow the pattern used by existing list endpoints (e.g., `modules/fundamental/src/sbom/endpoints/list.rs` for `GET /api/v2/sbom`) that already implement query parameter extraction and filtering via shared helpers.
- Per docs/constraints.md §2 (Commit Rules): every commit must reference TC-9002 in the footer, follow Conventional Commits, and include the `Assisted-by: Claude Code` trailer.
- Per docs/constraints.md §3 (PR Rules): the feature branch must be named after the Jira issue ID, and the PR link must be posted as a comment on the Jira task.
- Per docs/constraints.md §5 (Code Change Rules): changes must be scoped to the files listed above, code must be inspected before modification, and implementation must follow referenced patterns.

**Convention-aware enrichment:**

- Per CONVENTIONS.md §Error Handling: all new or modified handlers must return `Result<T, AppError>` with `.context()` wrapping for error propagation. See `common/src/error.rs` for the `AppError` enum.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust handler file scope.

- Per CONVENTIONS.md §Response Types: list endpoints must return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

- Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`. Extend the existing helpers rather than building filter logic independently.
  Applies: task modifies `common/src/db/query.rs` matching the convention's query helper file scope.

- Per CONVENTIONS.md §Endpoint Registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules. The search endpoint is already registered; only the handler parameters change.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's Rust test file scope.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — shared filtering and pagination utilities to extend with search filter predicate support
- `modules/fundamental/src/sbom/endpoints/list.rs` — example of an existing list endpoint with query parameter extraction and filtering that can serve as a pattern reference
- `common/src/model/paginated.rs::PaginatedResults<T>` — response wrapper already used by all list endpoints; search filter results must use this same type

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?entity_type=package` returns only package results
- [ ] `GET /api/v2/search?severity=critical` returns only advisory results with critical severity
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` returns only results within the date range
- [ ] Multiple filters can be combined (AND logic): `entity_type=advisory&severity=high` returns only high-severity advisories
- [ ] Omitting all filter parameters returns unfiltered results (backward compatible)
- [ ] Invalid filter values return appropriate error responses (400 Bad Request)
- [ ] Existing search API response shape (`PaginatedResults<T>`) is preserved
- [ ] All existing search integration tests continue to pass

## Test Requirements
- [ ] Add integration tests in `tests/api/search.rs` for each filter parameter individually (entity_type, severity, date range)
- [ ] Add integration tests for combined filter parameters (AND logic verification)
- [ ] Add integration tests for omitted filters (backward compatibility — unfiltered results)
- [ ] Add integration tests for invalid filter values (error handling)
- [ ] Verify existing search integration tests in `tests/api/search.rs` continue to pass without modification

## Verification Commands
- `cargo test --test search` — run search integration tests and verify all pass
- `cargo build` — verify the project compiles without errors after changes

## Dependencies
- None
