# Repository Impact Map — TC-9006: Add vulnerability remediation tracking dashboard

## Type-to-Role Mapping

```
Type-to-role mapping:
  Feature: Feature (level: 2)
  Epic:    Epic (level: 1)
  Task:    Task (level: 0)
```

## Epic Grouping Strategy: by-repository

- **TC-9006: trustify-backend** — Backend remediation aggregation module and endpoints
- **TC-9006: trustify-ui** — Frontend remediation dashboard page, API client, routing, and documentation

## Impact Map

```
trustify-backend:
  changes:
    - Create remediation module with GET /api/v2/remediation/summary endpoint returning aggregated counts by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
    - Add GET /api/v2/remediation/by-product endpoint returning per-product remediation breakdown (total, open, resolved counts per product)
    - Add integration tests for both remediation endpoints
    - Add GET /api/v2/remediation/export endpoint for CSV export of remediation data (non-MVP)

trustify-ui:
  changes:
    - Add TypeScript interfaces, Axios client functions, and React Query hooks for remediation API endpoints
    - Create RemediationDashboardPage with summary cards (Open, In Progress, Resolved counts) and progress trend chart
    - Add filterable vulnerability table component with severity, product, and status filters
    - Register /remediation route in React Router and add navigation entry
    - Document the remediation dashboard and aggregation API endpoints (New Content — documentation task)
```

## Feature Field Inheritance

All created Epics and Tasks inherit the following fields from the Feature:

```
additional_fields: {
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

- **priority**: "Major" — inherited from Feature TC-9006 (not "Undefined", so propagated)
- **fixVersions**: ["RHTPA 1.5.0"] — inherited from Feature TC-9006 (fixVersion scope defaults to "both" since no Jira Field Defaults section exists)

## Feature Issue Label Update (feature-branch mode)

The feature issue TC-9006 will have `workflow:feature-branch` appended to its existing labels:

```
labels: ["ai-generated-jira", "workflow:feature-branch"]
```

## Documentation Signals

- **Doc impact type**: New Content
- **Details**: Document the remediation dashboard and aggregation endpoints
- **User purpose**: Security teams need a guide for using the dashboard; API consumers need endpoint reference

## Excluded Requirements

None — all requirements (MVP and non-MVP) have been decomposed into actionable tasks.
