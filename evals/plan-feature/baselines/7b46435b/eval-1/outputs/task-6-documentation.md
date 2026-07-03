# Task 6 — Update REST API documentation for advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The documentation should cover the endpoint path, HTTP method, path parameters, optional query parameters, response shape, error codes, and usage examples. The Feature's Documentation Considerations specify doc impact type "Updates" — add the endpoint to the existing REST API reference.

Doc impact type: Updates to existing content.

Details from Feature Documentation Considerations:
- User purpose: API consumers need to know the endpoint path, parameters, and response shape
- Reference material: Existing SBOM advisory endpoints documentation

## Acceptance Criteria
- [ ] REST API reference includes the advisory-summary endpoint with path, method, and description
- [ ] Documentation covers path parameter: SBOM ID
- [ ] Documentation covers optional query parameter: threshold (with valid values)
- [ ] Documentation includes response shape with all fields (critical, high, medium, low, total)
- [ ] Documentation includes error responses (404 for missing SBOM, 400 for invalid threshold)
- [ ] Documentation is consistent with the style of existing SBOM endpoint documentation

## Test Requirements
- [ ] Verify documentation accurately reflects the implemented endpoint behavior
- [ ] Verify response shape examples match actual API responses
- [ ] Verify error code documentation matches actual error responses

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute caching
- Depends on: Task 4 — Add threshold query parameter to advisory-summary endpoint (non-MVP)
