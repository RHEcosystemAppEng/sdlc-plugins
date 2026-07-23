## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The Feature's Documentation Considerations indicate this is an "Updates" impact type: API consumers need to know the endpoint path, query parameters, response shape, caching behavior, and error responses. Reference the existing SBOM advisory endpoints documentation for style consistency.

Documentation impact type: **Updates to existing content**
Details:
- User purpose: API consumers need to know the endpoint path, parameters, and response shape
- Reference material: Existing SBOM advisory endpoints documentation

## Acceptance Criteria
- [ ] REST API reference includes the `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation covers: endpoint path, HTTP method, path parameters, optional query parameters (`threshold`), response shape (`{ critical, high, medium, low, total }`), caching behavior (5-minute TTL), and error responses (404, 400)
- [ ] Documentation style is consistent with existing SBOM endpoint documentation
- [ ] Use cases (dashboard severity widget, alerting integration) are referenced or linked

## Test Requirements
- [ ] Verify documented endpoint path matches the implemented endpoint
- [ ] Verify documented response shape matches the actual `AdvisorySeveritySummary` struct
- [ ] Verify documented query parameters match the implemented threshold parameter
- [ ] Verify documentation is consistent with existing SBOM endpoint documentation style

## Dependencies
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
- Depends on: Task 4 — Add optional threshold query parameter for severity filtering
