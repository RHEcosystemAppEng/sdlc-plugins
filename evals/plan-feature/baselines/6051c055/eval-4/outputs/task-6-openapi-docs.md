## Repository
trustify-backend

## Target Branch
main

## Description
Update the OpenAPI specification and developer documentation to cover the new license compliance report endpoint. Ensure the endpoint, request parameters, and response schemas are fully documented in the generated API spec and that any relevant developer-facing documentation is updated.

## Files to Modify
- `modules/fundamental/src/license_report/endpoints.rs` — verify `#[utoipa::path]` annotations are complete with descriptions, parameter docs, and response examples
- `modules/fundamental/src/license_report/model.rs` — verify all `ToSchema` derives include doc comments that appear in the OpenAPI spec

## Files to Create
- None — documentation is generated from code annotations and existing doc infrastructure

## Implementation Notes
- Ensure the `#[utoipa::path]` macro on the endpoint handler includes:
  - `summary` and `description` fields
  - `params` section documenting the `id` path parameter (UUID, required)
  - `responses` section with 200 (LicenseReport body), 400 (invalid ID), 404 (SBOM not found)
- Add doc comments (`///`) to all public structs and fields in `model.rs` — these propagate to the OpenAPI schema descriptions
- Add the `LicenseReport`, `LicenseReportSummary`, `LicenseGroup`, `LicenseConflict`, and `Classification` schemas to the utoipa OpenAPI component registration (typically in a central `ApiDoc` struct)
- Verify the generated OpenAPI spec includes the new endpoint by running the spec generation command and inspecting the output

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` appears in the generated OpenAPI spec
- [ ] All response model schemas (`LicenseReport`, `LicenseGroup`, `LicenseConflict`, `LicenseReportSummary`) appear in the OpenAPI components
- [ ] Path parameter `id` is documented as UUID type, required
- [ ] Response codes 200, 400, and 404 are documented with descriptions
- [ ] All public struct fields have doc comments that appear as schema descriptions

## Test Requirements
- [ ] Verify OpenAPI spec generation succeeds without errors
- [ ] Verify the new endpoint path is present in the generated spec
- [ ] Verify response schemas are correctly referenced in the endpoint definition
