# Task 3: Add search filter query parameters

## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capability to the search endpoint via query parameters. The TC-9002 feature description requires "some kind of filtering capability" but does not specify which fields should be filterable or how filters should work.

**Ambiguity noted:** "Add filters -- some kind of filtering capability" provides no specification of which fields, which entity types, or which filter operators (exact match, range, multi-select) to support. Assumption pending clarification: we implement filters for entity type, advisory severity, and date range (created_at) as these are the most commonly useful domain filters. Filter parameters are optional query parameters with AND semantics.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` -- Add query parameter extraction for filter fields: `entity_type` (enum: sbom, advisory, package), `severity` (string, for advisories), `created_after` (ISO 8601 datetime), `created_before` (ISO 8601 datetime). Parse and validate filter parameters before passing to the service layer.
- `modules/search/src/service/mod.rs` -- Accept a filter struct parameter in the search method. Apply filter conditions as SQL `WHERE` clauses. For `entity_type`, restrict which tables are queried. For `severity`, add a `WHERE severity = $value` condition (advisory only). For date range, add `WHERE created_at >= $after AND created_at <= $before`.

## Files to Create
- `modules/search/src/model/mod.rs` -- Define `SearchFilters` struct with optional fields: `entity_type: Option<EntityType>`, `severity: Option<String>`, `created_after: Option<DateTime<Utc>>`, `created_before: Option<DateTime<Utc>>`. Define `EntityType` enum with variants `Sbom`, `Advisory`, `Package`. Implement `Deserialize` for query parameter extraction.

## Implementation Notes
Use Axum's `Query<SearchFilters>` extractor to parse filter parameters from the request URL. All filter fields should be `Option<T>` so they are all optional -- when absent, no filtering is applied for that dimension.

Filter logic in the service layer:
1. `entity_type` -- when set, only search the corresponding entity table(s). When absent, search all entity types.
2. `severity` -- only applicable when searching advisories. If `entity_type` is set to something other than `Advisory` and `severity` is provided, return a 400 error.
3. `created_after` / `created_before` -- apply as `>=` and `<=` on the `created_at` column. Validate that `created_after` is not after `created_before`.

Reuse the query builder helpers from `common/src/db/query.rs` for constructing filter conditions, following the same patterns used by list endpoints in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs`.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Module pattern: each domain module follows `model/ + service/ + endpoints/` structure. Applies: task creates `modules/search/src/model/mod.rs` matching the convention's Rust module scope.

## Reuse Candidates
- `common/src/db/query.rs` -- Shared query builder helpers for filtering. Reuse existing filter condition builders rather than writing raw SQL conditions.
- `modules/fundamental/src/advisory/endpoints/list.rs` -- Example of an existing list endpoint with filtering/pagination. Follow the same pattern for filter parameter handling.
- `modules/fundamental/src/advisory/model/summary.rs` -- `AdvisorySummary` struct includes a `severity` field. Reference this for the severity filter values.

## API Changes
- `GET /api/v2/search` -- MODIFY: Add optional query parameters `entity_type` (sbom|advisory|package), `severity` (string), `created_after` (ISO 8601), `created_before` (ISO 8601). All filters are optional. When multiple filters are provided, they combine with AND semantics.

## Acceptance Criteria
- [ ] Search endpoint accepts `entity_type` filter parameter and restricts results to that type
- [ ] Search endpoint accepts `severity` filter parameter and filters advisories by severity
- [ ] Search endpoint accepts `created_after` and `created_before` date range parameters
- [ ] All filter parameters are optional -- omitting them returns unfiltered results
- [ ] Invalid filter combinations return 400 with descriptive error (e.g., severity filter with entity_type=sbom)
- [ ] Invalid date ranges return 400 with descriptive error
- [ ] Filters work in combination with the search query and relevance ranking from Task 2
- [ ] Existing search tests pass without filter parameters (backward compatibility)

## Test Requirements
- [ ] Search with `entity_type=advisory` returns only advisories
- [ ] Search with `severity=critical` returns only advisories with critical severity
- [ ] Search with `created_after` returns only results created after the given date
- [ ] Search with combined filters returns correctly intersected results
- [ ] Search with no filters behaves identically to the pre-filter endpoint
- [ ] Invalid filter combination returns 400 status code
- [ ] Invalid date range (after > before) returns 400 status code

## Dependencies
- Depends on: Task 1 -- Add database indexes for search performance (B-tree indexes on severity and created_at are needed for filter performance)

[sdlc-workflow] Description digest: sha256-md:c457e2a8553a1f05ea478daffbf06e6c18b26963e2ee8656c9e3fd7c4dc1aee3
