## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The documentation should cover the endpoint path, HTTP method, path parameters, optional query parameters (`threshold`), response shape, status codes (200, 404, 400), and caching behavior. This corresponds to the Documentation Considerations in TC-9001 (Doc Impact: Updates — add endpoint to REST API reference).

API consumers need to know the endpoint path, parameters, and response shape. Reference existing SBOM advisory endpoints documentation as the model for style and detail level.

## Acceptance Criteria
- [ ] REST API reference includes the `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation covers: endpoint path, path parameters (SBOM ID), optional query parameters (threshold), response JSON shape, status codes (200, 404, 400), and caching behavior (5-minute TTL)
- [ ] Documentation style is consistent with existing SBOM endpoint documentation
- [ ] Threshold parameter documentation includes the severity hierarchy and filtering behavior

## Test Requirements
- [ ] Verify documentation accurately reflects the implemented endpoint behavior
- [ ] Verify response shape examples match the actual API response
- [ ] Verify all status codes and error conditions are documented

## Dependencies
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
- Depends on: Task 5 — Add optional threshold query parameter support
