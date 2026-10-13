## Repository
acme-backend

## Target Branch
main

## Description
Fix the missing pagination headers (`X-Total-Count`, `Link`) on the `GET /api/v2/advisories` endpoint when date range filter parameters (`publishedAfter`, `publishedBefore`) are used. The date-filtered query path bypasses the count query or header construction logic, causing clients to lose pagination metadata. Fixes ACME-510.

## Files to Modify
- `src/api/v2/advisories.rs` (or equivalent endpoint handler) -- ensure the date-filtered query path executes the count query and passes the result to the pagination header builder
- `src/api/pagination.rs` (or equivalent pagination utility) -- if the header construction function needs to be called from the filtered path, verify it handles date-filtered counts correctly

## Implementation Notes
The root cause is that the advisories endpoint handler has two code paths: one for unfiltered requests (which correctly sets pagination headers) and one for date-filtered requests (which skips the count query or header construction).

The fix must ensure that when `publishedAfter` and/or `publishedBefore` query parameters are present:

1. A count query is executed against the same filtered dataset to determine the total number of matching advisories.
2. The count result is passed to the pagination header helper function that sets `X-Total-Count` and builds the `Link` header.
3. The response includes both headers before being returned to the client.

**Approach**: Locate the branch in the advisories handler where date filter parameters cause divergence from the standard pagination flow. Unify the two paths so that pagination header construction is applied regardless of whether date filters are present. If the filtered and unfiltered paths use different query builder functions, ensure both return or make available the total count.

**Existing patterns**: The unfiltered query path already demonstrates the correct pattern for pagination header construction. Follow the same sequence for the filtered path: execute count query, call pagination header helper, set headers on the response.

No CONVENTIONS.md is present in the repository.

No data migration is needed -- pagination headers are computed at query time and are not persisted.

## Acceptance Criteria
- [ ] A reproducer test calls `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` with test data containing more than 10 matching advisories, and asserts that the response includes `X-Total-Count` header with the correct total and `Link` header with `rel="next"` -- this test must fail before the fix and pass after
- [ ] The `GET /api/v2/advisories` endpoint returns `X-Total-Count` and `Link` pagination headers when date range filter parameters (`publishedAfter`, `publishedBefore`) are provided
- [ ] Non-filtered requests to `GET /api/v2/advisories` continue to return pagination headers correctly (no regression)
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: integration test calling `GET /api/v2/advisories` with `publishedAfter` and `publishedBefore` query parameters and a `limit` smaller than the total matching count. Assert: (1) `X-Total-Count` header is present and its value equals the total number of advisories matching the date filter; (2) `Link` header is present and contains a `rel="next"` entry when more pages exist. Before the fix, this test should fail because the headers are absent. After the fix, the test should pass.
- [ ] Regression test: verify that `GET /api/v2/advisories` without date filter parameters still returns `X-Total-Count` and `Link` headers correctly
- [ ] Edge case test: verify pagination headers when date filters match exactly the page limit (no `Link: rel="next"` expected) and when date filters match zero results (`X-Total-Count: 0`, no `Link` header)

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start the backend service locally, call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`, inspect response headers.
- **Expected Result**: Response includes `X-Total-Count: <n>` header with total matching advisories and `Link: <url>; rel="next"` header when more pages exist.
- **Actual Result**: Response body contains correct filtered advisories, but `X-Total-Count` and `Link` headers are absent. Non-filtered requests return pagination headers correctly.
- **Root Cause**: The date-filtered query path in the advisories endpoint handler bypasses the count query or pagination header construction logic that the unfiltered path uses correctly. The data query applies filters properly (correct body), but the total count is not computed or propagated to the header builder when date range parameters are present.
