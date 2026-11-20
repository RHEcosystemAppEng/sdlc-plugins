# TC-9006 — Repository Impact Map

Feature: **TC-9006 — Add vulnerability remediation tracking dashboard**
Priority: Major | Fix Versions: RHTPA 1.5.0 | Labels: ai-generated-jira

## Planning context and assumptions

- **Step 0 (config validation):** Repository Registry, Jira Configuration (project key TC, Cloud ID, Feature type ID 10142) and Code Intelligence sections present — PASS. The eval's repositories (`trustify-backend`, `trustify-ui`) are taken from the supplied fixture files `repo-backend.md` and `repo-frontend.md`.
- **Step 1.5 (parent link):** Feature has no parent. The interactive prompt would be shown; non-interactive eval assumption: user pressed Enter (skip). No parent link set.
- **Step 2 (Figma):** No Figma URL in the arguments or the Feature description. No design inspection was done. Frontend tasks use standard PatternFly 5 layouts and say that no design is available.
- **Step 2.5 (issue types):** Type-to-role mapping:
  - Feature: Feature (ID: 10142, level: 2)
  - Epic: **Epic** (level: 1). This is the single level-1 type, named "Epic", so it is selected automatically.
  - Task: Task (level: 0)
- **Hierarchy Configuration:** the default Epic grouping strategy is **`by-repository`** (as specified for this run), so no grouping prompt is shown.
- **Step 3 (analysis):** No Serena instances are configured. Repository structure comes from the fixture trees. Both repos contain `CONVENTIONS.md`, and the Key Conventions in the fixtures were used for convention enrichment. The fixture trees have no `docs/testing-readiness.md`, so **no testing tasks** are generated. The Feature has a Documentation Considerations section ("New Content"), so **one documentation task** is generated.
- **Shared-artifact analysis:** not applicable. No acceptance criterion depends on a shared artifact with multiple producers. All new endpoints are read-only aggregations over existing entities.
- **Fail-open risks:** the Feature does not name any silent/empty-success risk. As a defensive measure, the frontend tasks still require error states that never show zero counts or an empty table when a request fails.

## Repository Impact Map

```
trustify-backend:
  changes:
    - Add a remediation domain module (model + service) that computes severity x status counts, per-product breakdown, a filterable vulnerability list and a 30-day trend from existing advisory/SBOM relationship data (no new tables)
    - Add GET /api/v2/remediation/summary endpoint (aggregated counts by severity x status)
    - Add GET /api/v2/remediation/by-product endpoint (paginated per-product total/open/resolved counts)
    - Add GET /api/v2/remediation/vulnerabilities endpoint (filter by severity, product, status; paginated; sortable)
    - Add GET /api/v2/remediation/trend endpoint (daily status counts, default 30 days)
    - Mount remediation routes in the server and add integration tests in tests/api/remediation.rs
    - Document the remediation dashboard and endpoints (New Content)

trustify-ui:
  changes:
    - Add remediation TypeScript types, REST client functions, React Query hooks and MSW mocks/fixtures
    - Add /remediation dashboard page with summary cards (Open / In Progress / Resolved) and 30-day trend chart
    - Add filterable (severity, product, status), sortable, server-paginated vulnerability table to the dashboard, with E2E coverage
```

## Excluded / deferred requirements

| Requirement | MVP? | Status | Reason / missing input |
|---|---|---|---|
| Export remediation report as CSV | No | **Deferred, not planned** | Non-MVP. The Feature does not specify the CSV column set, the filter scope (current filters or the full portfolio), or where the export lives (backend endpoint or client-side). These need to be specified before the work can be broken into tasks. |

## Open questions / risks (carried into task Implementation Notes)

1. **Source of remediation status:** the documented entities (`entity/src/sbom_advisory.rs`, `entity/src/advisory.rs`) have no explicit Open/In Progress/Resolved status column. The NFR forbids new tables. Task 1 tells the implementer to confirm the source column and to escalate rather than add a table.
2. **Source of trend history:** the 30-day trend chart needs timestamps on the relationship or advisory data. If none exist, the trend requirement may need to be descoped or redesigned.
3. **No Figma design:** the UI layout is based on PatternFly defaults.

## Workflow mode decision (Step 4.5)

**Mode: `direct-to-main`**

Rationale. Each atomicity indicator was checked:
1. *Coordinated schema migrations:* none. The NFR forbids new tables, and no migration is planned.
2. *Breaking API changes:* none. All four endpoints are new and additive. No existing contract changes.
3. *Cross-cutting refactors:* none.
4. *Tightly coupled components:* not present in a way that breaks `main`. The backend endpoints work and are useful on their own. The frontend tasks depend on them, and the Dependencies sections enforce the order: the backend merges first (Tasks 1→2→3), then the frontend (Tasks 4→5→6). The frontend API layer (Task 4) has no UI entry point, and the page (Task 5) only needs endpoints that have already merged. No single PR leaves either repository's `main` broken.

All tasks therefore target `main`. No bookend tasks are generated, and the `workflow:feature-branch` label is not applied.

## Epic grouping (strategy: by-repository)

| Epic (placeholder key) | Summary | Issue type | Parent | Tasks |
|---|---|---|---|---|
| TC-9007 | `TC-9006: trustify-backend` | Epic (level 1) | TC-9006 | Task 1, Task 2, Task 3, Task 7 |
| TC-9008 | `TC-9006: trustify-ui` | Epic (level 1) | TC-9006 | Task 4, Task 5, Task 6 |

Epic descriptions (plain text):
- **TC-9006: trustify-backend**: "Backend work for the vulnerability remediation tracking dashboard: remediation model and aggregation service, the summary, by-product, vulnerabilities and trend endpoints under /api/v2/remediation, integration tests, and documentation of the dashboard and endpoints."
- **TC-9006: trustify-ui**: "Frontend work for the vulnerability remediation tracking dashboard: remediation API client, types and hooks, the /remediation dashboard page with summary cards and trend chart, and the filterable vulnerability table."

## Task list and parent assignment

| # | Task | Repository | Parent Epic | Depends on | Placeholder key |
|---|---|---|---|---|---|
| 1 | Add remediation model and aggregation service | trustify-backend | TC-9007 (TC-9006: trustify-backend) | — | TC-9009 |
| 2 | Add remediation summary and by-product endpoints | trustify-backend | TC-9007 (TC-9006: trustify-backend) | 1 | TC-9010 |
| 3 | Add remediation vulnerabilities list and trend endpoints | trustify-backend | TC-9007 (TC-9006: trustify-backend) | 1, 2 | TC-9011 |
| 4 | Add remediation API client, types and React Query hooks | trustify-ui | TC-9008 (TC-9006: trustify-ui) | 2, 3 | TC-9012 |
| 5 | Create remediation dashboard page with summary cards and trend chart | trustify-ui | TC-9008 (TC-9006: trustify-ui) | 4 | TC-9013 |
| 6 | Add filterable vulnerability table to the remediation dashboard | trustify-ui | TC-9008 (TC-9006: trustify-ui) | 4, 5 | TC-9014 |
| 7 | Document remediation dashboard and endpoints (documentation) | trustify-backend | TC-9007 (TC-9006: trustify-backend) | 2, 3, 5, 6 | TC-9015 |

Backend implementation tasks (1–3) are numbered before the frontend tasks (4–6) that depend on them. The documentation task is last.

## Inherited fields (`additional_fields`) applied to every Epic and Task

- `labels`: `["ai-generated-jira"]`
- `priority`: `{"name": "Major"}`. Inherited from the Feature, which has priority "Major" (not "Undefined"), so it is propagated.
- `fixVersions`: `[{"name": "RHTPA 1.5.0"}]`. Inherited because the Feature has a non-empty fixVersions array and `fixVersion scope` in CLAUDE.md Jira Field Defaults is `both`.

See `task-creation-log.md` for the full create and link call parameters.

## Links (Step 6b)

- **Incorporates:** from Feature TC-9006 to each **Epic** only (TC-9006 → TC-9007, TC-9006 → TC-9008). No Incorporates links go to individual Tasks. Tasks belong to the hierarchy through their Epic `parent`.
- **Depend:** from each task to the tasks it depends on (see the task list above).
