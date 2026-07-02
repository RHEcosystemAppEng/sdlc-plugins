# Task 6 — Update REST API reference documentation

additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }

## Repository
trustify-backend

## Target Branch
main

## Description
Update the REST API reference documentation to include the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The feature's Documentation Considerations specify "Updates -- add endpoint to REST API reference" with the user purpose: "API consumers need to know the endpoint path, parameters, and response shape." This task ensures external consumers and the frontend dashboard team can discover and integrate with the new endpoint.

## Acceptance Criteria
- [ ] REST API reference includes the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint
- [ ] Documentation covers: endpoint path, HTTP method, path parameters (`id`), response shape (`{ critical, high, medium, low, total }`), response status codes (200, 404)
- [ ] Documentation notes the 5-minute cache behavior
- [ ] Non-MVP `threshold` query parameter is documented as planned/future (if API reference includes roadmap items) or omitted (if reference only covers current functionality)

## Test Requirements
- [ ] Documentation renders correctly (no broken links or formatting issues)
- [ ] Endpoint description is consistent with the actual implementation from Tasks 1-3

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 5 — Integration tests for advisory summary endpoint
