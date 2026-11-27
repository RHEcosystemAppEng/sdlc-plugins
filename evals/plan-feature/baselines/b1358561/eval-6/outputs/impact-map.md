# Repository Impact Map — TC-9006: Add vulnerability remediation tracking dashboard

> Eval run: no Jira or Serena calls were made. Jira keys below (TC-9101 to TC-9109) are placeholders for the keys Jira would return.

## Step 0 – Project Configuration validation
- Repository Registry, Jira Configuration (Project key TC, Cloud ID, Feature issue type ID 10142), and Code Intelligence sections are present. Validation passed.
- Target repositories come from the eval fixtures: `trustify-backend` (repo-backend.md) and `trustify-ui` (repo-frontend.md). No Serena instances are configured, so the fixture directory trees were used as the source of real paths (Glob/Read fallback).

## Step 1 – Feature fields extracted
- Title: Add vulnerability remediation tracking dashboard
- Priority: **Major** (set, not "Undefined", so it is inherited)
- fixVersions: **[RHTPA 1.5.0]** (non-empty)
- Figma link: none
- Documentation signals: **New Content**. Document the remediation dashboard and aggregation endpoints (user guide for security teams, endpoint reference for API consumers).

## Step 1.5 – Parent link
- The Feature has no existing parent. In this non-interactive eval run the parent-key prompt was treated as **skipped (Enter)**, so no parent link was set.

## Step 2 – Figma
- No Figma URL was passed as an argument or found in the description. UI layout is planned from the Feature text plus existing PatternFly page patterns. Display-text mapping (API `snake_case` values to labels) is still documented in Tasks 4–6.

## Step 2.5 – Issue types and hierarchy
```
Type-to-role mapping:
  Feature: Feature (ID: 10142, level: 2)
  Epic:    Epic    (level: 1)   # single level-1 type named "Epic", selected
  Task:    Task    (level: 0)
```
- Hierarchy Configuration: default Epic grouping strategy = **by-repository** (given in the eval scenario; it overrides the `by-sub-feature` value in the repo-root CLAUDE.md for this run). It is a valid strategy, so the interactive prompt was skipped.

## Step 3 – Analysis highlights
- CONVENTIONS.md exists at the root of both repositories. Its contents are taken from each fixture's "Key Conventions" section and applied to tasks with `Applies:` rationales.
- Testing readiness template: neither repo has `docs/testing-readiness.md`, so **no testing tasks** were generated.
- Documentation files found: `README.md` and `CONVENTIONS.md` in both repos.
- Backend API discovery: no `remediation` endpoints exist yet. The planned contracts are defined in Tasks 2 and 3 and copied into frontend Task 4.
- Shared-artifact analysis: not applicable. This is a read-only aggregation and has no shared-artifact acceptance criterion with multiple writers.
- Fail-open risks: no stated silent-success risk. As a defensive measure, invalid filter values must return 400 rather than an empty 200 (Task 3).
- Eval infrastructure: not applicable. No skill `SKILL.md` is modified.
- Reuse: `common/src/db/query.rs`, `common/src/model/paginated.rs`, `AdvisoryService`; UI `FilterToolbar`, `SeverityBadge`, `severityUtils`, `LoadingSpinner`, `EmptyStateCard`.

## Repository Impact Map

```
trustify-backend:
  changes:
    - Add a remediation domain module (model + service) that aggregates vulnerability counts by severity x status and per product from existing sbom/advisory/sbom_advisory data (no new tables)
    - Expose GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product and mount the routes in the server
    - Expose GET /api/v2/remediation/vulnerabilities (filter by severity/product/status, sort, paginate) and GET /api/v2/remediation/trend (30-day daily status counts)
    - Add integration tests for all remediation endpoints
    - Document the remediation dashboard and endpoints (New Content)

trustify-ui:
  changes:
    - Add remediation API types, REST functions, React Query hooks and MSW mocks
    - Add the /remediation dashboard page with summary cards (Open / In Progress / Resolved) and a 30-day trend chart
    - Add the filterable (severity, product, status), severity-sortable, paginated vulnerability table to the dashboard
```

### Excluded requirements
- **Export remediation report as CSV** (non-MVP). Excluded because the specification is insufficient: no column set is given, and it does not say whether the active filters apply or whether export runs server-side (endpoint) or client-side. Provide the CSV format and export mechanics to plan this.

### Open questions / risks (carried into task Implementation Notes)
- Remediation status (Open/In Progress/Resolved) source column must be confirmed on `entity/src/sbom_advisory.rs` (or a related entity). The "no new tables" NFR blocks adding one.
- The 30-day trend requires historical status timestamps in existing data. If they are missing, the trend chart cannot be built without a new table. Escalate rather than fabricate.
- Product identity is assumed to come from `entity/src/sbom.rs`. Verify the field at implementation time.

## Step 4.5 – Workflow mode
**Selected mode: `direct-to-main`**

Atomicity indicators evaluated:
1. Coordinated schema migrations: **none**. The NFR forbids new tables and no migration is planned.
2. Breaking API changes: **none**. All endpoints are new and additive, and no existing contract changes.
3. Cross-cutting refactors: **none**.
4. Tightly coupled components: **not present as an atomicity constraint**. The backend endpoints work on their own and are usable by any API consumer. The frontend depends on them, and that ordering is enforced through "Depend" links (Tasks 4–6 depend on Tasks 2–3), so the UI never merges ahead of its endpoints and no PR leaves `main` broken.

All tasks therefore use Target Branch `main`. No bookend tasks are created and no `workflow:feature-branch` label is applied.

## Epics (Step 5 grouping / Step 6a.0 creation)
Grouping strategy: **by-repository**

| Epic | Summary | Issue type | Parent | Tasks |
|---|---|---|---|---|
| TC-9101 | `TC-9006: trustify-backend` | Epic (level-1 type) | TC-9006 | Task 1, Task 2, Task 3, Task 7 |
| TC-9102 | `TC-9006: trustify-ui` | Epic (level-1 type) | TC-9006 | Task 4, Task 5, Task 6 |

Epic creation parameters (both Epics):
```
jira.create_issue(
  projectKey="TC",
  issueTypeName="Epic",
  summary="TC-9006: trustify-backend" | "TC-9006: trustify-ui",
  description=<plain text, see epic-N-*.md>,
  parent="TC-9006",
  additional_fields={
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "RHTPA 1.5.0"}]
  }
)
```

## Tasks

| # | Task | Repository | Parent Epic | Jira key | Depends on |
|---|---|---|---|---|---|
| 1 | Add remediation domain module with summary and per-product aggregation service | trustify-backend | TC-9101 | TC-9103 | — |
| 2 | Add GET /api/v2/remediation/summary and /by-product endpoints | trustify-backend | TC-9101 | TC-9104 | 1 |
| 3 | Add filterable remediation vulnerability list and 30-day trend endpoints | trustify-backend | TC-9101 | TC-9105 | 1, 2 |
| 4 | Add remediation API types, REST functions, hooks and MSW mocks | trustify-ui | TC-9102 | TC-9106 | 2, 3 |
| 5 | Add /remediation dashboard page with summary cards and trend chart | trustify-ui | TC-9102 | TC-9107 | 4 |
| 6 | Add filterable outstanding-vulnerability table | trustify-ui | TC-9102 | TC-9108 | 4, 5 |
| 7 | Document the remediation dashboard and endpoints (documentation task) | trustify-backend | TC-9101 | TC-9109 | 1–6 |

The backend tasks (1–3) are numbered before the frontend tasks (4–6) that depend on them.

## Links (Step 6b)
**Incorporates links: Feature to Epics only** (tasks inherit the hierarchy through their Epic parent, so there are no Feature-to-Task Incorporates links):
- TC-9006 incorporates TC-9101 (`TC-9006: trustify-backend`)
- TC-9006 incorporates TC-9102 (`TC-9006: trustify-ui`)

**Depend links** (inward = dependent, outward = dependency):
- TC-9104 → TC-9103
- TC-9105 → TC-9103, TC-9104
- TC-9106 → TC-9104, TC-9105
- TC-9107 → TC-9106
- TC-9108 → TC-9106, TC-9107
- TC-9109 → TC-9103, TC-9104, TC-9105, TC-9106, TC-9107, TC-9108

## Inherited fields
- Priority **Major** is propagated to both Epics and all 7 tasks.
- fixVersion **RHTPA 1.5.0** is propagated to both Epics and all 7 tasks (`fixVersion scope: both` in Jira Field Defaults).
- Label `ai-generated-jira` is set on every created issue.
- See `task-creation-log.md` for per-issue `additional_fields`.
