## Repository
acme-backend

## Target Branch
main

## Description
Fix the `/api/v2/advisories` endpoint to include `X-Total-Count` and `Link` pagination headers when date-range query parameters (`publishedAfter`, `publishedBefore`) are used. Currently, the date-filtered query path bypasses the pagination header generation logic, causing clients to lose pagination information on filtered requests. Fixes ACME-510.

## Files to Modify
- Advisories endpoint handler -- wire pagination header logic into the date-range filtered query path so that `X-Total-Count` and `Link` headers are generated for filtered requests
- Pagination header generation functions -- ensure the count query accepts date-range filter parameters so the total count reflects the filtered result set

## Implementation Notes
The unfiltered advisories query path correctly generates pagination headers by:
1. Executing a count query to determine total matching advisories
2. Setting the `X-Total-Count` header with the count result
3. Building the `Link` header with `rel="next"` (and other rel values) based on the count, limit, and offset

The date-range filtered path skips both the count query and the header generation. To fix:
1. Apply the same `publishedAfter`/`publishedBefore` WHERE clause to the count query when date-range filters are present
2. Call the pagination header generation functions from the filtered path, passing the filtered count
3. Ensure the `Link` header URLs preserve the date-range query parameters so that paginated navigation maintains the filter context

The fix should reuse the existing pagination header generation functions rather than duplicating them. The count query should be parameterized to accept optional date-range filters.

Fixes [ACME-510](https://mock-jira.example.com/browse/ACME-510).

## Acceptance Criteria
- [ ] A reproducer test calls `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` and asserts that `X-Total-Count` and `Link` headers are present and correct (test fails before fix, passes after)
- [ ] The `X-Total-Count` header value reflects the total number of advisories matching the date-range filter, not the unfiltered total
- [ ] The `Link` header includes `rel="next"` when filtered results exceed the limit, with date-range parameters preserved in the link URLs
- [ ] Non-filtered requests continue to return pagination headers correctly (no regression)
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: call the advisories endpoint with `publishedAfter` and `publishedBefore` query parameters and a `limit` that is smaller than the total filtered count; assert that (a) the `X-Total-Count` header is present and equals the total filtered advisory count, (b) the `Link` header contains a `rel="next"` URL that includes the original date-range query parameters, and (c) the response body contains only advisories within the specified date range
- [ ] Test that requests with only `publishedAfter` (no `publishedBefore`) also include correct pagination headers
- [ ] Test that requests with only `publishedBefore` (no `publishedAfter`) also include correct pagination headers
- [ ] Test that non-filtered requests continue to return pagination headers correctly (regression guard)

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start the backend service locally. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. Inspect the response headers.
- **Expected Result**: Response includes `X-Total-Count: <n>` header with total matching advisories and `Link: <url>; rel="next"` header when more pages exist.
- **Actual Result**: Response body contains correct filtered advisories, but `X-Total-Count` and `Link` headers are absent. Non-filtered requests return pagination headers correctly.
- **Root Cause**: The date-range filtered query path in the advisories endpoint handler does not invoke the pagination header generation logic. The count query and Link header builder are called from the unfiltered path but not from the filtered path.
