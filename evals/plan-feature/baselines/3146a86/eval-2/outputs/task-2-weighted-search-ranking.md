# Task 2 — Implement weighted full-text search ranking in SearchService

## Repository
trustify-backend

## Target Branch
main

## Description
Extend the SearchService to use PostgreSQL's `ts_rank` function for weighted full-text
search scoring. Currently, search results are not ranked by relevance, which causes users
to see irrelevant results at the top. This task adds weighted ranking so that matches in
high-priority fields (e.g., SBOM name, advisory title, package name) score higher than
matches in lower-priority fields (e.g., descriptions), producing more relevant result
ordering.

## Files to Modify
- `modules/search/src/service/mod.rs` — refactor `SearchService` to use `ts_rank` weighted scoring in search queries; replace simple text matching with `to_tsquery` + `ts_rank` ranking
- `common/src/db/query.rs` — add a shared query builder helper for full-text search with ranking, following the existing pattern of shared filtering/pagination/sorting helpers

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities — extend it rather than replacing it
- Use PostgreSQL `ts_rank(tsvector, tsquery)` for relevance scoring
- Apply weight categories: A (highest) for name/title fields, B for description fields, D (lowest) for other text fields
- Use `to_tsquery('english', <search_term>)` for query parsing — handle multi-word queries by converting spaces to `&` (AND) operators
- Follow the pattern in `common/src/db/query.rs` for adding shared query helpers — the existing code provides filtering, pagination, and sorting; add a `full_text_search` helper alongside these
- Reuse `PaginatedResults<T>` from `common/src/model/paginated.rs` for response wrapping — the search endpoint already uses this pattern
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per the project's error handling convention

## Reuse Candidates
- `common/src/db/query.rs` — existing query builder helpers (filtering, pagination, sorting) to follow as pattern and extend
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper already used by the search endpoint
- `common/src/error.rs` — `AppError` enum for error handling

## Acceptance Criteria
- [ ] Search queries return results ranked by relevance using `ts_rank` scoring
- [ ] Matches in name/title fields rank higher than matches in description fields
- [ ] Multi-word search queries work correctly (AND semantics)
- [ ] Empty search queries return results in default order (no ranking applied)
- [ ] Existing search endpoint contract is preserved (no breaking changes to response shape)
- [ ] A shared full-text search helper is available in `common/src/db/query.rs`

## Test Requirements
- [ ] Integration test: search for a term that appears in both an SBOM name and an advisory description — verify the SBOM result ranks higher
- [ ] Integration test: multi-word search returns only results matching all terms
- [ ] Integration test: empty search term returns results without errors
- [ ] Integration test: search ranking is deterministic for the same dataset
- [ ] Update existing tests in `tests/api/search.rs` if the result ordering changes

## Verification Commands
- `cargo test -p tests --test search` — search integration tests pass

## Dependencies
- Depends on: Task 1 — Add database indexes on searchable columns for search performance
