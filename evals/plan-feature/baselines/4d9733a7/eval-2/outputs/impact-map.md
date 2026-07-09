# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities

The feature description contains several ambiguous requirements that lack the specificity needed for precise implementation planning. The following ambiguities are flagged for clarification:

1. **"Search should be faster"** — No baseline performance metrics are provided. "Currently too slow" does not specify current latency, throughput, or query execution time. No target performance threshold is defined (e.g., "search should return results in under 200ms").
   - **Assumption (pending clarification):** The primary bottleneck is database query execution time, and adding PostgreSQL indexes on commonly searched text columns plus leveraging full-text search capabilities (tsvector/tsquery) will address the performance concern.

2. **"Results should be more relevant"** — No definition of "relevant" is provided. There is no ranking algorithm specification, no examples of good vs. bad search results, and no relevance scoring criteria.
   - **Assumption (pending clarification):** "Relevant" means results should be ranked by text match quality using PostgreSQL's built-in full-text search ranking functions (ts_rank/ts_rank_cd). No external search engine (e.g., Elasticsearch) or machine learning ranking is required.

3. **"Add filters — Some kind of filtering capability"** — No specification of which entity fields should be filterable, what filter operators are needed (exact match, range, contains), or whether filters should work across entity types or be entity-specific.
   - **Assumption (pending clarification):** Filters will be applied as query parameters to the existing `GET /api/v2/search` endpoint. Filter fields will include entity type (SBOM, advisory, package), date range, and severity/license fields available on the existing entity models. The existing query helper infrastructure in `common/src/db/query.rs` will be extended.

4. **"Should be fast enough"** (NFR) — No concrete latency or throughput targets. No percentile-based SLO (e.g., p99 < 500ms).
   - **Assumption (pending clarification):** Performance improvements from Task 1 (indexing) will satisfy this requirement. Specific targets should be defined by the team.

5. **"Don't break existing functionality"** (NFR) — Vague scope. Does not specify which existing functionality is critical, what constitutes "breaking", or whether backward compatibility of the search API response shape is required.
   - **Assumption (pending clarification):** The existing `GET /api/v2/search` endpoint response shape will remain backward-compatible. New filter parameters and relevance scoring will be additive (new query parameters, optional sort-by-relevance), not breaking changes.

## Excluded Requirements

| Requirement | MVP? | Reason for Exclusion |
|---|---|---|
| Better UI — "Make it look nicer" | No | No design mockups (Figma or otherwise) are available, and no frontend repository is listed in the Repository Registry. UI changes cannot be decomposed into actionable tasks without visual specifications and a target frontend codebase. |

## Impact Map

```
trustify-backend:
  changes:
    - Add database indexes on search-relevant columns and implement PostgreSQL full-text search (tsvector/tsquery) to optimize search query performance
    - Implement relevance-based result ranking using PostgreSQL ts_rank scoring in the SearchService
    - Add filtering capabilities to the search endpoint with query parameter-based filters for entity type, date range, and entity-specific fields
    - Update search integration tests to cover performance indexes, relevance ranking, and filter parameters
```

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present:
- No coordinated schema migrations — each task's migration (if any) is independently valid
- No breaking API changes — all changes are additive (new query parameters, new response fields for scoring)
- No cross-cutting refactors — tasks modify the same module but different aspects (indexes, ranking, filtering)
- Single repository — no cross-repo frontend/backend coupling since the "Better UI" requirement is excluded

Each task's PR can be merged independently to `main` without leaving the codebase in a broken state.
