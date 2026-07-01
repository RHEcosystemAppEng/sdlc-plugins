# Repository Impact Map — TC-9002: Improve Search Experience

## Ambiguities and Assumptions

The feature description is intentionally vague. The following ambiguities were identified and assumptions documented before planning:

### Ambiguities Flagged

1. **"Search should be faster"** — No current baseline latency provided, no target latency defined (e.g., "under 200ms for p95"). Assumption: optimize the existing full-text search query path with database indexing and query tuning. Actual performance targets should be defined by the product owner before implementation begins.

2. **"Results should be more relevant"** — No definition of what "relevant" means in this context. No ranking criteria specified (e.g., recency, severity, exact match vs fuzzy match). Assumption: implement basic relevance scoring using PostgreSQL full-text search ranking functions (ts_rank) and allow sorting by relevance score. The specific ranking algorithm should be validated with stakeholders.

3. **"Add filters"** — No specification of which fields should be filterable, what filter types are needed (text, enum, date range, etc.), or how filters compose (AND vs OR). Assumption: add filters for the common entity fields visible in the data model — entity type (SBOM, advisory, package), severity (for advisories), and date range. Filter field selection should be confirmed with the product owner.

4. **"Should be fast enough"** — Non-functional requirement has no quantified target. Assumption: search responses should complete within a reasonable timeframe for interactive use; database indexes will be the primary optimization mechanism.

5. **"Better UI"** — Marked as non-MVP in the feature description. **Out of scope**: no Figma mockups were provided, no frontend repository exists in the Repository Registry, and UI improvements cannot be planned without design specifications.

6. **Single repository scope** — Only `trustify-backend` is in the Repository Registry. Any frontend or UI changes are out of scope for this planning cycle.

### Assumptions

- The target is the existing `modules/search/` module and its `GET /api/v2/search` endpoint.
- PostgreSQL full-text search (tsvector/tsquery) is the appropriate technology for search improvements within this Rust/SeaORM backend.
- Filter parameters will be added as optional query parameters to the existing search endpoint, maintaining backward compatibility.
- All changes can be delivered incrementally without breaking existing functionality.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add full-text search indexes (GIN indexes on tsvector columns) for SBOM, advisory, and package entities to improve search performance
    - Refactor SearchService to use PostgreSQL full-text search ranking (ts_rank) for relevance-scored results
    - Add filter parameters (entity type, severity, date range) to the GET /api/v2/search endpoint
    - Update PaginatedResults or search response to include relevance score in results
    - Add database migration for GIN indexes and tsvector columns
    - Add integration tests for search filtering, relevance ranking, and performance characteristics
```

---

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:
- All changes are within a single repository (trustify-backend)
- Filter parameters are additive (optional query params) — backward compatible
- Search index and relevance improvements do not break the existing search endpoint contract
- No coordinated schema migrations that require all-or-nothing delivery
- No cross-repo dependencies (no frontend repository in scope)
- Each task can be merged independently without leaving main in a broken state

---

## Field Propagation

- **Priority:** Normal (propagated from TC-9002 to all tasks)
- **Fix Versions:** RHTPA 1.6.0 (propagated from TC-9002 to all tasks; no `fixVersion scope` restriction found in Jira Configuration)
