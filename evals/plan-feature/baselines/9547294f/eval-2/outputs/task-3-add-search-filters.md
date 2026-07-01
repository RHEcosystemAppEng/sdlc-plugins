# Task 3 — Add filter parameters to search endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the `GET /api/v2/search` endpoint. The feature requirement specifies "add filters" without defining which filters are needed. Based on the data model analysis, this task adds filters for: entity type (SBOM, advisory, package), severity (for advisories), and date range (created/modified). Filters are implemented as optional query parameters, maintaining backward compatibility with existing API consumers.

**Ambiguity note:** The feature description says "Some kind of filtering capability" without specifying filter fields or types. The filter fields chosen here (entity type, severity, date range) are based on the entity model analysis and common search UX patterns. The product owner should validate this selection before implementation begins.

## Files to Modify
- `modules/search/src/service/mod.rs` — extend SearchService to accept and apply filter parameters to search queries
- `modules/search/src/endpoints/mod.rs` — add query parameter deserialization for filter fields (entity_type, severity, date_from, date_to)
- `common/src/db/query.rs` — extend shared query helpers if new filter patterns are needed beyond existing capabilities

## API Changes
- `GET /api/v2/search` — MODIFY: accepts new optional query parameters:
  - `entity_type` (string, optional): filter by entity type — values: `sbom`, `advisory`, `package`
  - `severity` (string, optional): filter by advisory severity level (only applies when entity_type is `advisory` or unset)
  - `date_from` (ISO 8601 date, optional): filter results created/modified on or after this date
  - `date_to` (ISO 8601 date, optional): filter results created/modified on or before this date
  - All filters are optional and compose with AND semantics
  - When no filters are provided, behavior is identical to the current endpoint (backward compatible)

## Implementation Notes
- Use the existing query builder helpers in `common/src/db/query.rs` for filtering and pagination. The module already provides shared filtering infrastructure — extend it rather than building parallel filter logic in the search module.
- Filter parameters should be deserialized into a `SearchFilters` struct using Axum's `Query<T>` extractor, following the pattern established in existing endpoint modules (e.g., `modules/fundamental/src/sbom/endpoints/list.rs`).
- For entity type filtering: the search query should conditionally join or filter against specific entity tables based on the `entity_type` parameter.
- For severity filtering: use the `severity` field from `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs`).
- For date range filtering: apply `WHERE created_at >= date_from AND created_at <= date_to` (or equivalent column) using SeaORM's `Condition` builder.
- Follow the existing error handling pattern: `Result<T, AppError>` with `.context()` wrapping.
- Per CONVENTIONS.md: follow the established endpoint registration pattern — each module's `endpoints/mod.rs` registers routes.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination, and sorting helpers; likely already supports some filter patterns that can be reused
- `modules/fundamental/src/sbom/endpoints/list.rs` — example of list endpoint with query parameter handling; follow the same pattern for filter deserialization
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct with `severity` field used for severity filtering
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper used by all list endpoints

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?entity_type=package` returns only package results
- [ ] `GET /api/v2/search?severity=critical` filters advisory results by severity
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` filters by date range
- [ ] Multiple filters can be combined (AND semantics)
- [ ] `GET /api/v2/search` without any filter parameters returns the same results as before (backward compatible)
- [ ] Invalid filter values return appropriate error responses

## Test Requirements
- [ ] Integration test: filter by each entity type returns only results of that type
- [ ] Integration test: severity filter narrows advisory results correctly
- [ ] Integration test: date range filter returns results within the specified range
- [ ] Integration test: combined filters (entity_type + severity) work correctly with AND semantics
- [ ] Integration test: no filters provided returns all results (backward compatibility)
- [ ] Integration test: invalid filter values return 400 Bad Request with descriptive error
- [ ] Tests added in `tests/api/search.rs` following the existing test pattern

## Verification Commands
- `cargo test -p search` — search module tests pass
- `cargo test --test search` — search integration tests pass

## Dependencies
- Depends on: Task 1 — Add full-text search indexes via database migration
