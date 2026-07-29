## Repository
trustify-backend

## Target Branch
main

## Description
Document the new SBOM comparison endpoint and comparison UI workflow. The feature description indicates "New Content" documentation impact: API consumers need an endpoint reference for the comparison API, and UI users need a guide for the comparison workflow. Documentation should cover the REST API contract (endpoint path, parameters, response shape), the comparison UI layout and user workflow, and integration with the existing SBOM documentation.

The doc impact type is **New Content** per the Feature's Documentation Considerations section:
- **User purpose**: API consumers need endpoint reference; UI users need a guide for the comparison workflow
- **Reference material**: Existing SBOM detail page documentation, package/advisory data model docs

Reference: Feature TC-9003 (SBOM comparison view)

## Acceptance Criteria
- [ ] API endpoint documentation covers `GET /api/v2/sbom/compare` with parameters, response shape, and error codes
- [ ] UI workflow documentation describes how to select two SBOMs and interpret the comparison view
- [ ] Documentation references the six diff categories (added/removed packages, version changes, new/resolved vulnerabilities, license changes)
- [ ] Documentation is consistent with the implemented feature behavior
- [ ] Performance characteristics are documented (p95 < 1s for up to 2000 packages)

## Test Requirements
- [ ] Verify API endpoint documentation matches the actual endpoint path, parameters, and response shape
- [ ] Verify UI workflow documentation accurately describes the comparison page layout and interaction
- [ ] Verify documentation integrates with existing SBOM documentation structure

## Dependencies
- Depends on: Task 3 — Backend comparison endpoint (API must be finalized before documenting)
- Depends on: Task 5 — Frontend comparison page (UI must be finalized before documenting)
