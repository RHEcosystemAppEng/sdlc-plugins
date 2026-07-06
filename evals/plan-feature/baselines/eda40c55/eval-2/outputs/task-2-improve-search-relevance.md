## Repository
trustify-backend

## Target Branch
main

## Description
Improve the relevance of search results returned by GET /api/v2/search so that users see the most useful results first. The feature description states that "users complain about irrelevant results" but does not define relevance criteria. This task implements a scoring/ranking mechanism in the SearchService to order results by relevance rather than returning them in arbitrary or insertion order.

**Assumption (pending clarification):** Relevance scoring will use PostgreSQL's built-in `ts_rank` (or `ts_rank_cd`) full-text search ranking functions as a starting point. This ranks results by how closely they match the search query terms, considering factors like term frequency and proximity. If stakeholders require a different ranking strategy (e.g., recency-weighted, entity-type-boosted, field-specific weighting), the scoring algorithm will need adjustment. This assumption should be validated with stakeholders before implementation.

**Assumption (pending clarification):** The search scope covers all entity types (SBOMs, advisories, packages) with a unified relevance score. If different entity types require different ranking strategies or weighting, the implementation will need to be extended.

## Files to Modify
- `modules/search/src/service/mod.rs` — Implement relevance scoring in the SearchService: add `ts_rank` or equivalent scoring to search queries, order results by score descending, and optionally expose the relevance score in the response
- `modules/search/src/endpoints/mod.rs` — Update the search endpoint to accept an optional `sort` parameter that allows sorting by relevance (default) or other fields

## Implementation Notes
- Use PostgreSQL's `ts_rank(tsvector_column, to_tsquery(search_term))` to compute relevance scores. This requires that the searchable columns have been indexed with tsvector (see Task 1 for index creation).
- Add the relevance score as an `ORDER BY` clause in the search query. The default sort order for search should be by relevance score descending.
- Consider adding the relevance score to the response payload so the frontend can display it if desired (e.g., as a percentage or normalized score). This is optional and can be deferred.
- Review how `common/src/db/query.rs` handles sorting — extend the shared sorting helpers if needed to support score-based ordering, or implement score ordering directly in the search service if the shared helpers do not accommodate computed columns.
- Ensure that the existing pagination behavior (via `PaginatedResults<T>` from `common/src/model/paginated.rs`) is preserved when relevance sorting is applied.

Per CONVENTIONS.md §Error handling: ensure all new or modified handler functions return `Result<T, AppError>` with `.context()` wrapping for meaningful error messages.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

Per CONVENTIONS.md §Response types: list endpoints must return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

Per CONVENTIONS.md §Module pattern: follow the model/ + service/ + endpoints/ structure for any new types or functions added to the search module.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust module file scope.

Per CONVENTIONS.md §Testing: add integration tests in `tests/api/` using a real PostgreSQL test database with the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `common/src/db/query.rs::query` — Shared query builder helpers. Check if sorting helpers can accommodate computed score columns for relevance ordering.
- `common/src/model/paginated.rs::PaginatedResults` — Response wrapper. Ensure relevance-sorted results still conform to this type.

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (most relevant first) by default
- [ ] A relevance scoring mechanism (e.g., ts_rank) is integrated into the SearchService query
- [ ] Existing search response shape (PaginatedResults) is preserved — no breaking changes
- [ ] Users searching for a specific term see results containing that term ranked higher than tangentially related results

## Test Requirements
- [ ] Integration test verifying that search results are ordered by relevance (a document containing the exact search term in its title ranks higher than one with the term only in a nested field)
- [ ] Integration test verifying that search with an empty or very broad query still returns valid paginated results
- [ ] Regression test verifying existing search queries continue to return correct results after relevance ordering is added

## Verification Commands
- `cargo test -p tests --test search` — verify all search integration tests pass

## Dependencies
- Depends on: Task 1 — Optimize search query performance (database indexes for full-text search must be in place before relevance scoring can use ts_rank effectively)
