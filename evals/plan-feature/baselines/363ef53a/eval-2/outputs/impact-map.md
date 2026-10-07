# Repository Impact Map -- TC-9002: Improve search experience

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified. The three planned changes (performance optimization, relevance ranking, filter support) can each be merged independently without leaving `main` in a broken state:
- Performance optimization (indexes) is purely additive and does not change the API contract.
- Relevance ranking adds an optional response field; existing consumers are unaffected.
- Filter support adds optional query parameters; omitting them returns unfiltered results (backward compatible).

No coordinated schema migrations, no breaking API changes, and no tightly coupled cross-repo dependencies are present.

## Inherited Field Values

- **Priority:** Normal (inherited from TC-9002; will be propagated to all created tasks and epics)
- **Fix Versions:** RHTPA 1.6.0 (inherited from TC-9002; will be propagated to all created tasks and epics -- fixVersion scope defaults to "both" since no Jira Field Defaults section exists)

## Epic Grouping

**Strategy:** by-sub-feature (from Hierarchy Configuration in CLAUDE.md)

| Epic | Sub-feature | Tasks |
|---|---|---|
| TC-9002: Search Performance Optimization | Optimize query speed via indexes and query patterns | Task 1 |
| TC-9002: Search Relevance Improvement | Add relevance scoring and result ranking | Task 2 |
| TC-9002: Search Filter Support | Add filtering capabilities to the search endpoint | Task 3 |

## Changes

trustify-backend:
  changes:
    - Add database indexes on searchable columns for sbom, advisory, and package entities to improve query performance
    - Optimize SearchService query execution patterns to leverage indexes and reduce response latency
    - Introduce a SearchResultSummary model with relevance scoring using PostgreSQL full-text search ranking
    - Update search endpoint response to include relevance score and order results by rank
    - Add filter query parameters to GET /api/v2/search (entity_type, date range, severity)
    - Extend shared query builder helpers to support filter predicate composition
    - Add integration tests for performance, relevance ranking, and filter scenarios

## Excluded Requirements

| Requirement | MVP? | Reason for Exclusion |
|---|---|---|
| Better UI -- "Make it look nicer" | No | Cannot be planned: no design mockups or Figma URL provided, and no frontend repository is listed in the Repository Registry. This requirement requires a frontend implementation target and UI design specifications before it can be decomposed into actionable tasks. |

## Ambiguities Identified

The feature description TC-9002 contains significant ambiguities that affect planning precision. The following assumptions were made and are documented in the individual task descriptions as pending clarification:

1. **No performance targets defined.** "Search should be faster" and "should be fast enough" provide no baseline metrics, target latency, or SLA. Assumed target: search response time under 500ms for typical queries. The product owner should define specific performance requirements.

2. **No relevance criteria specified.** "Results should be more relevant" does not define what constitutes relevance, what ranking signals to use, or what constitutes an "irrelevant result." Assumed approach: PostgreSQL full-text search ranking (ts_rank). The product owner should clarify whether additional relevance signals are needed (recency, popularity, user-specific weighting).

3. **Filter types unspecified.** "Add filters -- some kind of filtering capability" does not specify which attributes to filter by, how many filters are needed, or the filter interaction model (AND vs OR). Assumed filter set: entity type, date range, severity. Assumed logic: AND semantics. The product owner should confirm the required filter set.

4. **No definition of "useful results."** The feature overview says search "doesn't return useful results" but provides no examples of problematic queries or expected vs actual results. This makes it impossible to validate whether the relevance improvements actually address the reported issue.

5. **Non-functional requirements are vague.** "Should be fast enough" and "don't break existing functionality" provide no measurable criteria. These should be converted into specific SLAs and regression test coverage requirements.

## Task Summary

| # | Task | Repository | Epic |
|---|---|---|---|
| 1 | Optimize search query performance | trustify-backend | TC-9002: Search Performance Optimization |
| 2 | Improve search result relevance ranking | trustify-backend | TC-9002: Search Relevance Improvement |
| 3 | Add search filters to the search endpoint | trustify-backend | TC-9002: Search Filter Support |
