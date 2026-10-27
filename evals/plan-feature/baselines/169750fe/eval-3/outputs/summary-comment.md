# Plan Summary — TC-9003: SBOM Comparison View

## Tasks Created

| # | Task | Repository | Target Branch |
|---|------|-----------|---------------|
| 1 | Create feature branch TC-9003 from main | trustify-backend | main |
| 2 | Backend comparison model | trustify-backend | TC-9003 |
| 3 | Backend comparison service | trustify-backend | TC-9003 |
| 4 | Backend comparison endpoint | trustify-backend | TC-9003 |
| 5 | Backend integration tests | trustify-backend | TC-9003 |
| 6 | Frontend API types and client | trustify-ui | TC-9003 |
| 7 | Frontend comparison page | trustify-ui | TC-9003 |
| 8 | Frontend MSW mocks | trustify-ui | TC-9003 |
| 9 | Frontend SBOM list compare action | trustify-ui | TC-9003 |
| 10 | Documentation | trustify-backend | TC-9003 |
| 11 | Merge feature branch TC-9003 to main | trustify-backend | main |

## Repositories Affected

- **trustify-backend** — new comparison model, service, endpoint, and integration tests
- **trustify-ui** — new comparison page, API layer, SBOM list page modification, MSW mocks

## Architecture Summary

The implementation adds a structured SBOM comparison capability spanning both repositories:

- **Backend**: A new `GET /api/v2/sbom/compare?left={id}&right={id}` endpoint computes diffs on-the-fly from existing package, advisory, and license data (no new database tables). The diff covers six categories: added/removed packages, version changes, new/resolved vulnerabilities, and license changes.
- **Frontend**: A new comparison page at `/sbom/compare` renders the diff using PatternFly ExpandableSection components with data tables, following the Figma design. The SBOM list page gains checkbox selection and a "Compare selected" action button as the primary entry point.
- **Workflow mode**: `feature-branch` — frontend depends on the new backend endpoint, requiring coordinated delivery.

## Inherited Field Propagation

| Field | Feature Value | Propagated to Tasks | Rationale |
|---|---|---|---|
| **Priority** | Critical | **Yes** — propagated to all created tasks | Feature has a defined priority (not "Undefined") |
| **Fix Versions** | RHTPA 1.5.0 | **Yes** — propagated to all created tasks | Feature has non-empty fixVersions array; `fixVersion scope` defaults to "both" (no `### Jira Field Defaults` section in CLAUDE.md) |

All created tasks receive `additional_fields`:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

## Excluded from Scope

- **Export diff as JSON or CSV** — marked non-MVP in feature requirements. The Export dropdown UI is wired but the handler is a placeholder for a follow-up feature.
