# Implementation Plan: TC-9204 -- Add SBOM Export Endpoint

## Summary

Add a GET endpoint at `/api/v2/sbom/{id}/export` that exports an SBOM in CycloneDX 1.5 JSON format. The endpoint retrieves an SBOM by ID, collects all linked packages via the `sbom_package` join table, maps them to CycloneDX component format, and returns schema-compliant JSON.

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**Change:** Add an `export_cyclonedx` method to `SbomService`.

- Follow the pattern of existing `fetch` and `list` methods.
- Accept an SBOM ID parameter and a database connection/transaction reference.
- Query the SBOM record by ID; return a 404-equivalent error if not found.
- Query the `sbom_package` join table to collect all packages linked to the SBOM.
- For each package, extract `name`, `version`, and `license` fields.
- Assemble a CycloneDX 1.5 JSON structure:
  - `bomFormat`: `"CycloneDX"`
  - `specVersion`: `"1.5"`
  - `version`: `1`
  - `serialNumber`: generated URN
  - `metadata`: timestamp and tool info
  - `components`: array of component objects mapped from packages
- Return the populated `CycloneDxExport` model struct.

### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

**Change:** Register the new export route.

- Add `mod export;` to include the new endpoint module.
- In the router configuration function, add a `.service()` or `.route()` entry for `GET /api/v2/sbom/{id}/export` pointing to `export::get_sbom_export`.

## Files to Create

### 3. `modules/fundamental/src/sbom/model/export.rs`

**Purpose:** Define the CycloneDX export model struct.

- Define `CycloneDxExport` struct with serde `Serialize` derive:
  - `bom_format: String` (serialized as `"bomFormat"`)
  - `spec_version: String` (serialized as `"specVersion"`)
  - `version: u32`
  - `serial_number: String` (serialized as `"serialNumber"`)
  - `metadata: CycloneDxMetadata`
  - `components: Vec<CycloneDxComponent>`
- Define `CycloneDxMetadata` struct:
  - `timestamp: String`
  - `tools: Vec<CycloneDxTool>`
- Define `CycloneDxTool` struct:
  - `vendor: String`
  - `name: String`
  - `version: String`
- Define `CycloneDxComponent` struct:
  - `type_field: String` (serialized as `"type"`, value `"library"`)
  - `name: String`
  - `version: String`
  - `licenses: Vec<CycloneDxLicense>`
- Define `CycloneDxLicense` struct:
  - `license: CycloneDxLicenseId`
- Define `CycloneDxLicenseId` struct:
  - `id: String`

### 4. `modules/fundamental/src/sbom/endpoints/export.rs`

**Purpose:** GET handler for `/api/v2/sbom/{id}/export`.

- Define an async handler function `get_sbom_export` following the pattern in `get.rs`.
- Extract the SBOM ID from the path parameter.
- Call `SbomService::export_cyclonedx(id, &db)`.
- On success, return `HttpResponse::Ok()` with `Content-Type: application/json` and the serialized CycloneDX JSON body.
- On not-found, return `HttpResponse::NotFound()` with an appropriate error body.
- On other errors, return `HttpResponse::InternalServerError()`.

### 5. `tests/api/sbom_export.rs`

**Purpose:** Integration tests for the export endpoint.

- **Test: valid SBOM export** -- Seed an SBOM with linked packages, call `GET /api/v2/sbom/{id}/export`, assert 200 status, assert response body is valid CycloneDX 1.5 JSON with correct `bomFormat`, `specVersion`, and `components` array matching the seeded packages.
- **Test: non-existent SBOM returns 404** -- Call `GET /api/v2/sbom/{nonexistent_id}/export`, assert 404 status.
- **Test: all linked packages appear as components** -- Seed an SBOM with multiple packages (e.g., 5), call the export endpoint, assert the `components` array length matches and each component has `name`, `version`, and `licenses` fields populated.

## Acceptance Criteria Verification

| Criterion | Covered By |
|---|---|
| GET /api/v2/sbom/{id}/export returns valid CycloneDX 1.5 JSON | Handler in export.rs + model in export.rs |
| Returns 404 when SBOM ID does not exist | Error handling in export.rs + test |
| Export includes all packages linked via sbom_package | Service query in sbom.rs |
| Each component includes name, version, and license fields | CycloneDxComponent model + mapping logic |

## Scope

This plan is scoped exclusively to the five files listed above. No other files are modified or created.
