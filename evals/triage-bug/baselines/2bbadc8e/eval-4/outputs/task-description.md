## Repository
acme-backend

## Target Branch
main

## Description
Fix the `/api/v2/advisories` endpoint to include `X-Total-Count` and `Link` pagination
headers when date range filter parameters (`publishedAfter`, `publishedBefore`) are
applied. Currently, the filtered query path bypasses the pagination header generation
logic that works correctly for unfiltered requests. Fixes ACME-510.

## Files to Modify
- Advisories endpoint handler (file containing the `GET /api/v2/advisories` route definition) -- add pagination header generation to the filtered query path
- Pagination header helper (if the total-count query needs modification to accept filtered query parameters) -- ensure it supports filtered result sets

## Implementation Notes
The unfiltered code path for `GET /api/v2/advisories` correctly computes a total count
of matching records and passes it to a pagination header helper that sets `X-Total-Count`
and `Link` headers. The filtered code path (activated when `publishedAfter` and/or
`publishedBefore` query parameters are present) does not invoke this pagination logic.

To fix:
1. Locate the advisories endpoint handler by searching for the `/api/v2/advisories`
   route definition in the acme-backend codebase.
2. Identify the branch point where filtered vs. unfiltered query paths diverge.
3. In the filtered branch, add a total-count query that counts all advisories matching
   the date range filter (not just the current page).
4. Pass the total count to the existing pagination header helper to set `X-Total-Count`
   and generate the `Link` header with `rel="next"` when additional pages exist.
5. Ensure the pagination header helper is reused rather than duplicated -- the same
   helper that works for unfiltered requests should be called from the filtered path.

**Reproducer test guidance**:
- **Input**: `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`
  against a test dataset containing more than 10 advisories published within that range.
- **Incorrect behavior (before fix)**: Response has correct body but `X-Total-Count` and
  `Link` headers are absent.
- **Correct behavior (after fix)**: Response includes `X-Total-Count` header with the
  total number of matching advisories, and `Link` header with `rel="next"` URL when
  more pages exist.

Fixes ACME-510.

## Acceptance Criteria
- [ ] Reproducer test: an integration test calls `GET /api/v2/advisories` with `publishedAfter` and `publishedBefore` parameters and asserts that `X-Total-Count` and `Link` pagination headers are present with correct values. This test must fail before the fix and pass after.
- [ ] The filtered query path in the advisories endpoint invokes the pagination header generation logic, setting `X-Total-Count` to the total count of advisories matching the date range filter.
- [ ] The `Link` header with `rel="next"` is included when the filtered result set has more pages beyond the current `limit`.
- [ ] Non-filtered requests to `GET /api/v2/advisories` (without date range parameters) continue to return pagination headers correctly (no regression).
- [ ] No regression in existing tests.

## Test Requirements
- [ ] Reproducer test: integration test that sends `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` with a test dataset containing more than 10 matching advisories, and asserts: (a) `X-Total-Count` header is present and equals the total count, (b) `Link` header is present and contains `rel="next"` URL. This test must fail before the code fix and pass after.
- [ ] Regression test: verify that unfiltered `GET /api/v2/advisories?limit=10` requests still return `X-Total-Count` and `Link` headers correctly.
- [ ] Edge case test: verify pagination headers when the filtered result set fits within a single page (total count <= limit) -- `X-Total-Count` should be present, `Link` with `rel="next"` should be absent.

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start the backend service locally. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. Inspect the response headers.
- **Expected Result**: Response includes `X-Total-Count: <n>` header with total matching advisories and `Link: <url>; rel="next"` header when more pages exist.
- **Actual Result**: Response body contains correct filtered advisories, but `X-Total-Count` and `Link` headers are absent. Non-filtered requests return pagination headers correctly.
- **Root Cause**: The date-range-filtered query path in the `/api/v2/advisories` endpoint bypasses the pagination header generation logic. The unfiltered path correctly sets these headers, but the filtered branch was implemented without integrating the existing pagination header helper.
