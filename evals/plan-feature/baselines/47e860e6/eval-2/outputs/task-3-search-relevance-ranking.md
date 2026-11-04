# Task 3 — Rank search results by relevance

**Summary:** TC-9002: Rank search results by relevance
**Issue type:** Task | **Labels:** ai-generated-jira | **Priority:** Normal | **Fix Versions:** RHTPA 1.6.0

## Repository
trustify-backend

## Target Branch
main

## Description
This task delivers the "Results should be more relevant" requirement of TC-9002. Users say search returns irrelevant results. This task orders `GET /api/v2/search` results by relevance: exact identifier or name matches come first, then full-text rank (`ts_rank_cd` over the tsvector indexed in Task 1). Relevance becomes the default sort. Callers can still ask for the existing ordering through a `sort` parameter.

**Planning assumption (A2, still to be confirmed):** "relevance" means the ranking above. The Feature gives no example bad queries. The Feature owner should provide 3–5 representative queries with the results they expect, and those become regression fixtures in this task.

## Files to Modify
- `modules/search/src/service/mod.rs` — compute a relevance score per result and order by it by default
- `modules/search/src/endpoints/mod.rs` — accept an optional `sort` value (`relevance` (default) or the existing order)
- `tests/api/search.rs` — relevance ordering tests

## API Changes
- `GET /api/v2/search` — MODIFY: the default ordering becomes relevance. A new optional query parameter `sort=relevance|<existing-order>` is added. The response shape is unchanged.

## Implementation Notes
- Ranking expression: `CASE WHEN lower(<identifier/name>) = lower(:q) THEN 1 ELSE 0 END DESC, ts_rank_cd(<tsvector>, websearch_to_tsquery('english', :q)) DESC`, with a stable tiebreaker (primary key) so pagination is deterministic. Weight the fields with `setweight` (name/identifier = A, description = B) if Task 1 built weighted vectors.
- Results come from several entity types (SBOM, advisory, package). The score must be comparable across them, or results must be merged after per-entity ranking. Choose the approach after inspecting how `SearchService` combines entity results today.
- Keep sorting going through the shared sort helpers in `common/src/db/query.rs` where possible. Extend them, do not bypass them.
- Changing the default order is a behavior change for existing callers (A5). Mention it in the PR description and keep the old order available through `sort`.
- Constraints (docs/constraints.md): §5.1, §5.2, §5.4, §5.6 trace the data flow from query parameter to ordered response, §2.1–2.3, §3.2–3.3.

## Reuse Candidates
- `common/src/db/query.rs` — shared sorting helpers to extend with relevance ordering
- `modules/fundamental/src/advisory/service/advisory.rs` — the existing advisory "search" operation. Check whether it already uses any ordering logic worth reusing.

## Acceptance Criteria
- [ ] With no `sort` parameter, results are ordered with exact identifier or name matches first, then by descending full-text rank
- [ ] Ordering is deterministic across pages (stable tiebreaker)
- [ ] `sort=<existing-order>` returns results in the order used before this change
- [ ] An unknown `sort` value returns 400 Bad Request with an `AppError` message. It is not silently ignored.
- [ ] The representative queries supplied by the Feature owner return the expected top results (once supplied)

## Test Requirements
- [ ] An integration test seeds an exact-name match and several partial matches and asserts the exact match comes first
- [ ] An integration test asserts that a result with more term matches ranks above one with fewer
- [ ] An integration test asserts stable ordering across two consecutive pages
- [ ] An integration test asserts `sort=<invalid>` returns 400
- [ ] An integration test asserts that the legacy sort value preserves the previous ordering

## Documentation Updates
- `README.md` — document the new default relevance ordering and the `sort` parameter on `GET /api/v2/search`, if the README documents API endpoints

## Dependencies
- Depends on: Task 1 — Add full-text search indexes migration
