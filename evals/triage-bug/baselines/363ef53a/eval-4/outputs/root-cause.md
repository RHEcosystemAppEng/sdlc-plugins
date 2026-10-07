# Step 4 -- Root Cause Analysis

## Summary

The `/api/v2/advisories` endpoint is missing pagination headers (`X-Total-Count` and `Link`) when the request includes date-range filter parameters (`publishedAfter`, `publishedBefore`). Unfiltered requests return these headers correctly.

## Root Cause

The most likely root cause is that the date-range filtering code path in the advisories endpoint handler bypasses the pagination header logic. Specifically:

1. **Divergent query paths**: The handler likely has separate query construction logic for filtered vs. unfiltered requests. The unfiltered path executes a count query and passes the total to the pagination header builder, while the filtered path either skips the count query entirely or fails to propagate the count to the header-setting code.

2. **Conditional header attachment**: The code that appends `X-Total-Count` and `Link` headers to the HTTP response may be conditionally gated on a variable (e.g., `total_count`) that is only populated in the unfiltered code path. When date-range filters are applied, this variable remains unset or is `None`, and the header attachment is silently skipped.

## Impact

- **Severity**: Medium-High. Clients relying on pagination headers (e.g., for progressive loading or page navigation) cannot paginate through filtered results. The response body is correct, so data is not lost, but the UX for filtered queries is degraded.
- **Scope**: Affects any consumer of the `/api/v2/advisories` endpoint that uses date-range filters with pagination.

## Affected Version

Reported in product version 0.9.0 (RHTPA 0.9.0, released 2025-06-15).

## Recommendation

Create a fix task that:
1. Adds a reproducer test asserting pagination headers are present on date-range-filtered advisory queries.
2. Ensures the count query runs for all query paths (filtered and unfiltered) in the advisories endpoint handler.
3. Verifies that `Link` headers are correctly computed from the filtered total count.
