## Repository
acme-backend

## Target Branch
main

## Description
Fix missing `X-Total-Count` and `Link` pagination headers on the
`GET /api/v2/advisories` endpoint when date-range query parameters
(`publishedAfter`, `publishedBefore`) are used. The pagination headers are
correctly returned for unfiltered requests but are absent when date-range
filtering is active, preventing clients from paginating filtered results.

## Files to Modify
- `src/api/v2/advisories.rs` -- Add total count computation to the date-range filtered query path and pass the count to the pagination header builder

## Implementation Notes
The non-filtered advisories query path already correctly computes a total count
and passes it to the pagination header builder that injects `X-Total-Count` and
`Link` headers. The date-range filtered path must follow the same pattern:

1. Execute a COUNT query with the same date-range WHERE clauses
   (`publishedAfter`, `publishedBefore`) applied.
2. Pass the resulting count to the existing pagination header builder.
3. Reuse the existing pagination header builder -- do not duplicate header
   construction logic.

Look at how the non-filtered path calls the count query and invokes the header
builder; replicate that flow in the date-range branch.

## Acceptance Criteria
- [ ] Reproducer test: `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` returns `X-Total-Count` and `Link` headers in the response
- [ ] `X-Total-Count` header value matches the total number of advisories within the specified date range
- [ ] `Link` header contains `rel="next"` when more pages exist beyond the current page
- [ ] `Link` header is absent (or contains only `rel="prev"`) when on the last page
- [ ] Non-filtered requests continue to return pagination headers correctly (no regression)
- [ ] Pagination headers are correct when date-range filtering returns zero results

## Test Requirements
- [ ] Reproducer test: integration test calling `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10` and asserting `X-Total-Count` and `Link` headers are present and correct
- [ ] Test that `X-Total-Count` reflects the filtered count, not the unfiltered total
- [ ] Test pagination with date-range filter across multiple pages (verify `Link` header progression)
- [ ] Test date-range filter returning zero results still includes `X-Total-Count: 0` header
- [ ] Regression test: non-filtered request still returns pagination headers

## Verification Commands
- `cargo test --test api_advisories` -- all advisory endpoint tests pass
- `curl -s -D- 'http://localhost:8080/api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10' | grep -E 'X-Total-Count|Link'` -- both headers present in response

## Bug Context

- **Bug Key**: ACME-510
- **Steps to Reproduce**:
  1. Start the backend service locally.
  2. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`.
  3. Inspect the response headers.
- **Expected Result**: Response includes `X-Total-Count: <n>` header with total matching advisories and `Link: <url>; rel="next"` header when more pages exist.
- **Actual Result**: Response body contains correct filtered advisories, but `X-Total-Count` and `Link` headers are absent. Non-filtered requests return pagination headers correctly.
- **Root Cause**: The date-range filtering code path bypasses or fails to invoke the total count computation and pagination header injection logic. The non-filtered path correctly computes the count and injects headers, but the filtered branch does not propagate the count to the header builder.
