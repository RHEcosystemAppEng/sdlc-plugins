# Task 8: Documentation for SBOM comparison feature

**Summary**: Document SBOM comparison endpoint and UI workflow

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Create documentation for the new SBOM comparison feature covering both the REST API endpoint and the UI workflow. The Feature's Documentation Considerations specify "New Content" — new documentation pages or sections are needed for:

- **API consumers**: endpoint reference for `GET /api/v2/sbom/compare` including request parameters, response shape, and example usage
- **UI users**: guide for the comparison workflow — selecting SBOMs, interpreting the diff view, and sharing comparison URLs

**Doc impact type**: New Content
**Reference material**: Existing SBOM detail page documentation, package/advisory data model docs
**Feature reference**: TC-9003 — SBOM comparison view

## Acceptance Criteria
- [ ] API endpoint documentation covers `GET /api/v2/sbom/compare` with query parameters, response schema, error codes (400, 404), and example request/response
- [ ] UI workflow documentation covers the end-to-end comparison flow: selecting SBOMs, clicking Compare, navigating diff sections, and sharing URLs
- [ ] Documentation accurately reflects the implemented feature behavior (endpoint paths, response fields, UI components)
- [ ] Documentation covers the performance characteristics (p95 < 1s for SBOMs with up to 2000 packages)

## Test Requirements
- [ ] Verify API documentation matches the actual endpoint behavior (path, parameters, response shape)
- [ ] Verify UI documentation screenshots or descriptions match the implemented comparison page
- [ ] Verify example requests in the API docs return valid responses against a running instance

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model and diff service
- Depends on: Task 3 — Add comparison endpoint with integration tests
- Depends on: Task 5 — Add SbomComparePage with diff sections UI
- Depends on: Task 6 — Add comparison route and SbomListPage multi-select
