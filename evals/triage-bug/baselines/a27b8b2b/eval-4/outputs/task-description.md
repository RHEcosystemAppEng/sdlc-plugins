# Step 5 -- Generated Task Description

**Task Summary**: Fix missing pagination headers on /api/v2/advisories when date range filter is applied

**Labels**: ai-generated-jira

**Issue Type**: Task

**Link**: Blocks ACME-510 (Bug-to-Task link type: Blocks)

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the `/api/v2/advisories` endpoint to include `X-Total-Count` and `Link` pagination headers when date range filter query parameters (`publishedAfter`, `publishedBefore`) are used. Currently, these headers are only returned for unfiltered requests. The pagination header generation logic must be applied uniformly to both filtered and unfiltered query paths, and the count query must incorporate the same date range filter conditions as the main data query. Fixes ACME-510.

## Files to Modify
- Advisory endpoint handler (route handler for `GET /api/v2/advisories`) -- add pagination header generation to the filtered query path
- Pagination header generation module -- ensure the count query includes date range filter conditions when present

## Implementation Notes
The defect is in the asymmetry between the filtered and unfiltered query paths for the `/api/v2/advisories` endpoint. Non-filtered requests correctly execute a count query and set `X-Total-Count` and `Link` headers. When `publishedAfter` and/or `publishedBefore` parameters are present, the filtered query path either skips the count query or does not propagate the count to the header-setting logic.

To fix:
1. Ensure the count query is always executed, regardless of whether date range filters are applied.
2. When date range filters are present, apply the same `publishedAfter`/`publishedBefore` conditions to the count query so that `X-Total-Count` reflects the filtered total, not the unfiltered total.
3. Ensure the `Link` header with `rel="next"` is generated based on the filtered count and the current page/limit.

Reproducer test guidance (derived from Steps to Reproduce):
- **Input**: `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`
- **Before fix (Actual Result)**: Response body contains correct filtered advisories, but `X-Total-Count` and `Link` headers are absent.
- **After fix (Expected Result)**: Response includes `X-Total-Count: <n>` with the total filtered count, and `Link: <url>; rel="next"` when more pages exist.

The repository does not have a CONVENTIONS.md file, so no conventions apply.

Fixes [ACME-510](https://mock-jira.example.com/browse/ACME-510).

## Acceptance Criteria
- [ ] A reproducer test calls `GET /api/v2/advisories` with `publishedAfter` and `publishedBefore` parameters and a `limit` that results in multiple pages, and asserts the presence and correctness of `X-Total-Count` and `Link` pagination headers. This test fails before the fix and passes after.
- [ ] The `/api/v2/advisories` endpoint returns the correct `X-Total-Count` header reflecting the total number of filtered advisories when date range parameters are provided.
- [ ] The `/api/v2/advisories` endpoint returns the correct `Link` header with `rel="next"` when more filtered results exist beyond the current page.
- [ ] Non-filtered requests to `/api/v2/advisories` continue to return pagination headers correctly (no regression).
- [ ] No regression in existing tests.

## Test Requirements
- [ ] Reproducer test: Create a test that sets up advisory data with known dates, calls `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` where total filtered results exceed the limit, and asserts: (1) `X-Total-Count` header is present and equals the correct filtered count, (2) `Link` header is present with `rel="next"`, (3) response body contains the correct filtered advisories. This test must fail before the fix is applied.
- [ ] Regression test: Verify that non-filtered requests (without `publishedAfter`/`publishedBefore`) still return `X-Total-Count` and `Link` headers correctly.
- [ ] Edge case test: Verify pagination headers when the filtered result set fits within a single page (no `Link` header expected, `X-Total-Count` matches result count).

## Verification Commands
- `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` -- response should include `X-Total-Count` and `Link` headers
- `GET /api/v2/advisories?limit=10` -- response should still include pagination headers (regression check)

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start backend service, call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`, inspect response headers.
- **Expected Result**: Response includes `X-Total-Count: <n>` header with total matching advisories and `Link: <url>; rel="next"` header when more pages exist.
- **Actual Result**: Response body contains correct filtered advisories, but `X-Total-Count` and `Link` headers are absent. Non-filtered requests return pagination headers correctly.
- **Root Cause**: The pagination header generation logic in the `/api/v2/advisories` endpoint is bypassed when date range filter parameters (`publishedAfter`, `publishedBefore`) are present. The filtered query path does not execute the count query or set the pagination headers that the unfiltered path correctly handles.
