## Repository
trustify-backend

## Target Branch
main

## Description
Extend the GET /api/v2/search endpoint to accept filtering query parameters so users can narrow search results by entity type and date range. The feature requirement states "Add filters — Some kind of filtering capability" (MVP). This task adds optional query parameters to the search endpoint and applies them as filters in the SearchService query.

Note: The feature description does not specify which filter dimensions are required. This task implements entity_type and date range filters based on the existing data model. The engineer should confirm the required filter set with the product owner.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameters (entity_type, date_from, date_to) to the search handler's query struct
- `modules/search/src/service/mod.rs` — extend SearchService to accept and apply filter parameters to the database query

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `entity_type` (enum: sbom, advisory, package), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date). When provided, results are filtered to match the specified criteria. All parameters are optional; omitting them returns unfiltered results (preserving backward compatibility).

## Implementation Notes
- Use the shared filtering infrastructure from `common/src/db/query.rs` which already provides filtering, pagination, and sorting helpers. Follow the query builder pattern established there.
- Reference `modules/fundamental/src/sbom/endpoints/list.rs` for how list endpoints handle query parameters — the SbomList handler shows how to define a query parameter struct with Axum's `Query<T>` extractor and pass filter values to the service layer.
- Define an `EntityType` enum (Sbom, Advisory, Package) for the entity_type filter. Use serde rename attributes for lowercase serialization/deserialization.
- Date filters should use `chrono::NaiveDate` or `chrono::DateTime<Utc>` for type-safe date parsing.
- Filters are additive (AND semantics) — when multiple filters are provided, all must match.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per the error handling convention.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; extend or reuse the existing filter application logic
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference implementation for a list endpoint with query parameter handling and filter application
- `common/src/model/paginated.rs::PaginatedResults<T>` — paginated response wrapper already in use

## Acceptance Criteria
- [ ] GET /api/v2/search accepts optional `entity_type`, `date_from`, and `date_to` query parameters
- [ ] When `entity_type` is provided, only results of that entity type are returned
- [ ] When date range filters are provided, only results within the range are returned
- [ ] When no filters are provided, all results are returned (backward compatible)
- [ ] Invalid filter values return an appropriate error response (400 Bad Request)
- [ ] Filters compose correctly (AND semantics)

## Test Requirements
- [ ] Test filtering by entity_type=sbom returns only SBOM results
- [ ] Test filtering by entity_type=advisory returns only advisory results
- [ ] Test filtering by date_from and date_to returns only results within the range
- [ ] Test combining entity_type and date range filters
- [ ] Test that omitting all filters returns the same results as before (backward compatibility)
- [ ] Test invalid entity_type value returns 400 Bad Request
- [ ] Test invalid date format returns 400 Bad Request

## Verification Commands
- `cargo build -p search` — compiles without errors
- `cargo test -p search` — tests pass

## Dependencies
- Depends on: Task 1 — Add search result model types (SearchResultSummary must include entity_type field for filtering)
