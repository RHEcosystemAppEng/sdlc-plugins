# Repository Impact Map — TC-9002: Improve Search Experience

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. Each task can be merged independently without leaving `main` in a broken state. The search performance optimization, relevance improvements, and filter additions are additive changes that do not break existing API contracts or require coordinated delivery.

## Ambiguities Identified

The feature description TC-9002 contains several ambiguities that must be resolved before or during implementation. These are flagged below and carried into task descriptions as assumptions pending clarification.

### Ambiguity 1: No quantitative performance target for "faster" search

The requirement states "Search should be faster" and "Currently too slow" without defining measurable criteria. There is no baseline latency measurement, no target latency, and no percentile specification (p50, p95, p99). The non-functional requirement "Should be fast enough" is equally unmeasurable.

**Assumption pending clarification:** We assume the goal is to add database indexing for full-text search columns and optimize the existing query in `modules/search/src/service/mod.rs` to reduce query execution time. A measurable target (e.g., "p95 search latency under 200ms for queries against 100k records") should be agreed upon with stakeholders before implementation is considered complete.

### Ambiguity 2: No definition of "more relevant" results

The requirement states "Results should be more relevant" and "Users complain about irrelevant results" without specifying what relevance means. There is no ranking algorithm preference, no indication of which entity types matter most, no weighting criteria, and no examples of "irrelevant" results.

**Assumption pending clarification:** We assume relevance improvement means implementing PostgreSQL full-text search ranking (ts_rank) to replace any naive LIKE/ILIKE pattern matching in the current `SearchService`. Results should be ranked by text match quality. Stakeholders should provide examples of searches that return poor results so the ranking can be validated.

### Ambiguity 3: No specification for "Add filters"

The requirement states "Some kind of filtering capability" without specifying which fields should be filterable, which entities support filtering, whether filters combine with AND/OR logic, or whether filters apply to the unified search endpoint or per-entity endpoints.

**Assumption pending clarification:** We assume filters should be added to the `GET /api/v2/search` endpoint for the most common entity attributes: entity type (SBOM, Advisory, Package), severity (for advisories), and date range. Filters should combine with AND logic. Stakeholders should confirm which fields users need to filter on.

### Ambiguity 4: "Better UI" excluded from scope

The requirement "Better UI — Make it look nicer" is marked non-MVP. Furthermore, the target repository (`trustify-backend`) is a Rust backend service with no frontend code. No design mockups or Figma links are provided. No frontend repository is listed in the Repository Registry.

**Decision:** This requirement is **excluded from scope** entirely. It cannot be planned without design mockups, a frontend repository, and clarification of what "nicer" means.

### Ambiguity 5: Scope of "Don't break existing functionality"

The non-functional requirement "Don't break existing functionality" is vague. It is unclear whether this refers to API backward compatibility, data integrity during migration, or behavioral parity of existing search results.

**Assumption pending clarification:** We assume this means all existing API endpoints must continue to accept the same request parameters and return responses in the same shape (backward-compatible). New query parameters for filters should be optional with no behavior change when omitted.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add database migration for full-text search index (tsvector column + GIN index) on searchable entity fields
    - Optimize SearchService to use PostgreSQL full-text search (tsvector/tsquery) with ts_rank for relevance scoring
    - Add filter parameters (entity type, severity, date range) to the search endpoint with query builder integration
    - Add integration tests for search performance, relevance ranking, and filter combinations
```

## Excluded from Scope

- **Better UI (non-MVP):** Cannot be planned — no design mockups, no frontend repository in Registry, and requirement is non-MVP. Requires Figma designs and a frontend repository before planning.

[sdlc-workflow] Description digest: sha256-md:af43f96c967629f05abc142b200d0cabd1520e3c5d708de1ee924a2c1caf81b7
