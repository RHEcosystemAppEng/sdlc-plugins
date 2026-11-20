## Repository
trustify-backend

## Target Branch
main

## Description
Improve the relevance of `GET /api/v2/search` results, addressing the TC-9002 MVP requirement "Results should be more relevant". The Feature gives no examples of irrelevant results and no definition of "relevant", so this task applies a documented, deterministic ranking model that the Product Owner must confirm before acceptance.

**Assumed relevance model (needs Product Owner confirmation on TC-9002):**
1. Exact identifier match (for example, a CVE/advisory ID, SBOM name, or package name/PURL equal to the query) ranks first
2. Prefix matches rank next
3. Other full-text matches are ordered by text-search rank (PostgreSQL `ts_rank`) and then by recency
4. Ties are broken deterministically by entity ID, so ordering is stable across pages

**Open question:** Do users want results grouped by entity type (SBOMs, advisories, packages) or one interleaved ranked list? This task assumes one interleaved ranked list that keeps the existing response shape.

## Files to Modify
- `modules/search/src/service/mod.rs` — compute a relevance score per result using the ranking model above and order results by score, with a deterministic tie-breaker
- `modules/search/src/endpoints/mod.rs` — expose the ordering (an optional `score` field in each result item) and make relevance the default sort
- `tests/api/search.rs` — add ranking tests that seed known data and assert the expected order

## API Changes
- `GET /api/v2/search` — MODIFY: results are ordered by relevance by default. Each result item gains an optional `score` field (additive, non-breaking). The request shape is unchanged.

## Implementation Notes
- Read the current query construction in `SearchService` (`modules/search/src/service/mod.rs`) to find how full-text matching is done today (for example `LIKE`/`ILIKE` or `tsvector`). Build the ranking on the existing mechanism instead of replacing it.
- If the Task 2 migration (`migration/src/m0002_search_indexes/mod.rs`) adds `tsvector`/GIN indexes, use them for `ts_rank`. That is why this task depends on Task 2. Do not add a second index migration here.
- Ordering must work with the pagination from Task 2: apply the sort before `offset`/`limit` and include the deterministic tie-breaker so pages do not overlap or skip results.
- Sorting must go through the shared sorting helpers in `common/src/db/query.rs` where they support expression-based ordering. If they cannot express a computed score, extend the shared helper rather than writing search-only sorting code.
- Per CONVENTIONS.md §Query Helpers: filtering, pagination, and sorting go through `common/src/db/query.rs`. See `modules/fundamental/src/sbom/service/sbom.rs` for usage.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's service query (`service/*.rs`) scope.
- Per CONVENTIONS.md §Error Handling: handlers return `Result<T, AppError>` with `.context()` wrapping. See `common/src/error.rs`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust handler (`.rs`) scope.
- Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)`. See `tests/api/advisory.rs`.
  Applies: task modifies `tests/api/search.rs` matching the convention's integration test (`tests/api/*.rs`) scope.
- Constraints (docs/constraints.md): §2.1–2.3 (commit rules); §3.1–3.3 (PR rules, `--base main`); §5.1–5.4 (scope, inspect first, follow patterns, no duplication).

## Reuse Candidates
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService::search` may already contain advisory matching logic. Reuse or align with it so advisory relevance stays consistent between `/api/v2/advisory` and `/api/v2/search`.
- `common/src/db/query.rs` — shared sorting helpers.

## Acceptance Criteria
- [ ] For a query equal to an existing advisory ID, that advisory is the first result
- [ ] Exact matches rank above prefix matches, and prefix matches rank above other full-text matches
- [ ] Ordering is deterministic: the same query against the same data always returns the same order, and paginated pages neither overlap nor skip results
- [ ] Result items include an optional `score` field; all existing fields keep their current names and types
- [ ] The relevance model in the Description is confirmed by the Product Owner on TC-9002 (or revised and the implementation updated) before the task is closed

## Test Requirements
- [ ] Ranking test: seed an exact match, a prefix match, and a substring/full-text match for the same term, and assert they come back in that order
- [ ] Stability test: run the same query twice and across two pages, and assert identical ordering with no overlap
- [ ] Backward-compatibility test: existing assertions in `tests/api/search.rs` on response fields still pass

## Verification Commands
- `cargo test --test api search` — all search tests, including the new ranking tests, pass

## Documentation Updates
- `README.md` — if the README documents the search API, describe the default relevance ordering and the `score` field

## Dependencies
- Depends on: Task 2 — Optimize search query performance (indexes and pagination)
