# Repository Impact Map — TC-9002: Improve Search Experience

## Feature Ambiguities Identified

The feature description TC-9002 contains several ambiguities that were resolved with reasonable defaults for planning purposes. In a real engagement, these would be raised with the product owner before proceeding.

| Ambiguity | What is unclear | Planning assumption |
|---|---|---|
| "Search should be faster" | No latency target specified (e.g., p95 < 200ms). No baseline measurement provided. | Add database indexing for full-text search columns and query optimization in SearchService. Introduce query-level timeouts. |
| "Results should be more relevant" | No definition of "relevant." No ranking criteria or scoring model specified. | Implement weighted full-text search scoring using PostgreSQL `ts_rank` or equivalent, prioritizing title matches over description matches. |
| "Add filters" | No filter dimensions specified (by entity type? by date? by severity? by license?). | Add filters for entity type (SBOM, advisory, package), date range, and severity (for advisories). These are the most common filtering dimensions given the data model. |
| "Better UI" | Marked as non-MVP. No Figma design provided. No specific UI improvements described. | Excluded from backend planning — this is a frontend concern marked non-MVP. |
| "Should be fast enough" | No quantitative performance requirement. | Target indexing and query optimization; add response time logging for future benchmarking. |
| "Don't break existing functionality" | Standard backward compatibility requirement — no specific concerns raised. | Ensure existing `GET /api/v2/search` endpoint remains backward compatible; new filters are optional query parameters. |

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. Each task can be merged independently without breaking main:
- Database indexing is additive (no breaking schema changes)
- Search relevance improvements are internal to SearchService
- Filter support uses optional query parameters (backward compatible)
- Each task is independently deployable and testable

## Impact Map

```
trustify-backend:
  changes:
    - Add full-text search indexes on searchable columns (sbom name/description, advisory title/description, package name) via new database migration
    - Enhance SearchService to use weighted full-text search ranking for improved result relevance
    - Add filtering support to the search endpoint (entity type, date range, advisory severity)
    - Extend common query helpers to support full-text search filtering and ranking
    - Add search result model types (SearchResult, SearchResultSummary) with relevance scores and entity type discrimination
    - Update search endpoint to accept new filter query parameters and return ranked results
    - Add integration tests for search relevance ranking, filtering, and performance
```

## Epic Grouping

**Strategy:** by-sub-feature (from Hierarchy Configuration)

| Epic | Tasks | Description |
|---|---|---|
| TC-9002: Search performance and indexing | Task 1 | Database indexing for full-text search performance |
| TC-9002: Search relevance and ranking | Tasks 2, 3 | Weighted ranking and search result models |
| TC-9002: Search filtering | Tasks 4, 5 | Filter query parameters and endpoint updates |
| TC-9002: Search integration tests | Task 6 | Integration test coverage for all search improvements |

## Fields Inherited from Feature

- **Priority:** Normal (propagated to all tasks)
- **Fix Versions:** RHTPA 1.6.0 (propagated to all tasks)
