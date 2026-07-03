## Repository
trustify-backend

## Target Branch
main

## Description
Improve the relevance of search results returned by GET /api/v2/search. Currently, search results lack quality ranking — users report that results are not useful. Implement relevance scoring in the SearchService to prioritize results that best match the query terms, considering factors such as exact vs partial matches, field weighting (e.g., name matches weighted higher than description matches), and recency.

Note: The Feature description does not specify relevance criteria or a scoring model. Implementers should define the scoring factors based on the entity types being searched (SBOMs, advisories, packages) and document the ranking logic.

## Files to Modify
- `modules/search/src/service/mod.rs` — implement relevance scoring logic in SearchService, order results by computed score

## Files to Create
- `modules/search/src/model/mod.rs` — search result model with relevance score field (e.g., `SearchResult<T>` wrapping entity summary + score)

## API Changes
- `GET /api/v2/search` — MODIFY: results are ordered by relevance score by default; response shape may include a relevance score field per result

## Implementation Notes
- Follow the model/ + service/ + endpoints/ module pattern used by other modules (e.g., `modules/fundamental/src/sbom/`)
- If creating search-specific model types, follow the struct definition pattern in `modules/fundamental/src/sbom/model/summary.rs` for `SbomSummary`
- Use SeaORM query builder with PostgreSQL full-text search ranking functions (e.g., `ts_rank`, `ts_rank_cd`) for relevance scoring
- Consider weighting: exact name matches > partial name matches > description matches > other fields
- Wrap scored results in `PaginatedResults<T>` from `common/src/model/paginated.rs` for consistent response format
- Per CONVENTIONS.md §Module Pattern: follow model/ + service/ + endpoints/ structure for new model types. Applies: task creates `modules/search/src/model/mod.rs` matching the convention's module structure scope.
- Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for all service methods. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's .rs file scope.
- Per CONVENTIONS.md §Response Types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's response type scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — example model struct pattern to follow for search result types
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper for consistent paginated responses
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — another model struct example; includes severity field which may inform relevance weighting

## Acceptance Criteria
- [ ] Search results are returned in relevance order by default
- [ ] Exact query term matches rank higher than partial matches
- [ ] Existing search API contract remains backward compatible (no breaking changes to response shape)
- [ ] All existing integration tests in `tests/api/search.rs` pass

## Test Requirements
- [ ] Add integration tests to `tests/api/search.rs` verifying result ordering reflects relevance (e.g., exact match appears before partial match)
- [ ] Test that a query matching an entity name exactly returns that entity as the first result
- [ ] Verify existing search tests continue to pass with unchanged behavior for unscored edge cases

## Verification Commands
- `cargo test --test search` — run search integration tests and verify all pass

## Dependencies
- None
