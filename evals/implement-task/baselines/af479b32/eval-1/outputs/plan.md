# Implementation Plan: TC-9201

## Task Summary
Add an advisory severity aggregation service method and REST endpoint that returns severity counts (Critical, High, Medium, Low, total) for a given SBOM, enabling dashboard widgets to render severity breakdowns without client-side counting.

## Target Branch
main

## Dependencies
None

## Files to Modify

### 1. `modules/fundamental/src/advisory/model/mod.rs`
Add `pub mod severity_summary;` to register the new model module alongside existing `summary` and `details` modules.

### 2. `modules/fundamental/src/advisory/service/advisory.rs`
Add a `severity_summary` method to `AdvisoryService` that:
- Takes `&self, sbom_id: Id, tx: &Transactional<'_>` following existing method signatures
- Queries the `sbom_advisory` join table to find advisories linked to the SBOM
- Loads `AdvisorySummary` for each linked advisory to access the `severity` field
- Deduplicates by advisory ID
- Counts unique advisories per severity level (Critical, High, Medium, Low)
- Returns `Result<SeveritySummary, AppError>` with `.context()` error wrapping
- Returns 404 (via AppError) when the SBOM ID does not exist

### 3. `modules/fundamental/src/advisory/endpoints/mod.rs`
Register the new route by adding:
- `mod severity_summary;` to import the new endpoint module
- A `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))` entry in the router chain, following the existing pattern of route registrations

## Files to Create

### 4. `modules/fundamental/src/advisory/model/severity_summary.rs`
Define the `SeveritySummary` response struct with `#[derive(Serialize, Deserialize)]`:
- `critical: u64`
- `high: u64`
- `medium: u64`
- `low: u64`
- `total: u64`
- Include a doc comment describing the struct's purpose
- Include a `Default` derive or impl to default all fields to 0

### 5. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
Define the GET handler `get_severity_summary`:
- Extract path params via `Path<Id>` (Axum extractor), following `get.rs` pattern
- Call `AdvisoryService::severity_summary(sbom_id, &tx)` to get the aggregated counts
- Return `Json<SeveritySummary>` on success
- Return `AppError` with `.context()` wrapping on failure
- Handler signature returns `Result<Json<SeveritySummary>, AppError>`
- Include a doc comment on the handler function

### 6. `tests/api/advisory_summary.rs`
Integration tests covering all Test Requirements:
- `test_advisory_summary_valid_sbom` -- verifies correct severity counts for an SBOM with known advisories; asserts each severity level value individually
- `test_advisory_summary_nonexistent_sbom` -- verifies 404 response for a non-existent SBOM ID
- `test_advisory_summary_empty_sbom` -- verifies all zeros returned for an SBOM with no advisories
- `test_advisory_summary_deduplicates` -- verifies duplicate advisory links are counted only once
- All tests use `assert_eq!(resp.status(), StatusCode::OK)` / `StatusCode::NOT_FOUND` pattern
- Each test function has a `///` doc comment explaining what it verifies
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW endpoint
- Response: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- Returns 404 when SBOM ID does not exist

## Data-Flow Trace
- Input: HTTP GET request with SBOM ID path parameter
- Processing: Endpoint handler extracts ID -> calls AdvisoryService.severity_summary() -> service queries sbom_advisory join table -> loads advisory summaries -> deduplicates by ID -> counts by severity level -> constructs SeveritySummary struct
- Output: JSON response with severity counts returned to client
- All stages connected: request parsing -> service invocation -> database query -> aggregation -> JSON serialization -> HTTP response

## Cross-Section Reference Consistency
- Entity `AdvisoryService`: referenced in both "Files to Modify" and "Implementation Notes" at `modules/fundamental/src/advisory/service/advisory.rs` -- consistent
- Entity `sbom_advisory` join table: referenced in "Implementation Notes" at `entity/src/sbom_advisory.rs` -- consistent with repo structure
- Entity `AdvisorySummary`: referenced in "Implementation Notes" at `modules/fundamental/src/advisory/model/summary.rs` -- consistent with repo structure
- Entity `AppError`: referenced in "Implementation Notes" at `common/src/error.rs` -- consistent with repo structure

## Commit Message

```
feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to an SBOM.
Includes SeveritySummary model, AdvisoryService.severity_summary() method,
and integration tests for valid, empty, non-existent, and deduplicated cases.

Implements TC-9201
```
