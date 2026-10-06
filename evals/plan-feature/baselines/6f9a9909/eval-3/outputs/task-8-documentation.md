## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Document the new SBOM comparison endpoint and comparison UI for the TC-9003 feature. The Feature's Documentation Considerations indicate "New Content" is needed: API consumers need an endpoint reference for `GET /api/v2/sbom/compare`, and UI users need a guide for the comparison workflow (selecting SBOMs, interpreting diff sections, sharing comparison URLs).

**Doc impact type:** New Content
**User purpose:** API consumers need endpoint reference; UI users need a guide for the comparison workflow
**Reference material:** Existing SBOM detail page documentation, package/advisory data model docs

## Acceptance Criteria
- [ ] API endpoint documentation covers `GET /api/v2/sbom/compare` with query parameters, request/response shapes, and error codes
- [ ] UI workflow guide covers SBOM selection from list page, comparison page navigation, diff section interpretation, and URL sharing
- [ ] Documentation references the correct API response shape matching the implemented endpoint
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify API endpoint documentation matches the actual endpoint behavior (path, parameters, response shape)
- [ ] Verify UI workflow guide accurately describes the implemented comparison page layout and interactions
- [ ] Verify all code examples and API samples are syntactically correct

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model and diff service
- Depends on: Task 3 — Add GET /api/v2/sbom/compare endpoint
- Depends on: Task 4 — Add integration tests for SBOM comparison endpoint
- Depends on: Task 5 — Add comparison API types, client function, and React Query hook
- Depends on: Task 6 — Add SBOM comparison page with diff sections
- Depends on: Task 7 — Add SBOM multi-select and comparison navigation on list page
