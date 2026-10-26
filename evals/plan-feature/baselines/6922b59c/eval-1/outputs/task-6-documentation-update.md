## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The documentation should cover the endpoint path, HTTP method, path parameters, optional query parameters (`threshold`), response shape, caching behavior, and error responses. This addresses the Documentation Considerations identified in the feature description (TC-9001): "Updates — add endpoint to REST API reference."

The documentation update ensures API consumers can discover and correctly integrate with the advisory severity summary endpoint without needing to inspect the source code.

## Acceptance Criteria
- [ ] REST API reference documentation includes the `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation describes the path parameter `{id}` (SBOM UUID)
- [ ] Documentation describes the optional `?threshold` query parameter with valid values (critical, high, medium, low)
- [ ] Documentation shows the response JSON shape: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Documentation notes the 5-minute cache TTL and `Cache-Control` header behavior
- [ ] Documentation describes the 404 response for non-existent SBOM IDs
- [ ] Documentation describes the 400 response for invalid threshold values
- [ ] Documentation is consistent with existing endpoint documentation style

## Test Requirements
- [ ] Documentation accurately reflects the implemented endpoint behavior
- [ ] All endpoint parameters, response fields, and error codes are documented
- [ ] Documentation is consistent with existing SBOM and advisory endpoint documentation

## Dependencies
- Depends on: Task 1 — Add advisory severity summary response model
- Depends on: Task 2 — Add SBOM advisory severity aggregation service method
- Depends on: Task 3 — Add advisory summary REST endpoint with caching
- Depends on: Task 4 — Add cache invalidation on advisory ingestion
- Depends on: Task 5 — Add integration tests for advisory summary endpoint
