# Repository Impact Map — TC-9002: Improve search experience

> Would be posted as a Jira comment on TC-9002 (Step 4), followed by the workflow mode decision (Step 4.5).
> Eval run: no Jira, Figma, or Serena access. Repository analysis used the `repo-backend.md` fixture (trustify-backend). Interactive prompts were answered with defaults, listed under "Non-interactive decisions" below.

## Ambiguity assessment (read this first)

The Feature description is **too vague to plan without assumptions**. None of its requirements have measurable acceptance criteria:

| Requirement (MVP?) | What is missing | How this plan handles it |
|---|---|---|
| Search should be faster (Yes) | No baseline latency, no target (for example a p95 in ms), no list of slow queries or entities, no dataset size. The NFR "should be fast enough" can't be tested. | **Planned with an assumption.** Task 1 measures the current latency and records a baseline. Task 2 adds database indexes for the search queries. The latency target stays an **open question**. Task 2's criteria compare against Task 1's baseline instead of a made-up number. |
| Results should be more relevant (Yes) | No definition of "relevant". No examples of bad results, no ranking signals, no relevance test set. | **Planned with an assumption.** Task 3 adds relevance-ranked ordering (best text match first, exact identifier matches boosted). The ranking rules are an assumption that the product owner has to confirm. |
| Add filters (Yes) | "Some kind of filtering capability": filter dimensions are not named. | **Planned with an assumption.** Task 4 adds filters only on fields the code already has: entity type, advisory `severity` (`AdvisorySummary`) and package `license` (`PackageSummary`). Any other filter needs clarification. |
| Better UI (No) | No frontend repository in the Repository Registry. No Figma design linked or provided. "Make it look nicer" has no specification. | **Excluded.** See "Excluded requirements". |

**Recommendation:** before anyone implements these tasks, the Feature owner should answer the open questions below and update TC-9002 with measurable acceptance criteria. Every task lists its own assumptions so it can be adjusted easily if the answers differ.

### Open questions for the Feature owner

1. **Performance target:** what latency counts as "fast enough"? For example, p95 below X ms for `GET /api/v2/search` at Y entities. Which queries or entity types are slow today?
2. **Relevance definition:** which queries return irrelevant results today? Please give examples. Should exact identifier matches (CVE IDs, package names or PURLs, SBOM names) always rank first?
3. **Filters:** which filter dimensions are needed? The plan assumes entity type, advisory severity and package license. Are date ranges, SBOM or product scope, or advisory status also needed?
4. **Better UI:** which frontend repository owns the search UI? Is there a Figma design?
5. **Caching:** is serving slightly stale search results (with a short TTL) acceptable? If yes, response caching through the existing `tower-http` caching middleware could be added. It is not planned because the freshness requirements are unknown.
6. **Compatibility:** "Don't break existing functionality" is read as: `GET /api/v2/search` keeps its current path, its current parameters and its `PaginatedResults<T>` response shape. All new parameters are optional. Please confirm.

## Repository analysis summary

- Repositories in the Registry: `sdlc-plugins` (the plugin itself, not relevant to search). The target backend is **trustify-backend**, analyzed from the fixture. There is no Serena instance, so the analysis used the fixture's directory tree and conventions.
- Search module: `modules/search/src/service/mod.rs` (`SearchService`, full-text search across entities) and `modules/search/src/endpoints/mod.rs` (`GET /api/v2/search`).
- Related domain search: `modules/fundamental/src/advisory/service/advisory.rs` (`AdvisoryService`: fetch, list, **search**). This is a duplication risk and a reuse candidate.
- Shared helpers: `common/src/db/query.rs` (filtering, pagination, sorting), `common/src/model/paginated.rs` (`PaginatedResults<T>`), `common/src/error.rs` (`AppError`).
- Filterable fields: `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary.severity`), `modules/fundamental/src/package/model/summary.rs` (`PackageSummary.license`), `entity/src/package_license.rs`.
- Entities searched: `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs`.
- Migrations: `migration/src/lib.rs`, `migration/src/m0001_initial/mod.rs`.
- Tests: `tests/api/search.rs` (search integration tests on a real PostgreSQL test DB).
- Docs: `README.md`, `CONVENTIONS.md`. The fixture provides the conventions as its "Key Conventions" list. No `docs/testing-readiness.md` was found, so **no testing tasks** are generated.
- Eval infrastructure: not applicable, because no task modifies a skill `SKILL.md`.

### Shared-artifact producer/consumer analysis

The **searchable entity data** (the `sbom`, `advisory` and `package` tables that `SearchService` queries) is a shared artifact.

- **Producers:** `modules/ingestor/src/graph/sbom/mod.rs` (SBOM ingestion; also stores and links packages), `modules/ingestor/src/graph/advisory/mod.rs` (advisory ingestion), orchestrated by `modules/ingestor/src/service/mod.rs` (`IngestorService`). `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` also lists "ingest" as a responsibility, which makes it an on-demand/API ingestion path.
- **Consumers:** `SearchService` (`modules/search/src/service/mod.rs`), `AdvisoryService` search (`modules/fundamental/src/advisory/service/advisory.rs`), and the list endpoints that use `common/src/db/query.rs`.
- **Impact on this plan:** Task 2 must use **expression indexes or generated columns**, so ingestion code does not need to change. If the implementer instead adds stored search columns (for example a `tsvector` column) that producers have to populate, then **every** producer above must be updated. That is a scope change and must be raised before implementation. Task 2 and Task 3 include tests that check entities ingested through the SBOM path and the advisory path are found and ranked. This avoids validating only data inserted by the test fixtures.
- **Coverage gap:** none, provided the generated-column or expression-index approach is used.

## Impact map

```
trustify-backend:
  changes:
    - Instrument the search request path and add a repeatable latency baseline for GET /api/v2/search (Task 1)
    - Add database indexes that support the search queries on sbom, advisory and package (Task 2)
    - Order search results by relevance score instead of the current order (Task 3)
    - Add optional filter query parameters (entity type, advisory severity, package license) to GET /api/v2/search (Task 4)
```

### Excluded requirements

- **"Better UI — Make it look nicer" (non-MVP).** Missing inputs: (a) no frontend repository is registered in the Repository Registry, so there is no target repository; (b) no Figma design is linked in TC-9002 or provided as an argument; (c) no specification of what "nicer" means. To plan it, add the frontend repository to the Registry, attach a Figma design, and re-run plan-feature.
- **Measurable performance target (part of "Search should be faster" / NFR "fast enough").** Missing input: a numeric latency or throughput target. Tasks 1 and 2 improve and measure performance. They do not and cannot verify that the goal is met until a target is defined.
- **Response caching.** Not a stated requirement. It is an optional technique held back by open question 5 (freshness requirements unknown).

## Workflow mode decision (Step 4.5)

**Mode: `direct-to-main`**

Atomicity indicators checked:
1. Coordinated schema migrations: **not present**. Task 2 adds indexes only, with no column changes that other code depends on. Main stays working whether or not the index migration is merged.
2. Breaking API changes: **not present**. Task 4 adds optional query parameters, and Task 3 changes only the result order. The path and response shape stay the same.
3. Cross-cutting refactors: **not present**.
4. Tightly coupled frontend/backend components: **not present**. Backend only, and the UI is excluded.

Each task PR can merge to `main` on its own. Ordering dependencies (Task 2 after Task 1, Task 3 after Task 2) control sequencing but do not require all-or-nothing delivery. All tasks therefore use Target Branch `main`, no bookend tasks are generated, and the `workflow:feature-branch` label is **not** applied.

## Non-interactive decisions (defaults chosen)

| Prompt / step | Default chosen | Rationale |
|---|---|---|
| Step 1.5: link Feature to a parent issue | Skipped (Enter) | No parent was specified. The step is optional. |
| Step 2: Figma | Skipped | No Figma URL in the arguments or the Feature description. |
| Step 2.5: issue type discovery | Assumed `Epic` (level 1) and `Task` (level 0). Feature ID 10142 comes from CLAUDE.md. | Jira was not reachable. A real run would call `get_project_issue_types` and would fall back to Feature → Task if no level-1 type exists. |
| Step 4: impact map approval | Approved with assumptions | Run is non-interactive. The ambiguities are recorded above so a human can reject the map. |
| Step 5: Epic grouping strategy | `by-sub-feature` (from CLAUDE.md Hierarchy Configuration) | Configured default. |
| Step 5: by-sub-feature grouping approval | Auto-approved (see below) | Run is non-interactive. |
| Prompt for priority / fixVersion | Inherited from the Feature (Normal / RHTPA 1.6.0) | Feature values are set, so no override is needed. |
| Documentation task | Not generated | TC-9002 has no "Documentation Considerations" section. |
| Testing tasks | Not generated | No `docs/testing-readiness.md` in trustify-backend. |

## Epic grouping (by-sub-feature)

| Epic summary | Tasks |
|---|---|
| TC-9002: Search performance | Task 1, Task 2 |
| TC-9002: Search relevance | Task 3 |
| TC-9002: Search filtering | Task 4 |

## Task creation log (Step 6, simulated)

Feature fields read in Step 1: priority `Normal` (set, not "Undefined"); fixVersions `[RHTPA 1.6.0]` (non-empty). CLAUDE.md `fixVersion scope: both` means fixVersions are propagated to Epics and Tasks.

`additional_fields` applied to **every** Epic and Task:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```

| # | Issue | Type | Parent | Placeholder key | File |
|---|---|---|---|---|---|
| E1 | TC-9002: Search performance | Epic | TC-9002 | EPIC-1 | — |
| E2 | TC-9002: Search relevance | Epic | TC-9002 | EPIC-2 | — |
| E3 | TC-9002: Search filtering | Epic | TC-9002 | EPIC-3 | — |
| 1 | Instrument search and establish a latency baseline | Task | EPIC-1 | TASK-1 | task-1-search-latency-baseline.md |
| 2 | Add database indexes for search queries | Task | EPIC-1 | TASK-2 | task-2-search-indexes.md |
| 3 | Rank search results by relevance | Task | EPIC-2 | TASK-3 | task-3-search-relevance-ranking.md |
| 4 | Add filter parameters to search endpoint | Task | EPIC-3 | TASK-4 | task-4-search-filters.md |

A description digest comment is posted on each task right after it is created: `task-N-digest.md`.

### Issue links (Step 6b)

- Incorporates: TC-9002 → EPIC-1, TC-9002 → EPIC-2, TC-9002 → EPIC-3
- Depend: TASK-2 depends on TASK-1; TASK-3 depends on TASK-2

### Feature labels

- `workflow:feature-branch` is **not** added (direct-to-main mode).

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.14.0.
