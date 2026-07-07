## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new GET /api/v2/sbom/{id}/advisory-summary endpoint. The feature's Documentation Considerations specified "Updates — add endpoint to REST API reference." Documentation should cover the endpoint URL, request parameters (including the optional threshold query parameter), response schema, error responses, and caching behavior.

## Acceptance Criteria
- [ ] REST API reference includes the new GET /api/v2/sbom/{id}/advisory-summary endpoint
- [ ] Documentation covers request path parameter (SBOM ID)
- [ ] Documentation covers optional `?threshold` query parameter with valid values
- [ ] Documentation includes response JSON schema with critical, high, medium, low, and total fields
- [ ] Documentation covers 404 error response for non-existent SBOM ID
- [ ] Documentation notes 5-minute cache behavior (Cache-Control: max-age=300)

## Test Requirements
- [ ] Verify documented endpoint URL matches the implemented endpoint
- [ ] Verify documented response schema matches the actual AdvisorySeveritySummary struct
- [ ] Verify documented query parameter values match the implemented threshold enum

## Dependencies
- Depends on: Task 1 — Advisory severity summary model
- Depends on: Task 2 — Advisory summary service
- Depends on: Task 3 — Advisory summary endpoint
- Depends on: Task 4 — Cache invalidation
- Depends on: Task 5 — Integration tests
- Depends on: Task 6 — Threshold query parameter
