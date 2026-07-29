## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The Feature's Documentation Considerations indicate a doc impact type of "Updates" — the endpoint must be added to the existing REST API reference. Documentation should cover the endpoint path, path parameters (SBOM ID), optional query parameters (threshold), response shape (`{ critical, high, medium, low, total }`), cache behavior (5-minute TTL), and error responses (404 for non-existent SBOM, 400 for invalid threshold). Reference existing SBOM advisory endpoint documentation as a baseline for style and structure.

## Acceptance Criteria
- [ ] REST API reference includes the `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation covers: endpoint path, HTTP method, path parameters, optional query parameters
- [ ] Documentation covers: response body shape with field descriptions and types
- [ ] Documentation covers: cache behavior (5-minute TTL)
- [ ] Documentation covers: error responses (404 for missing SBOM, 400 for invalid threshold)
- [ ] Documentation style is consistent with existing SBOM endpoint documentation

## Test Requirements
- [ ] Verify documentation accurately describes the implemented endpoint behavior
- [ ] Verify response shape examples match actual API responses
- [ ] Verify all parameters (path and query) are documented with types and valid values

## Dependencies
- Depends on: Task 2 — Add advisory-summary endpoint with caching
- Depends on: Task 5 — Add optional threshold query parameter
