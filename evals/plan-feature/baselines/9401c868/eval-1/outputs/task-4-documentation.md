## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint added by TC-9001. The documentation should cover the endpoint path, path parameters (`id`), optional query parameters (`threshold`), response shape (`{ critical, high, medium, low, total }`), error responses (404 for missing SBOM, 400 for invalid threshold), and caching behavior (5-minute TTL). The Documentation Considerations section of TC-9001 specifies this as an "Updates" doc impact, targeting API consumers who need to know the endpoint path, parameters, and response shape. Reference existing SBOM advisory endpoints documentation for style and structure consistency.

## Acceptance Criteria
- [ ] REST API reference includes the `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation covers path parameters, query parameters, response shape, and error codes
- [ ] Documentation describes the 5-minute caching behavior
- [ ] Documentation includes example request and response
- [ ] Documentation is consistent in style with existing SBOM and advisory endpoint documentation

## Test Requirements
- [ ] Verify the documented endpoint path, parameters, and response shape match the actual implementation
- [ ] Verify the documented error codes (404, 400) match the endpoint behavior
- [ ] Verify the documentation is accessible and renders correctly in the project's documentation system

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
- Depends on: Task 2 — Add advisory severity summary endpoint with caching and threshold filter
- Depends on: Task 3 — Add cache invalidation for advisory summaries in the ingestor
