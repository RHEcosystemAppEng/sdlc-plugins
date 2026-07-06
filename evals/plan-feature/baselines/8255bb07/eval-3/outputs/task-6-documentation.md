## Repository
trustify-backend

## Target Branch
main

## Description
Create documentation for the new SBOM comparison feature (TC-9003), covering both the backend REST API endpoint and the frontend comparison UI workflow. This addresses the "New Content" documentation impact identified in the feature's Documentation Considerations section.

Documentation scope:
- **API reference** for `GET /api/v2/sbom/compare?left={id1}&right={id2}` including request parameters, response schema with all six diff categories, error codes (400, 404), and example request/response pairs
- **User workflow guide** for the comparison UI: selecting SBOMs from the list, interpreting diff sections (added/removed packages, version changes, vulnerabilities, license changes), sharing comparison URLs, and exporting results as JSON or CSV
- **Reference material**: link to existing SBOM detail page documentation and package/advisory data model docs for context

Doc impact type: New Content
User purpose: API consumers need an endpoint reference; UI users need a guide for the comparison workflow.

## Acceptance Criteria
- [ ] API endpoint documentation includes request query parameters (left, right), response schema with all six diff categories and their field definitions, error codes (400 for invalid parameters, 404 for non-existent SBOMs), and at least one example request/response
- [ ] UI workflow guide covers: SBOM selection from the list page, comparison view layout and diff section interpretation, URL sharing for compliance workflows, and export functionality (JSON/CSV)
- [ ] Documentation references the existing SBOM detail page docs and package/advisory data model documentation for context
- [ ] Documentation is accurate and consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify API documentation matches the implemented endpoint's actual request parameters and response format
- [ ] Verify UI workflow guide matches the implemented comparison page behavior and navigation flow
- [ ] Verify all six diff categories (added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes) are documented with column descriptions

## Dependencies
- Depends on: Task 1 — Implement SBOM comparison diff service and model types
- Depends on: Task 2 — Add SBOM comparison REST endpoint with integration tests
- Depends on: Task 3 — Add SBOM comparison API types, client function, and React Query hook
- Depends on: Task 4 — Implement SBOM comparison page with diff sections and export
- Depends on: Task 5 — Add comparison route and SBOM list page integration
