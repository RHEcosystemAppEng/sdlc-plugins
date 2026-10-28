## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint added by feature TC-9001 (Add advisory severity aggregation endpoint).

**Doc impact type:** Updates to existing content

**Documentation scope:**
- Endpoint path, HTTP method, and URL parameters (path parameter `id`, optional query parameter `threshold`)
- Response shape: `{ critical: N, high: N, medium: N, low: N, total: N }`
- Error responses (404 for nonexistent SBOM, 400 for invalid threshold value)
- Caching behavior (5-minute cache with invalidation on advisory ingestion)
- Usage examples for dashboard severity widgets (UC-1) and alerting integrations (UC-2)

**User purpose:** API consumers need to know the endpoint path, parameters, and response shape to build severity widgets and alerting integrations.

**Reference material:** Existing SBOM advisory endpoints documentation

## Acceptance Criteria
- [ ] REST API reference includes the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation covers the request parameters (path parameter `id`, optional query parameter `threshold` with valid values)
- [ ] Documentation describes the response shape with field descriptions for each severity level and total
- [ ] Documentation covers error responses (404 for nonexistent SBOM, 400 for invalid threshold)
- [ ] Documentation notes the 5-minute cache behavior and cache invalidation on advisory ingestion
- [ ] Documentation is consistent with the implemented endpoint behavior

## Test Requirements
- [ ] Verify the documented endpoint path matches the implemented route
- [ ] Verify the documented response shape matches the actual API response
- [ ] Verify the documented error codes match the actual error responses
- [ ] Verify the documented threshold parameter values and behavior are accurate

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation endpoint
- Depends on: Task 2 — Add cache invalidation for advisory severity summaries
- Depends on: Task 3 — Add integration tests for advisory-summary endpoint
- Depends on: Task 4 — Add optional severity threshold filter
