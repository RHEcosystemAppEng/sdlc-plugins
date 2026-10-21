## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new GET /api/v2/sbom/{id}/advisory-summary endpoint. The feature's Documentation Considerations indicate a doc impact of type "Updates" -- the new endpoint must be added to existing API documentation. Document the endpoint path, HTTP method, path parameters (SBOM ID), optional query parameters (threshold), response shape (severity counts JSON object), response codes (200, 404, 400), and caching behavior (5-minute TTL). Reference the existing SBOM advisory endpoints documentation as the context for placement.

This documentation update ensures API consumers know the endpoint path, parameters, and response shape, as specified in the feature's Documentation Considerations.

Ref: TC-9001

## Acceptance Criteria
- [ ] REST API reference documentation includes the GET /api/v2/sbom/{id}/advisory-summary endpoint
- [ ] Documentation covers: endpoint path, HTTP method, path parameters, optional query parameters (threshold), response shape, response codes (200, 404, 400), and caching behavior
- [ ] Documentation is placed alongside existing SBOM endpoint documentation for consistency
- [ ] Documentation accurately reflects the implemented feature behavior

## Test Requirements
- [ ] Verify documentation is accurate and complete against the implemented endpoint behavior
- [ ] Verify response shape examples match the actual AdvisorySeveritySummary struct fields
- [ ] Verify threshold parameter documentation matches the implemented filtering behavior

## Dependencies
- Depends on: Task 1 -- Add AdvisorySeveritySummary model and aggregation service method
- Depends on: Task 2 -- Add advisory-summary endpoint with caching
- Depends on: Task 3 -- Add cache invalidation for advisory summaries
- Depends on: Task 4 -- Add threshold query parameter filtering
