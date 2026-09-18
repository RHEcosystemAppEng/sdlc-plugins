## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint (TC-9001). The doc impact type is "Updates" — add the endpoint to existing API documentation. API consumers need to know the endpoint path, query parameters, response shape, caching behavior, and error responses. Reference the existing SBOM advisory endpoints documentation for format consistency.

Documentation scope from Feature TC-9001 Documentation Considerations:
- **Doc Impact:** Updates — add endpoint to REST API reference
- **User purpose:** API consumers need to know the endpoint path, parameters, and response shape
- **Reference material:** Existing SBOM advisory endpoints documentation

## Acceptance Criteria
- [ ] REST API reference documents the `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation includes the endpoint path, HTTP method, and purpose
- [ ] Documentation describes the response shape: `{ critical: N, high: N, medium: N, low: N, total: N }`
- [ ] Documentation describes the optional `?threshold=<severity>` query parameter and its behavior
- [ ] Documentation notes the 5-minute cache TTL behavior
- [ ] Documentation describes the 404 response for non-existent SBOM IDs
- [ ] Documentation is consistent with the format of existing SBOM and advisory endpoint documentation

## Test Requirements
- [ ] Verify the documentation accurately describes the endpoint's behavior as implemented
- [ ] Verify the response shape example matches the actual API response
- [ ] Verify the documentation is consistent with existing endpoint documentation format

## Dependencies
- Depends on: Task 1 — Add advisory severity count model and service method
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory summaries in ingestion pipeline
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
