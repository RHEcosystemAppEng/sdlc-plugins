# Steps 2-3 -- Codebase Investigation

## Bug Summary

ACME-510 reports that the `/api/v2/advisories` endpoint returns correct response bodies when filtering by date range (`publishedAfter`/`publishedBefore`), but the pagination headers (`X-Total-Count` and `Link`) are missing from the response. Non-filtered requests return pagination headers correctly.

## Investigation Approach

The investigation targets the acme-backend repository (Rust backend service) at `/home/dev/repos/acme-backend`.

### Key areas to search:

1. **Advisories endpoint handler** -- locate the route handler for `GET /api/v2/advisories` to understand how query parameters are processed.
2. **Pagination header logic** -- find where `X-Total-Count` and `Link` headers are added to responses.
3. **Date range filter code path** -- identify the code path that applies `publishedAfter`/`publishedBefore` filters and check whether it diverges from the non-filtered path before headers are set.

## Findings

### 1. Endpoint handler structure

The `/api/v2/advisories` endpoint handles date-range filtering via `publishedAfter` and `publishedBefore` query parameters. The handler likely has two code paths: one for unfiltered queries and one for filtered queries.

### 2. Pagination header generation

Pagination headers (`X-Total-Count`, `Link`) are generated based on the total count of matching records and the current page/limit parameters. The header-setting logic likely runs after the query executes.

### 3. Probable root cause location

The bug description states that non-filtered requests return pagination headers correctly, but filtered requests do not. This strongly suggests that the date-range filtering code path either:
- Skips the count query that provides the total for `X-Total-Count`, or
- Returns early before the pagination headers are appended to the response, or
- Uses a different query builder that does not compute the total count alongside the filtered results.

### 4. Reproducer feasibility

The Steps to Reproduce are clear and actionable:
1. Start backend service locally.
2. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`.
3. Inspect response headers for `X-Total-Count` and `Link`.

This can be directly translated into an integration test that asserts the presence of pagination headers on filtered advisory queries.
