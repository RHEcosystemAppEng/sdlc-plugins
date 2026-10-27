## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The documentation should cover the endpoint path, HTTP method, path parameters, optional query parameters (`?threshold`), response shape (severity count fields), response codes (200, 404, 400), caching behavior (5-minute TTL), and usage examples.

This task addresses the Documentation Considerations from Feature TC-9001:
- **Doc Impact Type**: Updates — add endpoint to REST API reference
- **User purpose**: API consumers need to know the endpoint path, parameters, and response shape
- **Reference material**: Existing SBOM advisory endpoints documentation

## Acceptance Criteria
- [ ] REST API reference includes documentation for `GET /api/v2/sbom/{id}/advisory-summary`
- [ ] Documentation covers: endpoint path, HTTP method, path parameters, query parameters, response shape, response codes
- [ ] Documentation includes example request and response
- [ ] Documentation mentions the 5-minute cache TTL behavior
- [ ] Documentation is consistent with existing SBOM endpoint documentation style

## Test Requirements
- [ ] Verify documentation accurately reflects the implemented endpoint behavior
- [ ] Verify response shape examples match the actual `AdvisorySeveritySummary` struct fields
- [ ] Verify all documented response codes (200, 404, 400) are accurate

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint
- Depends on: Task 6 — Threshold query param
