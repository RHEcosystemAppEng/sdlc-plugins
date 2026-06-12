# Task 6 — Update REST API documentation for advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint to the REST API reference documentation. Document the endpoint path, HTTP method, path parameters, query parameters, response shape, status codes, and caching behavior. This enables API consumers and the frontend dashboard team to integrate with the new endpoint.

## Files to Modify
- `README.md` — add the new endpoint to the API endpoints section if one exists

## Implementation Notes
- Review the existing API documentation format in `README.md` to match the established documentation style for endpoint descriptions.
- Document the following for the new endpoint:
  - **Path**: `GET /api/v2/sbom/{id}/advisory-summary`
  - **Path parameters**: `id` (SBOM identifier)
  - **Query parameters**: `threshold` (optional) — filter severity counts to include only severities at or above the specified level. Values: `critical`, `high`, `medium`, `low`
  - **Response (200 OK)**: `{ "critical": 0, "high": 0, "medium": 0, "low": 0, "total": 0 }`
  - **Response (404 Not Found)**: SBOM ID does not exist
  - **Response (400 Bad Request)**: invalid threshold value
  - **Caching**: responses are cached for 5 minutes (Cache-Control: max-age=300)
- Reference the existing SBOM and advisory endpoint documentation for formatting consistency.
- Per the feature's Documentation Considerations: this is an update to existing API documentation, not a new standalone document.

## Acceptance Criteria
- [ ] New endpoint is documented in the API reference with path, parameters, and response shape
- [ ] Query parameter `threshold` is documented with valid values
- [ ] All status codes (200, 400, 404) are documented
- [ ] Caching behavior is documented
- [ ] Documentation format is consistent with existing endpoint documentation

## Test Requirements
- [ ] Review documentation for accuracy against the implemented endpoint
- [ ] Verify all response fields and status codes are documented

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
