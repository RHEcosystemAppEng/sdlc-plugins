# Task 6 — Update REST API reference documentation for advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The feature's Documentation Considerations section specifies a doc impact type of "Updates" — the endpoint must be added to the existing REST API reference so API consumers know the endpoint path, parameters, and response shape. Reference material includes the existing SBOM advisory endpoints documentation.

This task addresses the documentation signal extracted from Feature TC-9001:
- **Doc impact type**: Updates
- **User purpose**: API consumers need to know the endpoint path, parameters, and response shape
- **Reference material**: Existing SBOM advisory endpoints documentation

## Acceptance Criteria
- [ ] REST API reference includes the `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation covers the request path parameter (`{id}` — SBOM UUID)
- [ ] Documentation covers the optional `?threshold` query parameter with accepted values
- [ ] Documentation shows the response JSON shape with field descriptions
- [ ] Documentation lists HTTP status codes: 200 (success), 400 (invalid threshold), 404 (SBOM not found)
- [ ] Documentation is consistent with existing SBOM endpoint documentation style

## Test Requirements
- [ ] Verify the documentation accurately reflects the implemented endpoint behavior
- [ ] Verify response shape examples match the actual `AdvisorySeveritySummary` struct
- [ ] Verify the threshold parameter values and behavior are accurately described

## Dependencies
- Depends on: Task 3 — Add threshold query parameter to advisory-summary endpoint (documentation should be written after implementation is complete)
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint (documentation should reflect verified behavior)
