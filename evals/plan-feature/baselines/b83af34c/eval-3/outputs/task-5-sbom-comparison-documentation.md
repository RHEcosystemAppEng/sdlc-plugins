## Repository
trustify-backend

## Target Branch
main

## Description
Create documentation for the SBOM comparison feature (TC-9003). Document the new `GET /api/v2/sbom/compare` endpoint in the REST API reference and provide a user guide for the comparison UI workflow. This task addresses the Documentation Considerations from the feature description: "New Content — document the comparison endpoint and comparison UI."

**Priority**: Critical (inherited from TC-9003)
**Fix Version**: RHTPA 1.5.0 (inherited from TC-9003)

## Acceptance Criteria
- [ ] API endpoint documentation covers `GET /api/v2/sbom/compare` with query parameters (`left`, `right`), response schema (all six diff categories), status codes (200, 400, 404), and example request/response
- [ ] User guide documents the comparison workflow: selecting SBOMs, triggering comparison, navigating diff sections, sharing comparison URLs
- [ ] Documentation references existing SBOM detail page docs and package/advisory data model docs as related material
- [ ] Error scenarios are documented (missing parameters, non-existent SBOM IDs)

## Test Requirements
- [ ] Documentation review confirms accuracy against implemented endpoint behavior
- [ ] Example API request in documentation returns expected response when executed against a running instance
- [ ] User guide workflow steps match the actual UI flow in the comparison page

## Dependencies
- Depends on: Task 2 — SBOM comparison endpoint and integration tests
- Depends on: Task 4 — SBOM comparison page and components
