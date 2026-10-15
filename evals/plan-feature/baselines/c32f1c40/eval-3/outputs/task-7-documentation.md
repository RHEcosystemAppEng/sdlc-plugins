## Repository
trustify-backend

## Target Branch
main

## Description
Document the new SBOM comparison endpoint and comparison UI as part of Feature TC-9003 (SBOM comparison view). The Feature's Documentation Considerations specify "New Content" — new documentation pages or sections are needed. API consumers need an endpoint reference for `GET /api/v2/sbom/compare`, and UI users need a guide for the comparison workflow (selecting SBOMs, reading the diff, exporting results).

Doc impact type: **New Content**

Reference material: Existing SBOM detail page documentation, package/advisory data model docs.

## Acceptance Criteria
- [ ] API endpoint documentation for `GET /api/v2/sbom/compare?left={id1}&right={id2}` is complete, including request parameters, response shape, error codes, and example response
- [ ] UI workflow guide documents how to use the comparison view: selecting SBOMs from the list page, reading diff sections, and exporting comparison data
- [ ] Documentation accurately reflects the implemented feature behavior
- [ ] Documentation covers the scope identified in the Feature's Documentation Considerations section

## Test Requirements
- [ ] Verify endpoint documentation matches the actual API response shape from Task 1
- [ ] Verify UI workflow guide matches the implemented comparison page behavior from Tasks 4 and 5
- [ ] Verify example responses are valid JSON matching the `SbomComparisonResult` schema

## Dependencies
- Depends on: Task 1 — Add SBOM comparison model and service
- Depends on: Task 2 — Add SBOM comparison endpoint and tests
- Depends on: Task 3 — Add SBOM comparison API types, client function, and hook
- Depends on: Task 4 — Add SBOM comparison page
- Depends on: Task 5 — Add SBOM selection to list page
- Depends on: Task 6 — Add comparison page tests
