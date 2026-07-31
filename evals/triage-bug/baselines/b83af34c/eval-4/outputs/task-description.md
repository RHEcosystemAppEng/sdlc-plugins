## Repository
acme-backend

## Target Branch
main

## Description
Fix the `/api/v2/advisories` endpoint to include `X-Total-Count` and `Link` pagination
headers when date range filters (`publishedAfter`/`publishedBefore`) are applied. Currently,
the filtered query path bypasses the pagination header generation logic, causing clients
that rely on these headers to fail when using date range filtering. Fixes ACME-510.

## Files to Modify
- `src/api/v2/advisories.rs` -- add pagination header generation to the filtered query path

## Implementation Notes
The `/api/v2/advisories` endpoint handler has two code paths:

1. **Unfiltered path** (working correctly): queries all advisories, calls
   `build_pagination_headers()` to attach `X-Total-Count` and `Link` headers, returns
   the response with headers.
2. **Filtered path** (broken): when `publishedAfter`/`publishedBefore` query parameters
   are present, constructs a date-range-filtered query and returns results WITHOUT calling
   `build_pagination_headers()`.

**Fix approach**: In the filtered code path, after executing the filtered query:
1. Execute a count query for the total number of matching advisories (with the same
   date range filters applied).
2. Call `build_pagination_headers()` with the total count, current offset/page, and
   limit to generate the `X-Total-Count` and `Link` headers.
3. Attach the generated headers to the response before returning.

Follow the same pattern used by the unfiltered path -- reuse the existing
`build_pagination_headers()` utility rather than implementing header generation inline.

**Key code references**:
- `build_pagination_headers()` -- existing pagination utility that computes headers
  from total count and pagination parameters
- The unfiltered path in the advisories handler -- reference implementation showing
  correct pagination header attachment
- Existing test files for advisories endpoint (e.g., `tests/api/test_advisories.rs`)
  -- follow existing test patterns for the reproducer

No CONVENTIONS.md exists in the repository.

## Acceptance Criteria
- [ ] A reproducer test that calls `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` and asserts the presence and correctness of `X-Total-Count` and `Link` pagination headers -- this test must fail before the fix and pass after
- [ ] The filtered query path in the advisories endpoint calls `build_pagination_headers()` to generate and attach `X-Total-Count` and `Link` headers
- [ ] `X-Total-Count` reflects the total number of advisories matching the date range filter, not just the current page
- [ ] `Link` header includes `rel="next"` when additional pages of filtered results exist
- [ ] Unfiltered requests continue to return pagination headers correctly (no regression)
- [ ] No regression in existing tests

## Test Requirements
- [ ] Reproducer test: send `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` and assert that (a) `X-Total-Count` header is present and equals the total count of matching advisories, (b) `Link` header with `rel="next"` is present when more pages exist, and (c) the response body contains correctly filtered advisories. This test must fail before the fix is applied, confirming the bug, and pass after the fix.
- [ ] Regression test: verify that unfiltered `GET /api/v2/advisories?limit=10` continues to return `X-Total-Count` and `Link` pagination headers as before
- [ ] Edge case test: verify pagination headers when the filtered result set fits in a single page (no `Link` with `rel="next"` expected, but `X-Total-Count` should still be present)

## Verification Commands
- `cargo test test_advisories_filtered_pagination` -- should pass after the fix, confirming pagination headers are present on filtered requests
- `cargo test test_advisories` -- should pass, confirming no regression in existing advisory endpoint tests

## Bug Context

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510)
- **Steps to Reproduce**: 1) Start the backend service locally. 2) Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`. 3) Inspect the response headers.
- **Expected Result**: Response includes `X-Total-Count: <n>` header with total matching advisories and `Link: <url>; rel="next"` header when more pages exist.
- **Actual Result**: Response body contains correct filtered advisories, but `X-Total-Count` and `Link` headers are absent. Non-filtered requests return pagination headers correctly.
- **Root Cause**: The filtered query path (triggered by `publishedAfter`/`publishedBefore` parameters) does not call `build_pagination_headers()`, so pagination headers are omitted from filtered responses while unfiltered responses include them correctly.
