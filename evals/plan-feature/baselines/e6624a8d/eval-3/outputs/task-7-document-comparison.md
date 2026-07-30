## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Document the new SBOM comparison endpoint and the comparison UI workflow. The Feature description indicates a doc impact of "New Content" -- new documentation pages or sections are needed covering the comparison REST API endpoint reference and a user guide for the comparison UI workflow. This documentation supports both API consumers who need endpoint reference material and UI users who need a guide for the comparison workflow.

Doc impact type: New Content.
Reference: Feature TC-9003 -- SBOM comparison view.

## Acceptance Criteria
- [ ] API documentation covers the `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint with request parameters and response shape
- [ ] User guide documents the comparison workflow: selecting SBOMs, viewing diff sections, sharing comparison URLs, and exporting results
- [ ] Documentation accurately reflects the implemented feature behavior
- [ ] Documentation covers the scope identified in Feature TC-9003 Documentation Considerations: API endpoint reference and UI workflow guide

## Test Requirements
- [ ] Verify documentation is accurate and consistent with the implemented endpoint behavior
- [ ] Verify documentation covers both API consumers and UI users as specified in the Feature
- [ ] Verify all response fields and query parameters are documented correctly

## Dependencies
- Depends on: Task 2 -- Add SBOM comparison diff models and service
- Depends on: Task 3 -- Add SBOM comparison REST endpoint with integration tests
- Depends on: Task 4 -- Add comparison API types, client function, and React Query hook
- Depends on: Task 5 -- Implement SBOM comparison page with diff sections
- Depends on: Task 6 -- Add comparison route and SBOM list page selection integration
