# Repository Impact Map -- TC-9006

## Feature

**Key**: TC-9006
**Summary**: Add vulnerability remediation tracking dashboard
**Priority**: Major
**Fix Versions**: RHTPA 1.5.0

## Epic Hierarchy

Epics are grouped **by-repository** (default strategy from CLAUDE.md Hierarchy Configuration).

| Epic Key | Summary | Issue Type | Parent | Repository |
|---|---|---|---|---|
| TC-9007 | TC-9006: trustify-backend | Epic (hierarchyLevel 1) | TC-9006 | trustify-backend |
| TC-9008 | TC-9006: trustify-ui | Epic (hierarchyLevel 1) | TC-9006 | trustify-ui |

### Epic Creation Details

Each Epic is created with:
- **Issue type name**: Epic (hierarchyLevel 1)
- **Parent**: TC-9006 (Feature issue key)
- **additional_fields**:
  ```json
  {
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "RHTPA 1.5.0"}]
  }
  ```
- Priority "Major" inherited from Feature TC-9006 (not "Undefined", so included)
- fixVersions "RHTPA 1.5.0" inherited from Feature TC-9006 (Feature has non-empty fixVersions; no `fixVersion scope` setting in Jira Field Defaults, so default "both" applies -- propagate to Epics and Tasks)

### Incorporates Links (Feature to Epics)

- TC-9006 **Incorporates** --> TC-9007 (Epic: trustify-backend)
- TC-9006 **Incorporates** --> TC-9008 (Epic: trustify-ui)

Note: Incorporates links are from Feature to Epics only, not from Feature to individual Tasks. Tasks inherit hierarchy through their Epic parent.

### Task Creation Details

Each Task is created with:
- **Issue type name**: Task (hierarchyLevel 0)
- **Parent**: assigned Epic key (TC-9007 for backend tasks, TC-9008 for frontend tasks)
- **additional_fields**:
  ```json
  {
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "RHTPA 1.5.0"}]
  }
  ```

## Impact

### trustify-backend

changes:
- Add remediation data models (RemediationSummary, RemediationByProduct structs) following the model/ + service/ + endpoints/ module pattern
- Add remediation aggregation service to compute remediation counts from existing vulnerability and SBOM relationship data (no new database tables)
- Add `GET /api/v2/remediation/summary` endpoint returning aggregated counts by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved)
- Add `GET /api/v2/remediation/by-product` endpoint returning per-product remediation breakdown with total, open, resolved counts
- Add integration tests for both remediation endpoints using PostgreSQL test database

### trustify-ui

changes:
- Add TypeScript interfaces for remediation API response types in the API models layer
- Add Axios client functions for remediation endpoints (fetchRemediationSummary, fetchRemediationByProduct)
- Add React Query hooks (useRemediationSummary, useRemediationByProduct) for remediation data fetching
- Add RemediationDashboardPage at `/remediation` with summary cards (Open, In Progress, Resolved counts) and progress chart (30-day trend)
- Add filterable vulnerability table component with severity, product, and status filters
- Add route registration for `/remediation` and navigation entry
- Add unit/component tests for remediation dashboard using Vitest + React Testing Library + MSW

## Excluded Requirements

- **Export remediation report as CSV** (for management reporting) -- Explicitly marked as non-MVP in the Feature description. This requirement can be planned as a follow-up feature once the core remediation dashboard is implemented and validated.

## Workflow Mode

**Selected mode**: direct-to-main

**Rationale**: No atomicity indicators were identified:

1. **No coordinated schema migrations** -- the Feature explicitly requires no new database tables; aggregations are computed from existing vulnerability and SBOM relationship data.
2. **No breaking API changes** -- all endpoints are new additions (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`) that do not modify existing API contracts.
3. **No cross-cutting refactors** -- changes are confined to new modules in each repository with no structural modifications to existing code.
4. **No tightly coupled cross-repo deployment** -- the backend adds new endpoints that function independently (returning data from existing tables), and the frontend adds a new page at `/remediation` that does not affect existing pages. Neither partial delivery breaks existing functionality on `main`.

All tasks target `main` branch.

## Task-to-Epic Assignment

### Epic TC-9007: trustify-backend
| Task | Summary | Parent Epic |
|---|---|---|
| Task 1 | Add remediation data models and aggregation service | TC-9007 |
| Task 2 | Add remediation summary and by-product endpoints | TC-9007 |
| Task 3 | Add integration tests for remediation endpoints | TC-9007 |
| Task 8 | Document remediation dashboard and aggregation API endpoints | TC-9007 |

### Epic TC-9008: trustify-ui
| Task | Summary | Parent Epic |
|---|---|---|
| Task 4 | Add remediation API types, client functions, and React Query hooks | TC-9008 |
| Task 5 | Add RemediationDashboardPage with summary cards and progress chart | TC-9008 |
| Task 6 | Add filterable vulnerability table to remediation dashboard | TC-9008 |
| Task 7 | Add route registration, navigation, and tests for remediation dashboard | TC-9008 |

## Dependency Graph

```
Task 1 (backend models/service)
  --> Task 2 (backend endpoints)
        --> Task 3 (backend tests)
        --> Task 4 (frontend API types/hooks)
              --> Task 5 (dashboard page)
                    --> Task 6 (vulnerability table)
                    --> Task 7 (route/nav/tests)
Tasks 1-7 --> Task 8 (documentation)
```

## Documentation Signals

- **Doc impact type**: New Content
- **Details**: Security teams need a guide for using the dashboard; API consumers need endpoint reference
- **Action**: Documentation task (Task 8) generated to cover API reference and dashboard user guide

---

*This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.*
