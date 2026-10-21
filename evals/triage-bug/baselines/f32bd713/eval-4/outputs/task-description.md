# Step 5 -- Task Description: Fix pagination headers for date-range-filtered advisory queries

## Repository
acme-backend

## Target Branch
main

## Description
Fix the `/api/v2/advisories` endpoint to include `X-Total-Count` and `Link` pagination
headers when date range filter parameters (`publishedAfter`, `publishedBefore`) are
present. Currently, the filtered query path bypasses the pagination header generation
logic, causing clients to receive correct filtered results without pagination metadata.
Fixes ACME-510.

## Files to Modify
- `src/api/v2/advisories.rs` (or equivalent endpoint handler) -- wire the filtered query path into the existing pagination header generation logic
- `src/db/advisories_query.rs` (or equivalent query module) -- ensure the filtered database query returns a total count alongside filtered results

## Implementation Notes
The unfiltered code path for `GET /api/v2/advisories` already correctly invokes the
pagination header utility that sets `X-Total-Count` and `Link` headers. The fix should
reuse this existing pagination logic rather than implementing a separate mechanism.

Specifically:
1. Locate the endpoint handler for `GET /api/v2/advisories` and identify the branch
   that handles `publishedAfter`/`publishedBefore` query parameters.
2. In the filtered query path, ensure the database query returns a total count of
   matching records (the unfiltered path already does this -- follow the same pattern).
3. After obtaining the filtered results and total count, call the same pagination
   header generation function used by the unfiltered path to set `X-Total-Count`
   and `Link` headers on the response.
4. The `Link` header should follow RFC 5988 format with `rel="next"` when more pages
   exist beyond the requested limit.

The reproducer test should:
- Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`
- Assert `X-Total-Count` header is present and contains the correct integer count
- Assert `Link` header with `rel="next"` is present when total results exceed the limit
- Verify the response body still contains correctly filtered advisories

Fixes ACME-510.

## Acceptance Criteria
- [ ] Reproducer test: a test calling `GET /api/v2/advisories` with `publishedAfter` and `publishedBefore` parameters demonstrates that `X-Total-Count` and `Link` pagination headers are present in the response (test fails before fix, passes after)
- [ ] The `/api/v2/advisories` endpoint returns `X-Total-Count` header with the correct total count when date range filters are applied
- [ ] The `/api/v2/advisories` endpoint returns `Link` header with `rel="next"` when filtered results exceed the requested limit
- [ ] Non-filtered requests to `/api/v2/advisories` continue to return pagination headers correctly (no regression)
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` -- assert `X-Total-Count` header is present and correct, assert `Link` header with `rel="next"` is present when more pages exist, assert response body contains correctly filtered advisories
- [ ] Test that `X-Total-Count` reflects the total filtered count, not the page size
- [ ] Test that `Link` header is absent when all filtered results fit within the limit (no next page)
- [ ] Test that combining date range filters with other query parameters (if any) also produces correct pagination headers

## Verification Commands
- `cargo test advisories` -- run advisory-related tests, expect all to pass including the new reproducer test
- `curl -s -D- "http://localhost:8080/api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10" | head -20` -- manually verify `X-Total-Count` and `Link` headers are present in the response

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start the backend service locally; call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`; inspect the response headers.
- **Expected Result**: Response includes `X-Total-Count: <n>` header with total matching advisories and `Link: <url>; rel="next"` header when more pages exist.
- **Actual Result**: Response body contains correct filtered advisories but `X-Total-Count` and `Link` headers are absent. Non-filtered requests return pagination headers correctly.
- **Root Cause**: The date range filtering code path in the `/api/v2/advisories` endpoint bypasses the pagination header generation logic. The filtered query returns correct results but does not invoke the pagination header utility that sets `X-Total-Count` and `Link` headers.

---

```
jira.create_issue(
  project: "ACME",
  summary: "Fix pagination headers for date-range-filtered advisory queries",
  description: <task description above>,
  issue_type: "Task",
  additional_fields: { "labels": ["ai-generated-jira"] }
)
```
