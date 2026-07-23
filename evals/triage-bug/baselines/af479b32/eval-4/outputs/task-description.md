# Step 5 -- Generated Task Description

**Task Summary**: Add pagination headers to date-range-filtered advisories endpoint

**Labels**: `ai-generated-jira`

**Link**: Task blocks ACME-510 (link type: Blocks)

---

## Repository
acme-backend

## Target Branch
main

## Description
The `GET /api/v2/advisories` endpoint omits `X-Total-Count` and `Link` pagination
headers when date range filter parameters (`publishedAfter`, `publishedBefore`) are
applied. The unfiltered path correctly generates these headers, but the filtered code
path bypasses the pagination header pipeline. This task fixes the filtered path to
compute total count and attach pagination headers, matching the behavior of unfiltered
requests. Fixes ACME-510.

## Files to Modify
- `src/api/v2/advisories.rs` -- Wire the date-range-filtered query path through the pagination header utility
- `src/api/pagination.rs` (or equivalent pagination module) -- Ensure the pagination utility can accept a filtered count value (may already work as-is)

## Implementation Notes
The root cause is a missing integration between the date-range-filtered query path
and the existing pagination header pipeline. The unfiltered path already demonstrates
the correct pattern:

1. Execute the query to get the result set
2. Execute a count query to get the total number of matching records
3. Pass the total count to the pagination utility to generate `X-Total-Count` and
   `Link` headers
4. Attach the headers to the HTTP response

The fix should apply the same pattern to the filtered path:

1. In the endpoint handler (e.g., `src/api/v2/advisories.rs`), locate the conditional
   branch that handles `publishedAfter`/`publishedBefore` parameters.
2. After executing the filtered query, add a count query that applies the same date
   range filters to compute the total number of matching advisories.
3. Pass the total count to the existing pagination header utility (e.g., in
   `src/api/pagination.rs`).
4. Attach the resulting `X-Total-Count` and `Link` headers to the response.

Reference the unfiltered path's pagination logic as the pattern to follow. The
pagination utility functions that generate `X-Total-Count` and `Link` headers should
be reusable without modification -- the fix is in the caller (the filtered handler),
not the utility itself.

Fixes [ACME-510](https://mock-jira.example.com/browse/ACME-510).

## Acceptance Criteria
- [ ] A reproducer test sends `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` and asserts that `X-Total-Count` and `Link` headers are present in the response (fails before fix, passes after)
- [ ] Date-range-filtered requests to `/api/v2/advisories` return `X-Total-Count` header with the correct total number of matching advisories
- [ ] Date-range-filtered requests return `Link` header with `rel="next"` when more pages exist beyond the requested limit
- [ ] Unfiltered requests continue to return pagination headers correctly (no regression)
- [ ] Response body content for filtered requests remains correct (no regression)
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: integration test that calls `GET /api/v2/advisories` with `publishedAfter` and `publishedBefore` query parameters and a `limit` value, then asserts: (a) `X-Total-Count` header is present and contains the correct total count of advisories matching the date range, (b) `Link` header is present with `rel="next"` when the total exceeds the limit, (c) response body contains the correct filtered advisory records. This test must fail before the fix is applied and pass after.
- [ ] Regression test: verify that unfiltered requests to `/api/v2/advisories` with pagination (`limit` parameter) still return both `X-Total-Count` and `Link` headers correctly.
- [ ] Edge case test: verify pagination headers when the date range filter matches zero advisories (`X-Total-Count: 0`, no `Link` header).
- [ ] Edge case test: verify pagination headers when the date range filter matches exactly the limit count (no `Link` header with `rel="next"` since there is no next page).

## Verification Commands
- `cargo test` -- All existing and new tests pass
- `curl -i 'http://localhost:8080/api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10'` -- Response includes `X-Total-Count` and `Link` headers

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start the backend service locally, call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`, inspect response headers.
- **Expected Result**: Response includes `X-Total-Count: <n>` header with total matching advisories and `Link: <url>; rel="next"` header when more pages exist.
- **Actual Result**: Response body contains correct filtered advisories, but `X-Total-Count` and `Link` headers are absent. Non-filtered requests return pagination headers correctly.
- **Root Cause**: The date-range-filtered query path bypasses the pagination header pipeline. The unfiltered path correctly computes total count and attaches pagination headers, but the filtered path was implemented without wiring it through the same pagination utility.
