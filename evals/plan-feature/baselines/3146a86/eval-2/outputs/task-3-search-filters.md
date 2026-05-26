# Task 3 — Add filter support to the search endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capability to the `GET /api/v2/search` endpoint so users can narrow search
results by entity type, advisory severity, and date range. The feature description requires
"some kind of filtering capability" — this task implements the three most valuable filter
dimensions based on the existing data model: entity type (SBOM, advisory, package),
severity (for advisories), and date range (creation/modification time).

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameters to the `GET /api/v2/search` endpoint handler; parse `type`, `severity`, `date_from`, `date_to` query params
- `modules/search/src/service/mod.rs` — extend `SearchService` to accept and apply filter criteria in search queries
- `common/src/db/query.rs` — add shared filter builder helpers for entity type filtering, severity filtering, and date range filtering; these should be reusable by other list endpoints

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters:
  - `type` (string, optional) — filter by entity type: `sbom`, `advisory`, `package`
  - `severity` (string, optional) — filter by advisory severity (e.g., `critical`, `high`, `medium`, `low`)
  - `date_from` (ISO 8601 date, optional) — filter results created/modified on or after this date
  - `date_to` (ISO 8601 date, optional) — filter results created/modified on or before this date

## Implementation Notes
- Follow the existing query parameter pattern in `modules/search/src/endpoints/mod.rs` — the endpoint already accepts pagination parameters; add filter parameters alongside them
- Use the existing filtering pattern in `common/src/db/query.rs` to build reusable filter helpers
- Entity type filter: add a WHERE clause matching the entity type discriminator; the search service likely searches across multiple entity tables (sbom, advisory, package), so the filter should limit which tables are queried
- Severity filter: apply only when searching advisory entities; use the `severity` field from `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs`)
- Date range filter: apply on creation/modification timestamp columns; use `>=` for `date_from` and `<=` for `date_to`
- Invalid filter values should return `400 Bad Request` via the `AppError` pattern in `common/src/error.rs`
- All new query parameters must be optional — omitting a filter means no filtering on that dimension
- Filters are AND-combined: specifying both `type=advisory` and `severity=high` returns only high-severity advisories matching the search query

## Reuse Candidates
- `common/src/db/query.rs` — existing filtering and pagination helpers to extend
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct containing the `severity` field definition
- `modules/fundamental/src/sbom/endpoints/list.rs` — example of a list endpoint with query parameter handling
- `common/src/error.rs` — `AppError` for returning 400 on invalid filter values

## Acceptance Criteria
- [ ] `GET /api/v2/search?q=term&type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?q=term&type=advisory&severity=high` returns only high-severity advisory results
- [ ] `GET /api/v2/search?q=term&date_from=2024-01-01&date_to=2024-12-31` returns only results within the date range
- [ ] Multiple filters combine with AND semantics
- [ ] Omitting all filters returns unfiltered results (backward compatible)
- [ ] Invalid filter values (e.g., `type=invalid`) return 400 Bad Request with a descriptive error
- [ ] Response shape remains `PaginatedResults<T>` — no breaking changes

## Test Requirements
- [ ] Integration test: filter by entity type returns only matching entity types
- [ ] Integration test: filter by severity returns only matching severity levels
- [ ] Integration test: date range filter returns only results within range
- [ ] Integration test: combined filters (type + severity) apply AND semantics
- [ ] Integration test: invalid filter value returns 400 status
- [ ] Integration test: no filters returns same results as unfiltered search
- [ ] Add tests to `tests/api/search.rs` following the existing `assert_eq!(resp.status(), StatusCode::OK)` pattern

## Verification Commands
- `cargo test -p tests --test search` — all search integration tests pass

## Dependencies
- Depends on: Task 2 — Implement weighted full-text search ranking in SearchService
