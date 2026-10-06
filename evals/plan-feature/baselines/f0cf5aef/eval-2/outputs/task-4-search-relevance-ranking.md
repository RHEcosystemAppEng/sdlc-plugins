# Task 4 — Implement search result relevance ranking

## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance-based ranking for search results returned by the SearchService. Currently, the search endpoint returns results without meaningful ordering by relevance. This task adds relevance scoring using PostgreSQL's `ts_rank` function (or equivalent) so that results matching the query more closely appear first, improving the perceived quality of search results.

This addresses the "Results should be more relevant" requirement from TC-9002. Note: the feature does not define what "relevant" means (text-match quality, recency, domain-specific scoring). This task implements PostgreSQL full-text search ranking (`ts_rank`) as a reasonable default, which scores results based on term frequency and proximity.

## Files to Modify
- `modules/search/src/service/mod.rs` — Add relevance scoring to search queries using `ts_rank`; order results by rank score descending; expose the rank score in the result model if needed
- `modules/search/src/endpoints/mod.rs` — Support an optional `sort` query parameter to allow users to switch between relevance-ranked and chronological ordering

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameter:
  - `sort` (string, optional): Sort order — `relevance` (default when a search query is present) or `date` (chronological). When no `q` parameter is provided, defaults to `date`.
  - Response items may include an optional `rank` field (float) indicating the relevance score when sorted by relevance

## Implementation Notes
- Use PostgreSQL `ts_rank(tsvector, tsquery)` to compute a relevance score for each result
- Order results by `ts_rank` descending by default when a text query is present
- When no text query is present (browsing mode), fall back to chronological ordering
- Consider using `ts_rank_cd` (cover density) for improved ranking quality if the column uses a `tsvector` with positional information
- The relevance score should be computed in the SQL query, not in application code, to leverage database-level optimization
- Per CONVENTIONS.md §Error handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md §Response types: ranked results must still use `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md §Query helpers: use shared sorting helpers from `common/src/db/query.rs` for the sort parameter rather than implementing custom sorting.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder with existing sorting helpers; extend for relevance-based sorting rather than implementing standalone sort logic
- `modules/fundamental/src/advisory/service/advisory.rs` — AdvisoryService search method; reference for how other services order query results
- `common/src/model/paginated.rs` — PaginatedResults<T>; ensure compatibility with ranked results

## Acceptance Criteria
- [ ] Search results are ordered by relevance (ts_rank) when a text query is present
- [ ] More closely matching results appear before loosely matching results
- [ ] The `sort=relevance` parameter explicitly selects relevance ordering
- [ ] The `sort=date` parameter selects chronological ordering
- [ ] When no `q` parameter is provided, results default to chronological ordering
- [ ] Relevance ranking does not break pagination (PaginatedResults still works correctly)
- [ ] Error handling follows `Result<T, AppError>` pattern

## Test Requirements
- [ ] Integration test: search for a specific term returns the most relevant result first
- [ ] Integration test: search with `sort=relevance` returns results ordered by rank
- [ ] Integration test: search with `sort=date` returns results ordered by creation date
- [ ] Integration test: search without `q` parameter returns results in chronological order
- [ ] Integration test: relevance ranking works correctly with pagination (page 2 results are less relevant than page 1)

## Verification Commands
- `cargo test --test search` — All search tests pass
- `curl "http://localhost:8080/api/v2/search?q=critical+vulnerability&sort=relevance"` — Returns results ranked by relevance

## Dependencies
- Depends on: Task 2 — Optimize SearchService query execution (relevance ranking builds on the full-text search query infrastructure optimized in Task 2)
