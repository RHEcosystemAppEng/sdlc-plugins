# Plan Summary — TC-9003: SBOM Comparison View

## Tasks Created

| # | Summary | Repository | Jira Key |
|---|---------|-----------|----------|
| 1 | Backend comparison model | trustify-backend | (to be created) |
| 2 | Backend comparison service | trustify-backend | (to be created) |
| 3 | Backend comparison endpoint | trustify-backend | (to be created) |
| 4 | Backend integration tests | trustify-backend | (to be created) |
| 5 | Frontend API types and client | trustify-ui | (to be created) |
| 6 | Frontend comparison hook | trustify-ui | (to be created) |
| 7 | Frontend comparison page | trustify-ui | (to be created) |
| 8 | Frontend SBOM list compare action | trustify-ui | (to be created) |
| 9 | Frontend MSW mocks and tests | trustify-ui | (to be created) |
| 10 | Documentation | trustify-backend | (to be created) |

## Repositories Affected

- **trustify-backend** — new comparison model, service, endpoint, and integration tests
- **trustify-ui** — new comparison page, API types, hooks, and tests; modification to SBOM list page

## Architecture Summary

The feature adds a side-by-side SBOM comparison view with:
- A backend diff computation service that computes on-the-fly diffs between two SBOMs using existing package, advisory, and license entity data (no new database tables)
- A REST endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` returning structured diff results
- A React frontend comparison page at `/sbom/compare` with PatternFly UI components (selectors, expandable diff sections, data tables) matching the Figma design
- SBOM list page enhanced with multi-select and "Compare selected" action for user workflow entry

## Workflow Mode

**direct-to-main** — no atomicity constraints. Backend endpoint is independently useful; frontend depends on backend via task ordering.

## Inherited Field Propagation

- **Priority:** Critical — propagated from Feature TC-9003 to all 10 created tasks. The Feature's priority is set (not "Undefined"), so it is inherited per the conditional inclusion rules.
- **fixVersions:** RHTPA 1.5.0 — propagated from Feature TC-9003 to all 10 created tasks. The Feature has a non-empty fixVersions array, and the fixVersion scope in Jira Field Defaults defaults to "both" (no explicit setting found), so fixVersions are propagated to tasks.

All tasks will be created with `additional_fields`:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```
