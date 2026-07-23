## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Document the new SBOM comparison endpoint and the frontend comparison UI workflow for the SBOM comparison view feature (TC-9003).

The Feature's Documentation Considerations indicate **New Content** is needed:
- **Doc impact type:** New Content
- **User purpose:** API consumers need endpoint reference; UI users need a guide for the comparison workflow
- **Reference material:** Existing SBOM detail page documentation, package/advisory data model docs

Documentation should cover:
1. The `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint -- request parameters, response shape, error codes, and performance characteristics
2. The comparison UI workflow -- how to select two SBOMs, interpret the diff sections, share comparison URLs, and understand the comparison categories (added/removed packages, version changes, new/resolved vulnerabilities, license changes)

## Acceptance Criteria
- [ ] API endpoint documentation covers request parameters (left, right), response schema, and error responses (400, 404)
- [ ] API documentation includes the full response JSON structure with field descriptions
- [ ] UI workflow guide explains how to select two SBOMs and initiate a comparison
- [ ] UI documentation describes all six diff section categories and their meaning
- [ ] Documentation explains URL-shareable comparisons for bookmarking and sharing
- [ ] Documentation references existing SBOM detail page docs for context
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Review documentation for accuracy against the implemented endpoint and UI
- [ ] Verify all documented API response fields match the actual SbomComparisonResult schema
- [ ] Verify all documented UI features are present in the comparison page
- [ ] Verify linked cross-references to existing docs are valid

## Dependencies
- Depends on: Task 2 -- Backend: Add SBOM comparison model and diff service
- Depends on: Task 3 -- Backend: Add SBOM comparison endpoint and integration tests
- Depends on: Task 5 -- Frontend: Build SBOM comparison page with diff sections
- Depends on: Task 6 -- Frontend: Add comparison route and SBOM list page selection
