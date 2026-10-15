# Step 5 -- Generated Task Description: ACME-510 Fix

**Task Summary**: Add pagination headers to date-filtered advisory listing endpoint

**Labels**: ai-generated-jira

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the `/api/v2/advisories` endpoint to include `X-Total-Count` and `Link` pagination
headers when date-range filter parameters (`publishedAfter`, `publishedBefore`) are
present in the request. Currently, pagination headers are only returned for unfiltered
advisory listings. The filtered query path bypasses the pagination header logic,
leaving clients unable to determine total result counts or navigate pages. Fixes ACME-510.

## Files to Modify
- `src/api/v2/advisories.rs` (or `src/handlers/advisories.rs`) -- add call to `add_pagination_headers()` in the filtered query branch of `list_advisories`

## Implementation Notes
The root cause is a code-path omission in the advisories endpoint handler. The endpoint
has two query paths:

1. **Unfiltered path** -- already calls `add_pagination_headers()` after executing the
   advisory query, correctly setting `X-Total-Count` and `Link` headers.
2. **Filtered path** (date-range) -- executes the filtered query and returns results
   but skips the pagination header step entirely.

**Fix approach**:
- In the filtered query branch of `list_advisories`, add a count query that applies the
  same date-range filters (`publishedAfter`, `publishedBefore`) to determine the total
  number of matching advisories.
- Pass the filtered count and pagination parameters to `add_pagination_headers()` to
  set `X-Total-Count` and build the `Link` header.
- Reuse the existing `add_pagination_headers()` utility -- do not duplicate header logic.
- Follow the same pattern used by the unfiltered path and other v2 endpoints
  (e.g., `/api/v2/vulnerabilities`, `/api/v2/sboms`).

**Reproducer test guidance** (derived from Steps to Reproduce):
- **Input**: `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`
- **Before fix (Actual Result)**: response body contains correct filtered advisories,
  but `X-Total-Count` and `Link` headers are absent.
- **After fix (Expected Result)**: response includes `X-Total-Count: <n>` with the
  total count of matching advisories, and `Link: <url>; rel="next"` when more pages exist.
- Model the reproducer test on existing advisory listing tests that verify pagination
  headers for the unfiltered case.

No persistence impact -- pagination headers are computed at query time and are not
stored in any database. No data migration is needed.

## Reuse Candidates
- `add_pagination_headers()` -- existing utility that computes and sets `X-Total-Count` and `Link` headers; already used by the unfiltered advisories path and other v2 endpoints
- `PaginationParams` -- struct holding `limit`, `offset`, and total count; reuse for the filtered path

## Acceptance Criteria
- [ ] A reproducer test calls `GET /api/v2/advisories` with `publishedAfter` and `publishedBefore` date filters and asserts that `X-Total-Count` and `Link` pagination headers are present and correct (fails before fix, passes after)
- [ ] The filtered advisories endpoint returns `X-Total-Count` header with the accurate count of date-filtered results
- [ ] The filtered advisories endpoint returns `Link` header with `rel="next"` when additional pages exist
- [ ] Existing advisory listing tests (unfiltered) continue to pass without regression
- [ ] No regression in other v2 endpoints that use `add_pagination_headers()`

## Test Requirements
- [ ] Integration test: call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` and assert `X-Total-Count` header is present with the correct count of matching advisories (reproducer test -- must fail before fix, pass after)
- [ ] Integration test: call the same filtered endpoint with data that spans multiple pages and assert `Link` header contains `rel="next"` URL
- [ ] Integration test: call the filtered endpoint with a date range matching zero advisories and assert `X-Total-Count: 0` and no `Link` header
- [ ] Verify existing unfiltered advisory listing tests still pass with pagination headers intact

## Verification Commands
- `cargo test --test advisories` -- run advisory endpoint integration tests, expect all pass including new reproducer tests
- `curl -s -D- "http://localhost:8080/api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10" | head -20` -- verify X-Total-Count and Link headers are present in the response

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start backend service, call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`, inspect response headers
- **Expected Result**: Response includes `X-Total-Count: <n>` and `Link: <url>; rel="next"` pagination headers
- **Actual Result**: Response body contains correct filtered advisories, but `X-Total-Count` and `Link` headers are absent; unfiltered requests return headers correctly
- **Root Cause**: The date-filtered query path in the advisories endpoint handler omits the call to `add_pagination_headers()` that the unfiltered path uses, so pagination headers are never set for filtered responses
