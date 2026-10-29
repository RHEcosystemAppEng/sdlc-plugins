## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint added by feature TC-9001. The feature adds a server-side advisory severity aggregation endpoint that returns counts of Critical, High, Medium, and Low advisories for a given SBOM, reducing client-side counting logic and multi-page fetch overhead.

Doc impact type: **Updates** — add the new endpoint to existing REST API reference documentation.

Per the Feature's Documentation Considerations:
- **User purpose**: API consumers need to know the endpoint path, parameters, and response shape
- **Reference material**: Existing SBOM advisory endpoints documentation

## Acceptance Criteria
- [ ] REST API documentation includes the `GET /api/v2/sbom/{id}/advisory-summary` endpoint with path, HTTP method, and description
- [ ] Documentation covers the response shape: `{ critical: N, high: N, medium: N, low: N, total: N }`
- [ ] Documentation covers the optional `?threshold` query parameter with valid values (`critical`, `high`, `medium`, `low`) and describes the filtering behavior
- [ ] Documentation covers the 404 response for non-existent SBOM IDs
- [ ] Documentation covers the 400 response for invalid threshold values
- [ ] Documentation covers the 5-minute cache behavior (`Cache-Control: max-age=300`)
- [ ] Documentation is consistent with the actual implemented endpoint behavior

## Test Requirements
- [ ] Verify the documented endpoint path, method, parameters, and response shape match the actual implementation
- [ ] Verify the documented error responses (404 for missing SBOM, 400 for invalid threshold) match actual endpoint behavior
- [ ] Verify the documented cache behavior matches the actual response headers

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service method
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory severity summaries
