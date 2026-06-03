# Repository Impact Map — TC-9002: Improve Search Experience

## Feature Ambiguities Identified

The feature description TC-9002 is underspecified in several areas. The following
ambiguities were identified and resolved with reasonable defaults for planning
purposes. These should be confirmed with the product owner before implementation
begins.

1. **"Search should be faster"** — No performance target specified (e.g., p95 latency,
   maximum query time). Interpreted as: add database indexing for full-text search
   columns and optimize the SearchService query path to reduce unnecessary joins or
   scans.

2. **"Results should be more relevant"** — No definition of "relevant" provided. No
   ranking criteria or weighting scheme specified. Interpreted as: implement
   PostgreSQL full-text search with `tsvector`/`tsquery` and relevance-based ranking
   (`ts_rank`) instead of naive `LIKE`/`ILIKE` pattern matching.

3. **"Add filters"** — No specification of which filters, what entity fields are
   filterable, or what filter UI/UX pattern to use. Interpreted as: add query
   parameter-based filtering to the search endpoint for common entity fields
   (entity type, severity for advisories, license for packages) using the existing
   `query.rs` filter builder pattern.

4. **"Should be fast enough"** — Non-functional requirement with no measurable target.
   Interpreted as: search queries should complete within acceptable limits after
   indexing; verify with integration tests that include timing assertions or at
   minimum do not regress.

5. **"Don't break existing functionality"** — Standard backward compatibility
   requirement. Interpreted as: existing `GET /api/v2/search` endpoint contract
   must remain backward-compatible; new filter parameters are optional additions.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add PostgreSQL full-text search indexes via database migration for SBOM, advisory, and package entities
    - Refactor SearchService to use tsvector/tsquery full-text search with ts_rank relevance scoring instead of LIKE-based queries
    - Add filter query parameters (entity_type, severity, license) to GET /api/v2/search endpoint
    - Extend common/src/db/query.rs with full-text search filter builder helpers
    - Update search endpoint to return results sorted by relevance score by default
    - Add integration tests for new search filters, relevance ranking, and backward compatibility
```

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. All changes are confined to a
single repository (trustify-backend). The migration adds new indexes and columns
without breaking existing schema. The search endpoint changes are additive (new
optional query parameters) and backward-compatible. Each task can be merged
independently without leaving main in a broken state:
- The migration can land first (adding indexes has no effect until the service uses them)
- The query helper extensions are additive and do not change existing helper behavior
- The SearchService refactor uses the new indexes but falls back gracefully if they exist without being queried
- Filter parameters are optional and do not break existing API consumers
- Tests can be added at any point

No coordinated schema migrations, breaking API changes, cross-cutting refactors,
or tightly coupled components were identified.
