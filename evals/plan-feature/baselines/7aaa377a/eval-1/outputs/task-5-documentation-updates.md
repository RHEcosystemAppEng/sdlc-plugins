# Task 5 — Update REST API documentation for advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The feature's Documentation Considerations specify a doc impact type of "Updates" — the existing API documentation needs to be updated with the new endpoint path, query parameters, and response shape. API consumers need to know the endpoint path, parameters, and response shape to integrate advisory severity summaries into their dashboards and alerting systems.

Reference: Feature TC-9001 — Add advisory severity aggregation endpoint.

## Acceptance Criteria
- [ ] REST API reference includes documentation for `GET /api/v2/sbom/{id}/advisory-summary`
- [ ] Documentation covers the response schema: `{ critical: N, high: N, medium: N, low: N, total: N }`
- [ ] Documentation covers the optional `?threshold` query parameter with valid values (critical, high, medium, low)
- [ ] Documentation covers error responses (404 for nonexistent SBOM, 400 for invalid threshold)
- [ ] Documentation notes the 5-minute cache behavior
- [ ] Documentation is consistent with the existing SBOM advisory endpoints documentation style

## Test Requirements
- [ ] Verify the documentation accurately reflects the implemented endpoint behavior
- [ ] Verify the response schema in documentation matches the actual `AdvisorySeveritySummary` struct
- [ ] Verify the query parameter documentation matches the actual `ThresholdQuery` implementation

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
