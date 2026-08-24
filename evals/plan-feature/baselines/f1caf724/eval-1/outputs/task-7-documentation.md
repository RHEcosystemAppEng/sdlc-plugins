## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint added by feature TC-9001. The feature's Documentation Considerations specify "Updates" doc impact type: the new endpoint must be added to the existing API reference with its path, parameters, and response shape. The documentation should cover the endpoint path, the optional `?threshold` query parameter, the response JSON structure (`{ critical, high, medium, low, total }`), error responses (404 for non-existent SBOM), and caching behavior (5-minute cache TTL). Reference the existing SBOM advisory endpoints documentation for style and format consistency.

## Acceptance Criteria
- [ ] REST API reference includes the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation describes the response JSON structure with all fields (`critical`, `high`, `medium`, `low`, `total`)
- [ ] Documentation describes the optional `?threshold` query parameter and its valid values
- [ ] Documentation describes error responses (404 for non-existent SBOM ID)
- [ ] Documentation notes the 5-minute caching behavior
- [ ] Documentation style is consistent with existing SBOM and advisory endpoint documentation

## Test Requirements
- [ ] Verify the documented endpoint path, parameters, and response shape match the implemented endpoint
- [ ] Verify the documented error responses match actual endpoint behavior
- [ ] Verify the documentation is consistent in style and format with existing API reference entries

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory summary on advisory ingestion
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
