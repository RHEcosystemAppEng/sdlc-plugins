## Repository
trustify-backend

## Target Branch
main

## Description
Add search filter parameters to the `GET /api/v2/search` endpoint, allowing users to narrow search results by type, date range, and severity. Currently, the search endpoint accepts only a query string. This task extends it with optional filter parameters that are composed into the database query as `WHERE` clauses.

ASSUMPTION (pending clarification): The "add filters" requirement does not specify which filter types to support. This task implements three commonly useful filters based on the expected data model: `type` (entity type), `date_from`/`date_to` (creation or modification date range), and `severity` (vulnerability severity level). The actual filter set should be confirmed with the Product Owner.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add filter query parameters (`type`, `date_from`, `date_to`, `severity`) to the search endpoint using an Axum `Query` extractor struct; validate parameter formats
- `modules/search/src/service/mod.rs` — Accept filter parameters in the SearchService search method; compose them into the database query as `WHERE` clauses combined with `AND`
- `common/src/db/query.rs` — Add filter composition helpers: enum filtering (exact match on type/severity), date range filtering (>= and <= on timestamp columns), and a filter builder that chains multiple optional conditions

## Files to Create
- `modules/search/src/model/filters.rs` — Define `SearchFilters` struct with optional fields for each filter type, plus validation logic and `From` implementation for the query parameter struct

## Implementation Notes
- Per the repo's CONVENTIONS.md, the project uses the module pattern: model/ + service/ + endpoints/. The filter model belongs in `model/`, the filter application logic in `service/`, and the parameter extraction in `endpoints/`.
- Per the repo's CONVENTIONS.md, the framework is Axum for HTTP. Use `#[derive(Deserialize)]` on the query parameter struct with `Option<T>` for each filter so all filters are optional.
- Per the repo's CONVENTIONS.md, error handling uses `Result<T, AppError>` with `.context()`. Invalid filter values (e.g., malformed date) should return 400 Bad Request with a descriptive error message.
- Per the repo's CONVENTIONS.md, the database ORM is SeaORM. Use SeaORM's `Condition::all()` builder to compose multiple optional filters into a single `WHERE` clause.
- Date parameters should accept ISO 8601 format (`2024-01-01T00:00:00Z`). Use `chrono::DateTime<Utc>` for parsing.
- ASSUMPTION (pending clarification): The `type` filter values depend on the entity types in the system (e.g., "advisory", "sbom", "vulnerability", "package"). The exact enum values should be derived from the data model.
- ASSUMPTION (pending clarification): The `severity` filter values are assumed to follow CVSS severity levels ("none", "low", "medium", "high", "critical"). This should be confirmed against the actual data model.
- Filters should be composable: if multiple filters are provided, they are combined with `AND`. If no filters are provided, the search behaves as before (no regression).

## Acceptance Criteria
- [ ] The search endpoint accepts optional `type` query parameter to filter by entity type
- [ ] The search endpoint accepts optional `date_from` and `date_to` query parameters to filter by date range
- [ ] The search endpoint accepts optional `severity` query parameter to filter by severity level
- [ ] All filters are optional and composable (multiple can be applied simultaneously)
- [ ] Invalid filter values return 400 Bad Request with a descriptive error message
- [ ] When no filters are provided, search behavior is unchanged (backward-compatible)
- [ ] The `SearchFilters` model validates date ranges (date_from must be before date_to)

## Test Requirements
- [ ] Integration test in `tests/api/search.rs`: verify filtering by `type` returns only matching entity types
- [ ] Integration test: verify filtering by date range returns only results within the range
- [ ] Integration test: verify filtering by `severity` returns only matching severity levels
- [ ] Integration test: verify combining multiple filters narrows results correctly
- [ ] Integration test: verify invalid filter values (e.g., bad date format) return 400
- [ ] Integration test: verify no filters returns the same results as before (regression test)
