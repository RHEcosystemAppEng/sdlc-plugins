# Repository Impact Map — TC-9002: Improve search experience

## Ambiguity flags

The feature description (TC-9002) contains several ambiguities that must be resolved before or during implementation. These are flagged here so they are visible in every downstream task:

1. **No performance targets** — "Search should be faster" and "Should be fast enough" provide no quantitative targets (e.g., p95 latency < 200ms, indexing throughput). Tasks below assume reasonable defaults but the product owner should confirm acceptable latency SLAs.
2. **No relevance criteria defined** — "Results should be more relevant" does not specify what relevance means. Does it mean text-match ranking, recency weighting, severity-based boosting for advisories, or some combination? Tasks below assume PostgreSQL full-text search ranking (`ts_rank`) as a starting point.
3. **Filter fields unspecified** — "Add filters — Some kind of filtering capability" does not enumerate which entity fields should be filterable. Tasks below propose filtering by entity type, date range, and severity (for advisories) based on the existing data model. The product owner should confirm or extend this list.
4. **No backward compatibility constraints detailed** — "Don't break existing functionality" is noted but there is no specification of which clients consume the search API or what response shape changes would be breaking.

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified. All changes are in a single repository (trustify-backend). Search performance improvements, relevance ranking, and filter additions can each be delivered independently without leaving `main` in a broken state. Each task preserves backward compatibility with the existing `GET /api/v2/search` endpoint by adding optional parameters and improving internal behavior.

## Impact Map

```
trustify-backend:
  changes:
    - Add PostgreSQL full-text search indexes (GIN) on searchable entity fields (sbom, advisory, package) to improve search performance
    - Implement relevance ranking in SearchService using PostgreSQL ts_rank for full-text search results
    - Add filter parameters to the search endpoint (entity type, date range, severity) with query builder integration
    - Update search integration tests to cover new filtering, ranking, and performance characteristics
```
