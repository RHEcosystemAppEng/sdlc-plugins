## Repository
trustify-backend

## Target Branch
main

## Description
Order `GET /api/v2/search` results by relevance instead of insertion/ID order, so that the most relevant SBOMs, advisories, and packages appear first. This addresses the TC-9002 MVP requirement "Results should be more relevant".

**Assumptions pending clarification (TC-9002):**
- ASSUMPTION: "Relevant" means ranked by text-match quality. The Feature provides no definition of relevance, no examples of irrelevant results, and no ranking criteria. This task adopts: exact identifier match (e.g., CVE ID, package name) ranks highest, followed by PostgreSQL full-text rank (`ts_rank`) on the searched text columns.
- ASSUMPTION: Relevance ordering becomes the default sort when a query term is provided; an explicit `sort` parameter (if already supported via `common/src/db/query.rs`) continues to override it.
- ASSUMPTION: No boosting by recency, severity, or entity type is required. If the Feature owner wants such boosts, they must be specified before implementation.
- OPEN QUESTION: Concrete examples of queries that currently return "irrelevant results" are needed to build regression fixtures; until then the tests below use synthetic fixtures.

## Files to Modify
- `modules/search/src/service/mod.rs` — compute a relevance score per result and order by it
- `modules/search/src/endpoints/mod.rs` — default ordering to relevance when `q` is provided and no explicit sort is requested
- `tests/api/search.rs` — add relevance-ordering tests

## API Changes
- `GET /api/v2/search` — MODIFY: default ordering becomes relevance-descending when `q` is present. Response body shape unchanged.

## Implementation Notes
- Build ranking into the SQL issued by `SearchService` (`modules/search/src/service/mod.rs`) so ordering and pagination happen together in the database; do not sort in memory after fetching (that would undo Task 2's pagination work).
- Use the index expressions introduced in Task 1 (`migration/src/m0002_search_indexes/mod.rs`) so the ranking expression can use the GIN index.
- Exact-match boosting: advisory identifiers live on the advisory entity (`entity/src/advisory.rs`), package names on `entity/src/package.rs`, SBOM names on `entity/src/sbom.rs`.
- Check `modules/fundamental/src/advisory/service/advisory.rs` (`AdvisoryService` search) for any existing matching/ranking logic and reuse it rather than writing a parallel implementation.
- Sort handling should go through the shared sorting helpers in `common/src/db/query.rs`.
- Per CONVENTIONS.md §Query helpers: use the shared filtering, pagination, and sorting helpers from `common/src/db/query.rs`.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust database query scope.
- Per CONVENTIONS.md §Error handling: handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust handler scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` against the PostgreSQL test database, using `assert_eq!(resp.status(), StatusCode::OK)`.
  Applies: task modifies `tests/api/search.rs` matching the convention's `tests/api/` scope.

Constraints (docs/constraints.md):
- §2 Commit rules: Conventional Commits format, Jira task ID in footer, `Assisted-by:` trailer.
- §3 PR rules: `gh pr create --base main`; post the PR link on the Jira task.
- §5 Code change rules: scope changes to the listed files; inspect before modifying; reuse existing search/ranking logic in `AdvisoryService` if present.

## Reuse Candidates
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — has existing `search` capability; candidate for shared matching logic
- `common/src/db/query.rs` — shared sorting helpers for default/override ordering
- `migration/src/m0002_search_indexes/mod.rs` (from Task 1) — index expressions the ranking expression must match

## Acceptance Criteria
- [ ] When `q` is provided and no `sort` is requested, results are ordered by relevance score descending
- [ ] An exact identifier match (e.g., searching a CVE ID that exists) is returned as the first result
- [ ] An explicit `sort` parameter overrides relevance ordering
- [ ] Ranking and pagination are applied in a single SQL query (no in-memory re-sort)
- [ ] Response body shape is unchanged; existing search tests still pass

## Test Requirements
- [ ] Integration test: seed entities where one has an exact identifier match and others partial matches; assert the exact match is first
- [ ] Integration test: seed entities with differing match strength; assert result order is by descending relevance
- [ ] Integration test: explicit `sort` parameter overrides relevance ordering
- [ ] Integration test: relevance ordering is stable across pages (no duplicates or gaps between page 1 and page 2)
- [ ] Existing tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test --test api search` — search integration tests pass

## Dependencies
- Depends on: Task 1 — Add full-text search indexes (migration)
- Depends on: Task 2 — Optimize search queries and add response caching
