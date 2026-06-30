# Task 2: Implement Search Relevance Ranking in SearchService

**Parent Feature**: TC-9002 — Improve search experience

## Repository
trustify-backend

## Target Branch
main

## Description
Refactor the `SearchService` to use PostgreSQL full-text search ranking (`ts_rank`) instead of simple pattern matching, so that search results are ordered by relevance. Currently, search results are returned without meaningful ordering, causing users to see irrelevant results first.

**Ambiguity flag (assumption pending clarification):** The feature description states "results should be more relevant" but provides no definition of relevance or ranking criteria. This task assumes relevance is defined as PostgreSQL's `ts_rank` scoring based on term frequency and document length normalization. The ranking weights are assumed to be: title fields weighted highest (A), description fields medium (B), and other indexed fields lower (C/D). These weights should be reviewed with the product owner to ensure they match user expectations.

## Files to Modify
- `modules/search/src/service/mod.rs` — Refactor SearchService to use tsvector-based full-text search with ts_rank scoring instead of LIKE/ILIKE queries
- `common/src/db/query.rs` — Add full-text search query builder helpers (plainto_tsquery, ts_rank) to shared query utilities

## Implementation Notes
- The current `SearchService` in `modules/search/src/service/mod.rs` likely uses LIKE or ILIKE for text matching; replace with `plainto_tsquery` or `websearch_to_tsquery` against the tsvector columns added in Task 1
- Use `ts_rank(search_vector, query)` to score results and `ORDER BY` rank descending
- Add a shared helper in `common/src/db/query.rs` alongside existing query builder helpers for filtering, pagination, and sorting — this ensures other modules can also leverage full-text search
- Use `websearch_to_tsquery('english', ...)` to support natural language queries including quoted phrases and boolean operators
- Apply rank normalization (e.g., `ts_rank(search_vector, query, 32)` for length normalization) so shorter, more focused documents rank higher
- Results should still be wrapped in `PaginatedResults<T>` from `common/src/model/paginated.rs`

Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`.
Applies: task modifies `common/src/db/query.rs` matching the convention's query helper scope.

Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `common/src/db/query.rs` — Existing query builder helpers for filtering, pagination, and sorting; extend with full-text search helpers
- `common/src/model/paginated.rs::PaginatedResults<T>` — Use for wrapping ranked search results with pagination metadata

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (tsquery/tsvector) instead of LIKE/ILIKE
- [ ] Results are ranked by relevance using ts_rank scoring
- [ ] Title matches rank higher than description-only matches
- [ ] Empty or whitespace-only queries return an appropriate error or empty result set
- [ ] Existing pagination behavior is preserved (results are paginated via PaginatedResults<T>)
- [ ] Search query syntax errors (malformed queries) return a meaningful error, not a 500

## Test Requirements
- [ ] Search for a known SBOM name returns that SBOM as the top result
- [ ] Search with multiple terms returns results containing all terms ranked above partial matches
- [ ] Pagination of ranked results works correctly (page 2 contains lower-ranked results)
- [ ] Empty query string returns a 400 Bad Request or empty result set

## Dependencies
- Depends on: Task 1 — Add Full-Text Search Indexes via Database Migration (tsvector columns must exist)

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Normal"}, "fixVersions": [{"name": "RHTPA 1.6.0"}]}

[sdlc-workflow] Description digest: sha256-md:9a5a6580163b63c621372ca450084e8faefccae124ded834e310c1835f4405ab
