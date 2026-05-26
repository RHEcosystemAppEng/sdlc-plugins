# Repository Impact Map — TC-9002: Improve Search Experience

## Feature Ambiguity Notes

The feature description TC-9002 contains several ambiguous requirements that were interpreted
as follows during planning. These interpretations should be validated with the product owner
before implementation begins.

| Requirement | Ambiguity | Planning Interpretation |
|---|---|---|
| "Search should be faster" | No performance target specified | Optimize query execution by adding database indexes on commonly searched fields and implementing query result caching via `tower-http` caching middleware |
| "Results should be more relevant" | No definition of relevance | Implement weighted full-text search using PostgreSQL `ts_rank` scoring, prioritizing matches in title/name fields over description/body fields |
| "Add filters" | No filter types specified | Add filtering by entity type (SBOM, advisory, package), severity (for advisories), and date range, following the existing filter pattern in `common/src/db/query.rs` |
| "Should be fast enough" | No quantitative target | Target sub-200ms p95 response time for search queries, add query execution time logging |

## Impact Map

```
trustify-backend:
  changes:
    - Add database indexes on searchable text columns across entity tables (sbom, advisory, package) to improve query performance
    - Extend SearchService to support weighted full-text search ranking using PostgreSQL ts_rank
    - Add filter parameter support to the search endpoint (entity type, severity, date range)
    - Add filter query builders to common query helpers for reuse across search and list endpoints
    - Implement search result caching using tower-http caching middleware
    - Update search endpoint to accept filter query parameters and return paginated, ranked results
    - Add integration tests for filtered search, ranking accuracy, and performance baseline
```

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:
- No coordinated schema migrations — each index addition is independently safe
- No breaking API changes — the search endpoint changes are additive (new optional query parameters)
- No cross-cutting refactors — changes are localized to the search module and common query helpers
- No tightly coupled cross-repo components — this is a single backend repository change

Each task can be merged independently without leaving `main` in a broken state. The existing
search endpoint continues to function while individual improvements land incrementally.
