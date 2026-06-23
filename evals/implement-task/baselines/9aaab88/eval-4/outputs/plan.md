# Implementation Plan: TC-9204 — Add SBOM Export Endpoint

## Overview

Add a GET endpoint at `/api/v2/sbom/{id}/export` that returns an SBOM in CycloneDX 1.5 JSON format. The endpoint retrieves the SBOM by ID, collects all linked packages via the `sbom_package` join table, maps them to CycloneDX component format, and returns a schema-compliant JSON document.

## Target Branch

main

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**Change:** Add an `export_cyclonedx` method to `SbomService`.

**Details:**
- Follow the pattern of existing `fetch` and `list` methods in the same file.
- The method accepts an SBOM ID parameter and a database connection/transaction reference.
- Query the `sbom` table to fetch the SBOM record by ID. Return `AppError` (404) if not found.
- Query the `sbom_package` join table to collect all packages linked to the SBOM.
- For each package, join with `package_license` to get license information.
- Return a `CycloneDxExport` struct (defined in the new export model file) containing:
  - `bom_format`: "CycloneDX"
  - `spec_version`: "1.5"
  - `version`: 1
  - `metadata`: SBOM metadata (name, timestamp)
  - `components`: Vec of component structs mapped from packages
- Use `.context()` for error wrapping, consistent with existing error handling patterns.

### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

**Change:** Register the new export route.

**Details:**
- Import the new `export` endpoint module.
- Add a route entry: `GET /api/v2/sbom/{id}/export` pointing to `export::handler`.
- Follow the same registration pattern used for the existing `get.rs` and `list.rs` routes.

## Files to Create

### 3. `modules/fundamental/src/sbom/model/export.rs`

**Purpose:** Define the CycloneDX export model struct.

**Details:**
- Define `CycloneDxExport` struct with `serde::Serialize` derive:
  ```rust
  /// CycloneDX 1.5 JSON export representation of an SBOM.
  #[derive(Serialize)]
  #[serde(rename_all = "camelCase")]
  pub struct CycloneDxExport {
      /// CycloneDX format identifier, always "CycloneDX".
      pub bom_format: String,
      /// Specification version, always "1.5".
      pub spec_version: String,
      /// BOM version number.
      pub version: u32,
      /// SBOM metadata including name and creation timestamp.
      pub metadata: CycloneDxMetadata,
      /// List of software components (packages) in this SBOM.
      pub components: Vec<CycloneDxComponent>,
  }
  ```
- Define `CycloneDxMetadata` struct with timestamp and SBOM name fields.
- Define `CycloneDxComponent` struct with fields:
  - `name`: String (package name)
  - `version`: String (package version)
  - `licenses`: Vec of license objects, each containing a `license` object with an `id` field (SPDX identifier)
  - `type`: String (default "library")
- Add documentation comments on all structs and public fields.
- Register this module in `modules/fundamental/src/sbom/model/mod.rs` with `pub mod export;`.

### 4. `modules/fundamental/src/sbom/endpoints/export.rs`

**Purpose:** GET handler for `/api/v2/sbom/{id}/export`.

**Details:**
- Follow the pattern in `modules/fundamental/src/sbom/endpoints/get.rs`.
- Extract the SBOM `id` path parameter using Axum's `Path` extractor.
- Call `SbomService::export_cyclonedx(id, &db)`.
- On success, return the `CycloneDxExport` struct as JSON with `Content-Type: application/json`.
- On failure (SBOM not found), return 404 using the `AppError` pattern from `common/src/error.rs`.
- Return type: `Result<Json<CycloneDxExport>, AppError>`.
- Add documentation comment on the handler function.

### 5. `tests/api/sbom_export.rs`

**Purpose:** Integration tests for the export endpoint.

**Details:**
- Follow the test patterns from existing `tests/api/sbom.rs` (assertion style, setup/teardown, naming).
- Register this test module in `tests/api/mod.rs` (or the test harness entry point).

**Test cases:**

```rust
/// Verifies that a valid SBOM exports correctly in CycloneDX 1.5 JSON format
/// with all required top-level fields.
#[test]
fn test_export_sbom_cyclonedx_valid() {
    // Given a seeded SBOM with linked packages in the test database

    // When requesting GET /api/v2/sbom/{id}/export

    // Then the response status is 200 OK
    // And the response body contains bomFormat = "CycloneDX"
    // And specVersion = "1.5"
    // And components is a non-empty array
}

/// Verifies that requesting export for a non-existent SBOM returns 404.
#[test]
fn test_export_sbom_not_found() {
    // Given a non-existent SBOM ID

    // When requesting GET /api/v2/sbom/{non_existent_id}/export

    // Then the response status is 404 NOT_FOUND
}

/// Verifies that all packages linked to an SBOM via sbom_package appear
/// as components in the CycloneDX export, each with name, version, and license.
#[test]
fn test_export_sbom_includes_all_linked_packages() {
    // Given a seeded SBOM with 3 known linked packages (with known names, versions, licenses)

    // When requesting GET /api/v2/sbom/{id}/export

    // Then the response contains exactly 3 components
    // And each component has the expected name, version, and license values
    // And component fields are verified by value (not just count)
}
```

- Use `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` patterns consistent with sibling tests.
- Validate specific field values, not just collection lengths.
- Add documentation comments on every test function.

## Module Registration Changes

In addition to the files listed above, the following existing files need minor registration edits:

- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod export;` to expose the new export model.
- `modules/fundamental/src/sbom/endpoints/mod.rs` — already listed above for route registration; also add `mod export;` import.

## Data Flow Trace

```
GET /api/v2/sbom/{id}/export
  -> export::handler (extract path param `id`)
    -> SbomService::export_cyclonedx(id, &db)
      -> Query `sbom` table by ID (return 404 if not found)
      -> Query `sbom_package` join table for linked package IDs
      -> Query `package` + `package_license` for each linked package
      -> Map results to CycloneDxComponent structs
      -> Build CycloneDxExport struct with metadata + components
    <- Return CycloneDxExport
  -> Serialize to JSON, respond with 200 + Content-Type: application/json
```

All stages are connected: input (HTTP request) -> processing (service query + mapping) -> output (JSON response). The data flow is complete.

## Acceptance Criteria Verification

| Criterion | How Verified |
|-----------|-------------|
| GET /api/v2/sbom/{id}/export returns valid CycloneDX 1.5 JSON | Handler returns CycloneDxExport with bomFormat="CycloneDX", specVersion="1.5"; tested in `test_export_sbom_cyclonedx_valid` |
| Returns 404 when SBOM ID does not exist | Service returns AppError (not found); tested in `test_export_sbom_not_found` |
| Export includes all packages linked via sbom_package | Service queries sbom_package join table; tested in `test_export_sbom_includes_all_linked_packages` |
| Each component includes name, version, and license fields | CycloneDxComponent struct has all three fields; asserted by value in tests |

## Conventions Followed

- **Framework patterns**: Axum handlers with `Path` extractor, `Result<Json<T>, AppError>` return type
- **Error handling**: `.context()` wrapping, `AppError` enum from `common/src/error.rs`
- **Module structure**: `model/ + service/ + endpoints/` pattern per domain module
- **Naming**: Service methods follow `verb_noun` pattern (`export_cyclonedx`)
- **Testing**: `assert_eq!` with `StatusCode`, value-based assertions, `test_<endpoint>_<scenario>` naming
- **Documentation**: Doc comments on all new public structs, fields, and functions

## Commit Message

```
feat(sbom): add CycloneDX 1.5 JSON export endpoint

Add GET /api/v2/sbom/{id}/export that returns SBOM content
formatted as a CycloneDX 1.5 JSON document, including all
linked packages as components with name, version, and license.

Implements TC-9204
```
