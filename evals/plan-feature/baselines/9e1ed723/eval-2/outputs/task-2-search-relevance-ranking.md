## Repository
trustify-backend

## Target Branch
main

## Description
Improve the relevance of results returned by `GET /api/v2/search` (TC-9002 requirement "Results should be more relevant", MVP).

The Feature says users "complain about irrelevant results" but gives no examples of bad results, no definition of "relevant", and no ranking criteria. This task orders search results by a deterministic relevance score instead of an arbitrary or insertion order, and exposes the ordering in a backward-compatible way.

**Assumptions (pending clarification on TC-9002):**
- ASSUMPTION B1: "Relevance" means ranking text matches by match quality. Exact identifier or name matches come first, then prefix matches, then full-text matches ranked by PostgreSQL text-search rank. The product owner must confirm the criteria, ideally with 3–5 example queries and their expected top results.
- ASSUMPTION B2: Ranking is computed at query time inside `SearchService`. No precomputed search column or index is added in this task. If a precomputed column turns out to be needed, the ingestion paths (`modules/ingestor/src/graph/sbom/mod.rs`, `modules/ingestor/src/graph/advisory/mod.rs`) would also have to write it. That is a scope expansion, recorded as an open item in the impact map, and is not part of this task.
- ASSUMPTION B3: Relevance becomes the default sort order. Existing explicit sort parameters, if any, still take precedence so existing behavior does not break.

## Files to Modify
- `modules/search/src/service/mod.rs` — add relevance scoring and ordering to the `SearchService` full-text query
- `modules/search/src/endpoints/mod.rs` — make relevance the default ordering for `GET /api/v2/search` and keep explicit sort parameters working
- `tests/api/search.rs` — add ranking-order tests

## API Changes
- `GET /api/v2/search` — MODIFY: results are ordered by relevance by default. The response shape stays `PaginatedResults<T>`, and adding an optional score field to items is subject to ASSUMPTION B1 confirmation. No existing parameter is removed or renamed.

## Implementation Notes
- Implement the ranking in `SearchService` (`modules/search/src/service/mod.rs`). Build the ordering expression with the shared sorting helpers in `common/src/db/query.rs`, so ranking composes with existing pagination and sorting instead of adding a parallel code path.
- Ranking tiers (ASSUMPTION B1): (1) exact match on name or identifier, (2) prefix match, (3) full-text rank, for example PostgreSQL `ts_rank`, through SeaORM custom expressions. Use a stable tie-breaker such as entity id so pagination stays deterministic.
- Keep the `PaginatedResults<T>` wrapper (`common/src/model/paginated.rs`) unchanged. If a score field is added to result items, it must be additive and optional.
- Check `AdvisoryService::search` in `modules/fundamental/src/advisory/service/advisory.rs` for existing matching or ranking logic before writing new logic, so the domain behavior is not duplicated.
- Per CONVENTIONS.md §Error handling: every handler returns `Result<T, AppError>` (`common/src/error.rs`) and wraps fallible calls with `.context()`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust handler (`.rs`) scope.
- Per CONVENTIONS.md §Query helpers: use the shared filtering, pagination, and sorting helpers in `common/src/db/query.rs` for the relevance ordering.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust database-query (`.rs`) scope.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's list endpoint (`.rs`) scope.
- Per CONVENTIONS.md §Testing: integration tests go in `tests/api/`, run against the real PostgreSQL test database, and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's integration test (`tests/api/*.rs`) scope.
- Constraints (docs/constraints.md): changes stay within the files listed above (§5.1). Inspect code before modifying it (§5.2). Reuse rather than duplicate (§5.4). Commits use Conventional Commits with a Jira footer and an `Assisted-by:` trailer (§2.1–2.3). The PR targets `main` via `--base main` and its link is posted to the Jira task (§3.2, §3.3).

## Reuse Candidates
- `common/src/db/query.rs` — shared sorting helpers. Express the relevance ordering through them.
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — has an existing `search` operation that may already contain matching logic to reuse or align with.
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper that must be preserved.

## Acceptance Criteria
- [ ] For a query matching an entity's name or identifier exactly, that entity is ranked above entities that only partially match
- [ ] Prefix matches rank above matches that only appear elsewhere in the full text
- [ ] Ordering is deterministic across repeated identical requests and across pages (stable tie-breaker)
- [ ] Relevance is the default ordering, and existing explicit sort parameters (if present) still override it
- [ ] The response shape stays backward compatible (`PaginatedResults<T>`; any score field is additive)
- [ ] Ranking criteria are confirmed with the product owner, or ASSUMPTION B1 is explicitly accepted on TC-9002, before merge

## Test Requirements
- [ ] Integration test in `tests/api/search.rs`: seed entities with exact, prefix, and partial matches for one term, and assert that the result order follows the ranking tiers
- [ ] Integration test: the same query run twice, and across two pages, gives a consistent order with no duplicates or omissions
- [ ] Integration test: an explicit sort parameter (if supported) overrides relevance ordering
- [ ] Existing search integration tests keep passing

## Verification Commands
- `cargo test --test search` (run from `tests/`) — all search integration tests pass

## Dependencies
- Depends on: Task 1 — Search performance baseline and optimization (shares `modules/search/src/service/mod.rs`; ranking cost must be measured against the Task 1 baseline)
