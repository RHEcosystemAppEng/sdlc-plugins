## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The feature TC-9001 adds a server-side advisory severity aggregation endpoint that replaces client-side counting. The documentation should cover the endpoint path, HTTP method, path parameters, optional query parameters (`?threshold`), response shape, error responses (404), and caching behavior (5-minute TTL).

Doc impact type: Updates to existing content.
Reference: Feature TC-9001 — Add advisory severity aggregation endpoint.

## Acceptance Criteria
- [ ] REST API reference documents the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation includes the response shape: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Documentation describes the optional `?threshold` query parameter and its valid values (critical, high, medium, low)
- [ ] Documentation notes the 404 response for non-existent SBOM IDs
- [ ] Documentation mentions the 5-minute cache TTL behavior

## Test Requirements
- [ ] Verify documentation accurately reflects the implemented endpoint path and response shape
- [ ] Verify the threshold parameter description matches the implementation
- [ ] Verify documentation is consistent with existing SBOM endpoint documentation style

## Dependencies
- Depends on: Task 1 — Add advisory severity summary response model
- Depends on: Task 2 — Add advisory severity aggregation service method
- Depends on: Task 3 — Add advisory-summary REST endpoint with caching
- Depends on: Task 4 — Add cache invalidation for advisory ingestion
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint
