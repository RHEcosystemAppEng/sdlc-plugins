# Repository Impact Map — TC-9002: Improve search experience

## Step 0 — Project Configuration validation
- Repository Registry, Jira Configuration (project key TC, Cloud ID, Feature issue type ID 10142), and Code Intelligence sections are present in CLAUDE.md. Validation passed.
- Eval mode: no Jira, Figma, or Serena access. The Feature was read from `feature-ambiguous.md`. The target repository structure was read from `repo-backend.md` (synthetic `trustify-backend` manifest). All Jira writes are captured as files in this directory.

## Step 1 — Feature extraction
- Title: Improve search experience
- Priority: Normal (set, not "Undefined", so it is propagated)
- Fix Versions: RHTPA 1.6.0 (non-empty, so it is propagated)
- Acceptance criteria: **none provided** in the Feature
- Figma links: none
- Documentation Considerations section: **absent**, so there are no documentation signals and no documentation task is generated
- Step 1.5 (parent link): skipped. The Feature has no parent and there is no interactive user in eval mode.

## Step 2 — Figma
No Figma URL in the arguments or the Feature description. Figma analysis skipped.

## Step 2.5 — Issue type discovery
`jira.get_project_issue_types` cannot be called in eval mode. CLAUDE.md `## Hierarchy Configuration` specifies `by-sub-feature`. See `task-creation-log.md` for the intended Epic grouping if a level-1 type exists. Otherwise the plan falls back to Feature → Task with no error.

## Step 3 — Repository analysis findings (trustify-backend)
- Search lives in `modules/search/`: `service/mod.rs` (`SearchService`, full-text search across entities) and `endpoints/mod.rs` (`GET /api/v2/search`). Tests are in `tests/api/search.rs`.
- Searchable entities: `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs`, `entity/src/package_license.rs`.
- Filterable fields that already exist: `AdvisorySummary.severity` (`modules/fundamental/src/advisory/model/summary.rs`) and `PackageSummary.license` (`modules/fundamental/src/package/model/summary.rs`).
- Reuse: `common/src/db/query.rs` (filtering, pagination, sorting), `common/src/model/paginated.rs` (`PaginatedResults<T>`), `common/src/error.rs` (`AppError`), and the `tower-http` caching config in endpoint route builders. `AdvisoryService` (`modules/fundamental/src/advisory/service/advisory.rs`) also has a `search` capability, which is a duplication risk for ranking logic.
- Migrations: `migration/src/m0001_initial/mod.rs`, registered in `migration/src/lib.rs`.
- CONVENTIONS.md exists at the repo root. Its conventions are taken from the manifest's "Key Conventions" section: Module pattern, Error handling, Endpoint registration, Response types, Query helpers, Testing, Caching.
- Documentation files: `README.md`, `CONVENTIONS.md`.
- `docs/testing-readiness.md`: **not present**, so no testing tasks are generated.
- Shared-artifact analysis: no Feature criterion depends on a shared artifact's contents. The search reads entity tables populated by the ingestor (`modules/ingestor/`). The planned indexes and ranking are read-side only, so ingestion paths do not change.
- Eval infrastructure: not applicable (no skill `SKILL.md` is modified).

## Ambiguities flagged (clarification required before or during implementation)

| # | Feature text | Ambiguity | Assumption used in plan (pending clarification) |
|---|---|---|---|
| A1 | "Search should be faster" / NFR "Should be fast enough" | No latency baseline, no target (p50/p95), no dataset size, no identified slow queries | Add indexes, push pagination into SQL, add short-lived caching. Record before/after latency in PRs. No numeric threshold is asserted until a target is defined. |
| A2 | "Search" (scope) | Unclear whether this means the unified `GET /api/v2/search`, the per-entity list endpoints (`/api/v2/sbom`, `/api/v2/advisory`, `/api/v2/package`), or `AdvisoryService` search | Scope limited to `GET /api/v2/search` (`modules/search/`) |
| A3 | "Results should be more relevant" | No definition of relevance, no examples of irrelevant results, no ranking criteria or boosts | Exact identifier match first, then PostgreSQL full-text rank. No recency, severity, or entity-type boosting. |
| A4 | "Add filters — some kind of filtering capability" | Which fields, combination semantics, and multi-value support are not specified | `type`, `severity`, `license`. AND across filters, OR within one filter. Invalid values return 400. |
| A5 | "Better UI — make it look nicer" | No design, no frontend repository, no definition of "nicer" | **Excluded** (see below) |
| A6 | NFR "Don't break existing functionality" | No regression suite or API compatibility contract is defined | Response shape stays unchanged. All new parameters are optional. Existing `tests/api/*.rs` must keep passing. |
| A7 | Caching (introduced by the plan) | Acceptable staleness for search results after ingestion is unspecified | Conservative short TTL (for example, 60s), to be confirmed |
| A8 | Feature has no acceptance criteria | Success cannot be verified against stakeholder expectations | Task-level ACs written from the assumptions above. The Feature owner should add Feature-level ACs. |

## Impact map

```
trustify-backend:
  changes:
    - Add a migration creating full-text/trigram indexes on the columns searched by SearchService (Task 1)
    - Push pagination into SQL, remove per-result follow-up queries, cap page size, and enable tower-http caching on GET /api/v2/search (Task 2)
    - Order search results by relevance (exact identifier match, then full-text rank) when a query term is given (Task 3)
    - Add optional type / severity / license filters to GET /api/v2/search, with validation, and document them in README.md (Task 4)
```

## Excluded requirements

| Requirement | MVP? | Reason it cannot be planned / missing input |
|---|---|---|
| Better UI ("Make it look nicer") | No | No Figma design or mockups were provided, and no frontend repository is registered in the Repository Registry. The target repository (`trustify-backend`) is backend-only. "Nicer" has no measurable definition. To plan it we need a design and a frontend repo entry. |
| Frontend filter controls (UI part of "Add filters") | Yes (partial) | Same missing inputs as above. Only the backend API for filters is planned (Task 4). |
| Numeric performance target (NFR "fast enough") | Yes | No baseline or target was given. Tasks record measurements but cannot assert a threshold until one is provided. |

## Step 4.5 — Workflow mode decision

**Mode: `direct-to-main`**

Rationale. No atomicity indicators were found:
1. Coordinated schema migrations: none. Task 1 adds indexes only. No other task's code requires them to compile or work correctly; they only speed it up.
2. Breaking API changes: none. All changes to `GET /api/v2/search` are additive (optional parameters, headers, default ordering). The response shape is unchanged.
3. Cross-cutting refactors: none.
4. Tightly coupled frontend/backend components: none. The plan is backend-only.

Each task can merge independently to `main` in dependency order without breaking it. All tasks use Target Branch `main`. No bookend tasks are generated.

## Inherited field values (`additional_fields`)

Applied to every created task (and every Epic, if a level-1 type exists):

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```

- priority: `Normal`, **propagated** (the Feature priority is set and is not "Undefined")
- fixVersions: `RHTPA 1.6.0`, **propagated** (the Feature has fixVersions and `fixVersion scope` is `both`)

## Generated tasks

| # | File | Title | Depends on | Digest |
|---|---|---|---|---|
| 1 | task-1-search-indexes-migration.md | Add full-text search indexes (migration) | none | see task-1-digest.md |
| 2 | task-2-search-query-caching.md | Optimize search queries and add response caching | Task 1 | see task-2-digest.md |
| 3 | task-3-search-relevance-ranking.md | Rank search results by relevance | Tasks 1, 2 | see task-3-digest.md |
| 4 | task-4-search-filters.md | Add filters to the search endpoint | Task 2 | see task-4-digest.md |

- Documentation task: **not generated**. The Feature has no Documentation Considerations section. The README update for filters is included in Task 4's Documentation Updates.
- Testing tasks: **not generated**. There is no `docs/testing-readiness.md` in the target repository.

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
