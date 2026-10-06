## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Document the SBOM comparison endpoint and comparison UI workflow. The feature's Documentation Considerations specify "New Content" doc impact: API consumers need an endpoint reference for `GET /api/v2/sbom/compare`, and UI users need a guide for the comparison workflow.

**Doc impact type:** New Content

**Documentation Considerations from Feature TC-9003:**
- User purpose: API consumers need endpoint reference; UI users need a guide for the comparison workflow
- Reference material: Existing SBOM detail page documentation, package/advisory data model docs

This task should be completed after all implementation tasks are done, so the documentation accurately reflects the implemented behavior.

## Acceptance Criteria
- [ ] API endpoint reference documents `GET /api/v2/sbom/compare` with request parameters, response shape, error codes, and example request/response
- [ ] UI workflow guide documents the comparison page: selecting SBOMs, triggering comparison, reading diff sections, and sharing comparison URLs
- [ ] Documentation covers the SBOM list page entry point (checkbox selection and "Compare selected" button)
- [ ] Documentation references existing SBOM detail page docs for context on the data model
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify the API endpoint reference matches the actual endpoint behavior (parameters, response shape, error codes)
- [ ] Verify the UI workflow guide matches the actual page behavior and component layout
- [ ] Verify all six diff section categories are documented with their column structures

## Dependencies
- Depends on: Task 3 — Add SBOM comparison endpoint with integration tests
- Depends on: Task 7 — Add comparison page unit and E2E tests
