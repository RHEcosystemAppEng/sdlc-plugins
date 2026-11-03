# Repository Impact Map — TC-9002: Improve search experience

## Execution context (eval mode)

- **Step 0 (Project Configuration):** PASS. Repository Registry, Jira Configuration (Project key TC, Cloud ID, Feature issue type ID 10142), and Code Intelligence sections are all present in CLAUDE.md.
- **Step 1 (Fetch feature):** read from the mock `feature-ambiguous.md`. Priority = `Normal`. fixVersions = `[RHTPA 1.6.0]`. There is no "Documentation Considerations" section, so no documentation signals were found.
- **Step 1.5 (Parent link):** the Feature has no parent. In eval mode the interactive prompt was skipped and no parent link was set.
- **Step 2 (Figma):** no Figma URL in the arguments or in the Feature description. No design input.
- **Step 2.5 (Issue types):** Jira is unavailable in eval mode, so issue types could not be discovered. CLAUDE.md `## Hierarchy Configuration` sets `Default epic grouping strategy: by-sub-feature`. The Epic plan below is **conditional**: Epics are created only if discovery finds a level-1 type. Otherwise tasks are created directly under the Feature (graceful degradation).
- **Step 3 (Repository analysis):** no Serena instance and no checkout of `trustify-backend` were available. The analysis is based only on the repository structure in `repo-backend.md` (directory tree and Key Conventions). The contents of `CONVENTIONS.md` and the code bodies (e.g., how `SearchService` runs queries) could **not** be inspected. Every task tells the implementer to check current behavior before changing it.
- **Documentation files found:** `README.md`, `CONVENTIONS.md`.
- **Testing readiness template (`docs/testing-readiness.md`):** not present, so no testing tasks are generated.
- **Eval infrastructure:** not applicable, because no `SKILL.md` is being modified.

## Ambiguity assessment

The Feature description is underspecified. None of the requirements has measurable acceptance criteria:

| Requirement | MVP | Ambiguity | Planning decision |
|---|---|---|---|
| Search should be faster | Yes | No latency target ("fast enough"), no slow queries named, no baseline measurement, no dataset size | **Partially planned** (Task 1): low-regret changes that follow existing repo conventions (pagination via the shared query helpers, response caching via the `tower-http` caching convention) plus a baseline latency measurement. Fully meeting this requirement is **unresolved** until a target is given. |
| Results should be more relevant | Yes | No definition of "relevant", no example queries or bad results, no ranking criteria | **Excluded.** See Excluded requirements below. |
| Add filters | Yes | "Some kind of filtering capability". The filter dimensions are not specified. | **Planned with assumptions** (Tasks 2–3). Filter dimensions were inferred from repo evidence: entity type (the search spans SBOM/advisory/package), advisory `severity` (in `AdvisorySummary`), and package `license` (in `PackageSummary`). These must be confirmed. |
| Better UI | No | "Make it look nicer". No design. | **Excluded.** See Excluded requirements below. |
| NFR: Don't break existing functionality | — | — | Becomes a backward-compatibility acceptance criterion in every task: requests without the new parameters behave as before, and the existing `tests/api/search.rs` keeps passing. |

### Clarification requested from the Feature owner

1. **Performance target:** what latency is "fast enough"? (e.g., p95 < N ms for `GET /api/v2/search` at M records). Which queries or entity types are slow today?
2. **Relevance:** please give example queries with the results you expected and the results you got. Should results be ranked by text match score, by recency, by severity, or by exact identifier match (CVE ID, PURL, SBOM name)?
3. **Filters:** confirm the assumed filters (entity type, advisory severity, package license). Are other dimensions needed (date ranges, SBOM, product/version)?
4. **UI:** which frontend repository is in scope, and are there Figma mockups?

## Repository Impact Map

```
trustify-backend:
  changes:
    - Paginate GET /api/v2/search results using the shared PaginatedResults<T> wrapper and query helpers (Task 1)
    - Add response caching to the search route builder per the tower-http caching convention (Task 1)
    - Add a search latency baseline integration test (Task 1)
    - Add an entity-type filter to GET /api/v2/search, rejecting invalid values (Task 2)
    - Add advisory severity and package license filters to GET /api/v2/search (Task 3)
    - Extend search integration tests for filters and backward compatibility (Tasks 2, 3)
```

### Shared-artifact producer/consumer note (unresolved verification)

`SearchService` (`modules/search/src/service/mod.rs`) runs "full-text search across entities". The analysis could not tell whether it queries the entity tables directly (`entity/src/advisory.rs`, `entity/src/package.rs`, `entity/src/package_license.rs`, `entity/src/sbom.rs`) or a separate search index or `tsvector` column filled in at ingestion time.

- **Consumers:** `modules/search/src/service/mod.rs`, `modules/search/src/endpoints/mod.rs`. Tests: `tests/api/search.rs`.
- **Possible producers (if an index or derived column exists):** `modules/ingestor/src/graph/sbom/mod.rs`, `modules/ingestor/src/graph/advisory/mod.rs`, `modules/ingestor/src/service/mod.rs`, and `migration/src/` for the schema.
- **Open question:** if search reads a derived index, Task 3's severity and license filters need those fields in the index. That would add ingestor and migration changes, which are **not** in the current task scope. The implementer of Task 3 must check this first. If it applies, stop and ask for a scope expansion before claiming the filter criteria are met.

### Excluded requirements

| Requirement | Missing input that prevents planning |
|---|---|
| Results should be more relevant (MVP) | No definition of relevance, no example queries or bad results, and no ranking criteria. Without these the work cannot be broken into verifiable tasks: any ranking change would be a guess, and its acceptance criteria could not be checked. Needs answers to clarification question 2. |
| Better UI (non-MVP) | No frontend repository in the Repository Registry (only `sdlc-plugins` is registered, and the analyzed target is the backend), and no Figma mockups. Needs a target frontend repository and a design. |
| Search should be faster: target-metric portion (MVP) | Task 1 covers low-regret improvements and a baseline. There is no latency target, so "search is fast" cannot be verified. Needs answers to clarification question 1. Further optimization tasks (e.g., indexes, query rewrites) need profiling data. |

## Step 4.5 — Workflow mode

**Mode: `direct-to-main`**

Rationale: no atomicity indicators were found.
1. Coordinated schema migrations: none planned.
2. Breaking API changes: none. All new query parameters are optional and additive. Task 1's pagination keeps the default behavior of unparameterized requests compatible (see the Task 1 acceptance criteria).
3. Cross-cutting refactors: none.
4. Tightly coupled frontend and backend: none (backend only).

Tasks 2 and 3 touch the same files as Task 1 (search endpoint and service), so they are ordered with dependencies to avoid merge conflicts. Each merged PR leaves `main` working on its own.

## Step 5 — Epic grouping (conditional on a level-1 type being discovered)

Strategy: `by-sub-feature` (from CLAUDE.md Hierarchy Configuration). In interactive mode the suggested grouping would be shown for approval. In eval mode it is recorded as proposed.

| Epic summary | Tasks |
|---|---|
| TC-9002: Search performance | Task 1 |
| TC-9002: Search filtering | Task 2, Task 3 |

If no level-1 type exists, skip Epics. Tasks are then created under the Feature, with "Incorporates" links from TC-9002 to each task.

## Generated tasks

| # | File | Summary | Depends on |
|---|---|---|---|
| 1 | task-1-search-pagination-caching.md | Paginate and cache GET /api/v2/search, and add a latency baseline | — |
| 2 | task-2-search-entity-type-filter.md | Add an entity-type filter to GET /api/v2/search | Task 1 |
| 3 | task-3-search-attribute-filters.md | Add advisory severity and package license filters to GET /api/v2/search | Task 2 |

No documentation task (no Documentation Considerations section). No testing tasks (no `docs/testing-readiness.md`). No bookend tasks (direct-to-main mode).

## Step 6 — Task creation log (`additional_fields`)

Inherited field values:
- **priority:** `Normal`, set on the Feature (not "Undefined"), so it is **propagated**.
- **fixVersions:** `RHTPA 1.6.0`, set on the Feature, and `fixVersion scope: both`, so it is **propagated** to tasks and Epics.

Epics (only if a level-1 type is discovered), with `parent = TC-9002`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```

Tasks 1–3 (issue type = the discovered level-0 type; `parent` = the assigned Epic key when Epics exist, otherwise omitted or set to TC-9002):

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```

| Task | Summary | Epic (if available) | parent |
|---|---|---|---|
| 1 | TC-9002: Paginate and cache GET /api/v2/search, and add a latency baseline | TC-9002: Search performance | Epic key |
| 2 | TC-9002: Add an entity-type filter to GET /api/v2/search | TC-9002: Search filtering | Epic key |
| 3 | TC-9002: Add advisory severity and package license filters to GET /api/v2/search | TC-9002: Search filtering | Epic key |

After each task is created, post a description digest comment (see `task-N-digest.md`).

Issue links (Step 6b):
- Incorporates: TC-9002 → each Epic (or each task if there are no Epics)
- Depend: Task 2 depends on Task 1. Task 3 depends on Task 2.

Feature label: no `workflow:feature-branch` label (direct-to-main mode).
