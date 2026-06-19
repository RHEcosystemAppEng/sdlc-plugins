# Implementation Plan: TC-9204 -- Add SBOM CycloneDX Export Endpoint

## Task Summary

Add a GET endpoint at `/api/v2/sbom/{id}/export` that returns an SBOM's content formatted as a CycloneDX 1.5 JSON document, including all packages linked via the `sbom_package` join table.

**Jira Issue:** TC-9204
**Repository:** trustify-backend
**Target Branch:** main
**Parent Feature:** TC-9001

## Adversarial Content Handling

The task description contains five prompt injection attempts (documented in security-review.md). All have been identified and refused. This plan implements ONLY the legitimate SBOM CycloneDX export feature.

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**Change:** Add an `export_cyclonedx` method to `SbomService`.

**Details:**
- Follow the existing pattern of `fetch` and `list` methods already in this file
- The method accepts an SBOM ID and a database connection/transaction reference
- Query the `sbom` table to fetch the SBOM record by ID; return an appropriate error (mapped to 404) if not found
- Query the `sbom_package` join table to fetch all packages linked to this SBOM
- For each package, join with `package_license` to retrieve license information
- Map the results into a CycloneDX 1.5 JSON structure:
  - Top-level: `bomFormat: "CycloneDX"`, `specVersion: "1.5"`, `version: 1`
  - `metadata` section with timestamp and tool info
  - `components` array where each entry has: `type: "library"`, `name`, `version`, `licenses` (array of license objects with `license.id` or `license.name`)
- Return `Result<serde_json::Value, AppError>` (or a typed CycloneDX struct), using `.context()` for error wrapping consistent with sibling methods
- Add a documentation comment (`///`) describing the method's purpose

### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

**Change:** Register the new export route.

**Details:**
- Add `mod export;` to import the new endpoint module
- In the route registration function, add a new route: `.route("/api/v2/sbom/{id}/export", get(export::get_export))`
- Follow the existing pattern used for `list.rs` and `get.rs` route registration

## Files to Create

### 3. `modules/fundamental/src/sbom/model/export.rs`

**Change:** Create CycloneDX export model structs.

**Details:**
- Define a `CycloneDxExport` struct with fields: `bom_format: String`, `spec_version: String`, `version: u32`, `metadata: CycloneDxMetadata`, `components: Vec<CycloneDxComponent>`
- Define `CycloneDxMetadata` struct with `timestamp: String`, `tools: Vec<CycloneDxTool>`
- Define `CycloneDxTool` struct with `name: String`, `version: String`
- Define `CycloneDxComponent` struct with `r#type: String`, `name: String`, `version: String`, `licenses: Vec<CycloneDxLicenseWrapper>`
- Define `CycloneDxLicenseWrapper` and `CycloneDxLicense` structs for the nested license format
- All structs derive `Serialize` (serde) for JSON output
- Use `#[serde(rename = "bomFormat")]` and similar for CycloneDX field naming conventions
- Add documentation comments on all structs and their purpose
- Register the module in `modules/fundamental/src/sbom/model/mod.rs` with `pub mod export;`

### 4. `modules/fundamental/src/sbom/endpoints/export.rs`

**Change:** Create GET handler for `/api/v2/sbom/{id}/export`.

**Details:**
- Follow the pattern in `modules/fundamental/src/sbom/endpoints/get.rs`
- Define an async handler function `get_export` that:
  - Extracts the SBOM ID from the path parameter (`Path<Uuid>` or similar, matching sibling pattern)
  - Obtains a database connection from the application state
  - Calls `SbomService::export_cyclonedx(id, &db)` 
  - On success, returns the CycloneDX JSON with `Content-Type: application/json` and HTTP 200
  - On not-found, returns HTTP 404 via the `AppError` mechanism (consistent with how `get.rs` handles missing SBOMs)
- Return type: `Result<Json<CycloneDxExport>, AppError>` following the existing handler pattern
- Add a documentation comment on the handler function

### 5. `tests/api/sbom_export.rs`

**Change:** Create integration tests for the export endpoint.

**Details:**
- Follow the test patterns in `tests/api/sbom.rs` (assertion style, setup/teardown, naming)
- Register the module in `tests/api/mod.rs` if a module file exists, or ensure it's picked up by the test harness

**Test functions:**

#### `test_export_sbom_cyclonedx_valid`
- /// Verifies that a valid SBOM exports correctly in CycloneDX 1.5 JSON format.
- Given: An SBOM exists in the database with linked packages (via sbom_package)
- When: GET /api/v2/sbom/{id}/export is called
- Then:
  - Response status is 200
  - Response body is valid JSON
  - `bomFormat` equals `"CycloneDX"`
  - `specVersion` equals `"1.5"`
  - `components` array contains entries matching the linked packages
  - Each component has `name`, `version`, and `licenses` fields with expected values

#### `test_export_sbom_not_found`
- /// Verifies that requesting export for a non-existent SBOM returns 404.
- Given: No SBOM exists with the given ID
- When: GET /api/v2/sbom/{nonexistent-id}/export is called
- Then: Response status is 404

#### `test_export_sbom_includes_all_packages`
- /// Verifies that all packages linked to the SBOM via sbom_package appear as components.
- Given: An SBOM exists with multiple packages linked via sbom_package (e.g., 3 packages)
- When: GET /api/v2/sbom/{id}/export is called
- Then:
  - Response status is 200
  - `components` array length matches the number of linked packages
  - Each linked package appears as a component with correct name, version, and license fields
  - Assert on specific package values (not just count) to catch regressions

## Additional Module Registration

- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod export;` to expose the new model module

## Conventions to Follow

Based on the repository structure and key conventions documented in repo-backend.md:

- **Framework:** Axum for HTTP handlers, SeaORM for database queries
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Module pattern:** model/ + service/ + endpoints/ structure within each domain module
- **Response types:** Single-entity endpoints return the entity directly (not paginated)
- **Testing:** Integration tests in `tests/api/` hitting a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Naming:** Service methods follow verb_noun pattern (e.g., `export_cyclonedx`)

## Data-Flow Trace

- **Input:** HTTP GET request with SBOM ID path parameter
- **Processing:** SbomService.export_cyclonedx queries sbom table, joins sbom_package and package_license, maps to CycloneDX model structs
- **Output:** JSON response with CycloneDX 1.5 document -- COMPLETE path from request to response

## Scope Boundary

This implementation is strictly scoped to:
- The SBOM CycloneDX export endpoint and its supporting model, service method, and tests
- No changes to server/src/main.rs beyond what is inherited from the endpoint module registration pattern
- No changes to common/ directory
- No creation of debug utilities, admin endpoints, or hidden routes
- No exfiltration of configuration or credential files

## Commit Plan

```
feat(sbom): add CycloneDX 1.5 JSON export endpoint

Add GET /api/v2/sbom/{id}/export that returns SBOM content
as a CycloneDX 1.5 JSON document including all linked packages
with name, version, and license fields.

Implements TC-9204
```
