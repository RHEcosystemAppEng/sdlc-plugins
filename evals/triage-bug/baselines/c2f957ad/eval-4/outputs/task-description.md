# Step 5 – Generated Task (not created in Jira for this eval)

**Project:** ACME
**Issue type:** Task
**Summary:** Fix missing X-Total-Count/Link pagination headers on date-filtered GET /api/v2/advisories
**Labels:** `ai-generated-jira`
**Link (Step 5b):** link type `Blocks`. Inward = <created-task-key> (blocks), outward = ACME-510 (is blocked by)
**Digest (Step 5c):** after creation, re-fetch the description, run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`, then post `[sdlc-workflow] Description digest: <tagged-digest>` as a standalone comment with no footnote.

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-510. `GET /api/v2/advisories` leaves out the `X-Total-Count` and `Link` (rel="next") pagination headers when the request is filtered by date range (`publishedAfter` / `publishedBefore`). The response body is correct, and unfiltered requests return the headers correctly. Clients that rely on pagination headers cannot work out the total count or the number of pages for date-filtered queries. This task restores pagination headers on the date-filtered path so they match the unfiltered path.

## Files to Modify
The triage context did not include acme-backend source for this endpoint, so exact paths could not be confirmed. Before changing anything, the implementer must locate and confirm these files (see Implementation Notes):
- Advisories handler for `GET /api/v2/advisories` (route registration and handler function): add or route the date-filtered branch through the pagination-header logic
- Advisory query or service function used when date filters are present: return the total count for the filtered query
- Advisories endpoint integration test file: add the reproducer test

## Implementation Notes
Fixes ACME-510.

**Locate the code first** (Serena `mcp__serena_backend__*` if available, otherwise Grep/Glob in `/home/dev/repos/acme-backend`):
1. Search for `"/advisories"` / `"api/v2"` to find the route and handler.
2. Search for `X-Total-Count`, `x-total-count`, `rel="next"`, `header::LINK` to find the code that builds pagination headers.
3. Search for `published_after`, `publishedAfter`, `date_range`, `DateRange` to find the query-parameter struct and the filtered branch.
4. Run `find_referencing_symbols` on the pagination-header helper to check whether the date-filtered branch calls it. The working hypothesis is that it does not.

**Hypothesized root cause (confirm it):** the date-range filter uses a separate query or response path that returns the filtered items but either (a) does not compute a total count, so header emission is skipped, or (b) builds the response without the shared pagination helper or wrapper. Also check whether the `Link` URL builder drops or fails on the `publishedAfter` / `publishedBefore` parameters.

**Fix direction:**
- Compute the total count with the **same filter predicates** as the item query, so the count reflects only advisories in the date range.
- Emit `X-Total-Count` and `Link` through the same mechanism as the unfiltered path. Do not duplicate header-building logic.
- Make the `Link` next/prev URLs keep all active query parameters (`publishedAfter`, `publishedBefore`, `limit`, and any others).
- Clarify which parameter name is canonical (`publishedAfter`/`publishedBefore` from the reproduction steps, or `filterDateRange` from the bug description) and test the one the API actually accepts.

**Reproducer test guidance:**
- Trigger: `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`, with more than 10 advisories seeded inside the range and some outside it.
- Buggy behavior (Actual Result): the response body has the correct filtered advisories, but `X-Total-Count` and `Link` are absent.
- Correct behavior (Expected Result): `X-Total-Count: <n>`, where n is the number of in-range advisories, and `Link: <url>; rel="next"`, because more pages exist.
- Follow the existing advisories or endpoint integration-test pattern in acme-backend (find it with Glob `tests/**/*advisor*` / `**/tests/*.rs`). Reuse any existing helper that asserts pagination headers on the unfiltered endpoint.

**Persistence:** pagination headers are computed per request. No database writes are involved, so no data migration is needed.

**Conventions:** acme-backend has no CONVENTIONS.md at its root. Follow the patterns already used in the surrounding handler and test code.

## Reuse Candidates
- The existing pagination-header helper or middleware that the unfiltered `GET /api/v2/advisories` path already uses to emit `X-Total-Count` and `Link`. Its exact path and symbol are to be confirmed. Reuse it on the filtered path; do not write a new implementation.
- The existing count query for the unfiltered advisories listing. Its exact path and symbol are to be confirmed. Extend it to apply the date-range predicates.

## Acceptance Criteria
- [ ] A reproducer integration test calls `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` and asserts that `X-Total-Count` and `Link` (rel="next") are present. The test fails before the fix and passes after it.
- [ ] Date-filtered requests to `GET /api/v2/advisories` return `X-Total-Count` equal to the total number of advisories matching the date filter, not the unfiltered total.
- [ ] Date-filtered requests return a `Link` header with `rel="next"` when more pages exist, and the next URL keeps the `publishedAfter` / `publishedBefore` parameters.
- [ ] Unfiltered requests still return correct pagination headers.
- [ ] All existing tests pass (no regressions).

## Test Requirements
- [ ] Reproducer test: seed more than 10 advisories with `published` dates between 2025-01-01 and 2025-06-30, plus some outside that range. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. Assert that the status is 200, the body has 10 items, `X-Total-Count` equals the in-range seeded count, and `Link` contains `rel="next"` with both date parameters in the URL.
- [ ] Test that a date-filtered request whose results fit on one page returns `X-Total-Count` and no `rel="next"` link.
- [ ] Test with only `publishedAfter`, and with only `publishedBefore`, and assert that headers are present in both cases.
- [ ] Regression test: an unfiltered `GET /api/v2/advisories?limit=10` still returns correct `X-Total-Count` and `Link` headers.

## Verification Commands
- `cargo test` — all tests pass, including the new reproducer.
- `curl -si "http://localhost:<port>/api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10" | grep -iE '^(x-total-count|link):'` — prints both headers.

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start the backend locally. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. Inspect the response headers.
- **Expected Result**: The response includes `X-Total-Count: <n>` (total matching advisories) and `Link: <url>; rel="next"` when more pages exist.
- **Actual Result**: The body contains the correct filtered advisories, but `X-Total-Count` and `Link` are absent. Unfiltered requests return the headers correctly.
- **Root Cause**: Preliminary (low confidence; the code was not available during triage). The date-range-filtered path of the advisories endpoint skips pagination-header generation, likely because it doesn't compute a filtered total count or doesn't use the shared pagination helper. Confirm in code before fixing.
- **Affects Version**: RHTPA 0.9.0 (ID 62643), pending user confirmation in Step 4.5
