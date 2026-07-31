## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Document the new SBOM comparison endpoint and comparison UI workflow. The Feature's Documentation Considerations indicate "New Content" is required:

- **Doc impact type**: New Content
- **User purpose**: API consumers need endpoint reference for `GET /api/v2/sbom/compare`; UI users need a guide for the comparison workflow (selecting SBOMs, reading diff sections, sharing comparison URLs)
- **Reference material**: Existing SBOM detail page documentation, package/advisory data model docs

This task should be completed after all implementation tasks are done so the documentation accurately reflects the final behavior.

## Acceptance Criteria
- [ ] API endpoint documentation covers `GET /api/v2/sbom/compare` including query parameters (`left`, `right`), response shape (six diff categories), error responses (400, 404), and example request/response
- [ ] UI workflow documentation covers: navigating to the comparison page, selecting SBOMs, triggering comparison, reading diff sections, sharing comparison URLs via query parameters
- [ ] Documentation references the existing SBOM detail page docs for context on SBOM data model
- [ ] Documentation is accurate and consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify API endpoint documentation matches the actual endpoint behavior (parameters, response shape, error codes)
- [ ] Verify UI workflow documentation matches the actual page behavior (selectors, diff sections, URL sharing)
- [ ] Verify all example requests and responses are valid and produce correct results when tested against the running service

## Dependencies
- Depends on: Task 2 — Backend comparison model and service logic
- Depends on: Task 3 — Backend comparison endpoint and integration tests
- Depends on: Task 4 — Frontend comparison API layer
- Depends on: Task 5 — Frontend comparison page
