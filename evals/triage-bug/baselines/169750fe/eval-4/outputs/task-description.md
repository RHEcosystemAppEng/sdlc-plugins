# Step 5 -- Generated Task Description: ACME-510 Fix

## Jira API Metadata

```
project: ACME
issueType: Task
labels: ["ai-generated-jira"]
link:
  type: Blocks
  inward: <created-task-key>
  outward: ACME-510
```

## Task Description

```
## Repository
acme-backend

## Target Branch
main

## Description
Fix missing `X-Total-Count` and `Link` pagination headers on the
`GET /api/v2/advisories` endpoint when date-range filter parameters
(`publishedAfter`, `publishedBefore`) are provided. The filtered query path
does not invoke the pagination header utility, so clients cannot determine
total pages for filtered results. Fixes ACME-510.

## Files to Modify
- `src/api/v2/advisories.rs` — Add pagination header utility call to the date-range-filtered query path, matching the existing unfiltered path logic
- `src/db/advisories.rs` — Ensure the filtered query function returns total count alongside filtered results (if not already provided)

## Implementation Notes
The unfiltered query path in the advisories endpoint handler already computes total
count and calls the pagination header utility to set `X-Total-Count` and `Link`
headers. The filtered path (triggered when `publishedAfter`/`publishedBefore` query
parameters are present) was added without replicating this pagination step.

To fix:
1. In the filtered branch of the advisories endpoint handler, add a `COUNT(*)`
   query against the filtered result set (applying the same `publishedAfter`/
   `publishedBefore` conditions) to compute the total count.
2. Call the existing pagination header utility (same function used by the unfiltered
   path) with the total count and the current page/limit parameters to set
   `X-Total-Count` and `Link` headers on the response.
3. Follow the same pattern as the unfiltered path to ensure consistency.

Look at the existing unfiltered path for the exact function signatures and calling
conventions for the pagination utility. The pagination utility likely accepts
parameters such as total count, current offset, limit, and base URL to compute
the `Link` header.

Fixes ACME-510.

## Acceptance Criteria
- [ ] A reproducer test calls `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` and asserts that `X-Total-Count` and `Link` pagination headers are present and correct -- this test must fail before the fix and pass after
- [ ] The filtered query path in the advisories endpoint handler calls the pagination header utility, producing `X-Total-Count` with the correct total count of matching advisories
- [ ] When more filtered results exist than the page limit, the `Link` header includes `rel="next"` pointing to the next page
- [ ] The response body continues to contain the correct filtered advisories (no regression in data)
- [ ] Non-filtered requests continue to return pagination headers correctly (no regression)
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: integration test that sends `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` and asserts (a) `X-Total-Count` header is present with a numeric value matching the total filtered advisory count, (b) `Link` header is present with `rel="next"` when total exceeds limit. This test must demonstrate failure without the fix.
- [ ] Regression test: verify that non-filtered `GET /api/v2/advisories?limit=10` requests still return `X-Total-Count` and `Link` headers correctly
- [ ] Edge case test: verify pagination headers when the filtered result set is empty (total count should be 0, no `Link` header with `rel="next"`)
- [ ] Edge case test: verify pagination headers when the filtered result set fits within a single page (total count equals result count, no `Link` header with `rel="next"`)

## Verification Commands
- `cargo test test_advisories_filtered_pagination` — reproducer test passes
- `cargo test test_advisories` — all existing advisory tests pass (no regression)

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start backend service, call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`, inspect response headers
- **Expected Result**: Response includes `X-Total-Count: <n>` header and `Link: <url>; rel="next"` header when more pages exist
- **Actual Result**: Response body has correct filtered advisories but `X-Total-Count` and `Link` headers are absent; non-filtered requests return headers correctly
- **Root Cause**: The date-range filter code path in the advisories endpoint handler does not invoke the pagination header utility after executing the filtered query, unlike the unfiltered path which correctly sets these headers
```
