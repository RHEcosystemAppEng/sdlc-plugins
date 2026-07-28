# Repository Impact Map -- TC-9006

## trustify-backend

changes:
  - Add remediation module following existing model/ + service/ + endpoints/ structure under modules/fundamental/src/remediation/
  - Create RemediationSummary model struct with severity x status aggregation (Critical/High/Medium/Low x Open/In Progress/Resolved)
  - Create ProductRemediation model struct with per-product total, open, resolved counts
  - Implement RemediationService with aggregation queries over existing advisory and sbom_advisory entities (no new database tables)
  - Add GET /api/v2/remediation/summary endpoint returning aggregated remediation counts by severity and status
  - Add GET /api/v2/remediation/by-product endpoint returning per-product remediation breakdown
  - Register remediation module routes in server/src/main.rs
  - Add integration tests for both remediation endpoints in tests/api/remediation.rs

## trustify-ui

changes:
  - Add TypeScript interfaces for RemediationSummary and ProductRemediation API response types in src/api/models.ts
  - Add API client functions fetchRemediationSummary() and fetchRemediationByProduct() in src/api/rest.ts
  - Create React Query hooks useRemediationSummary and useRemediationByProduct in src/hooks/
  - Create RemediationPage directory under src/pages/ with main page component
  - Create SummaryCards component showing total Open, In Progress, and Resolved counts
  - Create ProgressChart component showing remediation trend over the past 30 days
  - Create VulnerabilityTable component with filtering by severity, product, and status
  - Register /remediation route in src/routes.tsx
  - Add unit tests for RemediationPage with MSW mock handlers
  - Add mock fixtures for remediation data in tests/mocks/fixtures/
  - Add E2E test for remediation dashboard in tests/e2e/

## Excluded requirements

- **Export remediation report as CSV** (non-MVP): This requirement involves a file download/export feature. While plannable, it is explicitly marked as non-MVP in the feature description and is excluded from the initial implementation plan. It can be planned in a follow-up iteration once the MVP dashboard is delivered.

## Workflow Mode

- **Mode**: direct-to-main
- **Rationale**: No atomicity indicators were identified. All backend changes are additive (new endpoints that do not modify existing APIs or schemas). All frontend changes are additive (new page and components that do not alter existing pages). No coordinated schema migrations are needed (the feature explicitly requires no new database tables). No breaking API changes exist (all endpoints are new). No cross-cutting refactors are involved. Task dependencies ensure correct merge ordering (backend endpoints merged before frontend consumers).

## Epic Grouping

- **Strategy**: by-repository (from CLAUDE.md Hierarchy Configuration)
- **Epic 1**: TC-9006: trustify-backend -- Backend remediation aggregation module and API endpoints
- **Epic 2**: TC-9006: trustify-ui -- Frontend remediation dashboard page with summary, chart, and filterable table

## Jira Field Propagation (additional_fields)

The following fields are inherited from the parent Feature TC-9006 and applied to all created Epics and Tasks:

- **labels**: `["ai-generated-jira"]`
- **priority**: `{"name": "Major"}` (inherited from Feature; Feature priority is "Major", not "Undefined")
- **fixVersions**: `[{"name": "RHTPA 1.5.0"}]` (inherited from Feature; no `fixVersion scope` setting in Jira Field Defaults, so defaults to "both" -- propagated to tasks)

### Epic additional_fields

Each Epic is created with:
- `parent`: TC-9006 (the Feature issue)
- `labels`: ["ai-generated-jira"]
- `priority`: {"name": "Major"}
- `fixVersions`: [{"name": "RHTPA 1.5.0"}]

### Task additional_fields

Each Task is created with:
- `parent`: assigned Epic key (trustify-backend Epic or trustify-ui Epic)
- `labels`: ["ai-generated-jira"]
- `priority`: {"name": "Major"}
- `fixVersions`: [{"name": "RHTPA 1.5.0"}]

## Jira Links

### Feature "incorporates" links (Epic-aware)
- TC-9006 "Incorporates" --> trustify-backend Epic
- TC-9006 "Incorporates" --> trustify-ui Epic

### Task dependency links
- Task 2 "Depends on" Task 1
- Task 3 "Depends on" Task 1
- Task 3 "Depends on" Task 2
- Task 4 "Depends on" Task 1
- Task 4 "Depends on" Task 2
- Task 5 "Depends on" Task 4
- Task 6 "Depends on" Task 5
- Task 7 "Depends on" Task 5
- Task 7 "Depends on" Task 6
- Task 8 "Depends on" all implementation tasks (Tasks 1-7)
