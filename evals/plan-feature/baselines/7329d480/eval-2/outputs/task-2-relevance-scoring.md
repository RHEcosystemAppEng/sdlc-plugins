# Task 2: Implement relevance scoring in SearchService

additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Normal"}, "fixVersions": [{"name": "RHTPA 1.6.0"}] }

## Repository
trustify-backend

## Target Branch
main

## Description
Add relevance scoring and ranking to search results so that more relevant results appear first. The feature TC-9002 states "results should be more relevant" but provides no definition of relevance, no examples of irrelevant results, and no ranking criteria.

**Assumption**: Relevance will be determined by PostgreSQL's `ts_rank` function applied to full-text search vectors. This provides term-frequency-based ranking as a reasonable baseline. The ranking algorithm may need refinement once the product owner defines what "relevant" means concretely. This assumption is pending clarification.

**Assumption**: The search results will be sorted by relevance score descending by default, with an option to sort by other fields (e.g., date). The current sort order behavior is unspecified in the feature.

## Files to Modify
- `modules/search/src/service/mod.rs` — Extend SearchService to compute ts_rank scores and sort results by relevance
- `modules/search/src/endpoints/mod.rs` — Add optional `sort` query parameter to allow sorting by relevance (default) or date

## Implementation Notes
Modify the `SearchService` in `modules/search/src/service/mod.rs` to:

- Add `ts_rank(tsvector_column, query)` to the SELECT clause for scoring
- Order results by rank score descending by default
- Accept a sort parameter to allow alternative orderings

For the endpoint in `modules/search/src/endpoints/mod.rs`:
- Add an optional `sort` query parameter (values: `relevance`, `date`) defaulting to `relevance`
- Pass the sort preference through to the service layer

Reuse the query builder patterns from `common/src/db/query.rs` for constructing the ranked query. Follow the error handling pattern using `Result<T, AppError>` with `.context()` wrapping as used in existing service methods.

The response should continue to use `PaginatedResults<T>` from `common/src/model/paginated.rs` — consider extending the result items to include a `score` field so consumers can see the relevance score.

Per CONVENTIONS.md §Module pattern: Maintain the model/ + service/ + endpoints/ structure within the search module. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's modules directory scope.

Per CONVENTIONS.md §Error handling: Return Result<T, AppError> with .context() wrapping in service methods. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust syntax scope.

Per CONVENTIONS.md §Response types: Continue using PaginatedResults<T> for the search list endpoint. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust syntax scope.

Per CONVENTIONS.md §Query helpers: Use shared filtering and sorting utilities from common/src/db/query.rs. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's file path scope (common/src/db/query.rs).

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — Reuse existing sorting and pagination utilities rather than implementing custom sort logic
- `common/src/model/paginated.rs::PaginatedResults<T>` — Continue wrapping search results in the standard paginated response type
- `common/src/error.rs::AppError` — Use the existing error enum for error handling

## Dependencies
- Depends on: Task 1 — Add database indexes for search query performance (indexes must exist for ts_rank to perform well)

## Acceptance Criteria
- [ ] Search results are ranked by relevance score (ts_rank) by default
- [ ] A `sort` query parameter allows sorting by `relevance` or `date`
- [ ] Relevance score is included in search result items
- [ ] Default sort order (no parameter) is relevance descending
- [ ] Existing search API contracts are preserved (new parameters are additive/optional)

## Test Requirements
- [ ] Search for a known term returns results ordered by relevance (most relevant first)
- [ ] The `sort=date` parameter overrides default relevance sorting
- [ ] Empty search queries return results in a sensible default order
- [ ] Relevance score field is present in response items

## Verification Commands
- `cargo test -p modules-search` — search module compiles and tests pass
- `cargo test -p tests --test search` — integration tests pass
