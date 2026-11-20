# Repository Impact Map — TC-9002: Improve search experience

> This content would be posted as a Jira comment on TC-9002 (Step 4), followed by the workflow-mode decision (Step 4.5).

## Ambiguity assessment (read first)

TC-9002 is underspecified. Every MVP requirement is stated qualitatively, with no measurable acceptance criteria:

| Requirement (from Feature) | MVP | What is missing | How this plan handles it |
|---|---|---|---|
| Search should be faster | Yes | No latency figures, no target ("fast enough"), no list of slow queries | Task 1 measures a baseline first. Task 2 optimizes against that baseline. **The absolute latency target is an open question for the PO** |
| Results should be more relevant | Yes | No examples of irrelevant results, no definition of relevance | Task 3 implements an **assumed** deterministic ranking model (exact > prefix > ts_rank > recency) that the PO must confirm |
| Add filters | Yes | "Some kind of filtering": no filter dimensions named | Task 4 implements an **assumed** filter set (`type`, `severity`, `license`) based on fields that already exist in the models. The PO must confirm it |
| Better UI | No | No Figma design, no frontend repository in scope | **Excluded** (see below) |
| NFR: "Should be fast enough" | — | Not quantified | Same open question as "faster" |
| NFR: "Don't break existing functionality" | — | — | Every task has backward-compatibility and regression criteria |

**Recommendation:** before the tasks move to implementation, the Feature owner should add measurable acceptance criteria to TC-9002 (a latency target, examples of bad results, the required filters). Each task's Acceptance Criteria includes a PO-confirmation gate so that the assumptions are not silently treated as requirements.

## Impact map

```
trustify-backend:
  changes:
    - Add tracing instrumentation and a repeatable timing baseline for GET /api/v2/search (modules/search, tests/api/search.rs)
    - Add DB indexes for searched text columns (new migration migration/src/m0002_search_indexes/mod.rs, registered in migration/src/lib.rs)
    - Paginate search results via common/src/db/query.rs and PaginatedResults<T>; enable tower-http caching on the search route
    - Rank search results by relevance (exact > prefix > full-text rank > recency, deterministic tie-break) in SearchService
    - Add type / severity / license filters to GET /api/v2/search, applied in the DB query
    - Extend tests/api/search.rs with timing, pagination, ranking, filter, and regression tests
```

Repositories analysed: `trustify-backend` (structure from the eval fixture `repo-backend.md`). No other repositories need changes.

## Excluded requirements

- **"Better UI — Make it look nicer" (non-MVP).** This cannot be planned because of missing inputs:
  1. No Figma design or mockup is linked to TC-9002, so there is no target design to implement.
  2. No frontend repository is in scope for this plan. The target repository (`trustify-backend`) is a Rust REST API with no UI code, and the Repository Registry does not list a frontend repo.
  3. "Make it look nicer" does not say which screens or elements to change.
  To plan this requirement, provide a Figma design and the frontend repository (for example, the trustify UI repository and its Serena instance).

## Open questions for the Feature owner (TC-9002)

1. What is the latency target for search (for example, p95 in ms on the representative query set, at what data volume)?
2. Which queries or entity types are slow today? Are any customer examples available?
3. What does "relevant" mean to users? Can you give examples of queries that return irrelevant results? Is the assumed model (exact ID match first, then prefix, then text rank) acceptable?
4. Which filters are needed? Is the assumed set `type`, `severity`, `license` correct? Are date ranges or other dimensions wanted? Should the filters also apply to `/api/v2/advisory` and `/api/v2/package` list endpoints?
5. Should search results be one interleaved ranked list (assumed) or grouped by entity type?

## Analysis notes

- **Code intelligence:** no Serena instances are configured. The analysis used the repository structure fixture (`repo-backend.md`). File paths in the tasks come from that structure, and column and symbol details must be confirmed by reading the code at implementation time (each task's notes say so).
- **CONVENTIONS.md:** present at the `trustify-backend` root. The convention sections referenced in the tasks (§Error Handling, §Testing, §Response Types, §Query Helpers, §Caching) come from the repository's documented Key Conventions.
- **Reuse candidates found:** `common/src/db/query.rs` (filter/pagination/sort helpers), `common/src/model/paginated.rs::PaginatedResults`, `AdvisoryService::search` in `modules/fundamental/src/advisory/service/advisory.rs` (possible overlap with `SearchService`; flagged for reuse), the `AdvisorySummary.severity` and `PackageSummary.license` fields, and the `tower-http` caching setup in the existing route builders.
- **Documentation files discovered:** `README.md` and `CONVENTIONS.md`. Tasks 2–4 include a Documentation Updates entry for `README.md`, applied only if it documents the search API.
- **Documentation signals:** TC-9002 has no "Documentation Considerations" section, so no documentation task is generated.
- **Testing readiness template:** no `docs/testing-readiness.md` exists in `trustify-backend`, so no testing tasks are generated.
- **Shared-artifact analysis:** no acceptance criterion depends on a shared artifact with multiple producers. Search reads entities written by ingestion (`modules/ingestor`), but none of the changes alter ingestion. The Task 2 cache TTL is noted as a freshness consideration for newly ingested data.
- **Fail-open risks:** none are named in the Feature. Task 4 still requires that invalid or contradictory filters return 400 instead of being silently ignored.
- **Cross-cutting call sites:** the filters and pagination are scoped to the single endpoint `GET /api/v2/search` (`modules/search/src/endpoints/mod.rs`). Extending them to other list endpoints is an open question, not included.
- **Eval infrastructure:** not applicable, because no task modifies a skill `SKILL.md`.

---

## Workflow mode decision (Step 4.5)

**Selected mode: `direct-to-main`**

Rationale. Each atomicity indicator was evaluated:

1. **Coordinated schema migrations:** none. The only migration (Task 2) adds indexes only. It is additive and no other task's code requires it to be present to compile or run correctly (Task 3 benefits from the indexes but works without them).
2. **Breaking API changes:** none. All `GET /api/v2/search` changes are additive: optional `offset`/`limit`, optional filter parameters, and an optional `score` field. Callers that send no new parameters keep working.
3. **Cross-cutting refactors:** none. The changes are confined to `modules/search`, one new migration, and tests.
4. **Tightly coupled frontend/backend components:** none. Only the backend is in scope, and the UI requirement is excluded.

Each task PR leaves `main` working. Tasks are ordered by dependency links (1 → 2 → 3 → 4) to sequence edits to `SearchService`, not because of atomicity. All tasks use Target Branch `main`. No bookend tasks are generated, and the `workflow:feature-branch` label is not applied.

---

## Jira hierarchy and field propagation (Steps 2.5, 5, 6)

**Issue type discovery (Step 2.5).** Jira could not be queried in this eval. Assumed type-to-role mapping for project TC (to be confirmed with `jira.get_project_issue_types`):

```
Type-to-role mapping:
  Feature: Feature (ID: 10142, level: 2)
  Epic:    Epic    (ID: <discovered>, level: 1)
  Task:    Task    (ID: <discovered>, level: 0)
```

If discovery finds no level-1 type, Epics are skipped, tasks are created directly under the Feature, and "Incorporates" links go Feature → Task.

**Epic grouping:** `by-sub-feature`, taken from CLAUDE.md `## Hierarchy Configuration`. The interactive approval of the suggested groupings was skipped, and the suggested groupings below were used:

| Epic summary | Tasks |
|---|---|
| TC-9002: Search performance | Task 1, Task 2 |
| TC-9002: Search relevance | Task 3 |
| TC-9002: Search filtering | Task 4 |

**Inherited fields (Step 1 / 6a):**
- Priority: `Normal`. It is set and not "Undefined", so it **is propagated** to all Epics and Tasks.
- fixVersions: `RHTPA 1.6.0`. The Feature has a non-empty value and `fixVersion scope` is `both`, so it **is propagated** to all Epics and Tasks.

**`additional_fields` for every created Epic and Task:**

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```

**Parent linking (Step 1.5):** TC-9002 has no parent. The interactive prompt was skipped, which is the same as the user pressing Enter, so no parent link is set.

See `task-creation-log.md` for the full creation sequence, links, and digests.

---

This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
