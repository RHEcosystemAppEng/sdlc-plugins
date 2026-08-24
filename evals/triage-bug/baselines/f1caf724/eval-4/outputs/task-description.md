## Repository
acme-backend

## Target Branch
main

## Description
Fix missing pagination headers (`X-Total-Count` and `Link`) in the `/api/v2/advisories` endpoint when date-range filter query parameters (`publishedAfter`, `publishedBefore`) are applied. The filtered code path does not compute the total count of matching records or invoke the pagination header generation logic, causing clients to lose pagination metadata for filtered requests. Fixes ACME-510.

## Files to Modify
- `src/api/v2/advisories.rs` (or equivalent endpoint handler) -- add total count query and pagination header generation to the date-range filtered code path
- `src/api/pagination.rs` (or equivalent pagination utility) -- ensure the pagination header function is callable from the filtered path (may need no changes if already reusable)

## Implementation Notes
The root cause is that the date-range filtering branch in the `/api/v2/advisories` endpoint handler skips the total count computation and pagination header generation that the unfiltered branch performs correctly.

To fix:
1. In the filtered query path, add a count query that applies the same `publishedAfter`/`publishedBefore` conditions as the data query. This ensures the count reflects the filtered result set, not the total unfiltered count.
2. Pass the filtered count result to the existing pagination header utility (the same function used by the unfiltered path) to generate `X-Total-Count` and `Link` headers.
3. Reuse the existing pagination header generation logic -- do not duplicate it. The unfiltered path already demonstrates the correct pattern for computing count and generating headers.

The reproducer test should call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` against a test dataset containing advisory records that span the date range. The test should:
- **Before fix (fails)**: Assert that `X-Total-Count` header is present in the response -- this will fail, demonstrating the bug.
- **After fix (passes)**: Assert that `X-Total-Count` header is present with the correct filtered count, and `Link` header with `rel="next"` is present when total results exceed the limit.

Also verify that non-filtered requests continue to return pagination headers correctly (regression guard).

## Acceptance Criteria
- [ ] A reproducer test calls `GET /api/v2/advisories` with `publishedAfter` and `publishedBefore` parameters and asserts that `X-Total-Count` and `Link` pagination headers are present and correct -- this test fails before the fix and passes after
- [ ] The `/api/v2/advisories` endpoint returns `X-Total-Count` header with the correct count of advisories matching the date-range filter
- [ ] The `/api/v2/advisories` endpoint returns `Link` header with `rel="next"` when filtered results exceed the `limit` parameter
- [ ] Non-filtered requests to `/api/v2/advisories` continue to return pagination headers correctly (no regression)
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: integration test that sends `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` with a test dataset containing known advisory records, asserts `X-Total-Count` header equals the expected filtered count, and asserts `Link` header contains `rel="next"` when more pages exist. This test must fail before the fix and pass after.
- [ ] Regression test: verify that `GET /api/v2/advisories?limit=10` (no date-range filter) still returns `X-Total-Count` and `Link` headers correctly
- [ ] Edge case test: verify behavior when date-range filter matches zero results (should return `X-Total-Count: 0` and no `Link` header)
- [ ] Edge case test: verify behavior when date-range filter matches fewer results than the limit (should return correct `X-Total-Count` and no `Link` header since all results fit in one page)

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start the backend service locally, call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`, and inspect response headers.
- **Expected Result**: Response includes `X-Total-Count: <n>` header with total matching advisories and `Link: <url>; rel="next"` header when more pages exist.
- **Actual Result**: Response body contains correct filtered advisories but `X-Total-Count` and `Link` headers are absent. Non-filtered requests return pagination headers correctly.
- **Root Cause**: The date-range filtering code path in the `/api/v2/advisories` endpoint handler does not execute the total count query or pass its result to the pagination header generation logic, causing pagination headers to be omitted for filtered requests while unfiltered requests work correctly.
