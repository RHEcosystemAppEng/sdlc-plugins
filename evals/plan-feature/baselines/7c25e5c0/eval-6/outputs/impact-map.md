# Repository Impact Map — TC-9006

## Feature Summary

**TC-9006: Add vulnerability remediation tracking dashboard**

Backend aggregation endpoints for remediation status by severity and product, plus a frontend dashboard page with summary cards, progress chart, and filterable vulnerability table.

## Workflow Mode

**direct-to-main** — No atomicity constraints identified. Backend endpoints can land independently (consumers handle missing endpoints gracefully via React Query error states), and frontend pages can be merged once endpoints are available. No coordinated schema migrations or breaking API changes.

## Epic Hierarchy

**Grouping strategy:** by-repository (from CLAUDE.md Hierarchy Configuration)

| Epic | Summary | Issue Type | Parent |
|------|---------|------------|--------|
| Epic 1 | TC-9006: trustify-backend | Epic (level 1) | TC-9006 |
| Epic 2 | TC-9006: trustify-ui | Epic (level 1) | TC-9006 |

**Link decisions:**
- Feature TC-9006 → Incorporates → Epic 1 (TC-9006: trustify-backend)
- Feature TC-9006 → Incorporates → Epic 2 (TC-9006: trustify-ui)
- Individual Tasks are NOT linked directly to Feature — they inherit hierarchy through their parent Epic

## Epic 1: TC-9006: trustify-backend

Epic creation parameters:
- Issue type: Epic (hierarchyLevel: 1)
- Summary: TC-9006: trustify-backend
- Parent: TC-9006
- Labels: ["ai-generated-jira"]
- Priority: Major (inherited from Feature)
- Fix Versions: RHTPA 1.5.0 (inherited from Feature)

### Changes

trustify-backend:
  changes:
    - Add RemediationSummary model struct with severity × status counts (Critical/High/Medium/Low × Open/In Progress/Resolved)
    - Add RemediationByProduct model struct with per-product total/open/resolved counts
    - Add RemediationService with summary() and by_product() aggregation methods querying existing vulnerability/SBOM relationship data
    - Add GET /api/v2/remediation/summary endpoint handler returning aggregated counts
    - Add GET /api/v2/remediation/by-product endpoint handler returning per-product breakdown
    - Register remediation routes in server route mounting
    - Add integration tests for both remediation endpoints

### Tasks under this Epic

- Task 1: Remediation models (parent: Epic 1)
- Task 2: Remediation service (parent: Epic 1)
- Task 3: Remediation endpoints (parent: Epic 1)
- Task 4: Backend integration tests (parent: Epic 1)

## Epic 2: TC-9006: trustify-ui

Epic creation parameters:
- Issue type: Epic (hierarchyLevel: 1)
- Summary: TC-9006: trustify-ui
- Parent: TC-9006
- Labels: ["ai-generated-jira"]
- Priority: Major (inherited from Feature)
- Fix Versions: RHTPA 1.5.0 (inherited from Feature)

### Changes

trustify-ui:
  changes:
    - Add TypeScript interfaces for remediation API response types
    - Add API client functions for remediation summary and by-product endpoints
    - Add React Query hooks for remediation data fetching
    - Add RemediationDashboardPage with summary cards, progress chart, and filterable vulnerability table
    - Register /remediation route in route definitions
    - Add MSW mock handlers and test fixtures for remediation endpoints
    - Add unit tests for the dashboard page

### Tasks under this Epic

- Task 5: Frontend API types and client (parent: Epic 2)
- Task 6: Frontend React Query hooks (parent: Epic 2)
- Task 7: Remediation dashboard page (parent: Epic 2)
- Task 8: Frontend tests and MSW mocks (parent: Epic 2)

## Documentation task

- Task 9: Documentation — document remediation dashboard and aggregation endpoints (generated from Documentation Considerations: New Content)

## Inherited Field Propagation

| Field | Feature Value | Propagated to Tasks | Reason |
|-------|--------------|--------------------|---------| 
| Priority | Major | Yes | Feature priority is set (not "Undefined") — inherited by all tasks per plan-feature Step 6a |
| Fix Versions | RHTPA 1.5.0 | Yes | Feature has non-empty fixVersions and fixVersion scope defaults to "both" (no explicit setting in Jira Field Defaults) — inherited by all tasks |

## Excluded Requirements

- **Export remediation report as CSV** — marked non-MVP in the feature requirements table. Can be planned as a follow-up feature.
