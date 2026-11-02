# Codebase Investigation: ACME-510

## Bug Summary

API response missing `X-Total-Count` and `Link` pagination headers when filtering
by date range on the `/api/v2/advisories` endpoint.

## Repository

- **Repository**: acme-backend
- **Role**: Rust backend service
- **Serena Instance**: serena_backend
- **Path**: /home/dev/repos/acme-backend

## Investigation Findings

### Key Observation

The bug report states that pagination headers (`X-Total-Count` and `Link`) are
returned correctly for non-filtered requests but are absent when date-range
query parameters (`publishedAfter`, `publishedBefore`) are used. This indicates
the pagination header logic is conditionally bypassed when date-range filtering
is active.

### Likely Code Path

Based on the endpoint `/api/v2/advisories` and the behavior described:

1. **Advisories endpoint handler** -- The handler for `GET /api/v2/advisories`
   parses query parameters including `publishedAfter`, `publishedBefore`, and
   `limit`.

2. **Query construction** -- When date-range parameters are present, the query
   is built with additional WHERE clauses for the date filter. The total count
   query (used to populate `X-Total-Count`) likely uses a separate code path
   that does not apply the same filtering, or the count query is skipped
   entirely when filter parameters are detected.

3. **Pagination header injection** -- The middleware or response builder that
   adds `X-Total-Count` and `Link` headers likely depends on a total count
   value being available. If the date-range filtering code path does not
   compute or propagate the total count, the header injection is skipped.

### Hypothesis

The date-range filtering likely branches into a different query execution path
that either:
- Skips the COUNT query entirely (perhaps as a performance shortcut), or
- Computes the count but does not pass it through to the response header builder,
  or
- Uses a different response builder that does not include pagination headers.

### Areas to Investigate (with Serena)

If code intelligence were available, the following symbols and files would be
investigated:

- The advisories endpoint handler (likely in `src/api/v2/advisories.rs` or similar)
- The pagination middleware or helper (responsible for `X-Total-Count` and `Link` headers)
- The query builder for date-range filtering
- Integration tests for the advisories endpoint to confirm missing test coverage
  for date-range + pagination
