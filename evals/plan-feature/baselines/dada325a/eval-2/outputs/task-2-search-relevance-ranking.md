**Summary:** Rank search results by relevance

**Labels:** ai-generated-jira | **Priority:** Normal | **Fix Versions:** RHTPA 1.6.0

## Repository
trustify-backend

## Target Branch
main

## Description
Part of TC-9002 ("Improve search experience"), MVP requirement "Results should be more
relevant".

The Feature does not define relevance or give example queries, so this task is scoped
under planning assumption A3 (see the TC-9002 impact map): results from
`GET /api/v2/search` are ordered by full-text rank, with exact identifier/name matches
(e.g. a CVE ID or exact package name) boosted to the top, and each result exposes its
score. The ranking expression and the boost rule must be validated against example
queries supplied by the Feature owner before this task is closed.

## Files to Modify
- `modules/search/src/service/mod.rs` — compute `ts_rank` over `search_vector`, add exact-match boost, order by score descending with a deterministic tiebreaker
- `modules/search/src/endpoints/mod.rs` — include `score` in each result item; keep existing fields unchanged
- `tests/api/search.rs` — add ranking tests

## API Changes
- `GET /api/v2/search` — MODIFY: results are ordered by relevance (score descending) by default; each result item gains a numeric `score` field. No fields removed.

## Implementation Notes
- Builds on the `search_vector` columns and GIN indexes added in Task 1; rank with `ts_rank(search_vector, plainto_tsquery('english', :q))`.
- Exact-match boost: add a constant to the score when the query equals (case-insensitively) the entity's identifier/name column, so exact hits always outrank partial matches. Confirm which identifier columns exist in `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs`.
- Scores from different entity tables must be comparable when merged into one result list — compute them with the same expression in each sub-query and merge-sort in SQL (`UNION ALL ... ORDER BY score DESC, id`) rather than in Rust, so pagination from Task 1 remains correct.
- Use a deterministic tiebreaker (entity type, then id) so paginated pages do not overlap or skip results.
- Sorting must go through the sorting support in `common/src/db/query.rs` where possible.
- Per CONVENTIONS.md §Query helpers: use the shared sorting helpers in `common/src/db/query.rs`. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's database query scope.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's handler scope.
- Per CONVENTIONS.md §Testing: integration tests against a real PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/search.rs` matching the convention's integration test scope.
- Constraints (docs/constraints.md): §2 commit rules (Conventional Commits, `Implements TC-<task>` footer, `Assisted-by:` trailer); §3 PR rules (task-ID branch, `--base main`, PR link on Jira task); §5 code change rules (scope to listed files, inspect first, reuse helpers, compare with sibling implementations).

## Reuse Candidates
- `common/src/db/query.rs` — shared sorting helpers
- `modules/search/src/service/mod.rs::SearchService` — existing query to extend rather than replace
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — has its own search method; check for matching/ranking logic to reuse or align with

## Acceptance Criteria
- [ ] Search results are ordered by `score` descending, with a deterministic tiebreaker
- [ ] An entity whose identifier/name exactly matches the query appears before entities that only partially match
- [ ] Each result item includes a numeric `score`; all previously returned fields are still present
- [ ] Ranking is consistent across pages: concatenating page 1 and page 2 equals the first 2×limit results of a single larger request
- [ ] Ordering for the example queries supplied by the Feature owner matches the expected top results (**example queries pending — clarification question 2**)

## Test Requirements
- [ ] Integration test: query matching one entity exactly and others partially — exact match is first
- [ ] Integration test: a result with more term occurrences ranks above one with fewer
- [ ] Integration test: `score` present on every result and results are sorted descending
- [ ] Integration test: pagination stability across two pages with tied scores
- [ ] Existing search tests continue to pass (response shape is backward compatible)

## Verification Commands
- `cargo test -p tests search` — all search integration tests pass

## Dependencies
- Depends on: Task 1 — Add full-text indexes and paginated querying to SearchService
