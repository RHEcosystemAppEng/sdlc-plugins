# Task 2: Implement search relevance ranking

## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance-based ranking for search results using PostgreSQL full-text search scoring. The TC-9002 feature description states that "results should be more relevant" but does not define relevance criteria.

**Ambiguity noted:** "Results should be more relevant" has no definition of relevance or ranking specification. Assumption pending clarification: relevance is defined as PostgreSQL `ts_rank` scoring with title/name fields weighted higher (weight A) than description/body fields (weight D). Exact weights are subject to tuning.

**Ambiguity noted:** The feature does not specify which entity types are most important in cross-entity search results. Assumption pending clarification: all entity types (SBOM, advisory, package) are equally weighted; ranking is per-entity-type based on text match quality.

## Files to Modify
- `modules/search/src/service/mod.rs` -- Modify `SearchService` to use `ts_rank()` or `ts_rank_cd()` in the SQL query for full-text search. Replace any existing `LIKE`/`ILIKE` pattern matching with `to_tsquery()` + `tsvector` matching against the GIN indexes created in Task 1. Order results by rank score descending.
- `modules/search/src/endpoints/mod.rs` -- Update the search endpoint response to include a `relevance_score` field in each result, so consumers can understand ranking. Add the score to the serialized response struct.

## Implementation Notes
The existing search implementation in `modules/search/src/service/mod.rs` likely uses simple `LIKE` or `ILIKE` queries. Replace with PostgreSQL full-text search:

1. Parse the user query using `plainto_tsquery('english', $query)` for natural language queries or `to_tsquery('english', $query)` for advanced queries.
2. Match against `tsvector` columns using the `@@` operator.
3. Score results using `ts_rank(tsvector, tsquery)` with weight arrays: `'{0.1, 0.2, 0.4, 1.0}'` to prioritize title/name (weight D=1.0 in PostgreSQL convention) over description.
4. Order by rank descending, then by created_at descending as tiebreaker.

Reuse the pagination pattern from `common/src/model/paginated.rs` (`PaginatedResults<T>`) for the response wrapper. Reuse query builder helpers from `common/src/db/query.rs` for pagination and sorting.

Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs` -- Shared query builder helpers for filtering, pagination, and sorting. Reuse for constructing the ranked search query with pagination.
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` response wrapper. Reuse for the search results response.
- `common/src/error.rs` -- `AppError` enum. Use for error handling in the updated search service.

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (`tsvector`/`tsquery`) instead of `LIKE`/`ILIKE`
- [ ] Results are ordered by relevance score (highest first)
- [ ] Title/name matches rank higher than description/body matches
- [ ] Search response includes a `relevance_score` field per result
- [ ] Pagination continues to work correctly with ranked results
- [ ] Existing search tests pass (backward compatibility with query syntax)

## Test Requirements
- [ ] Search for a term that appears in a title returns that result ranked higher than one where the term only appears in description
- [ ] Empty query returns results (fallback to recency or all results)
- [ ] Relevance score is a positive number in the response
- [ ] Pagination with ranking returns consistent results across pages

## Dependencies
- Depends on: Task 1 -- Add database indexes for search performance (GIN indexes must exist for `tsvector` matching)

[sdlc-workflow] Description digest: sha256-md:67bc8d8d804d619579b7f7a0887b2aea44624e41adf0de0b569074b86e8867c9
