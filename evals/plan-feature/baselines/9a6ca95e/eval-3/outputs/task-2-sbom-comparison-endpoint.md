## Repository

trustify-backend

## Target Branch

main

## Priority

Critical

## Fix Versions

RHTPA 1.5.0

## Description

Expose the SBOM comparison service as a REST endpoint at `GET /api/v2/sbom/compare?left={id1}&right={id2}`. This task creates the endpoint handler, registers the route in the SBOM module's route configuration, and adds integration tests that verify the endpoint against a real PostgreSQL test database. The endpoint validates that both `left` and `right` query parameters are present, delegates to `SbomService::compare`, and returns the `SbomComparisonResult` as JSON.

## Acceptance Criteria

- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns a 200 response with the `SbomComparisonResult` JSON body
- [ ] Missing `left` or `right` query parameter returns 400 Bad Request with a descriptive error message
- [ ] Non-existent SBOM ID in either parameter returns 404 Not Found
- [ ] The endpoint is registered in the SBOM module's route configuration alongside existing SBOM endpoints
- [ ] The endpoint appears in the generated OpenAPI spec with correct query parameter documentation
- [ ] Response time is under 1 second (p95) for SBOMs with up to 2000 packages each

## Test Requirements

- [ ] Integration test: compare two SBOMs with known differences and verify the response body contains correct diff entries
- [ ] Integration test: compare with a missing query parameter returns 400
- [ ] Integration test: compare with a non-existent SBOM ID returns 404
- [ ] Integration test: compare an SBOM with itself returns 200 with empty diff arrays

## Dependencies

- Task 1 (sbom-comparison-model-and-service) -- provides the `SbomComparisonResult` type and `SbomService::compare` method

## Files to Modify

- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the new comparison route

## Files to Create

- `modules/fundamental/src/sbom/endpoints/compare.rs` -- `GET /api/v2/sbom/compare` handler
- `tests/api/sbom_compare.rs` -- integration tests for the comparison endpoint

## Implementation Notes

- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler signature, extractors, and error mapping.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing `/api/v2/sbom` and `/api/v2/sbom/{id}` routes.
- Use Axum `Query` extractor to parse `left` and `right` query parameters. Define a `CompareQuery` struct with `#[derive(Deserialize)]`.
- Return `Result<Json<SbomComparisonResult>, AppError>` following the pattern in `get.rs`.
- Integration tests follow the pattern in `tests/api/sbom.rs` -- set up test data, call the endpoint, assert status code and response body fields.
- Add OpenAPI documentation via `utoipa::path` attribute macro, consistent with existing endpoint annotations.

## Conventions

- **Error Handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's error handling scope.
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/sbom_compare.rs` matching the convention's testing scope.
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's route registration scope.
