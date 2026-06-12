# Task 2 — Implement relevance ranking for search results

## Repository
trustify-backend

## Target Branch
main

## Description
Add relevance-based ranking to the search endpoint so that results are ordered by how well they match the search query, rather than by insertion order or arbitrary database ordering. This addresses the TC-9002 requirement that "results should be more relevant." Use PostgreSQL's `ts_rank` (or `ts_rank_cd`) function to score full-text search matches and order results by descending relevance score.

**Ambiguity note:** The feature description does not define what "relevant" means beyond "users complain about irrelevant results." This task implements text-match relevance ranking using `ts_rank` as a reasonable default. If the product owner requires additional ranking signals (recency, severity, popularity), those should be specified and addressed in a follow-up.

## Files to Modify
- `modules/search/src/service/mod.rs` — Modify `SearchService` query logic to compute `ts_rank` scores and order results by relevance score descending
- `modules/search/src/endpoints/mod.rs` — Update the `GET /api/v2/search` endpoint to accept an optional `sort=relevance` query parameter (default when a search query is provided); preserve existing sort behavior when no search query is active

## API Changes
- `GET /api/v2/search` — MODIFY: add optional `sort` query parameter with values `relevance` (default when `q` is provided) and `date` (existing behavior). Response shape unchanged; result ordering changes to relevance-based when `sort=relevance`.

## Implementation Notes
- Build on the GIN indexes added in Task 1. The `ts_rank` function operates on the same `tsvector` and `tsquery` values used for matching, so no additional indexes are needed.
- Use `ts_rank(to_tsvector('english', column), to_tsquery('english', query))` in the SELECT and ORDER BY clauses. If searching across multiple entity types with different columns, compute a composite score or rank per entity type.
- Reference the existing query builder in `common/src/db/query.rs` — it provides sorting infrastructure. Integrate the relevance sort option into this framework rather than implementing ad-hoc sorting in the search module.
- Ensure backward compatibility: when no search query is provided (listing mode), default sort behavior should remain unchanged. Relevance sorting should only activate when a text search query (`q` parameter) is present.
- The response wrapper `PaginatedResults<T>` in `common/src/model/paginated.rs` does not need modification unless the product owner wants to expose the relevance score in the response. For now, use it for ordering only.
- Per docs/constraints.md Section 2 (Commit Rules): use Conventional Commits format and reference TC-9002 in the commit footer.
- Per docs/constraints.md Section 5 (Code Change Rules): inspect existing code before modifying, follow patterns found in the codebase.

## Reuse Candidates
- `common/src/db/query.rs` — shared sorting infrastructure; extend to support a `relevance` sort option rather than implementing custom sort logic
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper; use as-is for response formatting
- `modules/search/src/service/mod.rs` — existing `SearchService` query logic to extend with ranking

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (best match first) when a text search query is provided
- [ ] When no search query is provided, existing default sort order is preserved
- [ ] The `sort` query parameter is accepted and documented in the endpoint
- [ ] Response shape remains backward compatible (no breaking changes to existing consumers)

## Test Requirements
- [ ] Integration test verifying that a search query returns results in relevance order (e.g., exact match ranks higher than partial match)
- [ ] Integration test verifying that the `sort=relevance` parameter works correctly
- [ ] Integration test verifying that default sort behavior is unchanged when no search query is provided
- [ ] Existing search tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test -p tests --test search` — all search tests pass including new relevance tests

## Dependencies
- Depends on: Task 1 — Add full-text search indexes for searchable entities
