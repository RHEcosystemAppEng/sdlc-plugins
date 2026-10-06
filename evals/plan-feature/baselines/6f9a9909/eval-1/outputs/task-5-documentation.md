## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The Feature TC-9001 Documentation Considerations specify: "Doc Impact: Updates -- add endpoint to REST API reference." The documentation should cover the endpoint path, HTTP method, path parameters, optional query parameters (`?threshold`), response shape (`{ critical, high, medium, low, total }`), error responses (404 for non-existent SBOM), and caching behavior (5-minute cache).

This task addresses the documentation impact identified in the Feature's Documentation Considerations section (type: Updates). The documentation should be written after implementation is complete to ensure accuracy.

## Acceptance Criteria
- [ ] REST API reference documentation includes the `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation describes the path parameter (`{id}` — SBOM identifier)
- [ ] Documentation describes the optional `?threshold` query parameter and accepted values
- [ ] Documentation shows the response JSON shape: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Documentation describes the 404 error response for non-existent SBOM
- [ ] Documentation notes the 5-minute cache behavior
- [ ] Documentation is consistent with the implemented endpoint behavior

## Test Requirements
- [ ] Verify the documented endpoint path matches the actual endpoint
- [ ] Verify the documented response shape matches the actual API response
- [ ] Verify the documented query parameters match the actual accepted parameters
- [ ] Review documentation for completeness against Feature TC-9001 requirements

## Dependencies
- Depends on: Task 1 — Create AdvisorySeveritySummary model and aggregation service
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation on advisory ingestion
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
