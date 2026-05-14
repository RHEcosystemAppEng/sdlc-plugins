# Repository Impact Map — TC-9002: Improve Search Experience

## Ambiguities and Assumptions

The feature description (TC-9002) is vague and lacks measurable criteria. The following ambiguities have been identified and should be clarified with the product owner before implementation begins. Where assumptions have been made to unblock planning, they are labeled as such.

### Ambiguity 1: "Search should be faster" — No performance baseline or target

The requirement states search is "currently too slow" and should be "fast enough," but provides no measurable performance criteria.

- What is the current p50/p95 latency for search queries?
- What is the target latency (e.g., sub-200ms p95, sub-500ms p95)?
- Is the bottleneck in the database query layer, application logic, or network?

**Assumption (pending clarification):** The current `SearchService` in `modules/search/src/service/mod.rs` performs unoptimized text queries against PostgreSQL without proper indexing. We assume the goal is to add PostgreSQL full-text search indexing (`tsvector` columns with GIN indexes) and optimize the query path. Target latency is assumed to be under 500ms p95 for typical queries.

### Ambiguity 2: "Results should be more relevant" — No definition of relevance

The requirement says users complain about "irrelevant results" but does not define what constitutes a relevant result or how relevance should be measured.

- Which entity types should be searched (SBOMs, advisories, packages, or all)?
- Should results be ranked by a relevance score?
- What ranking factors matter (text match quality, recency, severity)?
- Are there specific user complaints or examples of poor results to reference?

**Assumption (pending clarification):** Relevance means implementing PostgreSQL full-text search ranking (`ts_rank`) across SBOMs, advisories, and packages, with results ordered by relevance score descending. The current `SearchService` likely uses basic `LIKE`/`ILIKE` queries without ranking.

### Ambiguity 3: "Add filters — some kind of filtering capability" — Filter criteria unspecified

The requirement asks for "some kind of filtering capability" without specifying:

- Which fields should be filterable (entity type, severity, date range, license, package name)?
- Should filters be combinable (AND/OR logic)?
- Should filters apply before or after full-text search?
- Are filters faceted (showing counts per filter value)?

**Assumption (pending clarification):** The MVP filter set includes: entity type (sbom, advisory, package), severity (for advisories), and date range (created_after, created_before). Filters are applied as query parameters on the search endpoint, combined with AND logic. Faceted counts are out of scope for MVP.

### Ambiguity 4: "Better UI" — Excluded from scope

The "Better UI" requirement is marked as non-MVP and cannot be planned without:

- Design mockups or Figma specifications
- A frontend repository (only `trustify-backend` is in the repository registry)

**Decision:** "Better UI" is excluded from this implementation plan. It should be planned separately once design assets and a frontend repository are available.

### Ambiguity 5: Non-functional requirements lack specificity

"Should be fast enough" and "Don't break existing functionality" are not measurable acceptance criteria.

**Assumption (pending clarification):** "Fast enough" is interpreted as the performance target in Ambiguity 1. "Don't break existing functionality" is interpreted as requiring backward-compatible API changes (existing search endpoint behavior must be preserved when no new parameters are supplied) and all existing integration tests must continue to pass.

---

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. Each task can be merged to `main` independently without breaking existing functionality:
- Task 1 adds database infrastructure (migration) that is inert until consumed by Task 2.
- Task 2 optimizes the search service using the new indexes but preserves the existing endpoint contract.
- Task 3 adds optional filter parameters that are backward compatible (no filters = same behavior).
- Task 4 adds integration tests that validate the new behavior.

No coordinated schema migrations, breaking API changes, cross-cutting refactors, or tightly coupled components require all-or-nothing delivery.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add database migration for full-text search indexes (tsvector columns and GIN indexes on sbom, advisory, and package tables)
    - Refactor SearchService to use PostgreSQL full-text search with ts_rank relevance scoring
    - Add filter query parameters (entity_type, severity, created_after, created_before) to the search endpoint
    - Add comprehensive integration tests for search performance, relevance ranking, filtering, and backward compatibility
```
