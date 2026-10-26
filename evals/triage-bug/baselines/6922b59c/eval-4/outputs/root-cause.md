# Root Cause Analysis - ACME-510

## Step 4: Root Cause Determination

### Bug Summary

API response missing `X-Total-Count` and `Link` pagination headers when the `/api/v2/advisories` endpoint is called with date range filter parameters (`publishedAfter`, `publishedBefore`). Non-filtered requests return pagination headers correctly.

### Root Cause

The most likely root cause is that the date range filtering code path in the advisory listing endpoint does not compute or propagate the total count of matching records to the pagination header injection logic.

Specifically:

1. The non-filtered advisory listing path computes a total count (e.g., via a `SELECT COUNT(*)` query or by extracting the count from the query result) and passes it to the response builder, which then sets `X-Total-Count` and constructs the `Link` header.

2. The date-range-filtered path applies the `publishedAfter` and `publishedBefore` filters to the main data query but either:
   - Does not execute a corresponding count query with the same filters, or
   - Does not pass the count result to the response/header builder.

3. The response builder conditionally adds pagination headers only when a total count is available. When the count is `None` or absent, it silently omits the headers rather than raising an error.

### Impact

- Clients relying on `X-Total-Count` for progress indication or UI pagination cannot determine the total number of results when date filters are active.
- Clients relying on `Link` headers for cursor-based pagination cannot discover subsequent pages.
- The response body data is correct, so the functional impact is limited to pagination metadata consumers.

### Severity Assessment

**Medium** -- The endpoint returns correct data, but pagination metadata is missing for a specific filter combination. This affects API consumers that depend on pagination headers for navigation, which is a standard REST API contract expectation.

### Recommended Fix Approach

1. Ensure the date-range-filtered query path computes a total count of matching records (applying the same `publishedAfter`/`publishedBefore` filters to the count query).
2. Pass the computed count to the response builder so that `X-Total-Count` and `Link` headers are emitted consistently regardless of which filters are active.
3. Add test coverage for pagination headers in combination with date range filters.
