# TC-9006 — Repository Impact Map and Plan

**Feature:** TC-9006 — Add vulnerability remediation tracking dashboard
**Priority:** Major · **Fix Versions:** RHTPA 1.5.0 · **Labels:** ai-generated-jira
**Figma:** none linked (Step 2 skipped — no Figma URL in arguments or description)
**Parent link (Step 1.5):** Feature has no parent; prompt would be shown — skipped in this eval (no user input).

> Eval run: no Jira or external services were contacted. Jira keys shown below (TC-9101 … TC-9109) are **simulated** placeholders for what `create_issue` would return.

---

## Step 2.5 — Issue type discovery and hierarchy

Type-to-role mapping (from `jira.get_project_issue_types(2b9e35e3-…, TC)`, mapped by `hierarchyLevel`):

```
Feature: Feature (ID: 10142, level: 2)
Epic:    Epic    (level: 1)          # level-1 type available -> Epics will be created
Task:    Task    (level: 0)
```

- Only one level-1 type exists and it is named "Epic" — selected for the intermediate role.
- **Hierarchy Configuration:** Default epic grouping strategy = **`by-repository`** (per the eval's CLAUDE.md configuration) → one Epic per repository in the impact map. No interactive prompt needed.

Resulting hierarchy: **Feature TC-9006 → Epic (per repository) → Tasks**.

---

## Step 3 — Analysis summary

- No Serena instances configured → analysis performed on the supplied repository structures (`repo-backend.md`, `repo-frontend.md`).
- Both repos contain `CONVENTIONS.md`; their Key Conventions were applied to tasks (with `Applies:` rationale per `shared/convention-applicability-rules.md`).
- No `docs/testing-readiness.md` in either repository → **no testing tasks generated**.
- Documentation signals: **New Content** (dashboard user guide + endpoint reference) → one documentation task generated.
- Existing backend endpoints (`/api/v2/sbom`, `/api/v2/advisory`, `/api/v2/package`, `/api/v2/search`) do not provide remediation aggregation, a product dimension, or a remediation-status filter → new endpoints required.
- Reuse candidates identified: `common/src/db/query.rs`, `common/src/model/paginated.rs::PaginatedResults`, `common/src/error.rs::AppError`, `AdvisorySummary` severity, `entity/src/sbom_advisory.rs`; frontend `FilterToolbar`, `SeverityBadge`, `EmptyStateCard`, `LoadingSpinner`, `severityUtils`, `formatDate`, `src/api/client.ts`.
- Shared-artifact analysis: not applicable — the feature is read-only aggregation over existing data; it adds no producer/writer of a shared artifact.

---

## Step 4 — Repository Impact Map

```
trustify-backend:
  changes:
    - Add a new remediation domain module (model/service/endpoints) in modules/fundamental, mounted in the server
    - Add GET /api/v2/remediation/summary returning counts by severity x status plus a 30-day trend
    - Add GET /api/v2/remediation/by-product returning paginated per-product total/open/in_progress/resolved counts
    - Add GET /api/v2/remediation/vulnerabilities returning a paginated list filterable by severity, product, status
    - Add integration tests for all remediation endpoints in tests/api/remediation.rs
    - Document the new endpoints in README.md

trustify-ui:
  changes:
    - Add remediation response types, API client functions and React Query hooks (+ MSW mocks)
    - Add /remediation dashboard page with Open/In Progress/Resolved summary cards and a 30-day progress chart
    - Add filterable (severity, product, status), sortable, paginated outstanding-vulnerability table to the dashboard
    - Add user documentation for the dashboard and an endpoint reference
```

### Excluded requirements

| Requirement | MVP? | Reason excluded / missing input |
|---|---|---|
| Export remediation report as CSV | No | Non-MVP and under-specified: no definition of which data the report contains (summary vs. per-product vs. filtered table), column set, or whether export is server-side (new endpoint) or client-side. Provide the report contents/columns to plan it. |

### Open questions / assumptions (to confirm before implementation)

1. **Remediation status source.** The feature requires Open / In Progress / Resolved status but forbids new tables. Task 1 assumes status is derivable from existing SBOM↔advisory relationship data (`entity/src/sbom_advisory.rs`) and instructs the implementer to verify the column and stop if it does not exist.
2. **30-day trend source.** The progress chart needs historical per-day counts; with no new tables, the trend must be reconstructable from existing timestamps. Task 1 includes the trend in the summary response and flags the same verification.
3. **Derived requirement:** `GET /api/v2/remediation/vulnerabilities` (Task 3) is not named in the feature but is required to deliver the filterable table (product + status filters, 10,000-row scale).

---

## Step 4.5 — Workflow mode

**Selected mode: `direct-to-main`**

| Atomicity indicator | Present? | Rationale |
|---|---|---|
| Coordinated schema migrations | No | NFR forbids new tables; no migrations. |
| Breaking API changes | No | All endpoints are new and additive; no existing contract changes. |
| Cross-cutting refactors | No | New module and new page only. |
| Tightly coupled components (neither side works alone) | No | Backend endpoints function independently. Frontend tasks depend on backend tasks via Depend links, so backend lands on `main` first and every merge leaves `main` working. |

All tasks target `main`; no bookend tasks generated; `workflow:feature-branch` label not applied.

---

## Step 5 — Epic grouping (by-repository) and tasks

| Epic (simulated key) | Summary | Issue type | Parent | Tasks |
|---|---|---|---|---|
| TC-9101 | `TC-9006: trustify-backend` | Epic (level 1) | TC-9006 | Task 1, Task 2, Task 3 |
| TC-9102 | `TC-9006: trustify-ui` | Epic (level 1) | TC-9006 | Task 4, Task 5, Task 6, Task 7 |

| # | Simulated key | Task | Repository | Parent Epic | Depends on |
|---|---|---|---|---|---|
| 1 | TC-9103 | Add remediation module with summary aggregation endpoint | trustify-backend | TC-9101 | — |
| 2 | TC-9104 | Add per-product remediation breakdown endpoint | trustify-backend | TC-9101 | 1 |
| 3 | TC-9105 | Add filterable remediation vulnerability list endpoint | trustify-backend | TC-9101 | 1 |
| 4 | TC-9106 | Add remediation API models, client functions, and React Query hooks | trustify-ui | TC-9102 | 1, 2, 3 |
| 5 | TC-9107 | Add remediation dashboard page with summary cards and progress chart | trustify-ui | TC-9102 | 4 |
| 6 | TC-9108 | Add filterable vulnerability table to remediation dashboard | trustify-ui | TC-9102 | 4, 5 |
| 7 | TC-9109 | Document the remediation dashboard and aggregation endpoints (documentation task) | trustify-ui | TC-9102 | 1–6 |

Backend tasks (1–3) are numbered before the frontend tasks that depend on them (4–6). The documentation task is placed in trustify-ui (user-facing dashboard guide is the primary doc purpose); backend endpoint README updates are included in Tasks 1–3 as Documentation Updates.

---

## Step 6 — Jira creation parameters (simulated)

### 6a.0 — Epics

```
jira.create_issue(projectKey="TC", issueTypeName="Epic", summary="TC-9006: trustify-backend",
  description=<see epic-1-trustify-backend.md>, parent="TC-9006",
  additional_fields={"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]})
  -> TC-9101

jira.create_issue(projectKey="TC", issueTypeName="Epic", summary="TC-9006: trustify-ui",
  description=<see epic-2-trustify-ui.md>, parent="TC-9006",
  additional_fields={"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]})
  -> TC-9102
```

### 6a — Tasks (`additional_fields` for every task)

```
additional_fields = {
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},            # inherited: Feature priority is "Major" (not Undefined)
  "fixVersions": [{"name": "RHTPA 1.5.0"}]  # inherited: Feature fixVersions non-empty AND fixVersion scope = "both"
}
parent = TC-9101 for Tasks 1-3; TC-9102 for Tasks 4-7
issue type = Task (level 0)
```

Each task is followed immediately by a description digest comment (`task-N-digest.md`). See `task-creation-log.md` for per-task details.

### 6b — Links

Incorporates links go from the Feature to each **Epic** (not to individual tasks — tasks inherit hierarchy through their Epic parent):

```
jira.create_issue_link(link_type="Incorporates", inward_issue_key="TC-9006", outward_issue_key="TC-9101")
jira.create_issue_link(link_type="Incorporates", inward_issue_key="TC-9006", outward_issue_key="TC-9102")
```

Depend links (dependent → dependency):

| Dependent | Depends on |
|---|---|
| TC-9104 (Task 2) | TC-9103 (Task 1) |
| TC-9105 (Task 3) | TC-9103 (Task 1) |
| TC-9106 (Task 4) | TC-9103, TC-9104, TC-9105 |
| TC-9107 (Task 5) | TC-9106 |
| TC-9108 (Task 6) | TC-9106, TC-9107 |
| TC-9109 (Task 7) | TC-9103, TC-9104, TC-9105, TC-9106, TC-9107, TC-9108 |

### Inherited field summary

- **Priority:** `Major` — propagated to both Epics and all 7 tasks.
- **fixVersions:** `RHTPA 1.5.0` — propagated to both Epics and all 7 tasks (`fixVersion scope: both`).

---

## Step 6c — Summary comment on TC-9006 (what would be posted)

### Implementation plan created for TC-9006

**Hierarchy:** TC-9006 (Feature) → 2 Epics (by-repository) → 7 Tasks. Incorporates links: TC-9006 → TC-9101, TC-9006 → TC-9102.

**TC-9101 — TC-9006: trustify-backend**
- TC-9103 — Add remediation module with summary aggregation endpoint
- TC-9104 — Add per-product remediation breakdown endpoint (depends on TC-9103)
- TC-9105 — Add filterable remediation vulnerability list endpoint (depends on TC-9103)

**TC-9102 — TC-9006: trustify-ui**
- TC-9106 — Add remediation API models, client functions, and React Query hooks (depends on TC-9103, TC-9104, TC-9105)
- TC-9107 — Add remediation dashboard page with summary cards and progress chart (depends on TC-9106)
- TC-9108 — Add filterable vulnerability table to remediation dashboard (depends on TC-9106, TC-9107)
- TC-9109 — Document the remediation dashboard and aggregation endpoints (depends on all implementation tasks)

**Repositories affected:** trustify-backend, trustify-ui

**Architecture summary:** A new `remediation` module in trustify-backend (`modules/fundamental/src/remediation/`, model/service/endpoints pattern) computes aggregations with grouped SQL over the existing SBOM↔advisory relationship (no new tables, p95 < 500ms target) and exposes `/api/v2/remediation/summary`, `/by-product` (paginated), and `/vulnerabilities` (filterable, paginated). In trustify-ui, typed API functions and React Query hooks back a new lazy-loaded `/remediation` PatternFly 5 page: summary cards, a 30-day trend chart, and a server-side filtered table that reuses `FilterToolbar` and `SeverityBadge`. Error states are kept separate from empty states so a failed request never shows as zero counts. Workflow mode: `direct-to-main`. Excluded: CSV export (non-MVP; report contents not specified).

**Inherited fields:**
- Priority: `Major`, inherited from the Feature and set on both Epics and all 7 tasks.
- fixVersion: `RHTPA 1.5.0`, inherited from the Feature and set on both Epics and all 7 tasks (`fixVersion scope: both`).

---

This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.
