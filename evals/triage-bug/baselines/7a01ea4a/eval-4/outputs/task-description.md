# Step 5 -- Task Description

The following Task description would be created in Jira with issue type Task,
labeled `ai-generated-jira`, and linked to ACME-510 via a "Blocks" link
(Task blocks Bug).

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix missing pagination headers (`X-Total-Count` and `Link`) on the `/api/v2/advisories` endpoint when date-range filter parameters (`publishedAfter`, `publishedBefore`) are applied. The filtered query path bypasses the count query and pagination header builder, causing clients that rely on pagination headers to fail when filtering by date range. Fixes ACME-510.

## Files to Modify
- Endpoint handler for `/api/v2/advisories` -- ensure the filtered query path invokes the count query and passes the result to the pagination header builder
- Date-range filter query builder -- add count query execution alongside the data query
- Pagination header utility integration -- ensure the header builder is called uniformly for both filtered and unfiltered paths

## Implementation Notes
The root cause is a conditional logic gap in the `/api/v2/advisories` endpoint handler. The unfiltered code path correctly performs both a data query and a count query, then passes the total count to the pagination header builder to generate `X-Total-Count` and `Link` headers. When `publishedAfter`/`publishedBefore` query parameters are present, the request is routed through a filtered code path that either skips the count query or fails to propagate the count result to the pagination header builder.

The fix should ensure that the count query and pagination header generation are applied uniformly regardless of whether filter parameters are present. Consider extracting the count + pagination logic into a shared step that executes after the data query, independent of filter branching.

**Reproducer test guidance:**
- **Trigger**: Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`
- **Before fix (Actual Result)**: Response body contains correctly filtered advisories, but `X-Total-Count` and `Link` headers are absent
- **After fix (Expected Result)**: Response includes `X-Total-Count: <n>` header with the total number of matching advisories, and `Link: <url>; rel="next"` header when more pages exist
- **Regression check**: Non-filtered requests to `/api/v2/advisories` must continue to return pagination headers correctly

Fixes [ACME-510](https://mock-jira.example.com/browse/ACME-510).

## Acceptance Criteria
- [ ] A reproducer test calls `GET /api/v2/advisories` with `publishedAfter` and `publishedBefore` query parameters and a `limit` producing multiple pages, and asserts that `X-Total-Count` and `Link` headers are present and correct (test fails before fix, passes after)
- [ ] The `/api/v2/advisories` endpoint returns `X-Total-Count` and `Link` pagination headers when date-range filter parameters are applied
- [ ] Non-filtered requests to `/api/v2/advisories` continue to return pagination headers correctly (no regression)
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` returns `X-Total-Count` header with correct total count and `Link` header with `rel="next"` when more pages exist
- [ ] Regression test: `GET /api/v2/advisories?limit=10` (without date filters) continues to return pagination headers correctly
- [ ] Edge case: filtered request with zero results returns `X-Total-Count: 0` and no `Link` header
- [ ] Edge case: filtered request where all results fit in one page returns `X-Total-Count` but no `Link: rel="next"` header

## Verification Commands
- `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` -- response should include `X-Total-Count` and `Link` headers
- `GET /api/v2/advisories?limit=10` -- response should continue to include `X-Total-Count` and `Link` headers (regression check)

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start the backend service locally, call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`, inspect response headers
- **Expected Result**: Response includes `X-Total-Count: <n>` header with total matching advisories and `Link: <url>; rel="next"` header when more pages exist
- **Actual Result**: Response body contains correct filtered advisories, but `X-Total-Count` and `Link` headers are absent; non-filtered requests return headers correctly
- **Root Cause**: The date-range filtered query path in the `/api/v2/advisories` endpoint handler bypasses the count query and pagination header builder, which are only invoked on the unfiltered code path
