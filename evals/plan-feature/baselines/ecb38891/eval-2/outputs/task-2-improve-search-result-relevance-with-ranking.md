## Repository
trustify-backend

## Target Branch
main

## Description
Improve search result relevance by implementing PostgreSQL `ts_rank`-based scoring and ordering search results by relevance score. Users have reported that search returns irrelevant results (TC-9002). This task addresses the relevance aspect by adding rank scoring to full-text search queries so that results most closely matching the search terms appear first.

**Note:** The feature does not define specific relevance criteria (e.g., field weighting, recency boost, exact-match priority). This task implements standard `ts_rank` scoring as a baseline. Ranking weights may need tuning once the product owner defines what constitutes a "relevant" result.

## Files to Modify
- `modules/search/src/service/mod.rs` — Add `ts_rank()` scoring to search queries; order results by rank score descending; optionally expose a `min_rank` threshold to filter low-relevance results
- `modules/search/src/endpoints/mod.rs` — Accept optional `sort_by=relevance` query parameter (default to relevance-sorted results when a search query is present)
- `tests/api/search.rs` — Add integration tests verifying that results are ordered by relevance (exact matches rank higher than partial matches)

## API Changes
- `GET /api/v2/search` — MODIFY: add optional `sort_by` query parameter (values: `relevance`, `name`, `date`; default: `relevance` when a search query is provided). Response items include a `rank` field (float) indicating the relevance score.

## Implementation Notes
- Per CONVENTIONS.md (Key Conventions) - Error handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping on database operations. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust error handling scope.
- Per CONVENTIONS.md (Key Conventions) - Response types: ensure the search response type extends (or wraps) the existing response to include the `rank` field while remaining compatible with `PaginatedResults<T>`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint response scope.
- Per CONVENTIONS.md (Key Conventions) - Query helpers: use the shared sorting utilities from `common/src/db/query.rs` to implement sort_by parameter handling. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's query builder scope.
- Per CONVENTIONS.md (Key Conventions) - Testing: integration tests go in `tests/api/` and hit a real PostgreSQL test database. Applies: task modifies `tests/api/search.rs` matching the convention's test file scope.
- Use `ts_rank(tsvector_column, to_tsquery('search terms'))` in the SELECT clause and ORDER BY the rank descending.
- Consider `ts_rank_cd` (cover density ranking) as an alternative if results need to account for term proximity.
- The `sort_by` parameter should integrate with the existing query builder sorting pattern in `common/src/db/query.rs` — add relevance as a sort option alongside existing sort fields.
- See `modules/fundamental/src/advisory/service/advisory.rs` for an example of a service method that implements search with result ordering.

## Reuse Candidates
- `common/src/db/query.rs::sorting helpers` — shared sorting utilities that the `sort_by` parameter should integrate with
- `common/src/model/paginated.rs::PaginatedResults<T>` — paginated response wrapper to extend with rank field
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService search` — example of a service implementing search functionality that can serve as a pattern reference

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (ts_rank) by default when a search query is provided
- [ ] The response includes a `rank` field (float) for each result indicating the relevance score
- [ ] Optional `sort_by` query parameter allows switching between relevance, name, and date ordering
- [ ] Exact matches rank higher than partial matches in search results
- [ ] Search results without a query term (empty search) fall back to default ordering (not relevance-based)
- [ ] Existing search functionality is not broken (all existing tests continue to pass)

## Test Requirements
- [ ] Integration test: verify that an exact-match search term returns the matching document with a higher rank than partial matches
- [ ] Integration test: verify that `sort_by=relevance` orders results by descending rank score
- [ ] Integration test: verify that `sort_by=name` orders results alphabetically regardless of relevance
- [ ] Integration test: verify that empty search queries return results in default order (not relevance-sorted)
- [ ] Integration test: verify the `rank` field is present and is a valid float in the response body

## Verification Commands
- `cargo test -p tests --test search` — all search integration tests pass

## Dependencies
- Depends on: Task 1 — Add search indexes and optimize query performance (requires GIN indexes and tsvector setup for ts_rank to function)
