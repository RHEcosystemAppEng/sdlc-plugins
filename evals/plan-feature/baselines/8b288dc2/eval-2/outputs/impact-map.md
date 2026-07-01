# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities and Clarifications Needed

The feature description TC-9002 contains several ambiguities that must be resolved before implementation begins. The following items are flagged for clarification:

1. **Performance targets undefined (Ambiguity):** "Search should be faster" and "Should be fast enough" lack quantifiable thresholds. What is the current search latency? What is the target latency (e.g., p95 < 200ms)? Without concrete metrics, there is no measurable acceptance criterion for "faster."

2. **Relevance criteria unspecified (Ambiguity):** "Results should be more relevant" does not define what relevance means. Should results be ranked by text match quality (TF-IDF, BM25)? Should specific fields be weighted higher (e.g., name > description)? Should fuzzy/partial matching be supported? What entities should be searchable (SBOMs, advisories, packages, or all)?

3. **Filter scope undefined (Ambiguity):** "Add filters — Some kind of filtering capability" does not specify which entity fields should be filterable, what filter types to support (text, enum, date range, severity level), or which search endpoints should accept filters. The type and number of filters affects the scope of schema and API changes.

4. **Non-functional requirements lack thresholds (Ambiguity):** "Should be fast enough" is not testable. A concrete SLA (e.g., p99 < 500ms for 10k records) is needed for performance validation.

5. **Backward compatibility scope unclear (Ambiguity):** "Don't break existing functionality" does not specify whether the existing `GET /api/v2/search` endpoint contract must remain identical or whether breaking changes with a version bump are acceptable.

6. **"Better UI" excluded from scope:** The "Better UI" requirement is marked as non-MVP and cannot be planned without design mockups or a frontend repository in the project's Repository Registry. This requirement is excluded from the current plan.

## Assumptions (Pending Clarification)

The following assumptions are made to produce a plannable scope. These must be validated with the product owner before implementation begins:

- **Assumption A1:** Performance improvement targets p95 search latency under 500ms for datasets up to 50k records. This will be validated via database query indexing and query optimization.
- **Assumption A2:** Relevance improvement means adding PostgreSQL full-text search (`tsvector`/`tsquery`) with field weighting (name fields weighted higher than description fields) to replace or augment the current search implementation.
- **Assumption A3:** Filters will be added for the primary search endpoint covering: entity type (SBOM, advisory, package), severity (for advisories), and date range (created/modified). These are the most commonly requested filter dimensions.
- **Assumption A4:** The existing `GET /api/v2/search` endpoint will maintain backward compatibility — new filter parameters will be optional query parameters that default to the current unfiltered behavior.
- **Assumption A5:** Search spans all three primary entity types: SBOMs, advisories, and packages.

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. Each task can be merged independently without leaving `main` in a broken state:
- Database indexing changes are additive (new indexes, no schema breaks)
- Search service improvements maintain the existing API contract with optional new parameters
- Filter additions use optional query parameters with backward-compatible defaults
- No cross-task data dependencies or breaking API changes exist between tasks

## Impact Map

```
trustify-backend:
  changes:
    - Add database indexes on searchable text columns to improve query performance (migration)
    - Implement full-text search using PostgreSQL tsvector/tsquery in the search service
    - Add filter parameters (entity type, severity, date range) to the search endpoint
    - Add integration tests for improved search relevance and filter functionality
```

## Priority and Fix Version Propagation

- **Priority:** Normal (inherited from TC-9002, will be propagated to all tasks)
- **Fix Versions:** RHTPA 1.6.0 (inherited from TC-9002, will be propagated to all tasks — fixVersion scope defaults to "both" since no Jira Field Defaults section exists)
