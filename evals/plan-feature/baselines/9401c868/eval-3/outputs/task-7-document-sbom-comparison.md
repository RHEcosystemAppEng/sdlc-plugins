## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Document the new SBOM comparison feature covering both the backend API endpoint and the frontend comparison UI. The Feature's Documentation Considerations specify "New Content" with doc impact: API consumers need endpoint reference documentation for `GET /api/v2/sbom/compare`, and UI users need a guide for the comparison workflow (selecting SBOMs, interpreting the diff view, sharing comparison URLs). Reference material includes existing SBOM detail page documentation and package/advisory data model docs.

Doc impact type: New Content.

## Acceptance Criteria
- [ ] API endpoint documentation covers `GET /api/v2/sbom/compare` with request parameters, response shape, and error codes
- [ ] UI documentation covers the comparison workflow: selecting SBOMs from the list page, navigating to the comparison view, and interpreting diff sections
- [ ] URL sharing workflow is documented (bookmarkable comparison URLs with left/right query params)
- [ ] Documentation references existing SBOM detail page and package/advisory data model docs
- [ ] Export functionality (JSON/CSV) is documented

## Test Requirements
- [ ] Verify documentation accurately reflects the implemented API endpoint path, parameters, and response shape
- [ ] Verify documentation accurately describes the UI workflow and PatternFly component behavior
- [ ] Verify all linked references to existing documentation are valid

## Dependencies
- Depends on: Task 3 -- Add SBOM comparison endpoint with integration tests
- Depends on: Task 5 -- Implement SBOM comparison page with diff sections
- Depends on: Task 6 -- Add SBOM comparison selection to list page
