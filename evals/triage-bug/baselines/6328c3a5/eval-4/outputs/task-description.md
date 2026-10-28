# Step 5 -- Generated Task Description: ACME-510

**Task Summary**: Fix missing pagination headers on date-range-filtered advisory queries

**Labels**: ai-generated-jira

---

## Repository
acme-backend

## Target Branch
main

## Description
Fix the `/api/v2/advisories` endpoint to include `X-Total-Count` and `Link` pagination
headers when date range filter parameters (`publishedAfter`, `publishedBefore`) are used.
Currently, filtered requests return correct result bodies but omit pagination headers,
while unfiltered requests include them correctly. The filtered query path must invoke the
same pagination header generation logic used by the unfiltered path, with the filter
predicates applied to the count query. Fixes ACME-510.

## Files to Modify
- `src/api/v2/advisories.rs` (or `src/handlers/advisories.rs`) -- update the filtered query branch to invoke the pagination helper with date range filter predicates
- `src/api/pagination.rs` (or equivalent) -- ensure the pagination helper accepts and applies optional filter predicates to the count query

## Implementation Notes
The advisories endpoint handler constructs queries differently depending on whether
date range parameters are present. The unfiltered path correctly calls the pagination
helper, which:

1. Executes a count query to determine total matching records
2. Sets the `X-Total-Count` response header to the count
3. Generates `Link` headers with `rel="next"`, `rel="prev"`, etc. based on total count, offset, and limit

The filtered path (activated when `publishedAfter` and/or `publishedBefore` query
parameters are present) must be updated to:

1. Pass the date range filter predicates to the pagination helper's count query
2. Invoke the pagination helper to set response headers, just as the unfiltered path does

**Key patterns to follow**:
- Look at how the unfiltered query path calls the pagination helper and replicate that
  pattern in the filtered branch
- The pagination helper may need to accept an optional filter/predicate parameter if it
  does not already support one
- Ensure the count query uses the same WHERE clause (including date range filters) as
  the results query to produce an accurate total count

**Reproducer test guidance** (derived from Steps to Reproduce):
- **Input**: `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`
- **Before fix (Actual Result)**: Response body contains correct filtered advisories, but `X-Total-Count` and `Link` headers are absent
- **After fix (Expected Result)**: Response includes `X-Total-Count: <n>` header with total count of matching advisories and `Link: <url>; rel="next"` header when more pages exist

Fixes ACME-510.

## Acceptance Criteria
- [ ] A reproducer test calls `GET /api/v2/advisories` with `publishedAfter` and `publishedBefore` parameters and asserts that `X-Total-Count` and `Link` pagination headers are present and correct (test fails before fix, passes after fix)
- [ ] The filtered query path in the advisories endpoint invokes pagination header generation with the date range filter predicates applied to the count query
- [ ] `X-Total-Count` header reflects the total number of advisories matching the date range filter, not the total unfiltered count
- [ ] `Link` header with `rel="next"` is present when more pages of filtered results exist
- [ ] Unfiltered requests continue to return pagination headers correctly (no regression)
- [ ] No regression in existing tests

## Test Requirements
- [ ] Integration test: call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` and assert `X-Total-Count` header is present with the correct count of matching advisories
- [ ] Integration test: call the same filtered endpoint with a limit smaller than total matching results and assert `Link` header contains `rel="next"` pointing to the next page
- [ ] Integration test: call `GET /api/v2/advisories?limit=10` (no date filter) and assert pagination headers are still present (regression guard)
- [ ] Edge case test: call with date range that matches zero advisories and assert `X-Total-Count: 0` is returned with no `Link` header

## Verification Commands
- `cargo test --test advisories` -- run advisories integration tests, expect all to pass
- `curl -s -D - "http://localhost:8080/api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10" | head -20` -- inspect response headers for X-Total-Count and Link presence

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: Start backend service, call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`, inspect response headers
- **Expected Result**: Response includes `X-Total-Count: <n>` header with total matching advisories and `Link: <url>; rel="next"` header when more pages exist
- **Actual Result**: Response body contains correct filtered advisories but `X-Total-Count` and `Link` headers are absent; unfiltered requests return pagination headers correctly
- **Root Cause**: The filtered query path in the advisories endpoint handler does not invoke the pagination helper (or does not pass date range filter predicates to the count query), causing pagination headers to be omitted from filtered responses
