# Repository Impact Map — TC-9002: Improve search experience

> Status: **DRAFT — requires clarification before task creation.** In an interactive
> run, Step 4 stops here and presents this map (including the open questions below)
> to the engineer for review. The task drafts in this directory are written against
> the explicitly stated assumptions and MUST be revisited once the questions are
> answered.

## Inputs used

| Input | Value |
|---|---|
| Feature | TC-9002 — "Improve search experience" (Status: New) |
| Priority | Normal |
| Fix Versions | RHTPA 1.6.0 |
| Figma | None (no URL in arguments or description) |
| Documentation Considerations | Section absent — no documentation signals |
| Target repository | trustify-backend (Rust, Axum + SeaORM, PostgreSQL) |
| CONVENTIONS.md | Present at repository root (Key Conventions used for enrichment) |
| `docs/testing-readiness.md` | Not present — no testing tasks generated |
| Serena | Not configured — repository analysed from the provided structure |

## Ambiguity analysis

The Feature description is too vague to plan with confidence. Each requirement was
checked for a measurable target, a concrete scope, and a planning input:

| Requirement | MVP | What is missing | Planning outcome |
|---|---|---|---|
| Search should be faster | Yes | No latency baseline, no target (e.g. p95), no slow query or dataset size identified. NFR "fast enough" is not measurable. | Planned under assumption A1/A2 (Task 1) — needs confirmation |
| Results should be more relevant | Yes | No definition of "relevant", no example queries with expected vs actual results, no ranking criteria | Planned under assumption A3 (Task 2) — needs confirmation |
| Add filters | Yes | "Some kind of filtering capability" — which fields, which entities, and what semantics (exact match, range, multi-value) are not specified | Planned under assumption A4 (Task 3) — needs confirmation |
| Better UI | No | No Figma design, no frontend repository in the Repository Registry, no definition of "nicer" | **Excluded** (see below) |
| Don't break existing functionality (NFR) | — | — | Applied to every task: `GET /api/v2/search` changes are additive and backward compatible; existing tests in `tests/api/search.rs` must keep passing |

### Clarification questions for the engineer / Feature owner

1. **Performance target:** what latency is "fast enough"? (e.g. p95 < 500 ms for
   `GET /api/v2/search` on a dataset of N SBOMs / advisories / packages). Which
   queries are slow today — is there a trace or a customer example?
2. **Relevance:** what does a "relevant" result look like? Please provide 3–5 example
   queries with the results users expect at the top. Should exact identifier matches
   (e.g. CVE ID, package name, SBOM name) outrank partial text matches?
3. **Filters:** which filters are required for MVP? Candidates visible in the data
   model: entity type (SBOM / advisory / package), advisory `severity`
   (`AdvisorySummary`), package `license` (`PackageSummary`). Are date-range filters
   (e.g. published / ingested) expected?
4. **Scope of "search":** does this Feature cover only the cross-entity endpoint
   `GET /api/v2/search`, or also the per-entity list endpoints
   (`GET /api/v2/sbom`, `GET /api/v2/advisory`, `GET /api/v2/package`) and
   `AdvisoryService` search?
5. **UI:** which frontend repository owns the search UI, and is a Figma design
   available? (Needed before "Better UI" can be planned.)

### Assumptions used for the draft tasks

- **A1** — "Search" refers to the cross-entity full-text endpoint `GET /api/v2/search`
  implemented in `modules/search/` (`SearchService`).
- **A2** — Slowness is caused by un-indexed full-text matching and unbounded result
  sets; the fix is a PostgreSQL full-text index (GIN over a stored generated
  `tsvector`) plus enforced pagination via the shared query helpers. The performance
  target is a placeholder until question 1 is answered.
- **A3** — "Relevance" means ordering results by full-text rank (`ts_rank`) with exact
  identifier/name matches boosted to the top, instead of the current unranked order.
- **A4** — MVP filters are: entity type, advisory severity, package license. These are
  the only filterable attributes already exposed in the model layer.

## Impact map

```
trustify-backend:
  changes:
    - Add a database migration creating full-text search columns/indexes for the entities searched by SearchService (SBOM, advisory, package)        [Task 1, A1/A2]
    - Make SearchService use the indexed full-text columns and enforce pagination through the shared query helpers                                      [Task 1, A2]
    - Order GET /api/v2/search results by relevance rank, boosting exact identifier/name matches, and expose the score on each result                  [Task 2, A3]
    - Add filter query parameters (entity type, advisory severity, package license) to GET /api/v2/search, rejecting invalid filter values             [Task 3, A4]
    - Extend search integration tests to cover indexing across all ingestion paths, ranking, filters, and backward compatibility                     [Tasks 1-3]
```

### Shared-artifact producer/consumer trace (search index)

The full-text search index (new generated `tsvector` columns + GIN indexes) is a
shared artifact. Every path that populates searchable rows must be covered:

| Role | Path | Coverage |
|---|---|---|
| Producer (primary) | `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion: stores SBOMs and links packages (writes `entity/src/sbom.rs`, `entity/src/package.rs`, `entity/src/sbom_package.rs`) | Task 1 test: newly ingested SBOM and its packages are searchable |
| Producer (primary) | `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion (writes `entity/src/advisory.rs`) | Task 1 test: newly ingested advisory is searchable |
| Producer (on-demand/API) | `modules/fundamental/src/sbom/service/sbom.rs` — `SbomService` ingest path | Task 1 test: SBOM ingested via `SbomService` is searchable |
| Producer (schema) | `migration/src/` — new migration back-fills existing rows (generated stored column is computed for all existing rows on `ALTER TABLE`) | Task 1 test: rows present before migration are searchable after it |
| Consumer | `modules/search/src/service/mod.rs` — `SearchService` | Tasks 1, 2, 3 |
| Consumer | `modules/search/src/endpoints/mod.rs` — `GET /api/v2/search` | Tasks 2, 3 |
| Test coverage | `tests/api/search.rs` | Tasks 1, 2, 3 |

Using a **stored generated column** (computed by PostgreSQL on every INSERT/UPDATE)
means no producer code has to change to keep the index current; the producers above
are listed so their behaviour is covered by tests rather than assumed.

**Unresolved:** if question 4 widens scope to the per-entity list endpoints, the
consumers `modules/fundamental/src/{sbom,advisory,package}/endpoints/list.rs` and
`modules/fundamental/src/advisory/service/advisory.rs` (`AdvisoryService` search)
would also need tasks. They are intentionally **not** in any task's Files to Modify
until the scope is confirmed.

## Excluded requirements

| Requirement | Reason excluded / missing input |
|---|---|
| **Better UI** ("Make it look nicer", non-MVP) | No Figma design was provided or linked; no frontend repository is listed in the Repository Registry (only trustify-backend was supplied); "nicer" has no acceptance criteria. Provide the frontend repository and a design to plan this. |
| **NFR "Should be fast enough"** as a verifiable criterion | No measurable latency target. Task 1 carries a placeholder benchmark; the real threshold must be supplied (clarification question 1) before the criterion can be considered covered. |
| Filters beyond A4 (e.g. date ranges, arbitrary fields) | Filter set is unspecified ("some kind of filtering capability"); only filters backed by attributes already in the model are planned. |

## Workflow mode decision (Step 4.5)

**Selected mode: `direct-to-main`**

Atomicity indicators evaluated:

1. Coordinated schema migrations — **not present.** Only Task 1 adds a migration; it is
   additive (new generated columns + indexes) and existing code keeps working with it.
2. Breaking API changes — **not present.** Tasks 2 and 3 only add optional query
   parameters / response fields to `GET /api/v2/search`; existing clients are unaffected.
3. Cross-cutting refactors — **not present.**
4. Tightly coupled frontend/backend components — **not present.** UI work is excluded.

Tasks 2 and 3 depend on Task 1 for ordering, but each task leaves `main` in a working
state when merged on its own. All tasks therefore use Target Branch `main`, no bookend
tasks are generated, and the `workflow:feature-branch` label is **not** applied.

## Hierarchy (Step 2.5 / Step 5 Epic grouping)

Issue types could not be discovered (no Jira access in this run). CLAUDE.md
`## Hierarchy Configuration` sets `Default epic grouping strategy: by-sub-feature`.

- **If a level-1 (Epic) type exists:** proposed by-sub-feature groups (would be
  presented for approval):
  - `TC-9002: Search performance and relevance` — Task 1, Task 2
  - `TC-9002: Search filtering` — Task 3
- **If no level-1 type exists:** "No Epic-level type found in project — tasks will be
  created directly under the Feature." Feature → Task hierarchy with Incorporates links.

## Task creation log (Step 6 — simulated)

Inherited field values (Step 1 + `### Jira Field Defaults`):

- Priority: `Normal` — set on Feature (not "Undefined") → **propagated**
- fixVersions: `RHTPA 1.6.0` — Feature has a value and `fixVersion scope: both` → **propagated**

`additional_fields` applied to every created Epic and Task:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```

| # | File | Summary | Issue type | Parent (if Epics) | Depends on |
|---|---|---|---|---|---|
| 1 | task-1-search-fulltext-index.md | Add full-text indexes and paginated querying to SearchService | Task | TC-9002: Search performance and relevance | — |
| 2 | task-2-search-relevance-ranking.md | Rank search results by relevance | Task | TC-9002: Search performance and relevance | Task 1 |
| 3 | task-3-search-filters.md | Add filter parameters to GET /api/v2/search | Task | TC-9002: Search filtering | Task 1 |

Links (Step 6b):

- Feature TC-9002 **Incorporates** each Epic (or each Task when no Epic type exists)
- Task 2 **Depend** → Task 1
- Task 3 **Depend** → Task 1

Digest comments (Step 6a): one per task, `task-N-digest.md`. Digests here are computed
with `scripts/sha256-digest.py` over the drafted markdown; in a live run they must be
recomputed over the description re-fetched from Jira.

Not generated: documentation task (no Documentation Considerations section), testing
tasks (no `docs/testing-readiness.md`), bookend tasks (direct-to-main mode).
