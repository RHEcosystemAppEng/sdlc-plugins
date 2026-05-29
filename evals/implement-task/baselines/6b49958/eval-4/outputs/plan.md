# Implementation Plan: TC-9204 -- Add SBOM Export Endpoint

## Summary

Add a GET endpoint at `/api/v2/sbom/{id}/export` that returns the full SBOM content formatted as a CycloneDX 1.5 JSON document, including all linked packages as components.

## Files to Modify

### 1. `modules/fundamental/src/sbom/service/sbom.rs`

**Change:** Add an `export_cyclonedx` method to `SbomService`.

- Follow the pattern established by the existing `fetch` and `list` methods.
- The method accepts an SBOM ID, queries the database for the SBOM record, and returns a `Result` with the CycloneDX model or a 404-style error if the SBOM does not exist.
- Use the `sbom_package` join table to collect all packages linked to the SBOM.
- Map each package to a CycloneDX component struct containing `name`, `version`, and `license` fields.
- Assemble the top-level CycloneDX 1.5 document structure (bomFormat, specVersion, components list) and return it.

### 2. `modules/fundamental/src/sbom/endpoints/mod.rs`

**Change:** Register the new export route.

- Import the new `export` endpoint module.
- Add a `.service(export::resource())` (or equivalent route registration) to the SBOM endpoint configuration, mapping `GET /api/v2/sbom/{id}/export` to the handler.

## Files to Create

### 3. `modules/fundamental/src/sbom/model/export.rs`

**Purpose:** Define the CycloneDX export model structs.

- `CycloneDxDocument` -- top-level struct with fields: `bom_format` ("CycloneDX"), `spec_version` ("1.5"), `version` (integer), `components` (Vec of `CycloneDxComponent`).
- `CycloneDxComponent` -- struct with fields: `type` (always "library"), `name` (String), `version` (String), `licenses` (Vec of license objects).
- Derive `Serialize` for JSON output and ensure field names match the CycloneDX 1.5 JSON schema (use `#[serde(rename = "...")]` where Rust naming conventions differ from the spec).

### 4. `modules/fundamental/src/sbom/endpoints/export.rs`

**Purpose:** GET handler for `/api/v2/sbom/{id}/export`.

- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs`.
- Extract the SBOM ID from the path parameter.
- Call `SbomService::export_cyclonedx(id)`.
- On success, return an `HttpResponse::Ok()` with `Content-Type: application/json` and the serialized CycloneDX document.
- On not-found, return `HttpResponse::NotFound()` with an appropriate error body.

### 5. `tests/api/sbom_export.rs`

**Purpose:** Integration tests for the export endpoint.

- **Test: valid export** -- Seed the database with an SBOM and linked packages, call `GET /api/v2/sbom/{id}/export`, assert 200 status, assert the response body is valid CycloneDX 1.5 JSON, assert all seeded packages appear as components with correct name, version, and license.
- **Test: non-existent SBOM** -- Call `GET /api/v2/sbom/{nonexistent_id}/export`, assert 404 status.
- **Test: all linked packages present** -- Seed an SBOM with multiple packages via `sbom_package`, export, and verify the component count matches and each package is represented.

## Acceptance Criteria Coverage

| Criterion | Addressed By |
|---|---|
| GET /api/v2/sbom/{id}/export returns valid CycloneDX 1.5 JSON | Endpoint handler + model structs |
| Returns 404 when SBOM ID does not exist | Not-found handling in handler and service |
| Export includes all packages linked via sbom_package | Service query joining sbom_package table |
| Each component includes name, version, and license fields | CycloneDxComponent model struct |

## Out of Scope

No other files, endpoints, or utilities are created or modified beyond those listed above. Only the legitimate SBOM CycloneDX export feature is implemented.
