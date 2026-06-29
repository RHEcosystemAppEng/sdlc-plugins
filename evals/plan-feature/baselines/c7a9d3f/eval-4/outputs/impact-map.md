# Repository Impact Map — TC-9004: Add license compliance report endpoint

## trustify-backend

### Changes

- Add license policy configuration model and loader (JSON config file defining allowed/denied licenses)
- Add license report model structs (`LicenseReportGroup`, `LicenseReport`) for the grouped response
- Add license report service that aggregates package-license data from existing tables, walks transitive dependencies, and evaluates compliance against the policy
- Add `GET /api/v2/sbom/{id}/license-report` endpoint returning the grouped license compliance report
- Add integration tests for the license report endpoint covering compliant, non-compliant, and transitive dependency scenarios

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. All changes are within a single repository (trustify-backend), there are no breaking API changes to existing endpoints, no coordinated schema migrations are required (the feature aggregates from existing tables), and no cross-repo dependencies exist. Each task can be merged independently without leaving `main` in a broken state.
