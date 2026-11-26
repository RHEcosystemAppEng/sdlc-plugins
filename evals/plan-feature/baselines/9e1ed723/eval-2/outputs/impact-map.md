# Repository Impact Map — TC-9002: Improve search experience

> In a live run this would be posted to TC-9002 as the impact map comment, together with the workflow mode decision. In a live run, the impact map and the clarification questions below would go to the user for review before any tasks are created.

## Feature fields extracted (Step 1)

| Field | Value |
|---|---|
| Key | TC-9002 |
| Summary | Improve search experience |
| Priority | Normal (set; not "Undefined") |
| fixVersions | RHTPA 1.6.0 |
| Figma link | None |
| Documentation Considerations section | Not present, so no documentation signals and no documentation task |
| Parent issue (Step 1.5) | None. Linking skipped (eval: no interactive input) |

## Ambiguities flagged (clarification required before implementation)

The feature description is vague. None of the gaps below can be resolved from the repository, so they have to be clarified with the product owner. Tasks fill these gaps with labeled assumptions (A1–A3, B1–B3, C1–C3) that stay pending clarification.

1. **No performance target.** "Search should be faster" and the NFR "Should be fast enough" give no latency target (p50/p95), no throughput target, and no dataset size. → Task 1 measures a baseline first. The provisional target is a measurable improvement over that baseline (ASSUMPTION A2).
2. **Unclear which "search" is slow.** The Feature does not say whether the problem is the unified `GET /api/v2/search` (`modules/search/`) or the per-entity list endpoints (`/api/v2/sbom`, `/api/v2/advisory`, `/api/v2/package`), or which queries are slow. → Assumed unified search (ASSUMPTION A1).
3. **"Relevant" is undefined.** There are no examples of irrelevant results, no ranking criteria, and no expected top results for sample queries. → Assumed tiered exact > prefix > full-text rank ordering (ASSUMPTION B1).
4. **The filter specification is missing.** "Some kind of filtering capability" names no fields, operators, combination semantics, or target endpoints. → Assumed `type`, `severity`, `license` on `GET /api/v2/search` with AND semantics (ASSUMPTIONS C1–C3).
5. **"Better UI" has no design and no repository.** It has no Figma mockups, no acceptance criteria, and no frontend repository in the Repository Registry. → Excluded (see below).
6. **No acceptance criteria.** The Feature has no measurable acceptance criteria at all. Task-level criteria are derived from the assumptions and must be confirmed.
7. **"Don't break existing functionality" is unbounded.** It is interpreted as: keep the `GET /api/v2/search` request and response contract (`PaginatedResults<T>`) backward compatible, and keep the existing `tests/api/*.rs` suites green.
8. **Background is unspecified.** "Several customers have mentioned it" comes with no customer cases or tickets that could help reproduce the slowness or the relevance problems.

### Questions for the product owner
- What latency target counts as "fast enough" (for example, p95 < N ms), at what data volume, and for which example queries?
- Which search surface is in scope: unified `/api/v2/search`, per-entity list endpoints, or both?
- Can you give 3–5 example queries with the results users expect at the top?
- Which fields should be filterable (entity type, severity, license, date, others?), and with which semantics?
- Is a frontend or UI change expected in this Feature? If so, which repository, and are there Figma designs?

## Repository impact

```
trustify-backend:
  changes:
    - Measure baseline search latency and optimize the SearchService query path (database-level pagination, page-size cap) [Task 1]
    - Configure tower-http response caching on the GET /api/v2/search route [Task 1]
    - Rank search results by relevance (exact > prefix > full-text rank) with a deterministic tie-breaker [Task 2]
    - Make relevance the default search ordering while keeping explicit sort parameters [Task 2]
    - Add optional filters (type, severity, license) to GET /api/v2/search using shared query helpers [Task 3]
    - Add integration tests for performance regression, ranking order, and filters in tests/api/search.rs [Tasks 1–3]
```

Files affected (all from the repository manifest):
- `modules/search/src/service/mod.rs` (Tasks 1, 2, 3)
- `modules/search/src/endpoints/mod.rs` (Tasks 1, 2, 3)
- `tests/api/search.rs` (Tasks 1, 2, 3)
- Read and reuse only: `common/src/db/query.rs`, `common/src/model/paginated.rs`, `common/src/error.rs`, `modules/fundamental/src/advisory/model/summary.rs`, `modules/fundamental/src/package/model/summary.rs`, `modules/fundamental/src/advisory/service/advisory.rs`

### Unresolved scope item (shared-artifact consideration)
- If relevance (Task 2) or performance (Task 1) work turns out to need a precomputed search column or index (for example a `tsvector` plus a GIN index), that column becomes a shared artifact. Its producers would be the ingestion paths `modules/ingestor/src/graph/sbom/mod.rs` and `modules/ingestor/src/graph/advisory/mod.rs` (plus `modules/ingestor/src/service/mod.rs`), and it would need a new migration under `migration/src/`. Those paths are **not** in any task's Files to Modify, because the current assumptions (A3, B2) keep ranking at query time. If profiling shows a precomputed column is needed, the user must approve expanding scope, and a follow-up task must cover every ingestion path and the migration.

## Excluded requirements

| Requirement | MVP? | Reason excluded / missing input |
|---|---|---|
| Better UI ("Make it look nicer") | No | Cannot be planned. There are no Figma design mockups, no frontend repository in the Repository Registry (only trustify-backend was analyzed), and no definition of "nicer". Provide the frontend repository and designs to plan it. |

## Conventions discovered
`CONVENTIONS.md` exists at the trustify-backend root. Its key conventions (module pattern, error handling, endpoint registration, response types, query helpers, testing, caching) are all Rust `.rs` scoped. They were applied per task only when a task modifies a matching file, with `Applies:` rationales.

No `docs/testing-readiness.md` was found in the repository manifest, so no testing tasks are generated. There is also no Documentation Considerations section, so no documentation task is generated.

## Workflow mode decision (Step 4.5)

**Mode: `direct-to-main`**

Rationale. None of the atomicity indicators is present:
- No coordinated schema migrations. No migration is planned.
- No breaking API changes. All `GET /api/v2/search` changes are additive (optional parameters, default ordering) and backward compatible.
- No cross-cutting refactors.
- No tightly coupled frontend and backend components. Only the backend is in scope.

Each task can merge to `main` on its own without breaking it. Tasks 2 and 3 depend on Task 1 only because they share files and need its baseline; that is ordering, not atomicity. All tasks use Target Branch `main`, and no bookend tasks are generated.

## Epic grouping (Step 2.5 / Step 5)

Issue type discovery (`jira.get_project_issue_types`) cannot run in this offline eval. CLAUDE.md `## Hierarchy Configuration` sets `Default epic grouping strategy: by-sub-feature`. If discovery finds a level-1 (Epic) type, tasks are grouped as follows. Otherwise the plan falls back to Feature → Task without error.

| Epic summary | Tasks |
|---|---|
| TC-9002: Search performance | Task 1 |
| TC-9002: Search relevance and filtering | Task 2, Task 3 |

## Task creation log (Step 6)

Inherited fields: the Feature priority is `Normal` (set), so it is propagated. The Feature fixVersions are `RHTPA 1.6.0` and `fixVersion scope: both`, so they are propagated to tasks and Epics.

`additional_fields` applied to every created issue (Epics and Tasks):

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```

| # | Summary | File | Issue type | Parent | Target Branch | Dependencies | Digest |
|---|---|---|---|---|---|---|---|
| 1 | Search performance baseline and optimization | task-1-search-performance-baseline-and-optimization.md | Task | Epic "TC-9002: Search performance" (if Epics available) | main | — | task-1-digest.md |
| 2 | Search relevance ranking | task-2-search-relevance-ranking.md | Task | Epic "TC-9002: Search relevance and filtering" (if available) | main | Task 1 | task-2-digest.md |
| 3 | Add filters to unified search | task-3-search-filters.md | Task | Epic "TC-9002: Search relevance and filtering" (if available) | main | Task 1 | task-3-digest.md |

Description digests (also in task-N-digest.md):
- Task 1: `[sdlc-workflow] Description digest: sha256-md:271123b2fece99320254e867c8be2dbbc95d42bb7aa231a8f0cfd7a26704cdba`
- Task 2: `[sdlc-workflow] Description digest: sha256-md:21b3f50b3277e05c9fa8a517ce301c02a872134bc18cd2b13d19054a2bb0a7c5`
- Task 3: `[sdlc-workflow] Description digest: sha256-md:c7a137f4c562b9eea6393ca23e8145cec910bd0c16606b3a11913a516a147fb1`

Issue links to create (Step 6b):
- With Epics: TC-9002 "Incorporates" each Epic. Without Epics: TC-9002 "Incorporates" Tasks 1, 2, 3.
- "Depend": Task 2 depends on Task 1, and Task 3 depends on Task 1.

No `workflow:feature-branch` label is applied (direct-to-main mode).

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
