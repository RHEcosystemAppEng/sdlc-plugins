## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint added by feature TC-9001. The feature's Documentation Considerations indicate this is an "Updates" doc impact type: the new endpoint must be added to the existing REST API reference so that API consumers know the endpoint path, parameters, and response shape.

**Doc impact type:** Updates to existing content
**User purpose:** API consumers need to know the endpoint path, parameters, and response shape
**Reference material:** Existing SBOM advisory endpoints documentation

## Acceptance Criteria
- [ ] REST API reference documentation includes the `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation describes the response shape: `{ critical: N, high: N, medium: N, low: N, total: N }`
- [ ] Documentation describes the optional `?threshold` query parameter and its behavior
- [ ] Documentation describes the 404 response for non-existent SBOM IDs
- [ ] Documentation describes the 5-minute cache behavior
- [ ] Documentation is consistent with the implemented endpoint behavior

## Test Requirements
- [ ] Verify the documented endpoint path matches the implemented path
- [ ] Verify the documented response shape matches the actual API response
- [ ] Verify the documented query parameter behavior matches the implementation
- [ ] Verify the documented error responses match the actual error responses

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model, service, and endpoint
- Depends on: Task 2 — Add cache invalidation for advisory-summary on advisory ingestion
- Depends on: Task 3 — Add threshold query parameter for advisory-summary endpoint
