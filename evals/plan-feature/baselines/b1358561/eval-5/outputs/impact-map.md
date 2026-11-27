# TC-9005 — Planning Record and Repository Impact Map

Feature: **TC-9005 — Drop status table and migrate to enum column**
Plugin: sdlc-workflow/plan-feature v0.14.0

## Step 0 — Project Configuration validation

- Repository Registry: present (`sdlc-plugins`); target repository for this eval is `trustify-backend` (structure supplied in `repo-backend.md`).
- Jira Configuration: present (Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID 10142).
- Code Intelligence: present (no Serena instances; fallback to Read/Glob/Grep over the supplied repository structure).

Result: PASS.

## Step 1 — Extracted Feature fields

| Field | Value |
|---|---|
| Title | Drop status table and migrate to enum column |
| Priority | High (propagate — not "Undefined") |
| fixVersions | RHTPA 2.0.0 (propagate — `fixVersion scope: both`) |
| Existing labels | `ai-generated-jira` |
| Figma links | None |
| Parent | None set |

Documentation signals: **Updates to existing content** — "Minor — update internal architecture docs to reflect schema change"; no external API documentation changes; reference: SeaORM enum mapping documentation.

**Prompt decisions (non-interactive eval, documented choices):**
- `Prompt for priority: true` — accepted the inherited Feature priority **High** without change.
- `Prompt for fixVersion: true` — accepted the inherited Feature fixVersion **RHTPA 2.0.0** without change.

## Step 1.5 — Parent link

Feature has no parent. Prompt "Link this Feature to a parent issue?" — **skipped** (no parent key supplied). No `edit_issue` call made.

## Step 2 — Figma

No Figma URL in arguments or description. Step skipped (backend-only feature).

## Step 2.5 — Issue type discovery

Jira was not contacted (eval). Assumed standard TC project hierarchy:

```
Type-to-role mapping:
  Feature: Feature (ID: 10142, level: 2)
  Epic:    Epic    (level: 1)
  Task:    Task    (level: 0)
```

Hierarchy Configuration override: `Default epic grouping strategy: by-sub-feature` (from CLAUDE.md) — applied without prompt.

## Step 3 — Repository analysis (trustify-backend)

### Relevant modules

| Area | Path | Role in feature |
|---|---|---|
| Migrations | `migration/src/lib.rs`, `migration/src/m0001_initial/mod.rs` | Migrator registry; initial schema that defines `advisory` / `advisory_status` |
| Entities | `entity/src/advisory.rs`, `entity/src/lib.rs` | SeaORM `advisory` entity (holds `status_id` FK + relation today) |
| Advisory model | `modules/fundamental/src/advisory/model/summary.rs`, `details.rs` | `AdvisorySummary` / `AdvisoryDetails` — status serialized as string (must stay a string) |
| Advisory service | `modules/fundamental/src/advisory/service/advisory.rs` | `AdvisoryService` fetch/list/search — joins `advisory_status` |
| Advisory endpoints | `modules/fundamental/src/advisory/endpoints/list.rs`, `get.rs`, `mod.rs` | `GET /api/v2/advisory` (status filter), `GET /api/v2/advisory/{id}` |
| Search | `modules/search/src/service/mod.rs` | `SearchService` full-text search across entities incl. advisories |
| Ingestion | `modules/ingestor/src/graph/advisory/mod.rs`, `modules/ingestor/src/service/mod.rs` | Advisory ingestion: parse, store, correlate — currently writes lookup-table row first |
| Shared query helpers | `common/src/db/query.rs` | Filtering/pagination/sorting helpers used by list endpoints |
| Errors | `common/src/error.rs` | `AppError` |
| Tests | `tests/api/advisory.rs`, `tests/api/search.rs` | Integration tests against real PostgreSQL |

### Discrepancy found

The Feature references `entity/advisory_status.rs`. The analyzed repository tree contains **no** `entity/src/advisory_status.rs` (entity module files: `sbom.rs`, `advisory.rs`, `sbom_advisory.rs`, `package.rs`, `sbom_package.rs`, `package_license.rs`). The lookup table is presumably defined in `migration/src/m0001_initial/mod.rs` and the relation may be inline in `entity/src/advisory.rs`. Task 3 instructs the implementer to delete `entity/src/advisory_status.rs` **only if it exists** and otherwise remove the inline relation/model from `entity/src/advisory.rs`.

### CONVENTIONS.md

`CONVENTIONS.md` exists at the repository root. Its conventions (as captured in the repo analysis): Framework (Axum + SeaORM), Module pattern (`model/ + service/ + endpoints/`), Error handling (`Result<T, AppError>` + `.context()`), Endpoint registration, Response types (`PaginatedResults<T>`), Query helpers (`common/src/db/query.rs`), Testing (integration tests in `tests/api/` against real PostgreSQL, `assert_eq!(resp.status(), StatusCode::OK)`), Caching (`tower-http`). All are Rust (`.rs`) scoped.

### Documentation files discovered

`README.md`, `CONVENTIONS.md`. No `docs/architecture.md` found — the internal architecture doc location must be identified by the documentation task implementer.

### Testing readiness template

`docs/testing-readiness.md` — **not found** in trustify-backend. No testing tasks generated.

### Shared-artifact producer/consumer analysis — `advisory.status`

The advisory status value is a shared artifact (a column read by every advisory query and written by ingestion).

| Kind | Path | Coverage task |
|---|---|---|
| Producer — schema/backfill (one-time) | `migration/src/m0002_advisory_status_enum/mod.rs` (new) | Task 2 |
| Producer — primary ingestion | `modules/ingestor/src/graph/advisory/mod.rs` | Task 6 |
| Producer — ingestion service entry (on-demand/API upload path) | `modules/ingestor/src/service/mod.rs` | Task 6 |
| Schema contract | `entity/src/advisory.rs`, `entity/src/lib.rs` | Task 3 |
| Consumer — list/filter/fetch | `modules/fundamental/src/advisory/service/advisory.rs`, `endpoints/list.rs`, `endpoints/get.rs` | Task 4 |
| Consumer — response models | `modules/fundamental/src/advisory/model/summary.rs`, `details.rs` | Task 4 |
| Consumer — search | `modules/search/src/service/mod.rs` | Task 5 |
| Tests | `tests/api/advisory.rs`, `tests/api/search.rs`, migration up/down tests | Tasks 2, 4, 5, 6 |

No scope exclusions were requested, so no unresolved scope conflicts.

### Duplication-risk / reuse scan

- `common/src/db/query.rs` — reuse existing filter helpers for the `status` equality filter instead of hand-written SQL.
- `migration/src/m0001_initial/mod.rs` — pattern for SeaORM migration structure and the existing `advisory_status` definition (needed for `down()` recreation).
- `entity/src/sbom_advisory.rs` / `entity/src/package_license.rs` — existing SeaORM entity patterns.
- No existing `DeriveActiveEnum` enum in the entity crate was identified; the new `AdvisoryStatus` enum is the single source of truth and must be reused by service, search, and ingestion (no duplicate string-mapping tables).

### Eval infrastructure

Not applicable — no plugin `SKILL.md` is modified.

## Step 4 — Repository Impact Map

```
trustify-backend:
  changes:
    - Add a reversible, atomic migration that creates PostgreSQL enum type advisory_status_enum (New, Analyzing, Fixed, Rejected), adds advisory.status, backfills it from the advisory_status join, drops advisory.status_id, and drops the advisory_status table
    - Register the new migration in the Migrator
    - Update the SeaORM advisory entity to expose a status enum column and remove the status_id column/relation and the advisory_status entity
    - Update AdvisoryService fetch/list/search and the advisory list/get endpoints to read and filter on advisory.status with no join, keeping the response status a string
    - Update SearchService advisory queries to use advisory.status with no join
    - Update the advisory ingestion pipeline to map feed status strings to the enum and write it directly, without inserting into the lookup table
    - Update integration tests for advisory, search, ingestion, and migration up/down
    - Update internal architecture documentation to reflect the schema change
```

### Excluded requirements

None. All seven MVP requirements are covered by tasks.

### Risks / notes for the engineer

- **Zero-downtime vs. destructive migration:** the NFRs require both zero downtime and that the migration drops `status_id` / `advisory_status`. Application instances still running pre-change code during a rolling deploy will fail advisory queries once the table is dropped. Planned as a single atomic migration per the Feature; the deploy procedure (migration and new binary rollout together, or a brief advisory-read maintenance window) must be agreed before the merge task. Not excluded — flagged for attention.
- **Production-sized dataset test** (Customer Considerations) is captured as a Test Requirement in Task 2.

Approval: auto-approved for eval (no interactive user). Would be posted to TC-9005 — see `impact-map-comment.md`.

## Step 4.5 — Workflow mode

**Selected: `feature-branch`** — see `workflow-mode-comment.md`.

Atomicity indicators found:
1. Coordinated schema migration — Task 2 drops `status_id`/`advisory_status`; Tasks 3–6 depend on the new `status` column.
2. Breaking internal data contract — the entity change (Task 3) breaks every consumer (Tasks 4, 5, 6) until they are updated.
3. Cross-cutting refactor — removal of the `advisory_status` entity/relation spans entity, fundamental, search, and ingestor crates.

## Step 5 — Epic grouping (by-sub-feature, auto-approved)

| Epic | Summary | Tasks |
|---|---|---|
| Epic A | TC-9005: Advisory status schema migration | Task 2, Task 3 |
| Epic B | TC-9005: Advisory status query and ingestion updates | Task 4, Task 5, Task 6 |
| Epic C | TC-9005: Feature branch delivery and documentation | Task 1, Task 7, Task 8 |

Epic descriptions (plain text):
- **Epic A:** Create the reversible, atomic migration that replaces the advisory_status lookup table with the advisory_status_enum column on advisory, and update SeaORM entities to match.
- **Epic B:** Move all advisory readers (AdvisoryService, advisory endpoints, SearchService) and the advisory ingestion writer to the new advisory.status enum column with no lookup-table join.
- **Epic C:** Create and merge the TC-9005 feature branch that carries all coordinated changes, and update internal architecture documentation.

## Task list

| # | File | Summary | Epic | Target Branch |
|---|---|---|---|---|
| 1 | task-1-create-feature-branch.md | Create feature branch TC-9005 from main | C | main |
| 2 | task-2-advisory-status-enum-migration.md | Add migration replacing advisory_status table with advisory_status_enum column | A | TC-9005 |
| 3 | task-3-update-seaorm-advisory-entity.md | Update SeaORM advisory entity for status enum column | A | TC-9005 |
| 4 | task-4-advisory-service-endpoints-status-column.md | Use advisory.status column in AdvisoryService and advisory endpoints | B | TC-9005 |
| 5 | task-5-search-service-status-column.md | Use advisory.status column in SearchService | B | TC-9005 |
| 6 | task-6-ingestion-write-status-enum.md | Write advisory status enum directly in ingestion pipeline | B | TC-9005 |
| 7 | task-7-architecture-docs.md | Update internal architecture docs for advisory status enum | C | TC-9005 |
| 8 | task-8-merge-feature-branch.md | Merge feature branch TC-9005 to main | C | main |

Bookend idempotency guard: TC-9005 has no linked issues ("Linked Issues: None") → no existing bookends; generated.

## Step 6 — Task creation log (simulated)

### 6a.0 Epics

All Epics: `issueTypeName=Epic`, `parent=TC-9005`, and

```json
additional_fields: {
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

| Epic | Placeholder key |
|---|---|
| Epic A — Advisory status schema migration | EPIC-A |
| Epic B — Advisory status query and ingestion updates | EPIC-B |
| Epic C — Feature branch delivery and documentation | EPIC-C |

### 6a Tasks

Every task: `issueTypeName=Task`, `projectKey=TC`, and

```json
additional_fields: {
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

| Task | Placeholder key | parent |
|---|---|---|
| Task 1 — Create feature branch TC-9005 from main | TASK-1 | EPIC-C |
| Task 2 — Advisory status enum migration | TASK-2 | EPIC-A |
| Task 3 — SeaORM advisory entity | TASK-3 | EPIC-A |
| Task 4 — AdvisoryService and endpoints | TASK-4 | EPIC-B |
| Task 5 — SearchService | TASK-5 | EPIC-B |
| Task 6 — Ingestion pipeline | TASK-6 | EPIC-B |
| Task 7 — Architecture docs | TASK-7 | EPIC-C |
| Task 8 — Merge feature branch TC-9005 to main | TASK-8 | EPIC-C |

Description digest comment posted on each task immediately after creation: see `task-N-digest.md`.

Feature label update (after all tasks created):

```
jira.edit_issue("TC-9005", fields={"labels": ["ai-generated-jira", "workflow:feature-branch"]})
```

### 6b Links

Incorporates (Feature → Epic): TC-9005 → EPIC-A, TC-9005 → EPIC-B, TC-9005 → EPIC-C.

Depend (dependent → dependency):

| Dependent | Depends on |
|---|---|
| TASK-2 | TASK-1 |
| TASK-3 | TASK-1, TASK-2 |
| TASK-4 | TASK-1, TASK-3 |
| TASK-5 | TASK-1, TASK-3 |
| TASK-6 | TASK-1, TASK-3 |
| TASK-7 | TASK-2, TASK-3, TASK-4, TASK-5, TASK-6 |
| TASK-8 | TASK-2, TASK-3, TASK-4, TASK-5, TASK-6, TASK-7 |

### 6c Summary comment

See `summary-comment.md`.
