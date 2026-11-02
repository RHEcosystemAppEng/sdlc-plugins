# Root Cause Analysis: ACME-510

## Summary

The `/api/v2/advisories` endpoint does not return `X-Total-Count` and `Link`
pagination headers when date-range query parameters (`publishedAfter`,
`publishedBefore`) are used, despite returning the correct filtered result set
in the response body.

## Root Cause

The date-range filtering code path in the advisories endpoint bypasses or fails
to invoke the pagination header logic. Specifically:

1. **Non-filtered path (working)**: When no date-range filters are provided,
   the endpoint executes a COUNT query to determine total matching records,
   then passes the count to the response builder which injects `X-Total-Count`
   and computes `Link` headers.

2. **Filtered path (broken)**: When `publishedAfter` and/or `publishedBefore`
   parameters are present, the query execution takes a different branch that
   either skips the total count computation or does not propagate the count
   to the pagination header builder.

The bug is a conditional logic gap -- the pagination header injection depends
on a total count value, and the date-range filtering code path does not supply it.

## Impact

- Clients using pagination headers to iterate through filtered results cannot
  determine total pages or fetch subsequent pages via the `Link` header.
- The response body data is correct, so clients parsing the body directly are
  unaffected.
- This affects version 0.9.0 as reported.

## Severity Assessment

- **Functional impact**: Moderate -- pagination is broken only for date-range
  filtered requests; unfiltered requests work correctly.
- **User impact**: Users relying on header-based pagination (standard REST
  practice) cannot paginate filtered results.

## Fix Approach

Ensure the date-range filtering code path also executes the COUNT query (with
the same date-range WHERE clauses applied) and passes the result to the
pagination header builder. The fix should:

1. Add the total count computation to the date-range filtered query path.
2. Ensure the count query applies the same date-range filters as the data query.
3. Pass the count through to the existing pagination header builder.
