# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities Identified

The following ambiguities in the feature description prevent fully deterministic planning. Assumptions are documented in each task where they fill in missing details.

1. **"Search should be faster" — no performance baseline or target.** The feature states search is "currently too slow" but provides no measurable baseline (current latency) or target (e.g., p95 < 200ms). Without these, "faster" is subjective. **Assumption:** performance improvements will focus on database indexing and query optimization, with before/after benchmarks captured in the PR.

2. **"Results should be more relevant" — no definition of relevance.** The feature does not define what makes a result "relevant" vs "irrelevant," does not specify ranking criteria, and does not indicate which entity types (SBOMs, advisories, packages) should be prioritized in results. **Assumption:** relevance will be improved using PostgreSQL full-text search ranking (ts_rank or ts_rank_cd) across all searchable entity types.

3. **"Add filters — Some kind of filtering capability" — no filter specification.** The feature does not specify which fields should be filterable, which entity types support filtering, what filter operators are needed (exact match, range, multi-select), or what the API contract for filter parameters should be. **Assumption:** filters will cover entity type, date range, and severity, based on fields present in existing entity models (SbomSummary, AdvisorySummary, PackageSummary).

4. **"Should be fast enough" (NFR) — no measurable target.** This non-functional requirement provides no quantifiable performance threshold. **Assumption:** "fast enough" means search response times are comparable to other list endpoints in the system.

5. **"Don't break existing functionality" (NFR) — no regression test baseline specified.** The feature does not specify what existing functionality must be preserved or how to verify it. **Assumption:** existing integration tests in `tests/api/search.rs` serve as the regression baseline.

6. **Entity scope for search improvements is unspecified.** The feature does not clarify whether search improvements apply to all searchable entities (SBOMs, advisories, packages) or a subset. **Assumption:** improvements apply to all entities currently handled by SearchService.

## Excluded Requirements

| Requirement | Reason for Exclusion |
|---|---|
| **Better UI** ("Make it look nicer", non-MVP) | Cannot be planned: no design mockups are available, and no frontend repository is present in the Repository Registry. UI improvements require design specifications and a frontend codebase to target. This requirement should be revisited when mockups are provided and a frontend repository is added to the project configuration. |

## Impact Map

```
trustify-backend:
  changes:
    - Add database indexes for search-relevant columns to improve query performance
    - Optimize SearchService query execution for faster response times
    - Add relevance ranking/scoring to search results in SearchService
    - Add filtering capabilities (entity type, date range, severity) to GET /api/v2/search endpoint
    - Update search integration tests to cover new filtering and relevance behavior
```

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators were identified:

1. **No coordinated schema migrations** — the index migration (Task 1) adds indexes only; Tasks 2 and 3 do not depend on these indexes to function correctly (they improve behavior, not prevent breakage).
2. **No breaking API changes** — the search endpoint gains optional query parameters (filters) and improved result ordering, both of which are backward-compatible additions.
3. **No cross-cutting refactors** — each task modifies the search module independently without structural reorganization.
4. **No tightly coupled components** — all changes are within a single backend repository with no frontend dependency.

Each task can be merged to `main` independently without leaving the codebase in a broken state.

## Field Inheritance

- **Priority:** `Normal` — inherited from Feature TC-9002, will be propagated to all created tasks.
- **fixVersions:** `RHTPA 1.6.0` — inherited from Feature TC-9002. No `fixVersion scope` setting found in Jira Field Defaults; defaulting to `"both"`, so fixVersions will be propagated to all created tasks.
