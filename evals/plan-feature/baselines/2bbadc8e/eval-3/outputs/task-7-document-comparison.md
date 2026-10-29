## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Document the SBOM comparison feature, covering both the backend REST endpoint and the frontend comparison UI. The Feature description identifies this as "New Content" documentation impact. API consumers need an endpoint reference for `GET /api/v2/sbom/compare`, and UI users need a workflow guide for the comparison view at `/sbom/compare`. Reference material includes existing SBOM detail page documentation and the package/advisory data model docs.

Doc impact type: New Content
Source: TC-9003 Feature description, Documentation Considerations section

## Acceptance Criteria
- [ ] API endpoint reference documents `GET /api/v2/sbom/compare?left={id1}&right={id2}` with request parameters, response shape, error codes (400, 404), and example response
- [ ] UI workflow guide documents the comparison page: selecting SBOMs, triggering comparison, reading diff sections, sharing comparison URLs
- [ ] Documentation accurately reflects the implemented feature behavior
- [ ] Coverage includes the six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes

## Test Requirements
- [ ] Verify API endpoint documentation matches the actual endpoint behavior (parameter names, response shape, error codes)
- [ ] Verify UI workflow guide accurately describes the page layout and interaction patterns
- [ ] Verify example response in documentation is valid and matches the SbomComparison response schema

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model and diff service
- Depends on: Task 3 — Add SBOM comparison REST endpoint with integration tests
- Depends on: Task 4 — Add API client and React Query hook for SBOM comparison
- Depends on: Task 5 — Create SBOM comparison page with diff sections
- Depends on: Task 6 — Add diff export for SBOM comparison
