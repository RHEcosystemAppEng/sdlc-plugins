# Implementation Plan: TC-9204 — SBOM CycloneDX Export Endpoint

## Overview

Add a GET endpoint at `/api/v2/sbom/{id}/export` that returns an SBOM in CycloneDX 1.5 JSON format. The endpoint fetches the SBOM by ID, collects all linked packages via the `sbom_package` join table, maps them to CycloneDX component format, and returns a schema-compliant JSON document.

## Files to Create

### 1. `modules/fundamental/src/sbom/model/export.rs` — CycloneDX export model

Define the response structs that represent a CycloneDX 1.5 JSON document:

- `CycloneDxExport` — top-level struct with fields: `bomFormat` ("CycloneDX"), `specVersion` ("1.5"), `version` (integer), `metadata` (SBOM metadata including timestamp and tool info), and `components` (Vec of CycloneDxComponent).
- `CycloneDxComponent` — struct with fields: `type` (default "library"), `name`, `version`, and `licenses` (list of license objects).
- `CycloneDxLicense` — struct wrapping a license `id` or `name` field.
- All structs derive `Serialize` for JSON output and use `#[serde(rename_all = "camelCase")]` where needed to match the CycloneDX schema.

### 2. `modules/fundamental/src/sbom/endpoints/export.rs` — GET handler

Implement the export endpoint handler following the pattern in `endpoints/get.rs`:

- Define an async handler function `export_cyclonedx` that extracts the SBOM ID from the path (`Path<Uuid>`).
- Inject `SbomService` via Axum's state extractor.
- Call `sbom_service.export_cyclonedx(id)` to retrieve the CycloneDX document.
- Return `Result<Json<CycloneDxExport>, AppError>`.
- On SBOM not found, return a 404 `AppError`.
- Set `Content-Type: application/json` (automatic via `Json` extractor).

### 3. `tests/api/sbom_export.rs` — Integration tests

Write integration tests against a real PostgreSQL test database:

- **Test valid export**: Ingest a test SBOM with linked packages, call `GET /api/v2/sbom/{id}/export`, assert status 200, validate that the response body is valid CycloneDX 1.5 JSON (`bomFormat` = "CycloneDX", `specVersion` = "1.5"), and confirm all linked packages appear as components with `name`, `version`, and `license` fields populated.
- **Test 404 for non-existent SBOM**: Call the export endpoint with a random UUID, assert status 404.
- **Test package completeness**: Ingest an SBOM with multiple packages, export it, and assert the component count matches the number of linked packages in `sbom_package`.

## Files to Modify

### 4. `modules/fundamental/src/sbom/service/sbom.rs` — Add `export_cyclonedx` method

Add an `export_cyclonedx` method to `SbomService` following the pattern of the existing `fetch` and `list` methods:

- Signature: `pub async fn export_cyclonedx(&self, id: Uuid) -> Result<CycloneDxExport, AppError>`
- Fetch the SBOM entity by ID; return 404 `AppError` if not found.
- Query the `sbom_package` join table to find all package IDs associated with this SBOM.
- Fetch the corresponding package entities (including license info via `package_license`).
- Map each package to a `CycloneDxComponent` with `name`, `version`, and `licenses`.
- Construct and return a `CycloneDxExport` with `bomFormat: "CycloneDX"`, `specVersion: "1.5"`, and the components list.

### 5. `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the export route

- Add `mod export;` to bring in the new handler module.
- Register the route `.route("/api/v2/sbom/{id}/export", get(export::export_cyclonedx))` alongside the existing SBOM routes.

## Module Declaration Updates

- Update `modules/fundamental/src/sbom/model/mod.rs` to add `pub mod export;` so the new model is accessible.
- Update `tests/api/mod.rs` (or equivalent test harness) to include `mod sbom_export;`.

## Implementation Sequence

1. Create `model/export.rs` (CycloneDX structs) — no dependencies on other new code.
2. Add `export_cyclonedx` method to `service/sbom.rs` — depends on the model structs.
3. Create `endpoints/export.rs` (handler) — depends on the service method and model.
4. Update `endpoints/mod.rs` to register the route.
5. Update `model/mod.rs` to declare the new module.
6. Create `tests/api/sbom_export.rs` and register in test harness.
7. Run `cargo check` and `cargo test` to validate compilation and test passage.

## Acceptance Criteria Mapping

| Criterion | Covered By |
|---|---|
| GET /api/v2/sbom/{id}/export returns valid CycloneDX 1.5 JSON | Handler in `endpoints/export.rs`, model in `model/export.rs` |
| Returns 404 when SBOM ID does not exist | 404 check in `service/sbom.rs` `export_cyclonedx`, tested in `sbom_export.rs` |
| Export includes all packages linked via sbom_package | Join query in `service/sbom.rs`, tested in `sbom_export.rs` |
| Each component includes name, version, and license fields | Mapping logic in `service/sbom.rs`, struct fields in `model/export.rs` |
