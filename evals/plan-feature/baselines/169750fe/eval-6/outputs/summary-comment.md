# Plan Summary — TC-9006: Add vulnerability remediation tracking dashboard

## Tasks Created

| # | Task | Repository | Epic | Jira Labels |
|---|---|---|---|---|
| 1 | Remediation summary model and service | trustify-backend | TC-9006: trustify-backend | ai-generated-jira |
| 2 | Remediation summary endpoint | trustify-backend | TC-9006: trustify-backend | ai-generated-jira |
| 3 | Remediation by-product endpoint | trustify-backend | TC-9006: trustify-backend | ai-generated-jira |
| 4 | Backend integration tests | trustify-backend | TC-9006: trustify-backend | ai-generated-jira |
| 5 | Frontend API types and client functions | trustify-ui | TC-9006: trustify-ui | ai-generated-jira |
| 6 | React Query hooks for remediation data | trustify-ui | TC-9006: trustify-ui | ai-generated-jira |
| 7 | Remediation dashboard page | trustify-ui | TC-9006: trustify-ui | ai-generated-jira |
| 8 | Frontend tests | trustify-ui | TC-9006: trustify-ui | ai-generated-jira |
| 9 | Documentation | trustify-backend | TC-9006: trustify-backend | ai-generated-jira |

## Epics Created

| Epic Summary | Issue Type | Parent | Repository Tasks |
|---|---|---|---|
| TC-9006: trustify-backend | Epic (level 1) | TC-9006 | Tasks 1, 2, 3, 4, 9 |
| TC-9006: trustify-ui | Epic (level 1) | TC-9006 | Tasks 5, 6, 7, 8 |

**Incorporates links**: TC-9006 → each Epic (not to individual Tasks)

## Repositories Affected

- **trustify-backend**: New remediation module with aggregation service and two REST endpoints
- **trustify-ui**: New dashboard page with summary cards, progress chart, and filterable vulnerability table

## Architecture Summary

The backend adds a new `remediation` domain module following the established `model/ + service/ + endpoints/` pattern. Two new endpoints aggregate existing vulnerability/SBOM data without new database tables. The frontend adds a complete data-fetching and rendering pipeline: TypeScript types → API client → React Query hooks → dashboard page with PatternFly 5 components.

## Inherited Field Propagation

| Field | Feature Value | Propagated | Rationale |
|---|---|---|---|
| **Priority** | Major | Yes — propagated to all tasks and Epics | Feature priority is "Major" (not "Undefined"), so it is inherited by all created issues |
| **Fix Versions** | RHTPA 1.5.0 | Yes — propagated to all tasks and Epics | Feature has non-empty fixVersions; `fixVersion scope` is absent from Jira Field Defaults, defaulting to "both" — propagation includes tasks |

All tasks and Epics were created with `additional_fields`:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Major"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

## Workflow Mode

**direct-to-main** — no atomicity indicators identified. All tasks target `main`.
