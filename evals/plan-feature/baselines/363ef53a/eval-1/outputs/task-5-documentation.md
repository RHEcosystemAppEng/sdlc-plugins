## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint (TC-9001). The feature's Documentation Considerations specify "Updates -- add endpoint to REST API reference." The documentation should cover the endpoint path, HTTP method, path parameters (SBOM ID), optional query parameters (threshold), response shape (severity counts JSON), example responses, error responses (404 for non-existent SBOM), and caching behavior (5-minute TTL). Reference the Feature issue TC-9001 for full context on the endpoint's purpose and use cases.

## Acceptance Criteria
- [ ] REST API reference includes documentation for `GET /api/v2/sbom/{id}/advisory-summary`
- [ ] Documentation covers path parameters, query parameters, response shape, and error responses
- [ ] Example request and response are provided for the basic case and the threshold filter case
- [ ] Caching behavior (5-minute TTL) is documented
- [ ] Documentation is consistent with the implemented endpoint behavior

## Test Requirements
- [ ] Verify the documented endpoint path, parameters, and response shape match the implementation
- [ ] Verify example responses are valid JSON matching the actual response format
- [ ] Verify error response documentation (404) matches actual error response format

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and aggregation service method
- Depends on: Task 2 — Add advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory summaries during advisory ingestion
- Depends on: Task 4 — Add integration tests for advisory-summary endpoint
