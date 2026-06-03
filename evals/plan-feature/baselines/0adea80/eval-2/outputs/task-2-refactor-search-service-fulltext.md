# Task 2 — Refactor SearchService to use full-text search with relevance ranking

## Repository
trustify-backend

## Target Branch
main

## Description
Refactor the `SearchService` in `modules/search/src/service/mod.rs` to use PostgreSQL
full-text search (`tsvector`/`tsquery`) with `ts_rank` relevance scoring instead of
naive LIKE/ILIKE pattern matching. This directly addresses the TC-9002 requirements
that "search should be faster" and "results should be more relevant."

Results will be sorted by relevance score by default, ensuring the most relevant
matches appear first. The existing search endpoint contract (`GET /api/v2/search`)
remains backward-compatible — the query parameter interface does not change, only the
underlying search mechanism improves.

## Files to Modify
- `modules/search/src/service/mod.rs` — replace LIKE-based search logic with tsquery full-text search using ts_rank for relevance scoring
- `modules/search/src/endpoints/mod.rs` — update the search endpoint handler to pass relevance sort order and expose an optional `sort_by` parameter (defaulting to relevance)

## Implementation Notes
- Inspect `modules/search/src/service/mod.rs` to understand the current search implementation before modifying it.
- Use `plainto_tsquery` or `websearch_to_tsquery` (PostgreSQL 11+) to parse the user's search string into a tsquery. Prefer `websearch_to_tsquery` if the project's minimum PostgreSQL version supports it, as it handles natural language queries more gracefully.
- Use `ts_rank(search_vector, query)` to compute a relevance score for each matching row.
- Search across all three entity tables (sbom, advisory, package) using the `search_vector` columns added in Task 1.
- Return results sorted by `ts_rank` descending by default. Allow an optional `sort_by` query parameter to switch to other sort orders (e.g., `name`, `created_at`).
- Use the existing query builder helpers in `common/src/db/query.rs` for pagination. The `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs` should be used for the response.
- Follow the existing error handling pattern: all handlers return `Result<T, AppError>` with `.context()` wrapping, as defined in `common/src/error.rs`.
- Ensure backward compatibility: if the search query parameter is empty or missing, return all results (existing behavior) rather than an empty set.
- Per docs/constraints.md §2 (Commit Rules): commit messages must follow Conventional Commits, reference TC-9002, and include the Assisted-by trailer.
- Per docs/constraints.md §5 (Code Change Rules): keep changes scoped to the listed files; inspect code before modifying.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; extend rather than duplicate for full-text search needs
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper already used by list endpoints
- `common/src/error.rs` — `AppError` enum implementing IntoResponse; use for error handling consistency
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` already has a `search` method; inspect for patterns to follow

## Acceptance Criteria
- [ ] SearchService uses tsquery/tsvector for full-text search instead of LIKE/ILIKE
- [ ] Results are ranked by relevance using ts_rank by default
- [ ] The search endpoint remains backward-compatible (existing query parameters still work)
- [ ] Empty search queries return all results (existing behavior preserved)
- [ ] An optional sort_by parameter allows switching between relevance and other sort orders
- [ ] Search queries execute using the GIN index (no sequential scans for text matching)

## Test Requirements
- [ ] Integration test: search with a known term returns matching results ranked by relevance
- [ ] Integration test: search with an empty query returns all results (backward compatibility)
- [ ] Integration test: search with a non-matching term returns empty results
- [ ] Integration test: verify that results for a multi-word query rank exact matches higher than partial matches
- [ ] Integration test: sort_by parameter overrides default relevance sorting

## Verification Commands
- `cargo test -p search` — search module unit tests pass
- `cargo test --test search` — search integration tests pass

## Dependencies
- Depends on: Task 1 — Add full-text search migration for SBOM, advisory, and package entities
