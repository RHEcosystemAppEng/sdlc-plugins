# Repository Impact Map — TC-9004: Add license compliance report endpoint

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators were found. This feature adds a new endpoint to a single repository (trustify-backend) with no breaking API changes, no coordinated schema migrations (no new database tables), no cross-cutting refactors, and no tightly coupled cross-repo components. All tasks can be merged independently to `main` without leaving the codebase in a broken state.

## Impact Map

```
trustify-backend:
  changes:
    - Add license policy configuration model (JSON config file for defining compliant/non-compliant license lists)
    - Add LicenseReportService with license grouping and compliance checking logic, including transitive dependency traversal
    - Add LicenseReport and LicenseGroup model structs for the report response
    - Add GET /api/v2/sbom/{id}/license-report endpoint returning grouped license data with compliance flags
    - Add integration tests for the license report endpoint
    - Add API documentation for the license report endpoint and license policy configuration
```
