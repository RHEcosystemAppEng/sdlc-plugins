# Repository Impact Map — TC-9003: SBOM comparison view

## Planning context

- **Feature**: TC-9003 — SBOM comparison view
- **Priority**: Critical (propagated to all created issues)
- **Fix Versions**: RHTPA 1.5.0 (propagated — `fixVersion scope: both`)
- **Labels on feature**: `ai-generated-jira` (+ `workflow:feature-branch` to be appended, see Workflow Mode)
- **Figma**: https://www.figma.com/design/mock123/SBOMCompare (design context from `figma-context.md`)
- **Repositories analyzed**: `trustify-backend` (Rust / Axum / SeaORM), `trustify-ui` (React 18 / TypeScript / PatternFly 5)
- **Code intelligence**: no Serena instances configured — analysis performed with Read on the repository structure descriptions (fallback path)
- **Documentation signals (Step 1)**: Doc Impact = **New Content** — document the comparison endpoint (API consumers) and the comparison UI workflow (UI users)
- **Testing readiness template (Step 3)**: no `docs/testing-readiness.md` discovered in either target repository — no testing tasks generated
- **Parent issue (Step 1.5)**: feature has no parent; linking skipped (non-interactive eval run)

## Issue type discovery (Step 2.5)

Jira was not contacted in this run, so `get_project_issue_types` could not be called. No level-1 (Epic) issue type could be confirmed, so the skill uses the graceful-degradation path: **Feature -> Task**, with no Epic creation. The `Default epic grouping strategy: by-sub-feature` setting in CLAUDE.md is recorded, but it does not apply when no Epic type is discovered. If a re-run against live Jira finds a level-1 type, the by-sub-feature groups would be:

- "TC-9003: Comparison API" — Tasks 2, 3
- "TC-9003: Comparison UI" — Tasks 4, 5, 6, 7, 8
- "TC-9003: Delivery & docs" — Tasks 1, 9, 10

Type-to-role mapping used:
```
Feature: Feature (ID: 10142, level: 2)   # from Jira Configuration
Epic:    (none discovered)
Task:    Task (level: 0)
```

## Discovered backend API contracts

| Endpoint | Method | Status | Source |
|---|---|---|---|
| `/api/v2/sbom` | GET | Existing. Returns `PaginatedResults<SbomSummary>` (`{ items: SbomSummary[], total: number }`) | `modules/fundamental/src/sbom/endpoints/list.rs`, `common/src/model/paginated.rs`, `modules/fundamental/src/sbom/model/summary.rs` |
| `/api/v2/sbom/{id}` | GET | Existing. Returns `SbomDetails` | `modules/fundamental/src/sbom/endpoints/get.rs`, `modules/fundamental/src/sbom/model/details.rs` |
| `/api/v2/sbom/compare?left={id1}&right={id2}` | GET | **NEW**. Returns `SbomComparison` (shape below) | to be created at `modules/fundamental/src/sbom/endpoints/compare.rs` |

`SbomComparison` response shape (agreed with the Figma backend-interaction spec):
```json
{
  "added_packages":           [{ "name": "string", "version": "string", "license": "string|null", "advisory_count": 0 }],
  "removed_packages":         [{ "name": "string", "version": "string", "license": "string|null", "advisory_count": 0 }],
  "version_changes":          [{ "name": "string", "left_version": "string", "right_version": "string", "direction": "upgrade|downgrade" }],
  "new_vulnerabilities":      [{ "advisory_id": "string", "severity": "critical|high|medium|low", "title": "string", "affected_package": "string" }],
  "resolved_vulnerabilities": [{ "advisory_id": "string", "severity": "critical|high|medium|low", "title": "string", "previously_affected_package": "string" }],
  "license_changes":          [{ "name": "string", "left_license": "string|null", "right_license": "string|null" }]
}
```

## Shared-artifact analysis

The comparison is **read-only**. It computes a diff on the fly from data that already exists (`sbom_package`, `package`, `package_license`, `sbom_advisory`, `advisory`). It writes no shared artifact, and the NFR says no new tables. Producers of that source data (the SBOM and advisory ingestion in `modules/ingestor/src/graph/sbom/mod.rs` and `modules/ingestor/src/graph/advisory/mod.rs`) do not change. Consumers of the new diff: the comparison page (Task 6) and the export action (Task 8). No scope conflict was found.

## Impact map

```
trustify-backend:
  changes:
    - Add SbomComparison response model types (added/removed packages, version changes, new/resolved vulnerabilities, license changes)
    - Add on-the-fly diff computation for two SBOMs in the SBOM service, built from existing package, license and advisory data (no new tables)
    - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint and register it in the SBOM route module
    - Return 404 when either SBOM ID does not exist and 400 when a parameter is missing or invalid (never an empty diff)
    - Add integration tests for the compare endpoint in tests/api/sbom.rs
    - Document the compare endpoint in the backend README

trustify-ui:
  changes:
    - Add TypeScript types for the comparison response, an API client function, and a React Query hook for the compare endpoint
    - Add MSW handler and fixture for the compare endpoint
    - Add comparison diff-section components (six collapsible sections with colored count badges, sortable tables, highlighted critical rows, and virtualization above 100 rows)
    - Add the /sbom/compare page with SBOM selectors, a Compare button, URL-encoded left/right state, and empty and loading states
    - Register the /sbom/compare route (lazy-loaded)
    - Add multi-select checkboxes and a "Compare selected" action to the SBOM list page
    - Add Export JSON / Export CSV dropdown on the comparison page (non-MVP)
    - Add user-facing documentation for the comparison workflow and API reference
```

## Excluded requirements

| Requirement | Reason excluded / missing input |
|---|---|
| "Add comparison endpoint to the API latency Grafana dashboard" (Supportability) | **No target repository.** Neither the dashboard definitions nor the monitoring configuration are in the Repository Registry, so this cannot be broken into tasks. Please give the repository that holds the Grafana dashboards. |
| "Monitor for timeouts on large SBOM comparisons (>2000 packages per SBOM)" (Supportability) | **No target repository** for alerting/monitoring config (same as above). The backend task does add tracing spans and timing on the compare handler so the data can be collected. |
| "Both SBOMs must be from the same product/project for a meaningful comparison" (Customer Considerations) | **Insufficient specification.** The repository analysis found no product/project field on `SbomSummary`/`SbomDetails`. The feature also does not say whether a cross-product comparison should be rejected (4xx), allowed with a warning, or blocked in the UI. Please clarify the expected behavior and the field that identifies the product. |
| "Large SBOM diffs (>1000 package changes) may require pagination or filtering" (Customer Considerations) | **Insufficient specification.** The wording is "may require" with no defined behavior, and the Figma spec says "no pagination (virtualized for >100 rows)". The planned tasks follow Figma: one full response plus client-side virtualization. Server-side pagination/filtering is not planned until it is specified. |

Note: "Export diff as JSON or CSV" is **non-MVP**, but it **is planned** (Task 8) because the Figma design fully specifies it and it needs no backend change.

## Workflow mode decision (Step 4.5)

**Selected mode: `feature-branch`**

Atomicity indicators evaluated:

1. Coordinated schema migrations — **not present** (no new tables, no migrations).
2. Breaking API changes — **not present** (the new endpoint is additive).
3. Cross-cutting refactors — **not present**.
4. Tightly coupled feature components — **PRESENT**. The new `/sbom/compare` page (Tasks 5, 6) and the "Compare selected" action (Task 7) call `GET /api/v2/sbom/compare`, which does not exist yet (Tasks 2, 3). If the UI tasks merge to `main` alone, users get a navigable page whose every comparison fails.

Interdependent tasks: Task 4 (API client/hook) -> Task 3 (endpoint contract); Task 6 (page) -> Tasks 4, 5; Task 7 (list action) -> Task 6; Task 8 (export) -> Task 6.

Consequences:
- Bookend tasks are generated: Task 1 (create branch `TC-9003`) and Task 10 (merge `TC-9003` to `main`). Both are placed in `trustify-ui`, where the majority of implementation tasks land (5 of 7 code tasks).
- All intermediate tasks use Target Branch `TC-9003`.
- The label `workflow:feature-branch` is appended to TC-9003 (existing label `ai-generated-jira` is kept).
- **Cross-repo caveat for reviewer:** the bookend rules allow one repository per bookend task. The backend tasks (2, 3) also target `TC-9003`, so a `TC-9003` branch is needed in `trustify-backend` too. Task 2's Implementation Notes tell the implementer to create `TC-9003` from `main` in `trustify-backend` if it is missing. Backend changes reach `main` through a backend PR from `TC-9003` that is raised together with the Task 10 merge.

## Task list

| # | Summary | Repository | Target Branch | Depends on |
|---|---|---|---|---|
| 1 | Create feature branch TC-9003 from main | trustify-ui | main | — |
| 2 | Add SBOM comparison diff model and service | trustify-backend | TC-9003 | 1 |
| 3 | Add GET /api/v2/sbom/compare endpoint | trustify-backend | TC-9003 | 1, 2 |
| 4 | Add comparison API client, types, and React Query hook | trustify-ui | TC-9003 | 1, 3 |
| 5 | Add comparison diff section components | trustify-ui | TC-9003 | 1, 4 |
| 6 | Add SBOM comparison page at /sbom/compare | trustify-ui | TC-9003 | 1, 4, 5 |
| 7 | Add multi-select and "Compare selected" to SBOM list page | trustify-ui | TC-9003 | 1, 6 |
| 8 | Add JSON/CSV export to SBOM comparison page (non-MVP) | trustify-ui | TC-9003 | 1, 6 |
| 9 | Document SBOM comparison endpoint and UI workflow | trustify-ui | TC-9003 | 1, 3, 6, 7, 8 |
| 10 | Merge feature branch TC-9003 to main | trustify-ui | main | 2, 3, 4, 5, 6, 7, 8, 9 |

## `additional_fields` for every created issue

Feature priority = `Critical` (not "Undefined", so it is propagated). Feature fixVersions = `[RHTPA 1.5.0]` (non-empty, and `fixVersion scope: both`, so it is propagated).

```json
{
  "labels": ["ai-generated-jira"],
  "priority": { "name": "Critical" },
  "fixVersions": [{ "name": "RHTPA 1.5.0" }]
}
```

Applied identically to Tasks 1–10. No `parent` field is set (no Epic type discovered). See `task-creation-log.md` for per-task create calls, links, and digests.

---
This comment was AI-generated by [sdlc-workflow/plan-feature](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10.
