## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance scoring in the SearchService so search results are ranked by relevance rather than returned in arbitrary order. The feature requirement states "Results should be more relevant — Users complain about irrelevant results" (MVP). This task adds PostgreSQL full-text search ranking to the search query and orders results by score descending.

Note: The feature description does not define specific relevance criteria or weighting. This task implements ts_rank-based scoring as a baseline. The engineer should confirm whether additional relevance signals (recency weighting, entity type prioritization, field-specific boosting) are needed.

## Files to Modify
- `modules/search/src/service/mod.rs` — add relevance scoring using PostgreSQL ts_rank or ts_rank_cd functions; order results by score descending
- `modules/search/src/model/summary.rs` — ensure relevance_score field is populated from the ranking query (if created in Task 1)

## Implementation Notes
- Use PostgreSQL full-text search ranking functions: `ts_rank(tsvector_column, to_tsquery(search_term))` to compute relevance scores. The `ts_rank_cd` variant considers cover density and may produce better results for phrase queries.
- The relevance score should be computed as part of the SQL query (not post-processed in Rust) to enable efficient ORDER BY on the score column.
- Use SeaORM raw SQL or expression API to include the ts_rank function in the SELECT and ORDER BY clauses. Reference the query pattern in `modules/fundamental/src/advisory/service/advisory.rs` for how service methods construct complex queries.
- Populate the `relevance_score` field in `SearchResultSummary` with the computed score.
- Default ordering should be by relevance_score DESC. When no search term is provided (listing all), fall back to a sensible default order (e.g., most recently updated).
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per the error handling convention.

## Reuse Candidates
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference implementation for service methods with complex query construction
- `common/src/db/query.rs` — sorting helpers that may be extended to support relevance-based sorting
- `modules/search/src/service/mod.rs::SearchService` — existing service to extend with ranking logic

## Acceptance Criteria
- [ ] Search results are ordered by relevance score descending when a search term is provided
- [ ] Each SearchResultSummary in the response includes a populated relevance_score field
- [ ] More relevant results (closer matches to the search term) appear before less relevant ones
- [ ] When no search term is provided, results are returned in a sensible default order
- [ ] Relevance scoring does not degrade query performance compared to the unranked baseline (no full table scans)

## Test Requirements
- [ ] Test that search results for a known term return the most relevant result first
- [ ] Test that relevance_score field is a non-negative number in the response
- [ ] Test that results are ordered by relevance_score descending
- [ ] Test that an empty search term returns results in default order without errors

## Verification Commands
- `cargo build -p search` — compiles without errors
- `cargo test -p search` — tests pass

## Dependencies
- Depends on: Task 1 — Add search result model types (relevance_score field must exist in SearchResultSummary)
