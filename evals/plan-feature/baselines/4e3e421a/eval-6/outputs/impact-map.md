# Repository Impact Map — TC-9006: Add vulnerability remediation tracking dashboard

> This is the comment that would be posted to TC-9006 via `jira.add_comment` after user approval (Step 4).

## Feature inputs (Step 1)

- **Feature**: TC-9006 — Add vulnerability remediation tracking dashboard
- **Priority**: Major (set, not "Undefined" → will be inherited)
- **fixVersions**: `[RHTPA 1.5.0]` (non-empty → will be inherited, `fixVersion scope: both`)
- **Labels on Feature**: `ai-generated-jira`
- **Figma**: none linked; Step 2 skipped
- **Documentation signals**: Doc Impact = **New Content** (dashboard guide + endpoint reference) → documentation task generated
- **Parent link (Step 1.5)**: Feature has no parent. The user was prompted to link a parent Outcome. No key was given (non-interactive eval run), so this step was skipped.

## Issue type discovery (Step 2.5)

```
Type-to-role mapping:
  Feature: Feature (ID: 10142, level: 2)
  Epic:    Epic    (level: 1)      # level-1 type found → Epic hierarchy enabled
  Task:    Task    (level: 0)
```

- **Epic grouping strategy**: `by-repository` (taken from the Hierarchy Configuration default given for this run; no interactive prompt)
- **Resulting hierarchy**: Feature TC-9006 → Epic per repository → Tasks

## Repository analysis notes (Step 3)

- No Serena instances are configured. Analysis used the repository structure documents (`repo-backend.md`, `repo-frontend.md`).
- Both repos have `CONVENTIONS.md`. Their Key Conventions were applied to tasks, with an `Applies:` rationale for each one used.
- Neither repo has `docs/testing-readiness.md`, so no testing tasks were generated.
- Docs found: `README.md` in each repo, plus `CONVENTIONS.md`.
- Backend API discovery: none of the needed endpoints exist yet (the existing routes are `/api/v2/sbom`, `/api/v2/advisory`, `/api/v2/package` and `/api/v2/search`). Contracts for the new endpoints are defined in backend Tasks 1–3 and repeated in frontend Tasks 4–6, with an instruction to verify them against the backend at implementation time.
- Shared-artifact analysis: not applicable. The work is read-only aggregation; no shared artifact has more than one writer.

## Impact map

```
trustify-backend:
  changes:
    - Add a new `remediation` domain module (model/service/endpoints) in modules/fundamental
    - Add GET /api/v2/remediation/summary — counts by severity × status, computed from sbom_advisory + advisory data (no new tables)
    - Add GET /api/v2/remediation/by-product — paginated per-product total/open/in_progress/resolved counts
    - Add GET /api/v2/remediation/vulnerabilities — filterable (severity, product, status), sortable, paginated outstanding vulnerability list backing the dashboard table
    - Mount remediation routes in server/src/main.rs
    - Add integration tests in tests/api/remediation.rs
    - Document dashboard and endpoints (New Content)

trustify-ui:
  changes:
    - Add remediation response types, REST client functions, and React Query hooks
    - Add MSW handlers and fixtures for remediation endpoints
    - Add /remediation route and RemediationDashboardPage with summary cards and progress chart
    - Add filterable/sortable/paginated vulnerability table to the dashboard
    - Add unit and Playwright E2E tests for the dashboard
```

## Excluded requirements

| Requirement | MVP? | Reason not planned / missing input |
|---|---|---|
| Export remediation report as CSV | No | Marked non-MVP in the Feature. It is left out of this MVP plan and has no export format spec (columns, filters applied, sync vs. async). Needs a separate request with a format spec if wanted. |
| Progress chart "shows trend over the past 30 days" (part of the MVP dashboard requirement) | Yes (partially) | No source of historical remediation-status data was found in the backend entities, and the NFR forbids new tables. The chart is planned against current status-by-severity data (Task 5). **The 30-day trend view is still unresolved** until the feature owner names a source, e.g. existing timestamps on `sbom_advisory`/advisory records. |

## Open questions (need feature-owner confirmation before or during implementation)

1. **How is remediation status derived?** Open, In Progress and Resolved are not explicit columns in the listed entities (`sbom_advisory`, `advisory`). Task 1 keeps the derivation in a single `RemediationService` function so the rule can be adjusted in one place.
2. **What is a "product"?** There is no product entity. Tasks 2 and 3 assume products come from SBOM identity in `entity/src/sbom.rs`.

## Workflow mode (Step 4.5)

**direct-to-main**. See `workflow-mode-decision.md` for the reasoning.

## Epics and task assignment (Step 5 / 6a.0)

Simulated Jira keys are shown in brackets. Real keys would come from `create_issue`.

| Epic | Summary | Issue type | Parent | Tasks |
|---|---|---|---|---|
| Epic A [TC-9010] | `TC-9006: trustify-backend` | Epic (level 1) | TC-9006 | Task 1, Task 2, Task 3, Task 7 |
| Epic B [TC-9011] | `TC-9006: trustify-ui` | Epic (level 1) | TC-9006 | Task 4, Task 5, Task 6 |

| # | Task | Repository | Parent Epic | Target Branch | Depends on |
|---|---|---|---|---|---|
| 1 [TC-9012] | Add remediation module and summary endpoint | trustify-backend | TC-9010 (`TC-9006: trustify-backend`) | main | — |
| 2 [TC-9013] | Add remediation by-product endpoint | trustify-backend | TC-9010 | main | 1 |
| 3 [TC-9014] | Add remediation vulnerability list endpoint | trustify-backend | TC-9010 | main | 1, 2 |
| 4 [TC-9015] | Add remediation API client types and React Query hooks | trustify-ui | TC-9011 (`TC-9006: trustify-ui`) | main | 1, 2, 3 |
| 5 [TC-9016] | Create remediation dashboard page with summary cards and progress chart | trustify-ui | TC-9011 | main | 4 |
| 6 [TC-9017] | Add filterable remediation vulnerability table | trustify-ui | TC-9011 | main | 4, 5 |
| 7 [TC-9018] | Document remediation dashboard and aggregation endpoints | trustify-backend | TC-9010 | main | 1–6 |

Backend tasks (1–3) have lower numbers than the frontend tasks that depend on them (4–6).

## Inherited fields / `additional_fields`

All Epics and Tasks get the same `additional_fields`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- **priority**: `Major` is propagated because the Feature's priority is set and is not "Undefined".
- **fixVersions**: `RHTPA 1.5.0` is propagated because the Feature's fixVersions are non-empty and `fixVersion scope` is `both`.

## Links (Step 6b)

- **Incorporates** links go from Feature to Epics only, not to individual Tasks:
  - TC-9006 → TC-9010 (`TC-9006: trustify-backend`)
  - TC-9006 → TC-9011 (`TC-9006: trustify-ui`)
- **Depend** links follow the task Dependencies; see `task-creation-log.md`.

---

This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.
