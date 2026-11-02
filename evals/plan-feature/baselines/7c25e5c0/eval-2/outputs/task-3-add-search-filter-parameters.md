## Repository
trustify-backend

## Target Branch
main

## Description
Add query parameter-based filters to the search endpoint so users can narrow search results by entity-specific fields. This addresses the requirement to "add filters" with "some kind of filtering capability."

**Assumption pending clarification:** The feature description does not specify which fields should be filterable, how filters combine (AND vs OR), or what filter value formats are expected. This task assumes:
- Filters will cover entity type (SBOM, advisory, package), severity (for advisories), and date range (ingestion date)
- Multiple filters combine with AND semantics (consistent with existing list endpoint patterns in `common/src/db/query.rs`)
- Filter values are passed as query parameters (e.g., `?type=advisory&severity=high`)

If stakeholders have different filtering requirements, this scope needs revision.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameters to the `GET /api/v2/search` endpoint handler
- `modules/search/src/service/mod.rs` — extend `SearchService` to accept and apply filter criteria to search queries
- `common/src/db/query.rs` — extend shared query builder helpers if new filter patterns are needed (e.g., date range filtering)

## Implementation Notes
- The existing query builder helpers in `common/src/db/query.rs` provide filtering, pagination, and sorting utilities. Reuse these patterns for search filters rather than implementing custom filtering logic.
- The list endpoints in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` demonstrate the established pattern for query parameter extraction and filter application. Follow this pattern for the search endpoint.
- Add optional query parameters to the search endpoint handler: `type` (entity type filter), `severity` (advisory severity filter), `from_date`/`to_date` (date range filter).
- In `SearchService`, apply filters as additional `WHERE` clauses combined with the full-text search `tsquery` match using AND semantics.
- Return `PaginatedResults<T>` from `common/src/model/paginated.rs` with filter-aware total counts.
- Per docs/constraints.md §5 (Code Change Rules): keep changes scoped to search and common modules.

## Reuse Candidates
- `common/src/db/query.rs::QueryBuilder` — shared filtering and pagination helpers; reuse for filter parameter extraction and SQL clause generation

## Acceptance Criteria
- [ ] `GET /api/v2/search?type=advisory` returns only advisory entities
- [ ] `GET /api/v2/search?severity=high` returns only advisories with high severity
- [ ] `GET /api/v2/search?type=sbom&q=openssl` combines text search with type filter
- [ ] Multiple filters combine with AND semantics
- [ ] Invalid filter values return appropriate error responses (not 500)
- [ ] Omitting all filters returns unfiltered results (backward compatible)
- [ ] **Assumption pending clarification:** filter field set is assumed — stakeholders may require additional or different filter fields

## Test Requirements
- [ ] Test each filter parameter in isolation (type, severity, date range)
- [ ] Test filter combinations (type + severity, type + date range, all three)
- [ ] Test that unrecognized filter values return a 400 error
- [ ] Test that omitting filters returns the same results as the unfiltered search
- [ ] Test pagination with active filters

## Dependencies
- Depends on: Task 1 — Add full-text search indexes (required for full-text search to work alongside filters)
