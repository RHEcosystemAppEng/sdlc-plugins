## Repository
trustify-backend

## Target Branch
main

## Description
Refactor the SearchService to replace naive text matching (LIKE/ILIKE) with PostgreSQL full-text search using tsvector/tsquery and ts_rank for relevance-based result ranking. This addresses both the "search should be faster" and "results should be more relevant" requirements from TC-9002.

**Ambiguity note:** The feature does not define what "more relevant" means. Assumption (pending clarification): relevance is determined by PostgreSQL ts_rank scoring with weighted fields — entity title/name fields are weighted higher (weight A) than description/summary fields (weight B). Results are returned ordered by descending rank score.

## Files to Modify
- `modules/search/src/service/mod.rs` — refactor `SearchService` full-text search implementation to use tsvector/tsquery with ts_rank ranking
- `modules/search/src/lib.rs` — update module exports if new types are introduced for search ranking configuration

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Replace the current query mechanism with PostgreSQL `to_tsquery` for parsing search terms and `ts_rank` for scoring results.
- Use `plainto_tsquery('english', search_term)` for user input to safely handle multi-word queries without requiring users to know tsquery syntax.
- Apply field weights using `setweight(to_tsvector('english', field), 'A')` for title/name fields and `setweight(to_tsvector('english', field), 'B')` for description fields to implement the relevance hierarchy.
- Order results by `ts_rank(tsvector, tsquery) DESC` to surface the most relevant matches first.
- The `common/src/db/query.rs` module contains shared query builder helpers for filtering, pagination, and sorting — reuse these patterns for composing the search query. Extend rather than duplicate.
- Results must continue to be returned as `PaginatedResults<T>` per the existing response pattern in `common/src/model/paginated.rs`.
- Per CONVENTIONS.md (repo-level): all handlers return `Result<T, AppError>` with `.context()` wrapping. Ensure the refactored search service propagates errors using this pattern.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `modules/search/src/service/mod.rs::SearchService` — existing search service implementation; refactor in place rather than replacing wholesale
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; extend for full-text search query composition
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper for paginated results; continue using for search results
- `common/src/error.rs::AppError` — error enum implementing IntoResponse; use for error handling in refactored search

## Acceptance Criteria
- [ ] SearchService uses PostgreSQL tsvector/tsquery for full-text search instead of LIKE/ILIKE
- [ ] Search results are ranked by relevance using ts_rank with weighted fields
- [ ] Title/name fields have higher relevance weight than description fields
- [ ] Multi-word search queries are handled correctly (all terms must match)
- [ ] The existing search API contract (GET /api/v2/search) is preserved — no breaking changes to request/response shape
- [ ] Pagination continues to work correctly with ranked results

## Test Requirements
- [ ] Integration test: search for a known term returns results ranked by relevance (title match ranks higher than description-only match)
- [ ] Integration test: multi-word search returns only results matching all terms
- [ ] Integration test: empty search term returns appropriate response (empty results or error)
- [ ] Integration test: search with special characters does not cause SQL injection or query errors
- [ ] Integration test: pagination works correctly with ranked results (consistent ordering across pages)

## Verification Commands
- `cargo test -p search` — search module tests pass
- `cargo test -p tests --test search` — search integration tests pass

## Dependencies
- Depends on: Task 1 — Add full-text search indexes migration (indexes must exist for efficient tsvector queries)

<!-- [sdlc-workflow] Description digest: sha256-md:2e63f8ec874219da8b1bd2747ec4995f4af4680a1fb48006c2314936cd818083 -->
