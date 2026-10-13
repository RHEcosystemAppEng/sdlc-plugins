## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Document the endpoint path, HTTP method, path parameters, optional query parameters, response schema, status codes, and example request/response. This ensures API consumers have accurate reference material for integrating with the advisory severity summary feature.

## Acceptance Criteria
- [ ] REST API reference includes the GET /api/v2/sbom/{id}/advisory-summary endpoint
- [ ] Documentation covers the path parameter (SBOM ID) and optional threshold query parameter
- [ ] Response schema is documented with all fields: critical, high, medium, low, total
- [ ] Status codes 200 and 404 are documented with descriptions
- [ ] An example request and response are provided

## Test Requirements
- [ ] Documentation renders correctly and links are valid
- [ ] Endpoint path, parameters, and response shape match the implementation

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service layer
- Depends on: Task 2 — Add advisory-summary endpoint with response caching
- Depends on: Task 3 — Invalidate advisory-summary cache on advisory ingestion
