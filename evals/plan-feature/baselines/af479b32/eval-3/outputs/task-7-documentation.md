## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Document the new SBOM comparison endpoint and comparison UI workflow introduced by feature TC-9003. The Feature's Documentation Considerations indicate a **New Content** doc impact: API consumers need an endpoint reference for `GET /api/v2/sbom/compare`, and UI users need a guide for the comparison workflow (selecting SBOMs, interpreting diff sections, sharing comparison URLs).

**Doc impact type:** New Content

**Details from Documentation Considerations:**
- User purpose: API consumers need endpoint reference; UI users need a guide for the comparison workflow
- Reference material: Existing SBOM detail page documentation, package/advisory data model docs

## Acceptance Criteria
- [ ] Comparison endpoint (`GET /api/v2/sbom/compare?left={id1}&right={id2}`) is documented with request parameters, response shape, and example responses
- [ ] Comparison UI workflow is documented: how to select SBOMs, initiate comparison, navigate diff sections, and share comparison URLs
- [ ] Documentation references the existing SBOM detail page docs and package/advisory data model docs for context
- [ ] Documentation covers error cases (missing parameters, non-existent SBOM IDs)
- [ ] Documentation accurately reflects the implemented feature behavior

## Test Requirements
- [ ] Verify endpoint documentation matches the actual API response shape from the backend implementation
- [ ] Verify UI workflow documentation matches the actual comparison page behavior
- [ ] Verify all six diff section categories are documented (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes)
- [ ] Verify URL-shareable comparison feature is documented with example URLs

## Dependencies
- Depends on: Task 2 -- Add SBOM comparison model and diff service
- Depends on: Task 3 -- Add SBOM comparison endpoint and integration tests
- Depends on: Task 4 -- Add comparison API types, client function, and React Query hook
- Depends on: Task 5 -- Create SBOM comparison page with diff sections
- Depends on: Task 6 -- Add comparison selection to SBOM list page
