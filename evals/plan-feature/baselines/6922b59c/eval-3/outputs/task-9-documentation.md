## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Document the SBOM comparison feature, covering both the backend REST endpoint and the frontend comparison UI workflow. The Feature's Documentation Considerations specify "New Content" impact: API consumers need an endpoint reference for `GET /api/v2/sbom/compare`, and UI users need a guide for the comparison workflow (selecting SBOMs, interpreting diff sections, sharing comparison URLs).

Documentation should reference existing SBOM detail page documentation and the package/advisory data model docs as specified in the Feature's reference material.

## Acceptance Criteria
- [ ] API endpoint documentation covers `GET /api/v2/sbom/compare?left={id1}&right={id2}` with request parameters, response shape, error codes (400, 404), and example response
- [ ] UI workflow documentation describes how to select two SBOMs, trigger comparison, interpret each diff section, and share comparison URLs
- [ ] Documentation references the six diff categories: Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes
- [ ] Documentation is consistent with the implemented feature behavior
- [ ] Performance expectations are documented (p95 < 1s for up to 2000 packages per SBOM)

## Test Requirements
- [ ] Verify the API endpoint documentation includes accurate request/response examples that match the actual endpoint behavior
- [ ] Verify the UI workflow documentation accurately describes the comparison page layout and interactions
- [ ] Verify cross-references to existing SBOM documentation are correct

## Dependencies
- Depends on: Task 3 — Add SBOM comparison service and REST endpoint
- Depends on: Task 4 — Add SBOM comparison endpoint integration tests
- Depends on: Task 6 — Build SBOM comparison page UI
- Depends on: Task 7 — Add comparison route and SBOM list selection
