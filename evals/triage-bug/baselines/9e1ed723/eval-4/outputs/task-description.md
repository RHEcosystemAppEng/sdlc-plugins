# Step 5 – Generated Task: ACME-510 fix

**Jira create_issue parameters (not executed, eval mode):**
- Project: `ACME`
- Issue type: Task
- Summary: `Fix missing pagination headers on /api/v2/advisories with date-range filter`
- Labels: `["ai-generated-jira"]`

**Step 5b link (not executed):** `jira.create_issue_link(link_type="Blocks", inward_issue_key=<new-task-key>, outward_issue_key="ACME-510")`. The Task blocks the Bug.

**Step 5c digest (not executed):** re-fetch the created task's description, run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`, then post `[sdlc-workflow] Description digest: <tagged-digest>` as a standalone comment with no footnote.

**Caveat:** the provided repository context did not cover the advisories endpoint (it describes ACME-500). No real file paths were found, so file entries below are marked "to be located" rather than invented. In a live run, the skill would run the searches listed in investigation.md and fill these in before creating the Task.

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-510. `GET /api/v2/advisories` leaves out the `X-Total-Count` and `Link` pagination headers when the request includes the `publishedAfter` / `publishedBefore` date-range filters, even though the filtered body is correct. Requests without these filters return the headers correctly. Clients that rely on the headers cannot work out the total number of pages for date-filtered queries. This task makes the date-filtered path return the same pagination headers as the unfiltered path, with the total count reflecting the filtered result set.

## Files to Modify
- acme-backend `/api/v2/advisories` endpoint handler (to be located: grep for the `/advisories` route registration under `**/*.rs`). Make the date-range branch return a paginated response so the pagination headers are emitted.
- acme-backend advisory query/service function used by the date-range branch (to be located: grep `published_after` / `publishedAfter`). Compute the total count with the date predicates applied, if it does not already.

## Files to Create
- acme-backend advisories endpoint integration test (to be located: add it next to the existing advisories endpoint tests, following their naming and placement). This is the reproducer test for ACME-510.

## Implementation Notes
- Fixes ACME-510.
- **Trigger scenario:** `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`.
- **Incorrect behaviour (Actual Result):** the body contains the correct filtered advisories, but the `X-Total-Count` and `Link` response headers are missing.
- **Correct behaviour (Expected Result):** `X-Total-Count: <n>`, where `<n>` is the total number of advisories in the date range (not the page size), and `Link: <url>; rel="next"` when more pages exist.
- **Likely defect:** the unfiltered path already emits both headers correctly. Find the code that builds them for the unfiltered path, which is probably a shared paginated-results type or header helper, and send the date-filtered path through it. Do not duplicate the header logic. Two forms are likely:
  1. The filtered branch returns a plain list instead of the paginated wrapper. Fix by returning the wrapper.
  2. The filtered branch skips the count query. Fix by running the count with the same `published_after` / `published_before` predicates, so `X-Total-Count` matches the filtered set.
- The `Link: rel="next"` URL must keep the `publishedAfter` / `publishedBefore` query parameters, so following the link stays in the filtered set.
- **Persistence impact:** none. The headers are computed for each request, so no data migration is needed.
- No CONVENTIONS.md exists at the repository root. Follow the patterns of the existing advisories endpoint and its tests.
- Discovery searches (Read/Grep/Glob, since no Serena instance is available): `X-Total-Count`, `header::LINK`, `rel="next"`, `paginate`, `total_count`, `published_after`.

## Reuse Candidates
- The existing pagination header and paginated-response logic used by the unfiltered `GET /api/v2/advisories` path (symbol to be located). Reuse it for the date-filtered path.

## Acceptance Criteria
- [ ] A reproducer integration test calls `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` against seeded data with more than 10 advisories in range, and asserts that `X-Total-Count` and `Link` (`rel="next"`) are present. It fails before the fix and passes after.
- [ ] Date-range-filtered requests to `/api/v2/advisories` return `X-Total-Count` equal to the total number of advisories in the range (not the page size and not the unfiltered total).
- [ ] Date-range-filtered requests return a `Link` header with `rel="next"` when more pages exist, and the next URL keeps the date-range parameters.
- [ ] Unfiltered requests to `/api/v2/advisories` still return correct pagination headers (no regression).
- [ ] All existing tests pass.

## Test Requirements
- [ ] **Reproducer (ACME-510):** seed more than 10 advisories with `published` dates between 2025-01-01 and 2025-06-30, plus several outside the range. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. Assert that the status is 200, the body has 10 items, `X-Total-Count` equals the in-range seeded count, and `Link` contains `rel="next"` with the `publishedAfter`/`publishedBefore` parameters kept. Before the fix, the header assertions fail because the headers are absent.
- [ ] Last-page case: with a date-range filter and an offset/page at the end of the result set, `X-Total-Count` is present and `Link` has no `rel="next"`.
- [ ] Regression: an unfiltered `GET /api/v2/advisories?limit=10` still returns `X-Total-Count` and `Link`.

## Verification Commands
- `cargo test` — all tests pass, including the new ACME-510 reproducer.
- `curl -si "http://localhost:<port>/api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10" | grep -iE '^(x-total-count|link):'` — prints both headers.

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start the backend locally. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. Inspect the response headers.
- **Expected Result**: The response includes `X-Total-Count: <n>` (total matching advisories) and `Link: <url>; rel="next"` when more pages exist.
- **Actual Result**: The body contains the correct filtered advisories, but `X-Total-Count` and `Link` are absent. Unfiltered requests return the headers correctly.
- **Root Cause**: The date-range branch of the `/api/v2/advisories` handler skips the paginated-response or total-count path that emits the pagination headers. This is inferred from symptoms; the exact code location is still to be confirmed.
