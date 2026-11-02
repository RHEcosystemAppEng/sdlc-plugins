## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The feature (TC-9001) adds a server-side advisory severity aggregation endpoint that replaces client-side counting. The Documentation Considerations section in the Feature description specifies:

- **Doc Impact**: Updates — add endpoint to REST API reference
- **User purpose**: API consumers need to know the endpoint path, parameters, and response shape
- **Reference material**: Existing SBOM advisory endpoints documentation

Document the endpoint path, HTTP method, path parameters (`id`), optional query parameters (`threshold`), response shape (`AdvisorySeveritySummary`), caching behavior, and error responses (404).

## Acceptance Criteria
- [ ] REST API reference includes the `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation includes the response shape with all fields (`critical`, `high`, `medium`, `low`, `total`)
- [ ] Documentation describes the optional `?threshold` query parameter and its valid values
- [ ] Documentation describes the 5-minute cache behavior
- [ ] Documentation describes the 404 error response for non-existent SBOM IDs
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify documented endpoint path matches the actual implementation
- [ ] Verify documented response shape matches the `AdvisorySeveritySummary` struct
- [ ] Verify documented query parameters match the implementation
- [ ] Verify all examples are valid and produce the described responses

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint with caching
- Depends on: Task 5 — Threshold query parameter filter
- Depends on: Task 6 — Integration tests for advisory summary
