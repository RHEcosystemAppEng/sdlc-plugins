# Jira API Metadata

```
jira.create_issue(
  project_key: "ACME",
  issue_type: "Task",
  labels: ["ai-generated-jira"],
  summary: "Fix missing pagination headers for date-range-filtered advisories endpoint",
  description: <task description below>
)
```

- **Project Key**: ACME
- **Issue Type**: Task
- **Labels**: ai-generated-jira

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the `/api/v2/advisories` endpoint to return `X-Total-Count` and `Link` pagination
headers when date-range query parameters (`publishedAfter`, `publishedBefore`) are used.
Currently, the filtered code path bypasses the pagination header construction logic,
causing clients that rely on these headers to be unable to determine total pages.
Fixes [ACME-510](https://mock-jira.example.com/browse/ACME-510).

## Files to Modify
- `src/api/v2/advisories.rs` -- add count query and pagination header construction to the date-range-filtered query path

## Implementation Notes
The unfiltered advisories query path correctly computes a total count and passes it
to the pagination header builder to produce `X-Total-Count` and `Link` headers. The
date-range-filtered path must follow the same pattern:

1. When `publishedAfter` and/or `publishedBefore` query parameters are present, execute
   a companion count query that applies the same date-range filter predicates.
2. Pass the resulting count to the shared pagination header builder (the same utility
   used by the unfiltered path).
3. Ensure the `Link` header's `rel="next"` URL preserves the date-range filter parameters
   so that paginated clients continue to receive filtered results.

Look for the existing pagination utility (e.g., in `src/pagination.rs` or
`src/middleware/pagination.rs`) and reuse its `X-Total-Count` and `Link` header
construction logic. Do not duplicate the header building -- invoke the same shared
function used by the unfiltered path.

Fixes ACME-510.

## Acceptance Criteria
- [ ] A reproducer test calls `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` and asserts that `X-Total-Count` and `Link` headers are present in the response (test fails before fix, passes after)
- [ ] The `X-Total-Count` header value reflects the count of advisories matching the date-range filter, not the total unfiltered count
- [ ] The `Link` header includes a `rel="next"` entry when more pages of filtered results exist, and the URL preserves the date-range filter parameters
- [ ] Non-filtered requests continue to return pagination headers correctly (no regression)
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: call the advisories endpoint with `publishedAfter` and `publishedBefore` query parameters and a `limit` that produces multiple pages; assert that the response includes `X-Total-Count` with the correct filtered count and `Link` with `rel="next"` pointing to the next page with the same filter parameters
- [ ] Test that `X-Total-Count` matches the actual number of advisories within the specified date range, not the total unfiltered count
- [ ] Test that the `Link` header's next-page URL includes the `publishedAfter` and `publishedBefore` parameters
- [ ] Regression test: verify that unfiltered requests (no date-range parameters) still return `X-Total-Count` and `Link` headers as before

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` and inspect response headers
- **Expected Result**: Response includes `X-Total-Count` header with total matching advisories and `Link` header with `rel="next"` when more pages exist
- **Actual Result**: Response body contains correct filtered advisories but `X-Total-Count` and `Link` headers are absent; non-filtered requests return pagination headers correctly
- **Root Cause**: The date-range filtering code path bypasses the pagination header construction logic, omitting the count query that feeds the `X-Total-Count` and `Link` header builder
