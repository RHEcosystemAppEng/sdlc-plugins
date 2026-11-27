# Repository Impact Map — TC-9002: Improve search experience

(This content is what plan-feature posts as the impact-map comment on TC-9002, followed by
the workflow-mode decision. Interactive approval of the map is assumed for this
non-interactive run.)

## Execution notes (non-interactive run)

- **Step 0 — Project Configuration:** Repository Registry, Jira Configuration (project TC,
  cloud ID, Feature type 10142), and Code Intelligence sections present. Validation passed.
- **Step 1 — Feature fetched (from fixture):** TC-9002, priority `Normal`,
  fixVersions `[RHTPA 1.6.0]`. No Figma links. No "Documentation Considerations" section
  (no documentation signals). No Acceptance Criteria section.
- **Step 1.5 — Parent link:** Feature has no parent; the optional prompt was skipped
  (no user available) — no parent link set.
- **Step 2 — Figma:** no Figma URL in arguments or description — skipped.
- **Step 2.5 — Issue types:** Jira not contacted in this run, so `get_project_issue_types`
  could not be executed. Documented choice: graceful degradation to Feature → Task hierarchy
  (no Epics created). If the live project exposes a level-1 type, the configured
  `Default epic grouping strategy: by-sub-feature` would apply with three groups matching
  the three tasks (Search performance / Search relevance / Search filters).
- **Step 3 — Repository analysis:** No Serena instance configured; analysis performed on the
  `trustify-backend` structure manifest (repo-backend.md). `CONVENTIONS.md` exists at the
  repo root; its conventions (as summarized in the manifest "Key Conventions") were applied
  with file-type applicability checks. No `docs/testing-readiness.md` exists → no testing
  tasks. Not a skill/SKILL.md change → no eval coverage propagation.

## Ambiguities flagged (clarification requested from Feature owner)

The Feature description is too vague to plan without assumptions. Each item below is
carried into the relevant task as a labeled ASSUMPTION pending clarification.

| # | Ambiguity in TC-9002 | Why it blocks precise planning | Assumption used (task) |
|---|---|---|---|
| 1 | "Search should be faster" / NFR "Should be fast enough" — no baseline, no target latency, no dataset size | No measurable acceptance criterion; cannot verify "done" | Measurably faster than recorded baseline on the same dataset; index used in query plan (Task 1, A3) |
| 2 | Which "search"? Unified `GET /api/v2/search` vs. per-entity list endpoints (`/api/v2/sbom`, `/api/v2/advisory`, `/api/v2/package`) | Determines which modules change | Unified search endpoint only, `modules/search/` (Task 1, A1) |
| 3 | Root cause of slowness unknown (no profiling data) | Fix could be indexing, query shape, caching, or connection pool (`common/src/db/limiter.rs`) | Unindexed text matching; validate with `EXPLAIN ANALYZE` first (Task 1, A2) |
| 4 | "Results should be more relevant" — "relevant" undefined; no example bad queries or expected rankings | No ranking criteria or evaluation corpus | Lexical ranking with `ts_rank_cd`, exact ID/name matches first, field weights A/B/C (Task 2, B1–B4) |
| 5 | "Add filters — some kind of filtering capability" — which fields, which entities, AND/OR semantics unspecified | Cannot define API contract | `type`, `severity`, `license` filters; OR within, AND across; invalid → 400 (Task 3, C1–C4) |
| 6 | "Better UI — make it look nicer" — no design, no frontend repo | Cannot be planned at all | Excluded (see below) |
| 7 | No Acceptance Criteria section in the Feature | Task ACs are derived from assumptions, not stakeholder-defined criteria | All task ACs labeled with the assumption they depend on |
| 8 | "Don't break existing functionality" — no definition of protected behavior | Unclear regression scope | Existing `tests/api/` suite must pass; `GET /api/v2/search` contract unchanged without filters (all tasks) |
| 9 | "Who benefits: All users" — no personas or usage patterns | Cannot prioritize which entity types/fields matter most | Equal treatment of SBOM, advisory, package |

**Clarification questions for the Feature owner:**
1. What is the current search latency and the target (e.g., p95 under N ms at M records)?
2. Is "search" the unified `/api/v2/search` endpoint, the per-entity list endpoints, or both?
3. Can you provide 3–5 example queries with the results users expected vs. what they got?
4. Which filters are required (fields, entity types), and how should they combine?
5. Is there a frontend repository and Figma design for the "Better UI" requirement?

## Changes

```
trustify-backend:
  changes:
    - Add a migration creating weighted, generated tsvector search columns with GIN indexes on the sbom, advisory, and package tables (migration/src/m0002_search_indexes/mod.rs, registered in migration/src/lib.rs)        [Task 1]
    - Expose the search vector columns on the SBOM, Advisory, and Package SeaORM entities (entity/src/sbom.rs, entity/src/advisory.rs, entity/src/package.rs)        [Task 1]
    - Switch SearchService queries to indexed full-text matching (modules/search/src/service/mod.rs)        [Task 1]
    - Order search results by relevance score with a deterministic tie-breaker (modules/search/src/service/mod.rs)        [Task 2]
    - Add validated type/severity/license filter query parameters to GET /api/v2/search (modules/search/src/endpoints/mod.rs, modules/search/src/service/mod.rs, common/src/db/query.rs if operators are missing)        [Task 3]
    - Add regression, index-usage, ranking, and filter integration tests (tests/api/search.rs)        [Tasks 1–3]
```

### Shared-artifact producer/consumer analysis

The search vectors are derived data on the `sbom`, `advisory`, and `package` tables.

- **Producers/writers of those tables:** SBOM ingestion (`modules/ingestor/src/graph/sbom/mod.rs`),
  advisory ingestion (`modules/ingestor/src/graph/advisory/mod.rs`), `IngestorService`
  (`modules/ingestor/src/service/mod.rs`), and the migration backfill for existing rows.
  Packages are written via SBOM ingestion (package linking).
- **Consumers:** `SearchService` (`modules/search/src/service/mod.rs`) via `GET /api/v2/search`.
- **Coverage:** Task 1 uses stored generated columns so every writer — including existing
  rows at migration time — populates the vector automatically; no writer changes are needed.
  Task 1 tests cover the backfill (pre-existing rows) and post-migration ingestion paths.
  If generated columns are rejected in review, the ingestor writers above must be added to
  Task 1 scope.

## Excluded requirements

| Requirement | MVP? | Reason excluded / missing input |
|---|---|---|
| Better UI — "Make it look nicer" | No | No Figma design mockups were provided and no frontend repository is registered in the Repository Registry (only `sdlc-plugins`/`trustify-backend` backend context available). "Nicer" has no concrete specification. Cannot be decomposed into tasks until a design and target frontend repository are supplied. |
| Frontend exposure of filters (implied by "Add filters") | Yes (partial) | Same missing inputs as above; only the backend API portion of filtering is planned (Task 3). |
| Numeric performance target | Yes (partial) | No target given; Task 1 uses a relative "faster than baseline" criterion until clarified. |

## Workflow mode decision (Step 4.5)

**Selected mode: `direct-to-main`**

Atomicity indicator evaluation:
1. Coordinated schema migrations — No. Only Task 1 adds a migration; it is additive
   (generated columns + indexes) and does not break code on `main` if merged alone.
2. Breaking API changes — No. Task 2 changes default ordering only; Task 3 adds optional
   parameters. No contract consumed by another task breaks.
3. Cross-cutting refactors — No.
4. Tightly coupled frontend/backend components — No. Backend only; UI excluded.

Each task can be merged to `main` independently once its dependency (Task 1) is merged.
All tasks use Target Branch `main`. No `workflow:feature-branch` label is applied; no
bookend tasks are generated.

## Task creation log (Step 6)

Hierarchy: Feature → Task (no Epics; see Step 2.5 note). Each task is linked from TC-9002
with an "Incorporates" link.

| Task | File | Summary | Depends on | Digest |
|---|---|---|---|---|
| Task 1 | task-1-search-indexes.md | Add full-text search indexes and use them in SearchService | — | sha256-md:c4584157f9b5cce2ab6a4b30b80555581eeb90b0ba5979866d75f896423ca913 |
| Task 2 | task-2-search-relevance-ranking.md | Rank unified search results by relevance | Task 1 | sha256-md:e01c660d08692f20a4b9fdac19cb98bedaa73d2c5a292dadbe49cb03a3a378a9 |
| Task 3 | task-3-search-filters.md | Add type, severity, and license filters to unified search | Task 1 | sha256-md:4024c51a381fe0a94cfd57d84528d2254ec2a2d531ed8f74591c7244ce8420f8 |

Digests computed with `scripts/sha256-digest.py` over the task description markdown (in a
live run, computed over the description re-fetched from Jira after creation). Digest comment
bodies are in `task-N-digest.md`.

**`additional_fields` applied to every created task (Tasks 1–3):**

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```

- `priority`: Feature priority is `Normal` (set, not "Undefined") → inherited.
- `fixVersions`: Feature has `RHTPA 1.6.0` and CLAUDE.md `fixVersion scope: both` → inherited.
- "Prompt for priority/fixVersion: true" in Jira Field Defaults: no user available; the
  inherited Feature values were accepted as the documented choice.

**Issue links:**
- TC-9002 —Incorporates→ Task 1, Task 2, Task 3
- Task 2 —Depend→ Task 1
- Task 3 —Depend→ Task 1

**Not generated:**
- Documentation task — Feature has no "Documentation Considerations" section.
- Testing tasks — no `docs/testing-readiness.md` in trustify-backend.
- Bookend tasks — workflow mode is `direct-to-main`.

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
