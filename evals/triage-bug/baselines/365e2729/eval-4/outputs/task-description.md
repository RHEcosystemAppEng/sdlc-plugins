# Step 5 – Generated Task (ACME-510)

**Task creation parameters (would be passed to `jira.create_issue`):**

- Project: ACME
- Issue type: Task
- Summary: Fix missing pagination headers on date-range filtered /api/v2/advisories responses
- Labels: `ai-generated-jira`
- Link (Step 5b): link type `Blocks`, inward = created Task (blocker), outward = ACME-510 (blocked)
- Digest (Step 5c): after creation, re-fetch the description, run `python3 scripts/sha256-digest.py`,
  and post `[sdlc-workflow] Description digest: <tagged-digest>` as a standalone comment

---

## Repository
acme-backend

## Target Branch
main

## Description
Fixes ACME-510. `GET /api/v2/advisories` omits the `X-Total-Count` and `Link`
pagination headers when the request includes the date-range filter (`publishedAfter` /
`publishedBefore`). The response body is correct, and unfiltered requests return the
headers correctly. Clients that paginate by these headers cannot work out the total
pages for date-filtered queries. This task makes the date-filtered list path emit the
same pagination headers as the unfiltered path, with the total count reflecting the
filtered result set. A reproducer test proves the fix.

## Files to Modify
- The `GET /api/v2/advisories` list handler in acme-backend — route the date-range
  filtered path through the existing pagination-header logic. The exact path was not
  available during triage. Locate it with `grep -rn "X-Total-Count" /home/dev/repos/acme-backend`
  and `grep -rnE "published_?[Aa]fter" /home/dev/repos/acme-backend`.
- The advisory service/query function used for date-filtered listing — make it return
  the total count (with the same filter predicates) together with the page items, if it
  currently returns items only.

## API Changes
- `GET /api/v2/advisories` — MODIFY: when `publishedAfter` and/or `publishedBefore` are
  supplied, the response now includes `X-Total-Count` (the filtered total) and a `Link`
  header with `rel="next"` when more pages exist. The response body is unchanged.

## Implementation Notes
- **Traceability:** Fixes ACME-510.
- **Root cause:** the pagination headers are produced only on the unfiltered list path.
  The date-filtered path returns the items but skips the paginated/counted response
  wrapper, so both headers are missing together. Also rule out the secondary
  possibility: a count or `Link` builder error that is silently swallowed when filter
  params are present.
- **Locate the code first.** Triage could not access the acme-backend source. Find:
  1. where `X-Total-Count` and the `Link` / `rel="next"` header are set (the existing
     pagination helper or response wrapper used by the unfiltered path)
  2. the advisories list handler and how it branches on `publishedAfter` / `publishedBefore`
  3. every caller of the pagination helper (to confirm the filtered path is not among them)
- **Fix direction:**
  - Reuse the existing pagination helper or wrapper from the unfiltered path. Do not
    write a second header implementation.
  - Apply the date-range predicates to **both** the items query and the total-count
    query, so `X-Total-Count` reflects the filtered set rather than all advisories.
  - Build the `Link` next-page URL so it keeps all active query parameters
    (`publishedAfter`, `publishedBefore`, `limit`, and any others), with the offset or
    cursor advanced.
  - Ideally, merge the filtered and unfiltered paths into one query builder with
    optional predicates, so later filters cannot regress the same way.
- **Reproducer guidance (from the Steps to Reproduce):**
  - Trigger: `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`
    with more than 10 advisories seeded in that range.
  - Actual (pre-fix) behavior the test exposes: correct body, but `X-Total-Count` and
    `Link` headers are absent.
  - Expected (post-fix) behavior to assert: `X-Total-Count: <filtered total>` and
    `Link: <url>; rel="next"`.
  - Put the test next to the existing advisories / pagination API tests in acme-backend.
    Find them by searching the test directories for `advisories` and `X-Total-Count`,
    and follow their fixture-seeding and header-assertion patterns.
- **Persistence:** no persistence impact. Pagination headers are computed per request,
  so no data migration is needed.
- **Conventions:** acme-backend has no CONVENTIONS.md, so follow the patterns of the
  surrounding handler code.

## Reuse Candidates
- The existing pagination-header helper or paginated response wrapper used by the
  unfiltered `GET /api/v2/advisories` path. It already produces correct `X-Total-Count`
  and `Link` headers, and the date-filtered path should reuse it. Its exact symbol and
  path were not available during triage; locate it via `X-Total-Count` search.

## Acceptance Criteria
- [ ] A reproducer test calls `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` with more than 10 in-range advisories seeded. It asserts that `X-Total-Count` and a `Link` header with `rel="next"` are present. The test fails before the fix and passes after.
- [ ] Date-range filtered requests return `X-Total-Count` equal to the number of advisories matching the filter (not the unfiltered total).
- [ ] Date-range filtered requests return a `Link` header with `rel="next"` when more pages exist, and the next URL keeps the `publishedAfter` / `publishedBefore` parameters.
- [ ] No `rel="next"` link is emitted on the last page of a filtered result set.
- [ ] Unfiltered requests still return correct pagination headers (no regression).
- [ ] All existing tests pass.

## Test Requirements
- [ ] Reproducer test (first): seed for example 15 advisories published between 2025-01-01 and 2025-06-30, plus several outside that range. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. Assert: `X-Total-Count == 15`; the `Link` header contains `rel="next"` and its URL includes `publishedAfter=2025-01-01` and `publishedBefore=2025-06-30`; the body has 10 items, all in range. Before the fix, the header assertions fail because the headers are absent.
- [ ] Last-page test: request the second page of the same filtered query. Assert that `X-Total-Count == 15`, the body has 5 items, and there is no `rel="next"`.
- [ ] Single-bound filters: `publishedAfter` only and `publishedBefore` only each return correct pagination headers.
- [ ] Regression test: the unfiltered `GET /api/v2/advisories?limit=10` still returns correct `X-Total-Count` and `Link`.

## Verification Commands
- `cargo test` (in acme-backend) — all tests pass, including the new reproducer.
- `curl -si "http://localhost:<port>/api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10" | grep -iE "^(x-total-count|link):"` — both headers are printed.

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start the backend locally. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. Inspect the response headers.
- **Expected Result**: The response includes `X-Total-Count: <n>` (total matching advisories) and `Link: <url>; rel="next"` when more pages exist.
- **Actual Result**: The body contains the correct filtered advisories, but `X-Total-Count` and `Link` are absent. Unfiltered requests return the headers correctly.
- **Root Cause**: The pagination-header logic is applied only on the unfiltered list path. The date-range filtered path returns items without going through the paginated/counted response wrapper, so both headers are omitted. The exact acme-backend file and symbol must be confirmed during implementation.
- **Affects Version**: RHTPA 0.9.0 (ID 62643), proposed for user confirmation in Step 4.5.
