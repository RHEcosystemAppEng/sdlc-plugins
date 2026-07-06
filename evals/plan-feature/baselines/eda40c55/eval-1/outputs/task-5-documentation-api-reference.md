## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The feature TC-9001 adds an advisory severity aggregation endpoint, and the Documentation Considerations section specifies doc impact type "Updates" — the endpoint must be added to the existing REST API reference.

The documentation should cover:
- Endpoint path and HTTP method
- Path parameters (SBOM ID)
- Optional query parameters (threshold)
- Response shape with field descriptions
- Response status codes (200, 404)
- Caching behavior (5-minute cache)
- Example request and response

Reference material: existing SBOM advisory endpoints documentation.

## Acceptance Criteria
- [ ] REST API reference includes the new GET /api/v2/sbom/{id}/advisory-summary endpoint
- [ ] Documentation covers path parameters, query parameters, response shape, status codes, and caching behavior
- [ ] Documentation is consistent with the implemented endpoint behavior
- [ ] An example request and response is included

## Test Requirements
- [ ] Verify documented endpoint path matches the implemented endpoint
- [ ] Verify documented response shape matches the actual SeveritySummary struct fields
- [ ] Verify documented query parameters match the implemented threshold filter
- [ ] Verify documented status codes (200, 404) match the endpoint behavior

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory ingestion
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
