## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Document the new SBOM comparison endpoint and comparison UI workflow. The Feature's Documentation Considerations indicate "New Content" is needed: API consumers need an endpoint reference for `GET /api/v2/sbom/compare`, and UI users need a guide for the comparison workflow (selecting SBOMs, viewing diffs, sharing comparison URLs).

Doc impact type: **New Content**

Reference the Feature issue TC-9003 for full context on the comparison capability, including use cases UC-1 (compare two SBOM versions) and UC-2 (share comparison with compliance team).

## Acceptance Criteria
- [ ] API endpoint documentation covers `GET /api/v2/sbom/compare?left={id1}&right={id2}` with request parameters, response shape, status codes (200, 400, 404), and example response
- [ ] UI workflow documentation covers the comparison page layout, SBOM selection, diff sections, URL sharing, and export functionality
- [ ] Documentation is consistent with the implemented feature behavior
- [ ] Documentation covers the scope identified in Documentation Considerations: endpoint reference and comparison workflow guide

## Test Requirements
- [ ] Verify API endpoint documentation matches the actual endpoint parameters, response shape, and error codes
- [ ] Verify UI workflow documentation accurately describes the comparison page as implemented
- [ ] Verify example API responses are valid and match the actual response structure

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model types and diff service
- Depends on: Task 3 — Add SBOM comparison endpoint and integration tests
- Depends on: Task 4 — Add SBOM comparison API types and React Query hook
- Depends on: Task 5 — Build SBOM comparison page UI with diff sections
- Depends on: Task 6 — Add SBOM selection to list page and register comparison route
