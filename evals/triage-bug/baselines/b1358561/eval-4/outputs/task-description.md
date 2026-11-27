# Step 5 — Generated Task (ACME-510)

## Task creation parameters (not executed in eval)

- Project: `ACME`
- Issue type: Task
- Summary: `Fix missing pagination headers on /api/v2/advisories when date-range filters are applied`
- Labels: `["ai-generated-jira"]`
- Link (Step 5b): link type `Blocks`. Inward = created Task (blocker), outward = ACME-510 (blocked). In other words, the Task blocks ACME-510.
- Digest (Step 5c): re-fetch the created task's description, write it to `/tmp/desc-<task-key>.txt`, run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`, then post the standalone comment `[sdlc-workflow] Description digest: <tagged-digest>` (no footnote).

---

## Task description

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-510. `GET /api/v2/advisories` leaves out the `X-Total-Count` and `Link` (`rel="next"`) pagination headers when the date-range filters `publishedAfter` and/or `publishedBefore` are supplied, even though the response body is correctly filtered and limited. Unfiltered requests return the headers correctly. Clients that rely on these headers cannot work out the total count or the next page for date-filtered queries. This task makes the date-filtered request path emit the same pagination headers as the unfiltered path, with counts and next-page links that respect the date filters.

## Files to Modify
- Advisories list handler for `GET /api/v2/advisories` in acme-backend (exact path not confirmed during triage; locate with `grep -rn "advisories" --include=*.rs src/` and `grep -rnE "published_?[Aa]fter|filter_?[Dd]ate_?[Rr]ange" --include=*.rs`). Route the date-filtered branch through the shared paginated response / header path.
- Advisories service/query function that applies the date-range filter (exact path not confirmed). Make sure the total count is computed with the same date predicates as the page query.
- Pagination header helper (locate with `grep -rn "X-Total-Count" --include=*.rs`). Only if needed, so the `Link` next-page URL keeps the `publishedAfter`/`publishedBefore` query parameters.

## Implementation Notes
- **Traceability:** Fixes ACME-510 (Affects Version: RHTPA 0.9.0).
- **Triage limitation:** Code intelligence (Serena) was unavailable, and the repository context available during triage did not include the advisories or pagination code. So the file paths above are search targets, not verified paths. Start by locating:
  1. the handler for `/api/v2/advisories`,
  2. where `publishedAfter`/`publishedBefore` (possibly an internal `filterDateRange` / `filter_date_range` struct or function) are applied,
  3. where `X-Total-Count` and `Link` are written for the unfiltered case.
- **Likely defect shape:** the body is correct but the headers are entirely missing only with date filters. So the date-filtered branch most likely returns a bare list/JSON body (or a result with no total) and skips the paginated-response wrapper or header helper used by the unfiltered branch. Another possibility: the count query fails with date predicates and the error is swallowed. Check both.
- **Fix direction:** keep a single code path. Apply the date predicates to a shared query builder that feeds both the page query (with `limit`/`offset`) and the total-count query. Then return through the same paginated response type/helper the unfiltered path already uses. Do not duplicate header-building logic in the filtered branch.
- **Link header:** the `rel="next"` URL must keep `publishedAfter`, `publishedBefore`, and `limit` so following it returns the next page of the *filtered* set. Omit `rel="next"` on the last page, the same as the unfiltered behavior.
- **Count correctness:** `X-Total-Count` must be the number of advisories matching the date filter, not the unfiltered table total.
- **Reproducer test guidance (from the Bug's Steps to Reproduce):**
  - Trigger: `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` with more than 10 seeded advisories in range.
  - Buggy behavior (Actual Result): body has 10 correctly filtered advisories, but `X-Total-Count` and `Link` headers are absent.
  - Correct behavior (Expected Result): `X-Total-Count: <in-range count>` and `Link: <url>; rel="next"` are present.
  - Model the test on existing endpoint integration tests that assert response headers (locate with `grep -rn "X-Total-Count" tests/`). Reuse their test-server and DB-seeding setup.
- **Conventions:** the repository has no CONVENTIONS.md at its root. Follow the patterns of the surrounding code.
- **No data migration:** pagination headers are computed per request. Nothing is persisted.

## Reuse Candidates
- Pagination response wrapper / header helper used by the unfiltered `GET /api/v2/advisories` path (locate via `grep -rn "X-Total-Count" --include=*.rs`). Reuse it for the date-filtered path instead of writing new header logic.
- Existing next-page `Link` URL builder. Extend it to carry the date-filter query parameters if it does not already forward all query params.

## Acceptance Criteria
- [ ] A reproducer integration test calls `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` with more than 10 in-range advisories seeded. It asserts that `X-Total-Count` and `Link; rel="next"` headers are present. The test fails before the fix and passes after.
- [ ] Date-filtered requests (`publishedAfter` only, `publishedBefore` only, or both) return `X-Total-Count` equal to the number of advisories matching the filter.
- [ ] Date-filtered requests return a `Link` header with `rel="next"` when more pages exist, and its URL keeps the date-filter and `limit` parameters. No `rel="next"` is returned on the last page.
- [ ] Response bodies for date-filtered requests are unchanged (still correctly filtered and limited).
- [ ] Unfiltered requests to `GET /api/v2/advisories` keep returning correct pagination headers (no regression).
- [ ] All existing tests pass.

## Test Requirements
- [ ] Reproducer test: seed 15 advisories published between 2025-01-01 and 2025-06-30 and 5 outside that range. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. Assert status 200, body length 10, `X-Total-Count == "15"`, and a `Link` header with `rel="next"` whose URL contains `publishedAfter=2025-01-01` and `publishedBefore=2025-06-30`. (Before the fix both headers are absent.)
- [ ] Test with only `publishedAfter`, and with only `publishedBefore`. Assert `X-Total-Count` reflects the filtered count.
- [ ] Last-page test: request the final page of a date-filtered result set. Assert `X-Total-Count` is present and `rel="next"` is absent.
- [ ] Regression test: unfiltered `GET /api/v2/advisories?limit=10` still returns `X-Total-Count` (full count) and `Link; rel="next"`.

## Verification Commands
- `cargo test` — all tests pass, including the new reproducer test
- `curl -si "http://localhost:<port>/api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10" | grep -iE "x-total-count|^link:"` — both headers are printed

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start the backend locally. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. Inspect the response headers.
- **Expected Result**: Response includes `X-Total-Count: <n>` (total matching advisories) and `Link: <url>; rel="next"` when more pages exist.
- **Actual Result**: Body contains the correct filtered advisories, but `X-Total-Count` and `Link` headers are absent. Non-filtered requests return the headers correctly.
- **Root Cause**: The date-range-filtered branch of the `/api/v2/advisories` list path does not produce pagination metadata (total count / next link), or does not pass it to the header helper used by the unfiltered path. As a result the headers are omitted whenever `publishedAfter`/`publishedBefore` are supplied. Exact file and symbol to be confirmed during implementation. Affects Version: RHTPA 0.9.0.
