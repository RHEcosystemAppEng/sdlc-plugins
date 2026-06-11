# Repository Impact Map — TC-9002: Improve Search Experience

## Ambiguity Assessment

The feature description TC-9002 contains significant ambiguity that was resolved with reasonable defaults based on the codebase analysis. The following assumptions were made:

1. **"Search should be faster"** — Interpreted as: add database indexing for full-text search columns, optimize the `SearchService` query execution, and consider adding caching to the search endpoint. No specific latency target was provided; the goal is measurable improvement over the current implementation.

2. **"Results should be more relevant"** — Interpreted as: implement ranked/scored search results using PostgreSQL full-text search ranking functions (e.g., `ts_rank`), and ensure search covers the key fields across SBOMs, advisories, and packages (name, description, identifiers).

3. **"Add filters"** — Interpreted as: add query parameter-based filtering to the search endpoint, supporting filtering by entity type (SBOM, advisory, package), severity (for advisories), and date range. This leverages the existing `query.rs` filtering infrastructure in `common/src/db/`.

4. **"Should be fast enough"** — No quantitative NFR defined. Interpreted as: search responses should complete within acceptable API response times, aided by proper indexing and query optimization.

## Impact Map

```
trustify-backend:
  changes:
    - Add database migration for full-text search indexes (GIN indexes on searchable columns across sbom, advisory, and package tables)
    - Extend SearchService to support ranked full-text search using PostgreSQL ts_rank and ts_vector
    - Add filtering parameters to GET /api/v2/search endpoint (entity type, severity, date range)
    - Add filter structs and query builder integration for search filters using existing common/src/db/query.rs patterns
    - Add search result scoring/ranking to the search response model
    - Add caching headers to the search endpoint using existing tower-http caching middleware
    - Update integration tests in tests/api/search.rs to cover filtering, ranking, and performance
```

## Workflow Mode

**Mode: `direct-to-main`**

**Rationale:** No atomicity indicators are present. Each change can be delivered incrementally without leaving `main` in a broken state:
- The migration adds indexes which are backward-compatible additions
- Service changes extend existing functionality without breaking the current API contract
- New filter parameters are additive (existing queries without filters continue to work)
- Each task can be merged independently and the search endpoint remains functional at every step
