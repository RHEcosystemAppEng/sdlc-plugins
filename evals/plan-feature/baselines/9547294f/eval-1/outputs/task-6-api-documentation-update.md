## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Document the endpoint path, HTTP method, path parameters, optional query parameters, response shape, caching behavior, and error responses. This ensures API consumers can discover and use the new endpoint.

## Files to Modify
- `README.md` — add the new endpoint to the API endpoint listing or reference section if one exists

## Implementation Notes
- Document the following for the new endpoint:
  - **Path**: `GET /api/v2/sbom/{id}/advisory-summary`
  - **Path parameters**: `id` (string) — the SBOM identifier
  - **Query parameters**: `threshold` (optional, string) — severity level filter. Accepted values: `critical`, `high`, `medium`, `low`. When provided, returns counts only for severities at or above the threshold.
  - **Response (200)**: `{ "critical": number, "high": number, "medium": number, "low": number, "total": number }`
  - **Response (404)**: SBOM not found
  - **Response (400)**: Invalid threshold value
  - **Cache**: Responses are cached for 5 minutes (300 seconds)
- Follow the documentation style of existing SBOM endpoint documentation. Reference the existing SBOM advisory endpoints documentation as stated in the feature's Documentation Considerations.
- Add the endpoint to any API latency monitoring documentation per the Customer Information/Supportability requirements: the endpoint should be added to the API latency Grafana dashboard configuration, with an alert if p95 exceeds 500ms.

## Acceptance Criteria
- [ ] API documentation includes the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation covers path parameters, query parameters, response shape, and error codes
- [ ] Documentation mentions the 5-minute cache behavior
- [ ] Documentation follows the style of existing endpoint documentation

## Test Requirements
- [ ] Review: documentation is accurate and complete per the endpoint implementation
- [ ] Review: response shape matches the actual `AdvisorySeveritySummary` struct

## Dependencies
- Depends on: Task 5 — Add threshold query parameter support (to document the complete endpoint including threshold)

---

> [sdlc-workflow] Description digest: (simulated) The digest would be posted as a Jira comment after task creation per the description-digest-protocol. Format: `[sdlc-workflow] Description digest: sha256-md:<64-hex-chars>`
