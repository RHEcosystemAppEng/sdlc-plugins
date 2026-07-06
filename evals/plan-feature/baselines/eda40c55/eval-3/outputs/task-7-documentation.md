## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Document the new SBOM comparison endpoint and comparison UI workflow. The feature description specifies "Doc Impact: New Content" -- new documentation pages or sections are needed for both the API endpoint reference and the UI comparison workflow.

- **Doc impact type:** New Content
- **User purpose:** API consumers need endpoint reference for `GET /api/v2/sbom/compare`; UI users need a guide for the comparison workflow (selecting SBOMs, interpreting diff sections, sharing comparison URLs)
- **Reference material:** Existing SBOM detail page documentation, package/advisory data model docs
- **Feature reference:** TC-9003 (SBOM comparison view)

## Acceptance Criteria
- [ ] API documentation covers the `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint including request parameters, response shape, and error responses (404 for missing SBOMs)
- [ ] UI documentation covers the comparison workflow: selecting SBOMs from the list page, using the comparison page, interpreting diff sections, and sharing comparison URLs
- [ ] Documentation accurately reflects the implemented feature behavior
- [ ] Documentation covers the six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes

## Test Requirements
- [ ] Verify documentation is accurate and complete against the implemented endpoint and UI
- [ ] Verify API endpoint documentation matches the actual request/response contract
- [ ] Verify UI workflow documentation matches the actual page behavior and navigation flow

## Dependencies
- Depends on: Task 2 -- Add SBOM comparison model types
- Depends on: Task 3 -- Add SBOM comparison service and endpoint with integration tests
- Depends on: Task 4 -- Add SBOM comparison API types, client function, and React Query hook
- Depends on: Task 5 -- Add SBOM comparison page with header toolbar and diff sections
- Depends on: Task 6 -- Add compare workflow to SBOM list page and route registration
