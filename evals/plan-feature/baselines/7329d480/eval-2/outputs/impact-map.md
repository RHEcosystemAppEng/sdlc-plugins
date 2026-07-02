# Impact Map: TC-9002 — Improve search experience

## Feature Summary

**Key**: TC-9002
**Summary**: Improve search experience
**Priority**: Normal
**Fix Versions**: RHTPA 1.6.0
**Workflow Mode**: direct-to-main (single repository, no atomicity constraints)

## Repositories Affected

| Repository | Role |
|---|---|
| trustify-backend | Backend search service, database, API endpoints |

## Ambiguities Identified

The feature description is underspecified in several critical areas. The following ambiguities were identified and must be clarified with the product owner before finalizing implementation:

1. **No performance baseline or target for "search should be faster."** The feature states search is "currently too slow" but provides no current latency measurements, no target response time (e.g., p95 < 200ms), and no benchmark methodology. The non-functional requirement "should be fast enough" is equally unmeasurable. **Assumption for planning**: We will add database indexes and query optimizations that improve full-text search performance; actual targets should be defined after baselining current performance.

2. **No definition of "relevant" for search result ranking.** "Results should be more relevant" lacks any specification of what relevance means — no ranking criteria, no examples of currently-irrelevant results, no user research or relevance feedback mechanism. **Assumption for planning**: We will implement PostgreSQL ts_rank-based relevance scoring using term frequency, which is a standard baseline. The ranking algorithm may need refinement once "relevant" is defined.

3. **No filter specification for "add filters."** The requirement says "some kind of filtering capability" without specifying which fields should be filterable, what filter types are needed (exact match, range, multi-select), or how filters interact with each other. **Assumption for planning**: We will add entity-type filtering (SBOM, advisory, package), severity filtering (for advisories), and date-range filtering, as these are the most commonly useful filters given the data model. Additional filters can be added once requirements are clarified.

4. **"Better UI" excluded from scope.** This non-MVP requirement cannot be planned: there is no frontend repository in the project scope (only trustify-backend), and no design mockups or UI specifications have been provided. This requirement is excluded from the current planning cycle entirely.

5. **"Don't break existing functionality" lacks scope definition.** No regression test suite or compatibility contract is specified. **Assumption for planning**: Existing API contracts (request/response shapes, status codes) will be preserved; new parameters will be additive and optional.

## MVP Scope

Based on the MVP requirements and assumptions above, the following capabilities will be delivered:

| Capability | Tasks | Assumption |
|---|---|---|
| Search performance improvement | Task 1 (indexes), Task 2 (query optimization) | Adding database indexes and relevance scoring as proxy for "faster" |
| Search result relevance | Task 2 (relevance scoring) | ts_rank-based scoring as baseline relevance algorithm |
| Search filters | Task 3 (entity-type filter), Task 4 (field-based filters) | Entity type, severity, and date range as initial filter set |
| Test coverage | Task 5 (integration tests) | Existing test patterns in tests/api/search.rs |

## Out of Scope

- **Better UI** — No frontend repository, no design mockups (non-MVP)
- **Performance benchmarking infrastructure** — No baseline defined; recommend as follow-up
- **Relevance feedback/tuning** — No definition of "relevant" provided; recommend user research

## Architecture Summary

All changes are confined to the `trustify-backend` repository. The search module (`modules/search/`) contains the SearchService and search endpoint. Performance improvements target the database layer via migrations (`migration/`). Filter and ranking changes extend the existing SearchService and endpoint, reusing shared query helpers from `common/src/db/query.rs` and the `PaginatedResults<T>` response wrapper from `common/src/model/paginated.rs`.

## Task Sequence

| Task | Title | Dependencies |
|---|---|---|
| 1 | Add database indexes for search query performance | None |
| 2 | Implement relevance scoring in SearchService | Depends on Task 1 |
| 3 | Add entity-type filter to search API | None |
| 4 | Add field-based filters to search API | Depends on Task 3 |
| 5 | Update search integration tests | Depends on Tasks 1-4 |

## Metadata Propagation

- **Priority**: Normal — propagated to all tasks
- **Fix Versions**: RHTPA 1.6.0 — propagated to all tasks
- **Labels**: ai-generated-jira — propagated to all tasks
