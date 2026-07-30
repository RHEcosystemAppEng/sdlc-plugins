# Repository Impact Map — TC-9002: Improve search experience

## Workflow Mode

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified. The three planned changes (performance optimization, relevance scoring, filtering) are all within the `modules/search/` module of the same repository. Each improvement is independently functional and can be merged to `main` without breaking the others. No coordinated schema migrations, no breaking API changes between tasks, no cross-cutting refactors, and no tightly coupled cross-repo components.

## Priority Inheritance

- **Feature priority:** Normal (ID not available in simulation)
- **Propagation:** Priority `Normal` is inherited by all created tasks. The priority is not `"Undefined"`, so it is propagated per Step 1 / Step 6a rules.

## fixVersion Inheritance

- **Feature fixVersions:** RHTPA 1.6.0
- **fixVersion scope:** No `### Jira Field Defaults` section exists in CLAUDE.md, so the default scope `"both"` applies.
- **Propagation:** fixVersion `RHTPA 1.6.0` is inherited by all created tasks.

## Epic Grouping

- **Hierarchy Configuration:** CLAUDE.md specifies `Default epic grouping strategy: by-sub-feature`.
- **Level-1 type discovery:** Cannot be verified in simulation (no Jira API access). If a level-1 type (Epic) exists in the project, tasks would be grouped by sub-feature into Epics. If no level-1 type exists, tasks are created directly under the Feature (Feature -> Task hierarchy).

## Documentation Task

- **Documentation signals:** None. The Feature description has no "Documentation Considerations" section.
- **Action:** No documentation task generated (per constraint 1.84).

## Testing Tasks

- **Testing readiness template:** Not found. No `docs/testing-readiness.md` exists in the fixture files.
- **Action:** No testing tasks generated (per constraint 1.86).

## Ambiguities Flagged

The feature description is intentionally vague. The following ambiguities were identified and documented as assumptions pending clarification:

1. **No performance baseline or target.** "Search should be faster" and "Should be fast enough" provide no quantifiable metrics. There is no current latency measurement, no target latency, no percentile target, and no concurrent user load specification. **Assumption pending clarification:** targeting query-level optimizations (indexing, query structure) that demonstrably reduce query execution time, without a specific latency SLA.

2. **No relevance criteria defined.** "Results should be more relevant" does not specify what constitutes relevance. Is it text-match scoring? Recency weighting? Entity-type boosting? Result ordering? **Assumption pending clarification:** implementing PostgreSQL full-text search ranking (e.g., `ts_rank` or equivalent SeaORM constructs) with configurable weights as a baseline relevance mechanism.

3. **No filter specification.** "Add filters — Some kind of filtering capability" does not specify which fields to filter by, what filter types to support (exact match, range, multi-select), or which entities support filtering. **Assumption pending clarification:** adding filters for entity type (SBOM, advisory, package) and basic field matching, following the existing `common/src/db/query.rs` filter pattern.

4. **No non-functional requirements quantification.** "Should be fast enough" and "Don't break existing functionality" are subjective. No SLA, no regression test baseline, and no backward compatibility contract is specified.

5. **No search scope definition.** The feature does not clarify whether "search" refers to the existing full-text search endpoint (`GET /api/v2/search`) only, or also includes the per-entity list endpoints (e.g., `GET /api/v2/sbom`, `GET /api/v2/advisory`) which also support query parameters via `common/src/db/query.rs`. **Assumption pending clarification:** changes target the dedicated search module (`modules/search/`) and its endpoint (`GET /api/v2/search`).

## Impact Map

```
trustify-backend:
  changes:
    - Optimize search query performance in SearchService (modules/search/src/service/mod.rs)
    - Add relevance scoring/ranking to search results in SearchService (modules/search/src/service/mod.rs)
    - Add filtering capabilities to the search endpoint (modules/search/src/endpoints/mod.rs, modules/search/src/service/mod.rs)
    - Extend shared query builder helpers to support search-specific filters (common/src/db/query.rs)
    - Update search integration tests for performance, relevance, and filtering (tests/api/search.rs)
```

## Excluded Requirements

| Requirement | MVP? | Reason for Exclusion |
|---|---|---|
| Better UI — "Make it look nicer" | No | Cannot be planned: no design mockups provided, and no frontend repository is listed in the Repository Registry. This requirement requires visual design input and a frontend codebase to decompose into actionable tasks. |

## Task Creation Log — additional_fields

All tasks will be created with the following `additional_fields`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```
