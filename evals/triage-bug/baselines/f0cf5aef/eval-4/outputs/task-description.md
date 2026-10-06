## Repository
acme-backend

## Target Branch
main

## Description
Fix the `/api/v2/advisories` endpoint to emit `X-Total-Count` and `Link` pagination headers when date range filter parameters (`publishedAfter`, `publishedBefore`) are supplied. Currently the filtered query path bypasses the pagination header generation logic, causing clients to lose pagination metadata when filtering by date range. Fixes ACME-510.

## Files to Modify
- Advisory endpoint handler module -- add pagination header generation to the filtered query path, ensuring the count query runs against the filtered result set
- Pagination utility (if the count query needs to accept filter predicates) -- extend to support filtered counts

## Implementation Notes
The root cause is that the date range filtering branch in the advisories endpoint handler returns results directly without invoking the shared pagination header logic. The unfiltered path correctly:
1. Executes a count query to determine total matching records
2. Sets the `X-Total-Count` header from the count result
3. Computes and sets the `Link` header with `rel="next"` when `offset + limit < total_count`
4. Returns the paginated data

The fix should ensure the filtered path follows the same pagination flow. Critically, the count query in the filtered path must apply the same `publishedAfter`/`publishedBefore` WHERE clause so that `X-Total-Count` reflects the filtered total, not the unfiltered total.

Look at how the unfiltered path invokes the pagination utility and replicate that pattern in the filtered branch. If the pagination utility or count query function does not currently accept filter predicates, extend it to do so. Reference existing pagination tests to understand the assertion patterns for `X-Total-Count` and `Link` headers.

No CONVENTIONS.md was found in the repository.

## Acceptance Criteria
- [ ] Reproducer test: a test that calls `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` against a dataset with more than 10 matching advisories and asserts that `X-Total-Count` and `Link` headers are present and correct (fails before fix, passes after)
- [ ] The `/api/v2/advisories` endpoint returns `X-Total-Count` header with the correct filtered count when date range parameters are provided
- [ ] The `/api/v2/advisories` endpoint returns a `Link` header with `rel="next"` when more pages of filtered results exist
- [ ] The `X-Total-Count` value reflects the count of advisories matching the date range filter, not the total unfiltered count
- [ ] Non-filtered requests continue to return correct pagination headers (no regression)
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: create a test with a dataset containing more than `limit` advisories within a specific date range. Issue `GET /api/v2/advisories?publishedAfter=<start>&publishedBefore=<end>&limit=<n>` and assert: (1) response status is 200, (2) `X-Total-Count` header is present and equals the total number of advisories in the date range, (3) `Link` header is present with `rel="next"` when total exceeds limit, (4) response body contains the correct filtered advisories
- [ ] Regression test: verify that a non-filtered paginated request (`GET /api/v2/advisories?limit=10`) still returns correct `X-Total-Count` and `Link` headers
- [ ] Edge case: verify pagination headers when the filtered result set is empty (total count should be 0, no `Link` header)
- [ ] Edge case: verify pagination headers when the filtered result set fits within a single page (total count <= limit, no `Link` header with `rel="next"`)

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start the backend service locally. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. Inspect the response headers.
- **Expected Result**: Response includes `X-Total-Count: <n>` header with the total number of matching advisories and `Link: <url>; rel="next"` header when more pages exist.
- **Actual Result**: Response body contains correct filtered advisories, but `X-Total-Count` and `Link` headers are absent. Non-filtered requests return pagination headers correctly.
- **Root Cause**: The date range filtering code path in the advisories endpoint handler bypasses the pagination header generation logic. The filtered branch returns results directly without executing the count query or invoking the shared pagination utility that sets `X-Total-Count` and `Link` headers.
