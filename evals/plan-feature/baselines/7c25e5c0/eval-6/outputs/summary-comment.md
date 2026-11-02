# Plan Summary — TC-9006: Add vulnerability remediation tracking dashboard

## Tasks Created

| # | Task | Repository | Parent Epic |
|---|------|------------|-------------|
| 1 | Remediation models | trustify-backend | TC-9006: trustify-backend |
| 2 | Remediation service | trustify-backend | TC-9006: trustify-backend |
| 3 | Remediation endpoints | trustify-backend | TC-9006: trustify-backend |
| 4 | Backend integration tests | trustify-backend | TC-9006: trustify-backend |
| 5 | Frontend API types and client | trustify-ui | TC-9006: trustify-ui |
| 6 | Frontend React Query hooks | trustify-ui | TC-9006: trustify-ui |
| 7 | Remediation dashboard page | trustify-ui | TC-9006: trustify-ui |
| 8 | Frontend tests and MSW mocks | trustify-ui | TC-9006: trustify-ui |
| 9 | Documentation | trustify-backend | TC-9006: trustify-backend |

## Epics Created

| Epic | Summary | Issue Type | Parent |
|------|---------|------------|--------|
| Epic 1 | TC-9006: trustify-backend | Epic (level 1) | TC-9006 |
| Epic 2 | TC-9006: trustify-ui | Epic (level 1) | TC-9006 |

## Repositories Affected

- **trustify-backend** — new remediation domain module (models, service, endpoints) and integration tests
- **trustify-ui** — new dashboard page, API layer, React Query hooks, and component tests

## Architecture Summary

The remediation tracking feature adds a new domain module to the backend following the established model/service/endpoints pattern. Aggregation queries run against existing vulnerability and SBOM relationship data — no new database tables. The frontend adds a dashboard page at `/remediation` using PatternFly components with React Query for data fetching.

## Hierarchy

Feature TC-9006 → Incorporates → Epic 1 (TC-9006: trustify-backend)
Feature TC-9006 → Incorporates → Epic 2 (TC-9006: trustify-ui)
Tasks are children of their respective Epics (not directly linked to the Feature).

## Inherited Field Propagation

| Field | Feature Value | Propagated to Epics | Propagated to Tasks | Reason |
|-------|--------------|--------------------|--------------------|--------|
| Priority | Major | Yes | Yes | Feature priority is set (not "Undefined") — inherited per plan-feature Step 6a |
| Fix Versions | RHTPA 1.5.0 | Yes | Yes | Feature has non-empty fixVersions; fixVersion scope defaults to "both" (no explicit setting in Jira Field Defaults) — propagated to both Epics and Tasks |

### additional_fields applied to each Epic and Task

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

## Workflow Mode

**direct-to-main** — no atomicity constraints identified. Backend and frontend changes can land independently.
