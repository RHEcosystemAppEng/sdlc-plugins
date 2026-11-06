# Step 5 — Generated Task (simulated, not created in Jira)

**Project**: ACME
**Issue type**: Task
**Summary**: Fix missing X-Total-Count and Link pagination headers on date-filtered GET /api/v2/advisories
**Labels**: `ai-generated-jira`

## Step 5b — Link (simulated)

```
jira.create_issue_link(
  link_type="Blocks",
  inward_issue_key=<created-task-key>,   # Task (blocker)
  outward_issue_key="ACME-510"           # Bug (blocked)
)
```

## Step 5c — Digest (simulated)

After creation: re-fetch the task description, run `python3 scripts/sha256-digest.py /tmp/desc-<task-key>.txt`, and post a standalone comment `[sdlc-workflow] Description digest: <tagged-digest>` with no footnote.

---

## Task Description

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-510. `GET /api/v2/advisories` leaves out the `X-Total-Count` and `Link` (`rel="next"`) pagination headers when the date-range filters `publishedAfter` / `publishedBefore` are supplied. The filtered body is correct, and unfiltered requests return both headers. The date-filtered branch returns results without the pagination metadata (total count and next-page cursor) that the response builder needs to write these headers. Clients that page using the headers cannot work out the total number of pages for date-filtered queries.

This task sends the date-filtered query through the existing pagination flow so that filtered responses carry correct pagination headers.

## Files to Modify
The triage repository context did not include source for this endpoint, so exact paths are **not yet confirmed**. Before changing anything, find them in `/home/dev/repos/acme-backend`:
- The HTTP handler / route for `GET /api/v2/advisories`. Grep for `advisories`, `publishedAfter`, `published_after`. Change it to use the paginated result on the date-filter branch.
- The advisory service or query function that applies the `publishedAfter` / `publishedBefore` predicates (the reporter calls it "filterDateRange"). Make it return the total count of the filtered set together with the page.
- The existing test module for the advisories endpoint. Add the reproducer test there.

## Implementation Notes
- **Traceability**: Fixes ACME-510.
- **Locate first**: search the repo for the code that writes `X-Total-Count` and `Link` (grep `X-Total-Count`, `x-total-count`, `rel=\"next\"`, `paginat`, `total`). The unfiltered listing path already emits both headers correctly. That path, its paginated result type, and its header-writing helper are the pattern to reuse.
- **Fix direction**: do **not** add a second header-writing path. Make the date-range branch produce the same paginated result (items + total + offset/limit) that the unfiltered path produces, and let the existing response builder write the headers. Usually that means either:
  - folding the date predicates into the shared paginated query (best option: a single code path with optional filters), or
  - making the date-range query also run the count query and return the same paginated wrapper.
- **Count correctness**: the total-count query must apply the **same** `publishedAfter` / `publishedBefore` predicates as the item query. `X-Total-Count` must be the number of matching advisories, not the total of all advisories.
- **Link correctness**: the `rel="next"` URL must keep `publishedAfter`, `publishedBefore`, and `limit`, and advance the offset/page. Otherwise following the link drops the filter. Leave out `rel="next"` on the last page, matching the unfiltered behavior.
- **Reproducer guidance** (from Steps to Reproduce, Expected and Actual Result):
  - Trigger: `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`, with more than 10 advisories seeded in that window plus some outside it.
  - Before fix (Actual): body correct, `X-Total-Count` and `Link` headers **absent**.
  - After fix (Expected): `X-Total-Count: <n>` equals the in-window count, and `Link: <url>; rel="next"` is present because more pages exist.
- **Persistence**: none. The headers are computed per request and nothing on this path writes to the DB, so no data migration is needed.
- **Conventions**: `acme-backend` has no `CONVENTIONS.md` at its root. Follow the existing handler and test patterns in the advisories module.
- Affects Version: RHTPA 0.9.0 (from the Bug's Environment / Version section: "Product version: 0.9.0").

## Reuse Candidates
Not confirmed in the triage context. Before implementing, find these and reuse them:
- The paginated query helper and result type used by the unfiltered `GET /api/v2/advisories` path. Reuse it for the date-filtered branch.
- The helper or middleware that writes `X-Total-Count` and `Link` from a paginated result. Reuse it unchanged.

## Acceptance Criteria
- [ ] A reproducer test calls `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` against seeded data with more than 10 in-window advisories. It asserts that `X-Total-Count` and `Link` (`rel="next"`) are present. The test fails before the fix and passes after it.
- [ ] Date-filtered requests to `GET /api/v2/advisories` return `X-Total-Count` equal to the number of advisories matching the date range (not the unfiltered total).
- [ ] Date-filtered requests return a `Link` header with `rel="next"` when more pages exist. The next URL keeps the `publishedAfter` / `publishedBefore` / `limit` parameters. `rel="next"` is left out on the last page.
- [ ] Filtering with only `publishedAfter` or only `publishedBefore` also returns correct pagination headers.
- [ ] Response bodies for filtered and unfiltered requests are unchanged.
- [ ] No regression in existing tests. Unfiltered requests still return correct pagination headers.

## Test Requirements
- [ ] **Reproducer test (first)**: seed 15 advisories published between 2025-01-01 and 2025-06-30 and 3 outside that window. Request `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. Assert:
  - `X-Total-Count` header is present and equals `15` (it fails today because the header is absent)
  - `Link` header is present and contains `rel="next"`, and its URL includes `publishedAfter=2025-01-01` and `publishedBefore=2025-06-30` (it fails today because the header is absent)
  - body has exactly 10 advisories, all inside the date window
- [ ] Last-page test: the same filter with an offset/page pointing at the final page. `X-Total-Count` is `15` and `Link` has no `rel="next"`.
- [ ] Single-bound tests: `publishedAfter` only and `publishedBefore` only each return a correct `X-Total-Count` for their filtered set.
- [ ] Regression test: unfiltered `GET /api/v2/advisories?limit=10` still returns correct `X-Total-Count` and `Link` headers.

## Verification Commands
- `cargo test` — all tests pass, including the new reproducer
- `curl -si "http://localhost:<port>/api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10" | grep -iE '^(x-total-count|link):'` — both headers are printed

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start the backend locally, call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`, and inspect the response headers.
- **Expected Result**: The response includes `X-Total-Count: <n>` (total matching advisories) and `Link: <url>; rel="next"` when more pages exist.
- **Actual Result**: The body has the correct filtered advisories, but `X-Total-Count` and `Link` are absent. Unfiltered requests return the headers correctly.
- **Root Cause**: The date-range filtered branch of the advisories list endpoint returns results without pagination metadata (total count and next-page cursor), so the response builder skips both pagination headers. The unfiltered path goes through the normal pagination flow. This is inferred from behavior: the exact file and symbol must be confirmed in `acme-backend`, because the triage context did not include the endpoint source.
- **Environment / Version**: Product 0.9.0 (Affects Version: RHTPA 0.9.0), RHEL 9.2, OpenShift 4.14
