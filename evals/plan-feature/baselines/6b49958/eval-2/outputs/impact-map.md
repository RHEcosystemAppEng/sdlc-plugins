# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities and Assumptions

The feature description TC-9002 contains several ambiguities that must be flagged. The following items require clarification from the product owner before implementation can be considered complete. In the interim, assumptions are documented below so that planning can proceed.

### Ambiguity 1: No performance targets for "Search should be faster"

The requirement states search is "currently too slow" but provides no baseline measurements or target thresholds (e.g., P95 latency under 200ms, query response under 500ms for 10k documents). Without quantitative targets, it is impossible to validate whether the improvement is sufficient.

**Assumption (pending clarification):** Target search response time is P95 < 500ms for typical queries. Performance will be improved via database indexing and query optimization on the existing `SearchService` and related entity queries.

### Ambiguity 2: No definition of "relevant" for search results

"Results should be more relevant" is subjective without a ranking specification. There is no indication of what ranking signals to use (recency, text match quality, entity type priority), whether to use full-text search scoring (ts_rank), or what constitutes an "irrelevant" result.

**Assumption (pending clarification):** Relevance will be improved by implementing PostgreSQL full-text search with `ts_rank` scoring to replace any naive LIKE/ILIKE queries. Results will be ranked by text match score descending. This is a reasonable default that can be refined once product provides specific ranking criteria.

### Ambiguity 3: No specification of which filters to add

"Add filters — Some kind of filtering capability" does not specify which entity fields should be filterable, what filter types are needed (exact match, range, multi-select), or which entities the filters apply to (SBOMs, advisories, packages, or all).

**Assumption (pending clarification):** Filters will be added to the existing search endpoint (`GET /api/v2/search`) for the most commonly useful fields: entity type (sbom, advisory, package), severity (for advisories), and date range. These are inferred from the existing entity models which include severity fields on `AdvisorySummary` and timestamp fields across entities.

### Ambiguity 4: Non-quantifiable non-functional requirements

"Should be fast enough" and "Don't break existing functionality" lack measurable criteria. "Fast enough" has no threshold; "don't break existing functionality" is a general regression avoidance statement.

**Assumption (pending clarification):** "Fast enough" is interpreted as the P95 < 500ms target stated above. "Don't break existing functionality" means existing API contracts (request/response shapes, endpoint paths) must remain backward-compatible. All existing integration tests must continue to pass.

### Ambiguity 5: "Better UI" excluded from scope

The "Better UI" requirement is marked as non-MVP and cannot be planned:
- No design mockups or Figma links are provided
- No frontend repository is listed in the Repository Registry — only `trustify-backend` is in scope
- Without a frontend repository structure and UI specifications, no actionable tasks can be generated

**Decision:** "Better UI" is excluded from this implementation plan entirely. It should be planned separately once design mockups are available and a frontend repository is added to the project configuration.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add full-text search indexes to SBOM, advisory, and package entities for improved search performance
    - Refactor SearchService to use PostgreSQL full-text search (tsvector/tsquery) with ts_rank scoring for relevance ranking
    - Add filter parameters (entity type, severity, date range) to the search endpoint
    - Update search endpoint to accept and apply filter query parameters
    - Add integration tests for search performance, relevance ordering, and filter functionality
```

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. All changes target a single repository (`trustify-backend`). Each task can be merged independently without breaking `main`:
- Database index migrations are additive and do not break existing queries
- Full-text search refactoring in `SearchService` is backward-compatible (same endpoint, enhanced behavior)
- Filter parameters are additive query parameters with no breaking API changes
- No cross-repository dependencies exist (single repo in scope)
