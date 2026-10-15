## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint added by TC-9001. The documentation should cover the endpoint path, HTTP method, path parameters, optional query parameters (`?threshold`), response shape, error responses (404), and caching behavior (5-minute cache). This addresses the Documentation Considerations from the feature description: "Updates — add endpoint to REST API reference."

## Acceptance Criteria
- [ ] REST API reference documentation includes the `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation covers the path parameter (`id` — SBOM UUID)
- [ ] Documentation covers the optional `?threshold` query parameter with valid values (`critical`, `high`, `medium`, `low`)
- [ ] Documentation includes the response shape: `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Documentation describes the 404 error response for nonexistent SBOM IDs
- [ ] Documentation notes the 5-minute cache behavior
- [ ] Documentation is consistent with the existing SBOM endpoint documentation style

## Test Requirements
- [ ] Verify the documented endpoint path, parameters, and response shape match the implemented endpoint behavior
- [ ] Verify the documentation is consistent with existing REST API reference format and style

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and aggregation service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching and threshold filter
- Depends on: Task 3 — Add cache invalidation in advisory ingestion pipeline
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
