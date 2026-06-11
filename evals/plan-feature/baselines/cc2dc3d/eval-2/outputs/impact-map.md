# Repository Impact Map — TC-9002: Improve Search Experience

## Ambiguities Identified

The feature description contains significant ambiguities that must be resolved before full implementation. The following are flagged for clarification:

1. **No performance targets for "faster" search.** The requirement says "currently too slow" and "should be fast enough" but provides no baseline latency measurements, target SLAs (e.g., p95 < 200ms), or methodology for measuring improvement. **Assumption (pending clarification):** Target search response time is under 500ms at p95 for typical queries. Will optimize query execution and add database indexing.

2. **No definition of "more relevant" results.** The requirement says "users complain about irrelevant results" but provides no ranking criteria, relevance scoring model, or examples of good vs bad results. **Assumption (pending clarification):** Relevance will be improved by implementing PostgreSQL full-text search with `ts_rank` scoring, replacing any naive LIKE/ILIKE pattern matching. Text-match ranking is a reasonable default until a domain-specific relevance model is defined.

3. **"Add filters" is unspecified.** "Some kind of filtering capability" does not identify which entity fields should be filterable, what filter types to support (text, date range, enum, multi-select), or which entities the filters apply to. **Assumption (pending clarification):** Filters will be added for the primary searchable entities (SBOMs, advisories, packages) on their most commonly useful fields — entity type, severity (for advisories), and date range. The existing `common/src/db/query.rs` query builder helpers will be extended to support these filters.

4. **No quantifiable non-functional requirements.** "Should be fast enough" and "don't break existing functionality" are not testable criteria. **Assumption (pending clarification):** Performance will be validated with benchmark queries against a representative dataset. Regression coverage will rely on existing integration tests in `tests/api/search.rs` plus new filter-specific tests.

5. **"Better UI" cannot be planned.** This non-MVP requirement references UI improvements but no design mockups or frontend repository are available. This is excluded from the current plan scope entirely.

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. Each task improves the search module independently — search performance optimization, relevance improvements, and filter additions can each be merged to `main` without breaking existing functionality. There are no coordinated schema migrations or breaking API contract changes between tasks.

## Impact Map

```
trustify-backend:
  changes:
    - Add database indexes on searchable text columns to improve query performance
    - Implement PostgreSQL full-text search (tsvector/tsquery) in the search service for improved relevance ranking
    - Add filter parameters (entity type, severity, date range) to the search endpoint
    - Extend query builder helpers to support the new filter types
    - Add integration tests for search performance, relevance ordering, and filter functionality
```
