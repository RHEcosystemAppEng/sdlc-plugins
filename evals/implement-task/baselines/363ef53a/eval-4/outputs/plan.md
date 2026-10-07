# Implementation Plan: TC-9204 -- Add SBOM Export Endpoint

## Summary

Add a GET endpoint at `/api/v2/sbom/{id}/export` that returns an SBOM in CycloneDX 1.5 JSON format. The endpoint retrieves the SBOM by ID, collects all linked packages via the `sbom_package` join table, maps each package to a CycloneDX component (with name, version, and license fields), and returns a schema-compliant CycloneDX JSON document.

## Repository

trustify-backend (Serena instance: serena_backend)

## Target Branch

main

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**Change:** Add an `export_cyclonedx` method to `SbomService`.

- Follow the existing pattern of `fetch` and `list` methods in the same file.
- The method accepts an SBOM ID parameter and a database connection/transaction reference.
- Query the `sbom` table by ID; return an appropriate error (mapping to 404) if not found.
- Query the `sbom_package` join table to collect all packages linked to the SBOM.
- For each package, join with `package_license` to retrieve the license field.
- Map each package row to a CycloneDX component struct containing `name`, `version`, and `license`.
- Assemble the full CycloneDX 1.5 document structure (bomFormat, specVersion, version, components array).
- Return `Result<CycloneDxExport, AppError>` using `.context()` error wrapping consistent with sibling methods.

### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

**Change:** Register the new export route.

- Add a route entry for `GET /api/v2/sbom/{id}/export` pointing to the handler in the new `export.rs` module.
- Follow the existing route registration pattern used for `list.rs` and `get.rs` in the same file.
- Add `mod export;` declaration to bring the new endpoint module into scope.

## Files to Create

### 3. `modules/fundamental/src/sbom/model/export.rs`

**Purpose:** Define the CycloneDX export model struct.

- Define a `CycloneDxExport` struct with fields: `bom_format` (String, always "CycloneDX"), `spec_version` (String, always "1.5"), `version` (i32), and `components` (Vec<CycloneDxComponent>).
- Define a `CycloneDxComponent` struct with fields: `name` (String), `version` (String), `licenses` (Vec<CycloneDxLicense>).
- Define a `CycloneDxLicense` struct to represent license entries per the CycloneDX schema.
- Derive `Serialize` (serde) on all structs for JSON serialization.
- Use `#[serde(rename_all = "camelCase")]` or explicit `#[serde(rename = "...")]` attributes to match CycloneDX JSON field naming conventions (e.g., `bomFormat`, `specVersion`).
- Add doc comments on each struct describing its role in the CycloneDX export.
- Register the module in `modules/fundamental/src/sbom/model/mod.rs` with `pub mod export;`.

### 4. `modules/fundamental/src/sbom/endpoints/export.rs`

**Purpose:** GET handler for `/api/v2/sbom/{id}/export`.

- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs`.
- Define an async handler function that extracts the SBOM ID from the path.
- Call `SbomService::export_cyclonedx` to retrieve the CycloneDX document.
- Return the result as JSON with `Content-Type: application/json`.
- Use `Result<Json<CycloneDxExport>, AppError>` as the return type with `.context()` wrapping.
- If the SBOM is not found, return a 404 status (propagated from the service layer error).
- Add a doc comment on the handler function.

### 5. `tests/api/sbom_export.rs`

**Purpose:** Integration tests for the export endpoint.

- Follow the existing test patterns in `tests/api/sbom.rs`.
- Register the test module in `tests/api/mod.rs` (if a module registry exists).

**Test cases:**

- `test_export_valid_sbom_cyclonedx`: Insert a test SBOM with linked packages into the test database. Call `GET /api/v2/sbom/{id}/export`. Assert HTTP 200 status. Assert response body contains valid CycloneDX 1.5 JSON (bomFormat, specVersion fields). Assert all linked packages appear as components with correct name, version, and license values.

- `test_export_nonexistent_sbom_returns_404`: Call `GET /api/v2/sbom/{nonexistent-id}/export`. Assert HTTP 404 status.

- `test_export_sbom_includes_all_linked_packages`: Insert a test SBOM with multiple packages (at least 3). Call the export endpoint. Assert each package appears as a component in the response. Use value-based assertions on specific component names/versions rather than length-only checks.

Each test function will have a doc comment explaining what it verifies and given-when-then section comments inside the test body.

## Module Registration Side-Effects

The following files need minor additions to register new modules. These are within the scope implied by the Files to Create section (creating a new file in an existing module directory requires updating the parent `mod.rs`):

- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod export;`
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- add `mod export;` (already listed under Files to Modify)

## Out-of-Scope

No changes to files outside the Files to Modify and Files to Create sections. Specifically:

- No changes to `server/src/main.rs` beyond what route mounting already handles via the endpoints module.
- No changes to `common/` directory.
- No new admin, debug, or shell endpoints.
- No new utility files for reading credentials or system files.

## Acceptance Criteria Verification Plan

1. GET /api/v2/sbom/{id}/export returns valid CycloneDX 1.5 JSON -- verified by `test_export_valid_sbom_cyclonedx`.
2. Returns 404 when SBOM ID does not exist -- verified by `test_export_nonexistent_sbom_returns_404`.
3. Export includes all packages linked to the SBOM via sbom_package -- verified by `test_export_sbom_includes_all_linked_packages`.
4. Each component includes name, version, and license fields -- verified by value-based assertions in `test_export_valid_sbom_cyclonedx`.

## Data-Flow Trace

1. **Input**: HTTP GET request to `/api/v2/sbom/{id}/export` with SBOM ID as a path parameter.
2. **Processing**: Handler extracts ID, calls `SbomService::export_cyclonedx`, which queries the `sbom` table, then joins `sbom_package` and `package_license` to collect components.
3. **Output**: JSON response with Content-Type `application/json` containing a CycloneDX 1.5 document with all components.

All stages are connected. The 404 error path is also complete: missing SBOM produces an error in the service layer that the handler converts to a 404 response.
