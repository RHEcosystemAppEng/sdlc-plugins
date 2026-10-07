## Repository
acme-backend

## Target Branch
main

## Description
Fix missing pagination headers (`X-Total-Count` and `Link`) on the `GET /api/v2/advisories` endpoint when date-range filter parameters (`publishedAfter`, `publishedBefore`) are applied. Currently, unfiltered requests return pagination headers correctly, but filtered requests omit them, breaking clients that rely on these headers for pagination.

## Files to Modify
- `src/handlers/advisories.rs` -- ensure the date-range-filtered query path computes total count and passes it to the pagination header builder
- `src/pagination.rs` -- verify pagination header generation works with filtered counts (if the count is passed correctly, no change may be needed)

## Implementation Notes
The advisories endpoint handler likely has divergent query construction for filtered vs. unfiltered requests. The fix should ensure that the count query executes in both code paths and that the resulting total is passed to the pagination header builder. Look at how unfiltered requests produce `X-Total-Count` and `Link` headers, and replicate that pattern for the filtered code path. Avoid duplicating pagination logic -- reuse the existing pagination utility that the unfiltered path already calls.

## Acceptance Criteria
- [ ] Reproducer test: `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` returns `X-Total-Count` header with the correct total of matching advisories
- [ ] Reproducer test: `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` returns `Link` header with `rel="next"` when more pages exist
- [ ] Unfiltered advisory queries continue to return pagination headers correctly (no regression)
- [ ] Pagination headers are correct when date-range filters return zero results

## Test Requirements
- [ ] Integration test that calls `GET /api/v2/advisories` with `publishedAfter` and `publishedBefore` parameters and asserts `X-Total-Count` header is present and matches the expected filtered count
- [ ] Integration test that calls the same filtered endpoint with a `limit` smaller than total results and asserts a `Link` header with `rel="next"` is present
- [ ] Integration test that calls the filtered endpoint with a date range returning zero results and asserts `X-Total-Count: 0` and no `Link` header
- [ ] Regression test confirming unfiltered `GET /api/v2/advisories` still returns both pagination headers

## Bug Context
- **Bug**: ACME-510 -- API response missing pagination headers when filtering by date range
- **Steps to Reproduce**: (1) Start backend service locally. (2) Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. (3) Inspect response headers.
- **Expected Result**: Response includes `X-Total-Count: <n>` and `Link: <url>; rel="next"` headers.
- **Actual Result**: Response body is correct but `X-Total-Count` and `Link` headers are absent. Non-filtered requests return pagination headers correctly.
- **Root Cause**: The date-range filtering code path bypasses the count query and/or pagination header attachment logic, so filtered responses omit headers that unfiltered responses include.
