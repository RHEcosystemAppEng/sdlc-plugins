# Repository Impact Map — TC-9002: Improve Search Experience

## Feature Ambiguities Identified

The feature description for TC-9002 is vague and underspecified in several critical areas.
The following ambiguities were identified and resolved with reasonable technical defaults
for planning purposes. These interpretations should be confirmed with the product owner
before implementation begins.

1. **"Search should be faster"** — No quantitative performance target provided (e.g.,
   p95 latency under 200ms, maximum query time). Interpreted as: add PostgreSQL
   full-text search indexes (`tsvector` columns with GIN indexes) to replace naive
   `LIKE`/`ILIKE` pattern matching in the `SearchService`, which is the most common
   cause of slow search in PostgreSQL-backed systems.

2. **"Results should be more relevant"** — No definition of "relevance" or ranking
   criteria specified (no weighting scheme, no boosting rules, no field priorities).
   Interpreted as: implement PostgreSQL native full-text search using
   `tsvector`/`tsquery` with `ts_rank` relevance scoring, which ranks results by
   term frequency and proximity instead of simple substring matching.

3. **"Add filters"** — No specification of which filters, which entity fields are
   filterable, or the filter interaction model (AND/OR). Interpreted as: add query
   parameter-based filtering to the `GET /api/v2/search` endpoint for common entity
   fields — entity type (sbom, advisory, package), severity (for advisories), and
   license (for packages) — using the existing `common/src/db/query.rs` filter
   builder pattern.

4. **"Should be fast enough"** — Non-functional requirement with no measurable
   threshold. Interpreted as: search queries must complete within acceptable limits
   after indexing is in place; verify with integration tests that performance does
   not regress.

5. **"Don't break existing functionality"** — Standard backward compatibility
   requirement. Interpreted as: existing `GET /api/v2/search` endpoint contract
   must remain backward-compatible; new filter parameters are additive (optional)
   and do not change existing response shapes.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add PostgreSQL full-text search database migration with tsvector columns and GIN indexes for sbom, advisory, and package entities
    - Refactor SearchService to use tsvector/tsquery full-text search with ts_rank relevance ranking instead of LIKE-based pattern matching
    - Add filter query parameters (entity_type, severity, license) to GET /api/v2/search endpoint with filter builder integration
    - Update search integration tests for full-text search, relevance ranking, filters, and backward compatibility
```

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present:

- **No coordinated schema migrations:** The migration adds new `tsvector` columns and
  GIN indexes without modifying existing columns or constraints. The migration can
  land independently — existing code continues to work because the new columns are
  populated by triggers and are not read until the SearchService refactor merges.
- **No breaking API changes:** The search endpoint changes are additive — new optional
  query parameters (`entity_type`, `severity`, `license`) do not alter the existing
  response shape or break existing API consumers.
- **No cross-cutting refactors:** Changes are confined to the search module and its
  supporting infrastructure (migration, entity definitions, query helpers). No
  rename or module reorganization spans multiple tasks.
- **No tightly coupled components:** All changes are in a single repository
  (trustify-backend). Each task can be merged independently without leaving `main`
  in a broken state.

No atomicity indicators were identified. Tasks will be created directly under the Feature.
