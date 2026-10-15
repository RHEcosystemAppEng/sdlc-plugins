# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities Identified

The feature description TC-9002 contains several ambiguities that prevent precise planning. The following are flagged for clarification:

1. **"Search should be faster" / "Currently too slow"** — No quantitative performance target is provided. There is no baseline latency measurement, no target SLA (e.g., p95 < 200ms), and no throughput or concurrency requirements. Without a measurable target, "faster" cannot be objectively verified.
   - **Assumption (pending clarification):** "Faster" means optimizing query performance via database indexing (GIN indexes for full-text search columns) and SeaORM query optimization. Acceptance will be validated by comparing query execution time before and after indexing.

2. **"Results should be more relevant" / "Users complain about irrelevant results"** — No definition of relevance is provided. There are no ranking criteria, no examples of current irrelevant results vs. expected relevant results, and no user stories describing specific search failures. The term "relevant" is subjective without a scoring model.
   - **Assumption (pending clarification):** "More relevant" means implementing PostgreSQL full-text search ranking (ts_rank) to order results by a computed relevance score instead of default database ordering (e.g., insertion order or primary key).

3. **"Add filters" / "Some kind of filtering capability"** — No specification of which fields to filter on, what filter types to support (exact match, range, multi-select, free-text), how filters interact with each other (AND vs. OR logic), or which entity types support which filters. "Some kind of filtering capability" is not a decomposable requirement.
   - **Assumption (pending clarification):** Filters will cover entity type (SBOM, advisory, package), date range (created/modified), and domain-specific fields (severity for advisories, license for packages), based on the existing data model. Filters will use AND logic (conjunctive).

4. **"Should be fast enough"** (Non-Functional Requirement) — This is a completely undefined acceptance threshold. No latency SLA, no throughput target, no concurrency requirements, no load profile. This NFR cannot be verified as stated.
   - **Assumption (pending clarification):** Performance will be validated by ensuring new indexes are used in query plans and that search queries complete within reasonable time under standard test database load.

5. **"Don't break existing functionality"** (Non-Functional Requirement) — No regression test baseline is established. No specific backward-compatibility criteria are defined. The existing test suite in `tests/api/search.rs` will serve as the regression baseline, but its coverage is unknown.
   - **Assumption (pending clarification):** Existing integration tests in `tests/api/search.rs` must continue to pass. New tests will be added for new functionality.

## Excluded Requirements

- **Better UI** (Non-MVP) — Cannot be planned. No design mockups are available, and no frontend repository is listed in the Repository Registry. This requirement belongs to a frontend domain that is outside the scope of the `trustify-backend` repository. Planning this requirement requires: (1) design mockups or a Figma link specifying the desired UI changes, and (2) a frontend repository with a Serena instance or accessible codebase for analysis.

## Impact Map

```
trustify-backend:
  changes:
    - Add database migration with GIN indexes on full-text search columns to improve query performance
    - Optimize SearchService queries to leverage new indexes and reduce query latency
    - Implement relevance scoring in SearchService using PostgreSQL ts_rank for result ordering
    - Update search endpoint response to include relevance scores
    - Add query parameter filters (entity type, date range, severity, license) to the search endpoint
    - Extend search service to support conjunctive filter queries
    - Add integration tests for search performance, relevance scoring, and filtering
```

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. All three planned changes (indexing/performance, relevance scoring, filtering) can be delivered independently to `main` without breaking existing functionality. There are no coordinated schema migrations that require all changes to land together, no breaking API changes between tasks, no cross-cutting refactors, and no tightly coupled components that require simultaneous delivery. Each task adds new capability without removing or modifying existing API contracts.
