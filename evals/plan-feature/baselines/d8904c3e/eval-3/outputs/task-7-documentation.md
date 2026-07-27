## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Document the SBOM comparison feature covering both the backend API endpoint and the frontend comparison UI workflow. The Feature's Documentation Considerations specify "New Content" impact: API consumers need endpoint reference documentation for `GET /api/v2/sbom/compare`, and UI users need a guide for the comparison workflow (selecting SBOMs, reading diff sections, sharing comparison URLs).

Documentation should cover:
- The comparison REST endpoint: path, query parameters, response shape, error codes
- The comparison UI workflow: navigating from the SBOM list page, using selectors, interpreting diff sections
- Reference to existing SBOM detail page documentation and package/advisory data model docs as context

## Acceptance Criteria
- [ ] API endpoint documentation covers GET /api/v2/sbom/compare with parameters, response schema, and error codes
- [ ] UI workflow documentation covers the comparison page layout, SBOM selection, diff section navigation, and URL sharing
- [ ] Documentation references existing SBOM and advisory documentation for context
- [ ] Documentation accurately reflects the implemented feature behavior

## Test Requirements
- [ ] Verify documentation accurately describes the API endpoint path, parameters, and response shape
- [ ] Verify documentation screenshots or descriptions match the actual UI rendering
- [ ] Verify all links to related documentation pages are valid
- [ ] Verify documentation covers the end-to-end workflow from SBOM selection to comparison viewing

## Dependencies
- Depends on: Task 2 -- Add SBOM comparison model and service
- Depends on: Task 3 -- Add SBOM comparison endpoint
- Depends on: Task 4 -- Add SBOM comparison API layer
- Depends on: Task 5 -- Implement SBOM comparison page UI
- Depends on: Task 6 -- Add comparison route and SBOM list page integration
