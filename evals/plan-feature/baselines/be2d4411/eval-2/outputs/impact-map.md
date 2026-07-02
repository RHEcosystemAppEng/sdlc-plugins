# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities Identified

The feature description TC-9002 contains several critical ambiguities that must be resolved
before implementation. The following items are flagged as **assumptions pending clarification**
where the plan fills in missing details:

1. **No performance baseline or target metrics.** "Search should be faster" and "should be
   fast enough" provide no quantitative targets — no current latency measurements, no target
   p50/p95/p99 response times, no throughput requirements. **Assumption:** current slowness
   is due to missing database indexes on searchable columns; adding GIN indexes for full-text
   search and B-tree indexes on commonly filtered columns will address this. Target assumed
   to be sub-500ms p95 for typical search queries pending clarification from stakeholders.

2. **No definition of search relevance.** "Results should be more relevant" does not specify
   what relevance means — no ranking algorithm preference (full-text ranking, fuzzy matching,
   semantic/vector search), no examples of "irrelevant" results, no test cases defining
   expected result ordering. **Assumption:** relevance means implementing PostgreSQL full-text
   search with `tsvector`/`tsquery` and `ts_rank` scoring to replace presumed simple
   LIKE/ILIKE pattern matching. This is the most common improvement for Rust/PostgreSQL
   backends and does not require external dependencies.

3. **No specification of filter dimensions.** "Add filters — some kind of filtering
   capability" does not define which fields should be filterable, what filter types to
   support (dropdown, range, free-text), or whether filters combine with AND or OR semantics.
   **Assumption:** filters will cover entity type (SBOM, advisory, package), date range
   (created/modified), and severity (for advisories) — the most common filter dimensions for
   this domain. Filters will use AND semantics (all conditions must match).

4. **No specification of which entities search spans.** The feature does not clarify whether
   the improved search applies to SBOMs only, advisories only, packages only, or all
   entities. **Assumption:** search improvements apply to all entities served by the existing
   `SearchService` in `modules/search/`, which appears to provide cross-entity full-text
   search.

5. **"Better UI" is out of scope.** The non-MVP requirement "Better UI — Make it look nicer"
   cannot be planned: the target repository (`trustify-backend`) is a backend Rust service
   with no frontend code, no frontend repository is included in the Repository Registry, and
   no Figma mockups or design specifications are provided. This requirement is **excluded
   from the plan** entirely.

6. **"Don't break existing functionality" lacks specificity.** This non-functional
   requirement provides no specific backward compatibility constraints — no mention of API
   versioning, response shape preservation, or deprecation strategy. **Assumption:** existing
   `GET /api/v2/search` response shape (`PaginatedResults<T>`) will be preserved; new filter
   parameters will be optional query parameters with no breaking changes to existing callers.

## Workflow Mode

**Mode: direct-to-main**

**Rationale:** No atomicity indicators are present. Each task (database indexes, relevance
scoring, filter parameters) can be merged independently without leaving `main` in a broken
state. The search endpoint's existing response contract is preserved across all tasks —
new parameters are additive and optional. No coordinated schema migrations, no breaking API
changes, and no tightly coupled cross-repository dependencies.

## Impact Map

```
trustify-backend:
  changes:
    - Add database migration with GIN indexes for full-text search and B-tree indexes on commonly filtered columns (severity, created date)
    - Enhance SearchService with PostgreSQL full-text search using tsvector/tsquery and ts_rank relevance scoring
    - Add filter query parameters (entity type, date range, severity) to GET /api/v2/search endpoint with AND semantics
    - Update search integration tests to cover relevance scoring, filtering, and performance baseline assertions
```
