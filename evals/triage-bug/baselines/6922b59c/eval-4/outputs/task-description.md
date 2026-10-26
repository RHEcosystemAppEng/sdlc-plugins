# Task Description - Fix pagination headers for date-range-filtered advisory queries

## Summary

Fix the `/api/v2/advisories` endpoint to return `X-Total-Count` and `Link` pagination headers when date range filter parameters (`publishedAfter`, `publishedBefore`) are used. Currently, pagination headers are only returned for non-filtered requests.

## Bug Reference

- **Bug**: [ACME-510](https://mock-jira.example.com/browse/ACME-510) -- API response missing pagination headers when filtering by date range
- **Link type**: Blocks

## Context

When calling `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`, the response body contains the correct filtered advisories but the `X-Total-Count` and `Link` pagination headers are absent. Non-filtered requests to the same endpoint return pagination headers correctly.

The root cause is that the date-range-filtered query path does not compute or propagate the total count of matching records to the pagination header builder.

## Acceptance Criteria

1. The `/api/v2/advisories` endpoint returns the `X-Total-Count` header with the correct total number of matching advisories when `publishedAfter` and/or `publishedBefore` query parameters are provided.
2. The `/api/v2/advisories` endpoint returns the `Link` header with `rel="next"` when more pages exist beyond the current result set, including when date range filters are active.
3. The total count reflects the filtered result set (i.e., only advisories matching the date range), not the unfiltered total.
4. Existing pagination behavior for non-filtered requests is unchanged.

## Implementation Notes

1. Locate the advisory listing endpoint handler for `GET /api/v2/advisories`.
2. In the date-range-filtered code path, ensure a count query is executed with the same `publishedAfter`/`publishedBefore` filters applied.
3. Pass the count result to the response/header builder so that `X-Total-Count` and `Link` headers are emitted.
4. If the count and data queries are separate, ensure both apply identical filter criteria to maintain consistency.

## Testing

- Add a test that calls `GET /api/v2/advisories` with `publishedAfter` and `publishedBefore` parameters and asserts:
  - `X-Total-Count` header is present and contains the correct count of filtered results
  - `Link` header is present with `rel="next"` when the filtered result set exceeds the page limit
  - `Link` header is absent when the filtered result set fits within a single page
- Verify that existing tests for non-filtered pagination continue to pass.

## Environment

- Product version: 0.9.0
- OS: RHEL 9.2
- Deployment: OpenShift 4.14
