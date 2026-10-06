<!--jira
project: ACME
issueType: Task
labels: ["ai-generated-jira"]
-->

## Repository
acme-backend

## Target Branch
main

## Description
Fix the `/api/v2/advisories` endpoint to include `X-Total-Count` and `Link` pagination headers when date-range filter query parameters (`publishedAfter`, `publishedBefore`) are applied. Currently, filtered requests return the correct response body but omit pagination headers, while non-filtered requests return them correctly. The date-range filtered code path must execute the same total-count query and pagination header insertion logic as the unfiltered path.

## Files to Modify
- `src/api/v2/advisories.rs` -- ensure the date-range filtered query path computes total count and attaches pagination headers
- `src/api/pagination.rs` -- verify pagination header helper is invoked for all query paths (if pagination is a shared utility)

## Implementation Notes
The non-filtered query path already produces correct `X-Total-Count` and `Link` headers. Investigate how the unfiltered path constructs these headers and ensure the date-range filtered path follows the same pattern. The fix likely involves either:
1. Ensuring the filtered branch calls the same pagination header helper function used by the unfiltered branch.
2. Moving pagination header logic to a shared post-processing step that runs regardless of filter parameters.
3. Adding a `COUNT(*)` query with the date-range filter conditions so the total count reflects filtered results.

Look for the existing pagination header construction in the non-filtered advisories handler and reuse that logic.

## Acceptance Criteria
- [ ] Reproducer test: a test calling `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` asserts that `X-Total-Count` and `Link` headers are present in the response
- [ ] `X-Total-Count` header reflects the total number of advisories matching the date-range filter, not the unfiltered total
- [ ] `Link` header with `rel="next"` is present when more filtered results exist beyond the current page
- [ ] Non-filtered requests continue to return pagination headers correctly (no regression)
- [ ] Pagination headers are correct when date-range filters return zero results (edge case)

## Test Requirements
- [ ] Reproducer test: integration test for `GET /api/v2/advisories` with `publishedAfter` and `publishedBefore` parameters that verifies `X-Total-Count` and `Link` response headers are present and correct
- [ ] Test that `X-Total-Count` value matches the count of advisories within the specified date range
- [ ] Test that `Link` header contains correct `rel="next"` URL when filtered results span multiple pages
- [ ] Test that pagination headers are absent or correct when filtered results fit in a single page (no `rel="next"`)
- [ ] Regression test: verify non-filtered `GET /api/v2/advisories` still returns pagination headers

## Verification Commands
- `cargo test --test api_advisories -- --test-threads=1` -- run advisory endpoint integration tests
- `curl -s -D- "http://localhost:8080/api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10" | head -20` -- manually verify pagination headers are present in filtered response

## Bug Context

**Originating Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510) -- API response missing pagination headers when filtering by date range

**Steps to Reproduce**:
1. Start the backend service locally.
2. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`.
3. Inspect the response headers.

**Expected Result**:
The response should include:
- `X-Total-Count: <n>` header with the total number of matching advisories
- `Link: <url>; rel="next"` header when more pages exist

**Actual Result**:
The response body contains the correct filtered advisories, but the `X-Total-Count` and `Link` headers are absent. Non-filtered requests (without `publishedAfter`/`publishedBefore`) return pagination headers correctly.

**Root Cause Summary**:
The date-range filtering code path in the advisories endpoint bypasses the pagination header logic. When `publishedAfter` and `publishedBefore` query parameters are present, the query execution follows a branch that either skips the total count query or returns the response before pagination headers are attached.
