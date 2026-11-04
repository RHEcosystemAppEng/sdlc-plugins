# Repository Impact Map — TC-9002: Improve search experience

> Posted as a comment on TC-9002 (Step 4) once approved by the user. In this eval it is written to a file instead of Jira.

## Planning context

| Item | Value |
|---|---|
| Feature | TC-9002 — Improve search experience |
| Priority | Normal |
| Fix Versions | RHTPA 1.6.0 |
| Figma | None linked, none supplied as an argument |
| Documentation Considerations section | Not present, so no documentation task is generated |
| Testing readiness template (`docs/testing-readiness.md`) | Not in the target repo, so no testing tasks are generated |
| Target repository | trustify-backend (from `repo-backend.md`) |
| Code intelligence | No Serena instance. The analysis used the repository structure fixture. |
| CONVENTIONS.md | Listed at the repo root, but its contents are not in the fixture. Task notes use the Key Conventions in `repo-backend.md` instead. |

## Ambiguity assessment (needs clarification from the Feature owner)

The Feature description is vague. It has no acceptance criteria, no baseline measurements and no measurable targets. The plan rests on the assumptions below. **Each one must be confirmed before tasks are treated as final.**

| # | Requirement / NFR | Ambiguity | Assumption used for planning | Question for the Feature owner |
|---|---|---|---|---|
| A1 | "Search should be faster" | No baseline latency, no target, and no named slow queries or entities | The main cost is full-text matching over un-indexed text columns in `SearchService`. Fix it with DB full-text indexes and indexed queries. Target: p95 latency on `GET /api/v2/search` at or below 500 ms on a representative dataset. | What latency is "fast enough" (p95/p99)? At what data volume? Which queries are slow? |
| A2 | "Results should be more relevant" | No definition of relevance and no example bad queries | Rank results by full-text relevance (`ts_rank`), with exact identifier and name matches first. Make relevance the default sort. | Which example queries return bad results today? Which fields matter most (name, identifier/CVE ID, description)? |
| A3 | "Add filters — some kind of filtering capability" | No filter dimensions named | Filter by entity type (sbom / advisory / package), advisory severity (`AdvisorySummary.severity`) and package license (`PackageSummary.license`). These fields already exist in the models. | Which filters do users need? Are date ranges or SBOM-scoped filters needed? |
| A4 | NFR "Should be fast enough" | Not measurable | Same target as A1 | Same as A1 |
| A5 | NFR "Don't break existing functionality" | No contract named | Keep the existing `GET /api/v2/search` contract backward compatible. New query parameters are optional, the response shape stays `PaginatedResults<T>`, and existing tests in `tests/api/search.rs` must keep passing. | Are there API consumers (UI, CLI) that depend on today's result ordering? |
| A6 | Scope: "search" | Unclear whether this means only the global `/api/v2/search` endpoint or also the per-entity list endpoints (`AdvisoryService` "search", `/api/v2/sbom`, `/api/v2/package`) | Only the global search module (`modules/search`). Per-entity list endpoints are out of scope. | Should the per-entity list endpoints get the same filters and ranking? |

## Impact map

```
trustify-backend:
  changes:
    - Add a database migration with full-text search indexes (tsvector/GIN) on the searchable columns of the sbom, advisory and package tables
    - Update SearchService to run indexed full-text queries and enable response caching on the search route (performance)
    - Rank search results by relevance and make relevance the default sort order
    - Add optional, validated filter parameters (entity type, advisory severity, package license) to GET /api/v2/search
```

### Change → task mapping

| Change | Task | File |
|---|---|---|
| Full-text search indexes migration | Task 1 | `task-1-search-fulltext-indexes.md` |
| Indexed full-text queries and caching | Task 2 | `task-2-search-query-performance.md` |
| Relevance ranking | Task 3 | `task-3-search-relevance-ranking.md` |
| Search filters | Task 4 | `task-4-search-filters.md` |

## Excluded requirements

| Requirement | MVP? | Reason excluded / missing input |
|---|---|---|
| Better UI ("Make it look nicer") | No | **No frontend repository** is in the Repository Registry or the supplied repository context, and **no Figma design** is linked or supplied. The requirement also gives no concrete UI changes. To plan it, add the frontend repo to the Registry, supply Figma mockups, and define what "nicer" means. |

No MVP requirement was dropped. Requirements A1–A3 are planned using the assumptions above, and the plan should be re-confirmed once the Feature owner answers the open questions. If the answers change the filter set (A3) or the scope (A6), Tasks 3–4 must be revised before implementation.

## Shared-artifact analysis

No acceptance criterion depends on a shared artifact (manifest, index file, registry or cache document) with several producers. Search reads entity tables that the ingestor fills (`modules/ingestor/src/graph/sbom/mod.rs`, `modules/ingestor/src/graph/advisory/mod.rs`). Because the indexes in Task 1 are database indexes, or columns generated from existing data, PostgreSQL keeps them up to date on every insert and update. No ingestor change is needed. Task 1 still requires a test that newly ingested data is searchable through the indexed path.

## Workflow mode decision (Step 4.5)

**Mode: `direct-to-main`**

Atomicity indicators checked:

1. Coordinated schema migrations: **none**. Task 1 adds indexes, or generated columns derived from existing data. Nothing breaks if it merges alone, and existing queries keep working.
2. Breaking API changes: **none**. Tasks 3–4 add optional query parameters and change the default ordering only. The response shape (`PaginatedResults<T>`) does not change.
3. Cross-cutting refactors: **none**.
4. Tightly coupled frontend and backend: **none**. Only the backend is in scope (the UI requirement is excluded).

Each task leaves `main` working. Ordering dependencies (Task 2 and Task 3 depend on Task 1) are handled with Jira "Depend" links, not a feature branch. Every task gets Target Branch `main`. No bookend tasks are generated, and the `workflow:feature-branch` label is not applied.

## Issue type discovery and hierarchy (Step 2.5)

- In this eval the Jira project issue types could not be fetched, because external services are disabled. No level-1 (Epic) type was discovered, so the skill falls back to **Feature → Task** without error. It logs: "No Epic-level type found in project — tasks will be created directly under the Feature."
- The `Default epic grouping strategy: by-sub-feature` in CLAUDE.md would apply if an Epic type were discovered. The groups would then be "TC-9002: Search performance" (Tasks 1–2) and "TC-9002: Search relevance and filtering" (Tasks 3–4).
- Step 1.5 (parent link): the Feature has no parent, and the user prompt was skipped in this non-interactive run, so no parent link is set.

## Task creation log (Step 6)

Issue type: Task (level 0). There is no `parent` field because no Epics exist. Each task is linked from the Feature with "Incorporates".

`additional_fields` applied to **every** created task:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```

- `priority`: "Normal" is set on the Feature and is not "Undefined", so it is **propagated**.
- `fixVersions`: the Feature has "RHTPA 1.6.0" and `fixVersion scope: both`, so it is **propagated**.

| Task | Summary | Placeholder key | Digest comment file |
|---|---|---|---|
| Task 1 | Add full-text search indexes migration | TC-9002-T1 | `task-1-digest.md` |
| Task 2 | Use indexed full-text queries and caching in SearchService | TC-9002-T2 | `task-2-digest.md` |
| Task 3 | Rank search results by relevance | TC-9002-T3 | `task-3-digest.md` |
| Task 4 | Add validated filters to GET /api/v2/search | TC-9002-T4 | `task-4-digest.md` |

Links (Step 6b):

- Incorporates: TC-9002 → T1, T2, T3, T4
- Depend: T2 depends on T1
- Depend: T3 depends on T1
- Depend: T4 depends on T2 (both tasks edit `SearchService` and the search endpoint, so this ordering avoids merge conflicts)

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.
