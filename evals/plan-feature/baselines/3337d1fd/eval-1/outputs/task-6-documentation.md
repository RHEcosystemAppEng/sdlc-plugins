## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Document the endpoint path, HTTP method, path parameters, optional query parameters, response shape, status codes, and example request/response. This enables API consumers to discover and correctly integrate with the advisory severity aggregation endpoint.

## Acceptance Criteria
- [ ] REST API reference includes the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation covers the endpoint path, method, and path parameter (SBOM ID)
- [ ] Documentation covers the optional `?threshold` query parameter and its valid values (critical, high, medium, low)
- [ ] Documentation includes the response JSON shape with all fields (critical, high, medium, low, total)
- [ ] Documentation covers status codes: 200 (success), 404 (SBOM not found)
- [ ] Documentation includes example request and response

## Test Requirements
- [ ] Documentation renders correctly and is accessible from the API reference index
- [ ] All endpoint details match the actual implementation

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching