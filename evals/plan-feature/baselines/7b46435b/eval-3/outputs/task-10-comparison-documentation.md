## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Document the new SBOM comparison endpoint and the comparison UI workflow. This includes API reference documentation for the `GET /api/v2/sbom/compare` endpoint with request parameters and response schema, and a user guide for the comparison workflow from the frontend.

Doc impact type: New Content.

API consumers need endpoint reference documentation covering the request format, response schema, and error codes. UI users need a guide for the comparison workflow: selecting SBOMs from the list page, interpreting the six diff sections, sharing comparison URLs, and exporting results for compliance.

Reference material: existing SBOM detail page documentation, package/advisory data model docs.

## Acceptance Criteria
- [ ] API reference documents the `GET /api/v2/sbom/compare` endpoint with `left` and `right` query parameters
- [ ] API reference includes the full response schema (`SbomComparisonResult`) with all six diff category types
- [ ] API reference documents error responses (400 for missing params, 404 for non-existent SBOMs)
- [ ] User guide covers the comparison workflow: selecting two SBOMs via checkboxes, clicking Compare, viewing diff sections
- [ ] User guide documents the six diff categories and what each represents (added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes)
- [ ] User guide covers URL sharing and bookmarking of comparison results
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Documentation accurately reflects the API endpoint path, parameters, and response shape
- [ ] Documentation is consistent with the UI implementation (section names, workflow steps, badge colors)
- [ ] All code examples and response schemas are valid and match the implemented types

## Dependencies
- Depends on: Task 4 -- Add SBOM comparison integration tests
- Depends on: Task 9 -- Add comparison page tests and mock fixtures
