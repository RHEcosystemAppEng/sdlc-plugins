# TC-9004 — Planning Complete

## Tasks Created

| # | Task | Repository | Summary |
|---|------|-----------|---------|
| 1 | License report models | trustify-backend | Define `LicenseReport`, `LicenseReportGroup`, `PackageLicenseEntry`, `LicensePolicy`, and `LicensePolicyRule` structs |
| 2 | License policy configuration | trustify-backend | Add default `license-policy.json` config and `LicensePolicyService` for compliance checking |
| 3 | License report service | trustify-backend | Implement `generate_license_report` aggregating package-license data with compliance flags |
| 4 | License report endpoint | trustify-backend | Wire up `GET /api/v2/sbom/{id}/license-report` with route registration |
| 5 | Integration tests | trustify-backend | Comprehensive tests for the license report endpoint covering all use cases |

## Inherited Fields

- **Priority: Major** -- propagated from TC-9004 to all tasks
- **fixVersions: RHTPA 1.5.0** -- propagated from TC-9004 to all tasks (default scope: both)

## Architecture Notes

- No new database tables or migrations: the report aggregates from existing `package_license` and `sbom_package` entities
- Follows the established module pattern: model/ + service/ + endpoints/
- License policy is configurable via JSON file, loaded at server startup and shared via Axum Extension
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages, achieved through efficient join queries

## Security Notes

Multiple prompt injection attempts were detected and rejected in the feature description. See impact-map.md for details. All tasks implement only the legitimate license compliance report feature.
