## Repository
trustify-backend

## Target Branch
main

## Priority
Major

## Fix Versions
RHTPA 1.5.0

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Document the endpoint path, HTTP method, path parameters, optional query parameters, response shape, status codes, and caching behavior. This addresses the Documentation Considerations in TC-9001 (Doc Impact: Updates -- add endpoint to REST API reference).

## Acceptance Criteria
- [ ] REST API reference includes the `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation covers: endpoint path, HTTP method, path parameter (`id`), optional query parameter (`threshold`), response JSON shape, status codes (200, 404), and Cache-Control behavior
- [ ] Response example shows: `{"critical": N, "high": N, "medium": N, "low": N, "total": N}`
- [ ] Threshold parameter values documented: `critical`, `high`, `medium`, `low`
- [ ] Documentation is consistent with existing SBOM endpoint documentation style

## Test Requirements
- [ ] Verify the documented endpoint path matches the implemented endpoint
- [ ] Verify the documented response shape matches the actual API response
- [ ] Verify the documented query parameter behavior matches the implementation

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching
