## Repository
trustify-backend

## Target Branch
main

## Description
Improve the relevance of results returned by `GET /api/v2/search` by ordering results
by a relevance score computed from the weighted full-text search vectors introduced in
Task 1, instead of the current (non-relevance) ordering.

This addresses the MVP requirement "Results should be more relevant" from TC-9002.

**Ambiguity flagged (pending clarification on TC-9002):** the Feature does not define
what "relevant" means, does not give examples of irrelevant results users complained
about, and provides no evaluation corpus or expected result ordering. The assumptions
below fill these gaps and must be confirmed by the Feature owner.

**Assumptions pending clarification:**
- ASSUMPTION B1: "more relevant" means results are ranked by textual match quality
  (PostgreSQL `ts_rank_cd` over the Task 1 `tsvector` columns), with exact identifier
  matches (e.g., an exact advisory ID or SBOM name) ranked first.
- ASSUMPTION B2: field weighting — identifier/name fields are weighted higher (weight `A`)
  than descriptive fields such as title/description (weight `B`/`C`). The exact weights
  are a starting point and should be tuned once the Feature owner provides example queries.
- ASSUMPTION B3: relevance ranking becomes the default sort order when a search query is
  present; any existing explicit `sort` parameter supported by the endpoint continues to
  take precedence.
- ASSUMPTION B4: no ML/semantic/vector search is in scope — only lexical ranking.

## Files to Modify
- `modules/search/src/service/mod.rs` — compute a relevance score per result and order by it (descending), with a deterministic tie-breaker
- `tests/api/search.rs` — add relevance-ordering tests

## API Changes
- `GET /api/v2/search` — MODIFY: default result ordering changes to relevance-descending when a query is supplied; response shape is unchanged (no new fields unless the Feature owner requests exposing the score)

## Implementation Notes
- Build on the weighted `tsvector` columns and GIN indexes added in Task 1 (Task 1 builds
  the vectors with `setweight` — identifier/name fields `A`, descriptive fields `B`/`C` — so
  no schema change is needed here; tune weights via a follow-up migration only if the
  Feature owner's example queries require it). Use `ts_rank_cd(<vector>, <tsquery>)` in the
  ORDER BY clause of the query constructed in `modules/search/src/service/mod.rs`.
- Add a stable secondary sort (e.g., entity primary key) so pagination through
  `common/src/db/query.rs` helpers is deterministic across pages — otherwise ties in score
  cause duplicate/missing items between pages.
- When merging results across entity types (SBOM, advisory, package), rank on the same score
  scale so results interleave by relevance rather than being grouped by type.
- If the endpoint already supports an explicit sort parameter via
  `common/src/db/query.rs`, keep honoring it (ASSUMPTION B3); relevance ordering is only the default.
- Keep `PaginatedResults<T>` (`common/src/model/paginated.rs`) as the response type; do not
  change the endpoint registration in `modules/search/src/endpoints/mod.rs`.
- Per CONVENTIONS.md §Module pattern: ranking logic belongs in `modules/search/src/service/`, not in the endpoint handler.
  Applies: task modifies modules/search/src/service/mod.rs matching the convention's `modules/*/src/{model,service,endpoints}` Rust module scope.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping for the ranked query.
  Applies: task modifies modules/search/src/service/mod.rs matching the convention's Rust handler/service (`.rs`) scope.
- Per CONVENTIONS.md §Query helpers: apply sorting/pagination through `common/src/db/query.rs` rather than ad-hoc SQL string building.
  Applies: task modifies modules/search/src/service/mod.rs matching the convention's Rust database-query (`.rs`) scope.
- Per CONVENTIONS.md §Testing: add integration tests to `tests/api/search.rs` against the real PostgreSQL test DB using the `assert_eq!(resp.status(), StatusCode::OK)` pattern (see `tests/api/advisory.rs`).
  Applies: task modifies tests/api/search.rs matching the convention's `tests/api/*.rs` integration-test scope.
- Constraints (docs/constraints.md): Conventional Commits with Jira ID footer and
  `Assisted-by:` trailer (§2.1–2.3); PR targets `main` and is linked on the Jira task
  (§3.2, §3.3); stay within listed files, inspect before modifying, reuse existing helpers
  (§5.1, §5.2, §5.4).

## Reuse Candidates
- `common/src/db/query.rs` — existing sorting and pagination helpers; extend usage for relevance ordering rather than duplicating
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — has its own advisory search; check whether it applies any ordering that should be aligned with unified search ranking

## Acceptance Criteria
- [ ] When a query is supplied, `GET /api/v2/search` returns results ordered by relevance score descending
- [ ] An exact identifier/name match ranks above a partial or description-only match for the same query (ASSUMPTION B1/B2)
- [ ] Ordering is deterministic: identical requests return identical ordering, and paging through results yields no duplicates or gaps
- [ ] An explicit sort parameter (if supported today) still overrides the default relevance ordering
- [ ] Response shape of `GET /api/v2/search` is unchanged
- [ ] Ranking keeps the GIN index in the query plan (no regression of Task 1 performance gains)

## Test Requirements
- [ ] Integration test in `tests/api/search.rs`: seed an advisory whose ID exactly matches the query and another whose description merely mentions it; assert the exact match is first
- [ ] Integration test: seed results across SBOM, advisory, and package with differing match quality; assert they are interleaved by score, not grouped by type
- [ ] Integration test: page through a result set with tied scores using offset/limit; assert no duplicates or missing items across pages
- [ ] Integration test: explicit sort parameter overrides relevance ordering (if the parameter exists)
- [ ] All existing tests in `tests/api/` pass

## Verification Commands
- `cargo test -p tests search` — all search integration tests, including new ranking tests, pass

## Dependencies
- Depends on: Task 1 — Add full-text search indexes and use them in SearchService
