## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint added by TC-9001. The documentation should cover the endpoint path, HTTP method, path parameters, optional query parameters (including the `?threshold` parameter), response schema, error responses (404, 400), and caching behavior. This task addresses the "Documentation Considerations" from the feature description: doc impact type is "Updates" (updates to existing documentation), targeting the REST API reference.

Reference material: existing SBOM advisory endpoints documentation.

## Acceptance Criteria
- [ ] REST API reference includes the `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation covers: endpoint path, HTTP method, path parameter (`id`), optional query parameter (`threshold`), response schema (`{ critical, high, medium, low, total }`), 404 response for nonexistent SBOM, 400 response for invalid threshold, caching behavior (5-minute cache)
- [ ] Documentation is consistent with the implemented endpoint behavior
- [ ] Documentation follows the format and style of existing SBOM endpoint documentation

## Test Requirements
- [ ] Verify the documented endpoint path, parameters, and response schema match the actual implementation
- [ ] Verify the documentation is accessible from the API reference index or table of contents
- [ ] Verify example requests and responses (if included) are accurate

## Dependencies
- Depends on: Task 1 — Add severity aggregation model and service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching
- Depends on: Task 4 — Add threshold query parameter support
- Depends on: Task 5 — Add integration tests for advisory-summary endpoint
