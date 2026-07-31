## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The Feature's Documentation Considerations specify doc impact type "Updates" — updates to existing content are needed to document the endpoint path, query parameters, request/response shape, and usage examples. API consumers need to know:
- The endpoint path and HTTP method
- The response shape (`{ critical, high, medium, low, total }`)
- The optional `?threshold` query parameter and its behavior
- Error responses (404 for non-existent SBOM, 400 for invalid threshold)
- Caching behavior (5-minute cache)

Reference: Feature TC-9001 — Add advisory severity aggregation endpoint.

## Acceptance Criteria
- [ ] REST API reference documentation includes the `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation describes the response shape with field names and types
- [ ] Documentation describes the optional `?threshold` query parameter, accepted values, and filtering behavior
- [ ] Documentation describes error responses (404, 400)
- [ ] Documentation mentions the 5-minute cache behavior
- [ ] Documentation is consistent with the implemented endpoint behavior

## Test Requirements
- [ ] Verify that the documented endpoint path, parameters, and response shape match the actual implementation
- [ ] Verify that the documented error responses match the actual endpoint behavior
- [ ] Verify that example requests and responses in the documentation are accurate

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service
- Depends on: Task 2 — Add advisory summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory severity summary
- Depends on: Task 4 — Add threshold query parameter for advisory summary
- Depends on: Task 5 — Add integration tests for advisory summary endpoint
