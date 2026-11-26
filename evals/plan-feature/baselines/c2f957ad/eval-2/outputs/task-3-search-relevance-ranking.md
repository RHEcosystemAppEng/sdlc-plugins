# Task 3 — Rank search results by relevance

**Jira:** Task, parent EPIC-2 ("TC-9002: Search relevance"), labels `ai-generated-jira`, priority `Normal`, fixVersions `RHTPA 1.6.0`

## Repository
trustify-backend

## Target Branch
main

## Description
TC-9002 reports that search "doesn't return useful results". This task changes `SearchService` so results are ordered by a relevance score instead of the current default order, with exact identifier matches ranked first.

**Assumptions (pending clarification on TC-9002, open question 2). The product owner must confirm these before implementation:**
- "Relevance" means: (1) exact matches on an entity's identifier or name (for example an advisory ID like a CVE, a package name, an SBOM name) rank first; (2) other results are ordered by full-text match score (`ts_rank` or the trigram similarity matching Task 2's indexes); (3) ties are broken by the existing sort order so pagination stays stable.
- The default sort for `GET /api/v2/search` becomes relevance. An explicit `sort` parameter (if `common/src/db/query.rs` already supports one for this endpoint) still overrides it.

## Files to Modify
- `modules/search/src/service/mod.rs` — compute a relevance score per result and order by it, with exact identifier matches boosted
- `modules/search/src/endpoints/mod.rs` — make relevance the default sort while keeping any explicit sort parameter working
- `tests/api/search.rs` — add relevance-ordering tests

## API Changes
- `GET /api/v2/search` — MODIFY: the default ordering of results becomes relevance-ranked. Path, parameters and `PaginatedResults<T>` response shape are unchanged

## Implementation Notes
- Build the score from the same expressions indexed in Task 2 so ranking does not undo the performance gains. Check with `EXPLAIN ANALYZE` and compare against the Task 1 baseline.
- Use a deterministic tie-breaker (for example the entity id) so offset/limit pagination over `PaginatedResults<T>` (`common/src/model/paginated.rs`) never repeats or skips results.
- Do not add a score field to the response. That would change the response shape, which "don't break existing functionality" rules out unless the owner approves.
- **Shared artifact:** ranking must work the same for data from every ingestion path (`modules/ingestor/src/graph/sbom/mod.rs`, `modules/ingestor/src/graph/advisory/mod.rs`). Tests must seed through ingestion, not fixture inserts.
- Per CONVENTIONS.md §Query helpers: shared filtering, pagination and sorting go through `common/src/db/query.rs`. Add the relevance ordering by extending or composing those sort helpers rather than writing a separate ORDER BY path. Applies: task modifies modules/search/src/service/mod.rs matching the convention's Rust query construction (`.rs`) scope.
- Per CONVENTIONS.md §Error handling: handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies modules/search/src/endpoints/mod.rs matching the convention's Rust handler (`.rs`) scope. Example: `modules/fundamental/src/advisory/endpoints/list.rs`.
- Per CONVENTIONS.md §Testing: integration tests go in `tests/api/` against the real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies tests/api/search.rs matching the convention's integration test (`tests/api/*.rs`) scope.
- Constraints (docs/constraints.md): §1.4 and §5.1 scope limits. §5.2 inspect before modifying. §5.4 no duplication. §5.8 parity with sibling search (`AdvisoryService`). §2.1–2.3 commit rules. §3.1–3.3 PR rules. §5.9–5.12 test conventions (parameterize the ordering cases if sibling tests do).

## Reuse Candidates
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — already implements advisory search. Reuse any existing scoring or match logic instead of re-implementing it, and keep the two consistent
- `common/src/db/query.rs` — shared sorting helpers to extend with relevance ordering
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper. Ordering must stay stable across pages

## Acceptance Criteria
- [ ] A search for an exact advisory identifier returns that advisory as the first result
- [ ] A search for an exact package name returns that package ahead of packages that only partly match
- [ ] Non-exact results are ordered by descending match score
- [ ] Ordering is deterministic: the same query returns the same order, and paging through all results yields no duplicates or gaps
- [ ] An explicit sort parameter, if the endpoint already supports one, still overrides relevance ordering
- [ ] Response path, parameters and `PaginatedResults<T>` shape are unchanged
- [ ] Search latency with ranking is no worse than the post-Task 2 measurement (numbers in the PR description)

## Test Requirements
- [ ] Test: exact identifier match ranks first for advisory, package and SBOM queries (parameterized if the sibling tests use that pattern)
- [ ] Test: a partial match ranks below an exact match
- [ ] Test: paginating through results with offset/limit yields each matching entity exactly once
- [ ] Test: data seeded through the SBOM and advisory ingestion paths is ranked correctly
- [ ] Existing `tests/api/search.rs` tests pass. Update only assertions that relied on the old implicit order, and explain each change in the PR

## Verification Commands
- `cargo test --test api search` — all search tests pass

## Dependencies
- Depends on: Task 2 — Add database indexes for search queries
