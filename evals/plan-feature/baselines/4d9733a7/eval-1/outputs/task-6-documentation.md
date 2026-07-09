## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The Feature's Documentation Considerations section specifies "Updates" as the doc impact type: the endpoint must be added to the existing REST API reference so API consumers know the endpoint path, parameters, and response shape.

**Doc impact type:** Updates to existing content
**Details:** Add the advisory-summary endpoint to the REST API reference, documenting:
- Endpoint path and HTTP method
- Path parameters (SBOM ID)
- Optional query parameters (threshold)
- Response shape with field descriptions
- Error responses (404 for nonexistent SBOM, 400 for invalid threshold)
- Caching behavior (5-minute TTL)

**Reference:** Feature TC-9001, existing SBOM advisory endpoints documentation

## Acceptance Criteria
- [ ] REST API reference documents the `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation includes path parameters, query parameters, response shape, and error responses
- [ ] Documentation is consistent with the implemented endpoint behavior
- [ ] Caching behavior (5-minute TTL) is documented

## Test Requirements
- [ ] Verify the documentation accurately reflects the endpoint path, parameters, and response shape
- [ ] Verify error response documentation matches actual API behavior
- [ ] Verify documentation is consistent with the existing REST API reference style

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory summaries
- Depends on: Task 4 — Add threshold query parameter support
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint
