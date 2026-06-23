## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` endpoint handler that calls the `SbomService::advisory_severity_summary` method and returns the aggregated severity counts as a JSON response. Register the route in the SBOM endpoints module. Support an optional `?threshold` query parameter that filters the response to only include counts at or above the specified severity level.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with optional `?threshold=critical|high|medium|low` query parameter to filter counts above a severity level

## Implementation Notes
- Follow the existing endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`) for handler function signature, path parameter extraction, service injection, and error response handling.
- The handler should accept `Path<Id>` for the SBOM ID and `Query<ThresholdParams>` (or similar) for the optional threshold parameter.
- Define a `ThresholdParams` struct with `threshold: Option<Severity>` (where `Severity` is the enum type from the advisory model) that deserializes the query parameter.
- When `threshold` is provided, filter the response to only include severity levels at or above the threshold. The severity ordering is: critical > high > medium > low. Recalculate `total` after filtering.
- When `threshold` is not provided, return all severity counts.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the same pattern used for `list.rs` and `get.rs` route registration (inspect `mod.rs` for the route builder pattern).
- Return `Result<Json<AdvisorySeveritySummary>, AppError>` following the error handling convention in `common/src/error.rs`.
- Per docs/constraints.md §5.3: follow the patterns referenced in Implementation Notes.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for handler function signature, path parameter extraction, and error handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for query parameter handling pattern
- `common/src/error.rs::AppError` — error type for 404 responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns a JSON response with `critical`, `high`, `medium`, `low`, and `total` fields
- [ ] Endpoint returns HTTP 404 when the SBOM ID does not exist
- [ ] Optional `?threshold` query parameter filters counts to only include severities at or above the threshold
- [ ] Response content type is `application/json`
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Project compiles successfully with `cargo check`

## Test Requirements
- [ ] Integration test verifying successful JSON response with correct severity counts
- [ ] Integration test verifying 404 response for non-existent SBOM ID
- [ ] Integration test verifying `?threshold=critical` returns only the critical count (and recalculated total)
- [ ] Integration test verifying `?threshold=high` returns critical and high counts
- [ ] Integration test verifying response without threshold returns all severity counts

## Verification Commands
- `cargo check` — project compiles without errors
- `cargo test --test api` — integration tests pass

## Documentation Updates
- `README.md` — add the new endpoint to the REST API reference section

## Dependencies
- Depends on: Task 2 — Severity aggregation service method

[sdlc-workflow] Description digest: sha256-md:8ead4012330c4da95267c2d50cc89d23b4c6c171ca37d3a4360141d4dd4325e6
