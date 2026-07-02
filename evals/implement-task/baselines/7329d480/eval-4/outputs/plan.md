# Implementation Plan for TC-9204: Add SBOM CycloneDX Export Endpoint

## Summary

Add a GET endpoint at `/api/v2/sbom/{id}/export` that exports an SBOM in CycloneDX 1.5 JSON format. The endpoint retrieves the SBOM by ID, collects all linked packages via the `sbom_package` join table, maps each package to a CycloneDX component, and returns a schema-compliant CycloneDX JSON document.

## Repository

trustify-backend

## Target Branch

main

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**Change:** Add an `export_cyclonedx` method to `SbomService`.

- Follow the existing pattern used by `fetch` and `list` methods in the same file.
- The method accepts an SBOM ID parameter and a database connection/transaction reference.
- Query the `sbom` table to fetch the SBOM record by ID. Return `AppError` with a 404 status if the SBOM does not exist.
- Query the `sbom_package` join table to collect all packages linked to the SBOM.
- For each package, join against `package_license` to retrieve license information.
- Map each package to a CycloneDX component struct containing `name`, `version`, and `license` fields.
- Assemble the full CycloneDX 1.5 JSON document structure including metadata (timestamp, tool identity) and the components array.
- Return the `CycloneDxExport` model struct (defined in the new `export.rs` model file).
- Use `.context()` for error wrapping, consistent with existing error handling conventions.

### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

**Change:** Register the new export route.

- Import the new `export` endpoint module.
- Add route registration for `GET /api/v2/sbom/{id}/export` pointing to the export handler.
- Follow the same route registration pattern used for existing routes (e.g., the `get` and `list` routes).

## Files to Create

### 3. `modules/fundamental/src/sbom/model/export.rs`

**Purpose:** Define the CycloneDX export model struct.

- Define `CycloneDxExport` struct with fields for:
  - `bom_format: String` (set to `"CycloneDX"`)
  - `spec_version: String` (set to `"1.5"`)
  - `version: i32` (BOM version, set to `1`)
  - `metadata: CycloneDxMetadata` (timestamp, tool info)
  - `components: Vec<CycloneDxComponent>` (the SBOM packages)
- Define `CycloneDxMetadata` struct with `timestamp` and `tools` fields.
- Define `CycloneDxComponent` struct with `name`, `version`, `type` (set to `"library"`), and `licenses` fields.
- Define `CycloneDxLicense` struct for the license representation.
- Derive `Serialize` on all structs for JSON serialization.
- Use `#[serde(rename_all = "camelCase")]` to match CycloneDX JSON field naming conventions.
- Add documentation comments on each struct and its public fields.
- Register this module in `modules/fundamental/src/sbom/model/mod.rs`.

### 4. `modules/fundamental/src/sbom/endpoints/export.rs`

**Purpose:** GET handler for `/api/v2/sbom/{id}/export`.

- Define an async handler function that extracts the SBOM ID from the path.
- Call `SbomService::export_cyclonedx` to retrieve the export data.
- Return 404 if the SBOM does not exist (propagated from the service layer via `AppError`).
- On success, return the CycloneDX JSON with `Content-Type: application/json`.
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure, error handling, and response construction.
- Return `Result<Json<CycloneDxExport>, AppError>` consistent with sibling endpoints.
- Add a documentation comment on the handler function.

### 5. `tests/api/sbom_export.rs`

**Purpose:** Integration tests for the export endpoint.

- **`test_export_sbom_cyclonedx`**: Verifies that a valid SBOM with linked packages exports correctly in CycloneDX 1.5 format.
  - Given: An SBOM exists in the database with linked packages via `sbom_package`.
  - When: `GET /api/v2/sbom/{id}/export` is called.
  - Then: Response status is 200, `bomFormat` is `"CycloneDX"`, `specVersion` is `"1.5"`, and `components` array contains the expected packages with correct `name`, `version`, and `license` values.

- **`test_export_sbom_not_found`**: Verifies that a non-existent SBOM returns 404.
  - Given: No SBOM exists with the given ID.
  - When: `GET /api/v2/sbom/{non-existent-id}/export` is called.
  - Then: Response status is 404.

- **`test_export_sbom_includes_all_packages`**: Verifies that all linked packages appear as components.
  - Given: An SBOM exists with multiple packages linked via `sbom_package`.
  - When: `GET /api/v2/sbom/{id}/export` is called.
  - Then: The `components` array length matches the number of linked packages, and each package's `name`, `version`, and license fields are present and correct.

- Follow the assertion pattern from `tests/api/sbom.rs` (e.g., `assert_eq!(resp.status(), StatusCode::OK)`).
- Add doc comments on each test function.
- Use given-when-then section comments inside each test body.
- Register the test module in `tests/api/mod.rs` if applicable.

## Acceptance Criteria Verification

| Criterion | How Verified |
|---|---|
| GET /api/v2/sbom/{id}/export returns valid CycloneDX 1.5 JSON | `test_export_sbom_cyclonedx` asserts `bomFormat`, `specVersion`, and component structure |
| Returns 404 when SBOM ID does not exist | `test_export_sbom_not_found` asserts 404 status |
| Export includes all packages linked via sbom_package | `test_export_sbom_includes_all_packages` asserts component count and values |
| Each component includes name, version, and license fields | Assertions in `test_export_sbom_cyclonedx` verify each field is present |

## Data-Flow Trace

- `GET /api/v2/sbom/{id}/export` (input: HTTP request with SBOM ID)
  - Parse path parameter (extract SBOM ID)
  - Call `SbomService::export_cyclonedx(id)` (processing: query DB, map to CycloneDX model)
  - Return `Json<CycloneDxExport>` (output: CycloneDX 1.5 JSON response)
  - Complete path: request -> handler -> service -> DB query -> model mapping -> JSON response

## Commit Message

```
feat(sbom): add CycloneDX 1.5 export endpoint

Add GET /api/v2/sbom/{id}/export that returns SBOM content as a
CycloneDX 1.5 JSON document including all linked packages as
components with name, version, and license fields.

Implements TC-9204
```
