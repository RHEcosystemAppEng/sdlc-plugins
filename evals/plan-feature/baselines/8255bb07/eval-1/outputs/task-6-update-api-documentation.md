## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint added by feature TC-9001. The feature's Documentation Considerations indicate doc impact type "Updates" — the endpoint must be added to the existing REST API reference documentation.

Documentation should cover:
- Endpoint path and HTTP method
- Path parameters (SBOM ID)
- Optional query parameters (?threshold with valid values: critical, high, medium, low)
- Response shape: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- Error responses (404 for non-existent SBOM, 400 for invalid threshold)
- Cache behavior (5-minute response cache)
- Example request and response

Reference material: existing SBOM advisory endpoints documentation.

## Acceptance Criteria
- [ ] REST API reference includes the new GET /api/v2/sbom/{id}/advisory-summary endpoint
- [ ] Documentation describes path parameters, query parameters, response shape, and error responses
- [ ] Documentation includes cache behavior (5-minute TTL)
- [ ] Documentation is consistent with the implemented endpoint behavior
- [ ] Example request and response are provided

## Test Requirements
- [ ] Verify documentation accurately describes the endpoint path, parameters, and response shape
- [ ] Verify example request and response match actual endpoint behavior
- [ ] Verify documentation covers error cases (404, 400)

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching and threshold filter
- Depends on: Task 3 — Add cache invalidation for advisory summaries on advisory ingestion
