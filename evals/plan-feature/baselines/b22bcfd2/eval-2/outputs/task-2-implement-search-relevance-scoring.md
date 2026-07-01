## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance scoring for search results so that results are ordered by match quality rather than insertion order. The feature requirement states results should be "more relevant" but provides no definition of relevance or scoring criteria. **Assumption pending clarification**: relevance means ordering results by PostgreSQL `ts_rank` score computed from full-text search matching, with optional weighting by entity recency.

## Files to Modify
- `modules/search/src/service/mod.rs` — Add `ts_rank` scoring to search queries, ordering results by descending rank score. Extend the search result model to include a relevance score field.
- `modules/search/src/endpoints/mod.rs` — Update the `GET /api/v2/search` handler to pass through a `sort_by=relevance` query parameter (default behavior) and support `sort_by=date` as an alternative
- `common/src/model/paginated.rs` — Extend `PaginatedResults<T>` or create a search-specific response wrapper that includes a `score` field alongside each result item

## Implementation Notes
- In `modules/search/src/service/mod.rs`, add `ts_rank(to_tsvector('english', column), tsquery)` as a computed column in the search query's SELECT clause. Order results by this rank descending.
- The `ts_rank` function relies on the GIN index created in Task 1. This task builds on that infrastructure.
- Follow the existing endpoint pattern in `modules/search/src/endpoints/mod.rs` where the handler extracts query parameters, calls the service, and returns `PaginatedResults<T>`.
- The `PaginatedResults<T>` wrapper in `common/src/model/paginated.rs` may need a generic score field or a search-specific variant. Follow the existing pattern of how `PaginatedResults` wraps items.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per the codebase error handling convention.
- Per CONVENTIONS.md: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `common/src/model/paginated.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md: each domain module follows `model/ + service/ + endpoints/` structure.
  Applies: task modifies `modules/search/src/service/mod.rs` and `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` module structure scope.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults` — Existing paginated response wrapper to extend or specialize for scored search results
- `common/src/db/query.rs` — Query builder helpers; the full-text search helper from Task 1 should be reused here

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (ts_rank) by default
- [ ] Each search result includes a numeric relevance score in the response
- [ ] `sort_by=relevance` and `sort_by=date` query parameters are supported
- [ ] Existing search API consumers are not broken — relevance sorting is the new default but response structure remains backward-compatible
- [ ] **Assumption pending clarification**: relevance scoring uses ts_rank; actual scoring model may need adjustment based on stakeholder feedback

## Test Requirements
- [ ] Search for a term present in multiple entities returns results ordered by match quality (exact match scores higher than partial)
- [ ] `sort_by=date` returns results in chronological order
- [ ] `sort_by=relevance` (or omitted) returns results in rank order
- [ ] Response includes `score` field for each result item

## Dependencies
- Depends on: Task 1 — Optimize search query performance (requires GIN index and full-text search infrastructure)

## Additional Fields
- priority: Normal
- fixVersions: RHTPA 1.6.0

## Description Digest
[sdlc-workflow] Description digest: sha256-md:<computed-at-creation-time>
(Actual digest computed by re-fetching description from Jira API and running `scripts/sha256-digest.py`)
