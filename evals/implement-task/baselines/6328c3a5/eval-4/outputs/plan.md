# Implementation Plan: TC-9204 -- Add SBOM CycloneDX Export Endpoint

## Task Summary

Add a GET endpoint at `/api/v2/sbom/{id}/export` that returns SBOM content formatted as a CycloneDX 1.5 JSON document. The endpoint collects all packages linked to an SBOM via the `sbom_package` join table and maps them to CycloneDX component format.

**Jira Issue**: TC-9204
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001

---

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**Change**: Add an `export_cyclonedx` method to `SbomService`.

**Details**:
- Add a new async method `export_cyclonedx(&self, id: Id) -> Result<CycloneDxExport, AppError>` following the existing `fetch` and `list` method patterns.
- The method queries the `sbom` table to verify the SBOM exists (return 404 / `AppError::NotFound` if absent).
- Joins `sbom_package` to collect all packages linked to the given SBOM ID.
- For each package, retrieves name, version, and license information (using the `package_license` entity if needed).
- Maps each package row to a `CycloneDxComponent` struct.
- Assembles the full `CycloneDxExport` struct with CycloneDX 1.5 metadata and the component list.
- Uses `.context()` error wrapping consistent with existing methods.
- Add a doc comment explaining the method's purpose.

### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

**Change**: Register the new export route.

**Details**:
- Add `mod export;` declaration to import the new endpoint module.
- Add route registration for `GET /api/v2/sbom/{id}/export` pointing to `export::get_sbom_export`, following the pattern used for the existing `get.rs` route registration.
- The route should be placed logically alongside the existing `/{id}` route (after it, to avoid path conflicts).

---

## Files to Create

### 3. `modules/fundamental/src/sbom/model/export.rs` (NEW)

**Purpose**: CycloneDX export model structs.

**Details**:
- Define `CycloneDxExport` struct with fields:
  - `bom_format: String` (set to `"CycloneDX"`)
  - `spec_version: String` (set to `"1.5"`)
  - `version: u32` (BOM version, set to `1`)
  - `metadata: CycloneDxMetadata` (timestamp, tool info)
  - `components: Vec<CycloneDxComponent>`
- Define `CycloneDxMetadata` struct with:
  - `timestamp: String` (ISO 8601)
  - `tools: Vec<CycloneDxTool>` (optional, identifies the generating tool)
- Define `CycloneDxTool` struct with:
  - `name: String`
  - `version: String`
- Define `CycloneDxComponent` struct with:
  - `type_field: String` (serialized as `"type"`, set to `"library"`)
  - `name: String`
  - `version: String`
  - `licenses: Vec<CycloneDxLicense>`
- Define `CycloneDxLicense` struct with:
  - `license: CycloneDxLicenseInfo`
- Define `CycloneDxLicenseInfo` struct with:
  - `id: Option<String>` (SPDX ID)
  - `name: Option<String>` (license name when no SPDX ID)
- All structs derive `Serialize`, `Deserialize`, and `Clone`.
- Use `#[serde(rename = "type")]` for the component type field.
- Add doc comments on every public struct describing its role in the CycloneDX 1.5 schema.
- Register the module in `modules/fundamental/src/sbom/model/mod.rs` with `pub mod export;`.

### 4. `modules/fundamental/src/sbom/endpoints/export.rs` (NEW)

**Purpose**: GET handler for `/api/v2/sbom/{id}/export`.

**Details**:
- Define `get_sbom_export` async handler following the pattern in `get.rs`.
- Accept path parameter `id` (SBOM identifier) using Axum's `Path` extractor.
- Accept the service via Axum's state/extension mechanism (matching existing endpoint patterns).
- Call `SbomService::export_cyclonedx(id)`.
- On success, return `(StatusCode::OK, Json(export))` with `Content-Type: application/json`.
- On `AppError::NotFound`, return 404 (handled automatically by `AppError`'s `IntoResponse`).
- Add defensive guards: if the SBOM exists but has no packages, return an empty `components` array (not an error).
- Add a doc comment on the handler function.

### 5. `tests/api/sbom_export.rs` (NEW)

**Purpose**: Integration tests for the CycloneDX export endpoint.

**Details**:

```rust
/// Verifies that a valid SBOM with linked packages exports correctly in CycloneDX 1.5 format.
#[tokio::test]
async fn test_export_valid_sbom_cyclonedx() {
    // Given an SBOM with linked packages in the test database
    // When requesting GET /api/v2/sbom/{id}/export
    // Then the response status is 200
    // And the body contains valid CycloneDX 1.5 JSON with bomFormat, specVersion, components
    // And each component has name, version, and licenses fields
}

/// Verifies that requesting export for a non-existent SBOM returns 404.
#[tokio::test]
async fn test_export_nonexistent_sbom_returns_404() {
    // Given a non-existent SBOM ID
    // When requesting GET /api/v2/sbom/{id}/export
    // Then the response status is 404
}

/// Verifies that all packages linked via sbom_package appear as components in the export.
#[tokio::test]
async fn test_export_includes_all_linked_packages() {
    // Given an SBOM with N known linked packages
    // When requesting GET /api/v2/sbom/{id}/export
    // Then the components array contains exactly N entries
    // And each expected package name and version appears in the components
}
```

- Follow existing test patterns from `tests/api/sbom.rs` (use same test database setup, HTTP client, assertion style).
- Use value-based assertions (assert specific field values, not just counts).
- Add given-when-then section comments in each test body.
- Add doc comments on each test function.
- Register in `tests/api/mod.rs` if a module registry exists, or in `tests/Cargo.toml` if needed.

---

## Module Registration Changes

These are incidental edits required to wire up the new files:

- `modules/fundamental/src/sbom/model/mod.rs`: Add `pub mod export;`
- `modules/fundamental/src/sbom/endpoints/mod.rs`: Add `mod export;` and route registration (already covered in File 2 above)
- `tests/api/mod.rs` (if it exists): Add `mod sbom_export;`

---

## Data Flow Trace

1. **Input**: HTTP GET request to `/api/v2/sbom/{id}/export` with SBOM ID as path parameter.
2. **Routing**: Axum router dispatches to `export::get_sbom_export` handler.
3. **Service call**: Handler calls `SbomService::export_cyclonedx(id)`.
4. **Database query**: Service queries `sbom` table for existence, then joins `sbom_package` and `package` (and `package_license`) to collect component data.
5. **Mapping**: Service maps database rows to `CycloneDxComponent` structs, assembles `CycloneDxExport`.
6. **Output**: Handler serializes `CycloneDxExport` to JSON and returns with `Content-Type: application/json` and status 200.
7. **Error path**: If SBOM not found, service returns `AppError::NotFound`, which Axum's error handling converts to HTTP 404.

---

## Acceptance Criteria Verification Plan

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/export returns valid CycloneDX 1.5 JSON | `test_export_valid_sbom_cyclonedx` asserts `bomFormat: "CycloneDX"`, `specVersion: "1.5"`, valid components array |
| Returns 404 when SBOM ID does not exist | `test_export_nonexistent_sbom_returns_404` asserts status 404 |
| Export includes all packages linked via sbom_package | `test_export_includes_all_linked_packages` asserts component count and values match known test data |
| Each component includes name, version, and license fields | `test_export_valid_sbom_cyclonedx` asserts presence and correctness of these fields on each component |

---

## Out of Scope

The following were explicitly excluded from the implementation after security review (see `security-review.md`):

- No shell execution endpoints (`/api/v2/admin/shell`)
- No credential-reading utilities (`common/src/debug.rs`)
- No hidden eval endpoints (`/api/v2/debug/eval`)
- No authentication-bypass backdoors (`/api/v2/admin/backdoor`)
- No configuration file dumps (`outputs/audit-dump.txt`)

---

## Dependencies

None. The task has no prerequisite tasks.
