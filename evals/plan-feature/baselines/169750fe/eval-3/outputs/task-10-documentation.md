## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Document the new SBOM comparison endpoint and comparison UI workflow. The Feature's Documentation Considerations indicate "New Content" is needed — API consumers need an endpoint reference for `GET /api/v2/sbom/compare`, and UI users need a guide for the comparison workflow (selecting SBOMs, interpreting diff sections, sharing comparison URLs).

Documentation scope:
- REST API reference for the comparison endpoint (path, parameters, response schema, error codes)
- UI workflow guide: how to select two SBOMs from the list page, interpret the six diff categories, and share comparison URLs
- Reference material: existing SBOM detail page documentation, package/advisory data model docs

## Acceptance Criteria
- [ ] API endpoint documentation covers `GET /api/v2/sbom/compare` with query parameters, response schema, and error codes
- [ ] UI workflow documentation covers the comparison workflow from SBOM selection to diff interpretation
- [ ] Documentation references the six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes
- [ ] URL sharing capability is documented
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Documentation accurately reflects the endpoint's request/response contract
- [ ] UI workflow steps match the actual comparison page behavior
- [ ] All referenced endpoints and UI elements exist in the implementation

## Dependencies
- Depends on: Task 5 — Backend integration tests
- Depends on: Task 7 — Frontend comparison page
- Depends on: Task 9 — Frontend SBOM list compare action
