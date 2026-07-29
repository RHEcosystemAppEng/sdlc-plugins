## Repository
trustify-backend

## Target Branch
main

## Description
Implement PostgreSQL full-text search with relevance ranking in the SearchService to improve the quality and ordering of search results. Currently, the SearchService performs full-text search across entities but does not rank results by relevance, causing users to see irrelevant results prominently.

This task replaces or augments the existing search implementation with PostgreSQL's built-in full-text search capabilities: tsvector columns for indexed text, GIN indexes for fast lookup, and ts_rank (or ts_rank_cd) for relevance scoring. Results will be sorted by relevance score by default, with an option to sort by other fields.

This addresses the Feature TC-9002 MVP requirement "Results should be more relevant — users complain about irrelevant results." The Feature description does not define specific relevance criteria or field weighting; this task implements standard PostgreSQL full-text ranking as a baseline. The feature owner should confirm the ranking approach before implementation begins.

## Files to Modify
- `modules/search/service/mod.rs` — Refactor SearchService to use PostgreSQL full-text search with `to_tsvector`, `to_tsquery`, and `ts_rank` for query construction and result scoring; add relevance score to result ordering
- `modules/search/endpoints/mod.rs` — Add an optional `sort_by` query parameter (relevance, date, name) to control result ordering; default to relevance when a search query is provided
- `tests/api/search.rs` — Add integration tests verifying that results are ranked by relevance (more relevant results appear first)

## Files to Create
- `migration/src/m0003_fulltext_search_indexes/mod.rs` — Database migration to add tsvector columns (or generated columns) to searchable entities (sbom, advisory, package) and create GIN indexes on those columns for fast full-text search

## Implementation Notes
- Use PostgreSQL's `to_tsvector('english', <text_columns>)` and `to_tsquery('english', <search_term>)` for full-text search. Combine multiple text columns per entity using `||` concatenation with appropriate weights (e.g., `setweight(to_tsvector('english', name), 'A') || setweight(to_tsvector('english', description), 'B')`).
- Use `ts_rank` or `ts_rank_cd` to compute relevance scores. Sort results by descending rank score by default when a search query is provided.
- The migration should add tsvector columns (or use generated columns) to the entity tables in `entity/src/` (sbom.rs, advisory.rs, package.rs). Create GIN indexes on these columns. Follow the migration pattern in `migration/src/m0001_initial/mod.rs` and register in `migration/src/lib.rs`.
- The SearchService in `modules/search/service/mod.rs` currently implements full-text search. Inspect the existing implementation before modifying to understand what data structures and query patterns are in use.
- Use `common/src/db/query.rs` sorting helpers to add the relevance sort option alongside existing sort capabilities.
- All handler functions must return `Result<T, AppError>` with `.context()` wrapping.
- Search results must continue to use `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Integration tests should verify ordering: insert test data with known relevance characteristics (e.g., one SBOM with search term in title, another with search term only in description) and assert that the title-match appears first.
- **Ambiguity note**: The Feature does not specify relevance criteria or field weighting. This task uses standard PostgreSQL full-text ranking with title/name weighted higher than description as a baseline. Confirm with the feature owner.

## Reuse Candidates
- `common/src/db/query.rs::query` — Shared query builder helpers for sorting. Extend with a relevance-sort option rather than implementing custom ORDER BY logic.
- `modules/search/service/mod.rs::SearchService` — Existing full-text search implementation. Inspect and extend rather than replacing entirely.
- `common/src/model/paginated.rs::PaginatedResults` — Paginated response wrapper. Continue using for ranked results.

## Acceptance Criteria
- [ ] Search results are ranked by relevance score when a search query is provided
- [ ] Results matching the search term in the title/name appear before results matching only in description or other fields
- [ ] An optional `sort_by` parameter allows sorting by relevance, date, or name
- [ ] Default sort order is by relevance when a search query is present
- [ ] Default sort order remains unchanged (e.g., by date) when no search query is provided (browse mode)
- [ ] Full-text search supports multi-word queries and partial matching
- [ ] GIN indexes are created via database migration for all searchable entity tables
- [ ] Existing search functionality is not broken — queries that worked before continue to work

## Test Requirements
- [ ] Integration test: search for a term that appears in one SBOM's name and another SBOM's description; verify the name-match result appears first
- [ ] Integration test: search with sort_by=relevance returns results ordered by ts_rank score
- [ ] Integration test: search with sort_by=date returns results ordered by creation date
- [ ] Integration test: search with no query and no sort_by uses default ordering (not relevance)
- [ ] Integration test: multi-word search query returns relevant results
- [ ] Integration test: verify search results still return PaginatedResults with correct total count

## Verification Commands
- `cargo test --test search -- --test-threads=1` — Run search integration tests; all tests should pass
- `cargo build` — Verify the project compiles without errors after changes

## Dependencies
- No dependencies on other tasks
