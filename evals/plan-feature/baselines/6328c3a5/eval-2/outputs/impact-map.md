# Repository Impact Map — TC-9002: Improve search experience

## trustify-backend

changes:
  - Add database indexes on search-relevant columns to improve query performance (migration)
  - Implement relevance ranking/scoring in SearchService for more meaningful result ordering
  - Add filter query parameters to the search endpoint (entity type, date range, severity)
  - Update search integration tests to cover new filtering and relevance behavior

## Ambiguities

The feature description is underspecified in several areas. The following ambiguities were identified and must be clarified with the product owner before or during implementation:

1. **No performance baseline or targets for "Search should be faster"** — The requirement states search is "currently too slow" but provides no response time measurements, no target latency (e.g., P95 < 200ms), and no load profile. It is unclear whether the bottleneck is database queries, application logic, or network. **Assumption pending clarification:** the primary bottleneck is unindexed database queries, and adding GIN indexes for full-text search columns will address the performance concern.

2. **No definition of "relevant" for search results** — The requirement says users complain about "irrelevant results" but provides no examples of bad results, no ranking criteria, and no definition of what makes a result relevant. It is unclear whether relevance means full-text match quality, recency, entity importance, or a combination. **Assumption pending clarification:** relevance is defined as PostgreSQL full-text search ranking (ts_rank) applied to searchable text columns.

3. **No specification of filter dimensions for "Add filters"** — The requirement says "some kind of filtering capability" but does not specify which attributes should be filterable, how filters combine (AND vs OR), or whether filters apply across entity types or within a single type. **Assumption pending clarification:** filters will include entity type (SBOM, advisory, package), date range (created/modified), and severity (for advisories). Filters combine with AND semantics.

4. **No quantitative non-functional requirements** — "Should be fast enough" provides no SLO, no percentile targets, no concurrent user load requirements. **Assumption pending clarification:** search queries should complete within 500ms at the database level under normal load.

5. **No regression baseline for "Don't break existing functionality"** — No specific existing behaviors are identified as must-preserve. No current test coverage baseline is established. **Assumption pending clarification:** existing search endpoint contract (request/response shape) is preserved; new parameters are additive.

6. **No frontend repository or design mockups for "Better UI"** — The non-MVP "Better UI" requirement cannot be decomposed into actionable tasks without a target frontend repository and design mockups.

## Excluded Requirements

| Requirement | Reason for Exclusion |
|---|---|
| Better UI (Non-MVP) | No frontend repository is in scope. No design mockups or Figma URL provided. This requirement targets a different repository domain (frontend) that is not included in the current planning scope. It cannot be planned without design input and a target frontend codebase. |

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:
- No coordinated schema migrations — the index migration (Task 1) is additive and does not break existing queries; it can land independently.
- No breaking API changes — filter parameters (Task 3) are additive query parameters; existing callers without filters continue to work.
- No cross-cutting refactors — each task modifies a distinct concern (indexing, ranking, filtering) within the search module.
- No tightly coupled components — all changes are in the backend repository with no frontend dependency.

Each task's PR can be merged to `main` independently without leaving the codebase in a broken state.

## Inherited Field Values

- **Priority:** Normal (propagated to all tasks)
- **Fix Versions:** RHTPA 1.6.0 (propagated to all tasks; `fixVersion scope` is "both" per Jira Field Defaults)
