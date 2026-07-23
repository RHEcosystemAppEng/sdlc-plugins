# Step 4 -- Root Cause Analysis

## Root Cause Determination

### What is broken

The `/api/v2/advisories` endpoint does not return `X-Total-Count` and `Link` pagination headers when the request includes date-range filter parameters (`publishedAfter`, `publishedBefore`). The response body contains correctly filtered results, but pagination metadata is missing from the headers.

### Why it is broken

The date-range filtering code path does not execute the count query or does not pass the total count to the pagination header builder. The unfiltered code path correctly performs both a data query and a count query, then passes the count to the shared pagination header utility. When date-range filters are applied, the query path diverges and either:
- Skips the count query entirely, or
- Executes the count query but fails to propagate the result to the pagination header builder

This is a conditional logic gap: the pagination header generation is tied to the unfiltered path rather than being applied uniformly to all query paths.

### Where it is broken

- **Endpoint handler** for `/api/v2/advisories` -- the branching logic between filtered and unfiltered queries
- **Date-range filter path** -- the code that constructs and executes the filtered query without including the count query
- **Pagination header builder integration** -- the call site where `X-Total-Count` and `Link` headers are set, which is only reached on the unfiltered path

### How to verify the fix

A reproducer test should:
1. Call `GET /api/v2/advisories` with `publishedAfter` and `publishedBefore` query parameters and a `limit` that produces multiple pages
2. Assert that the response includes the `X-Total-Count` header with the correct total count of matching advisories
3. Assert that the response includes the `Link` header with a `rel="next"` relation when more pages exist
4. Verify that the response body still contains the correctly filtered advisories (no regression on filtering)

## Jira Comment (would be posted to ACME-510)

The following root cause analysis comment would be posted on ACME-510:

**Root Cause**: The `/api/v2/advisories` endpoint has separate code paths for filtered and unfiltered queries. The unfiltered path correctly invokes the count query and passes the result to the pagination header builder. The date-range filtered path (`publishedAfter`/`publishedBefore`) bypasses the count query or fails to propagate the count, causing `X-Total-Count` and `Link` headers to be absent from the response.

**Affected Files**:
- Endpoint handler for `/api/v2/advisories` (query routing and filter branching)
- Date-range filter query builder (count query omission)
- Pagination header utility integration (conditional invocation)

**Suggested Approach**: Ensure the date-range filtered query path executes the same count query as the unfiltered path and passes the total count to the pagination header builder. This may involve extracting the count + pagination logic into a shared step that runs regardless of filter parameters.

**Reproducer Strategy**: Test `GET /api/v2/advisories` with date-range filters and a pagination limit, asserting that `X-Total-Count` and `Link` headers are present and correct. Compare against the same request without filters to confirm parity.
