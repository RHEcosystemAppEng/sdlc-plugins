## Repository
trustify-backend

## Target Branch
main

## Description
Document the new SBOM comparison endpoint and comparison UI for the SBOM comparison feature (TC-9003). The Feature's Documentation Considerations specify New Content: document the comparison endpoint and comparison UI. API consumers need an endpoint reference; UI users need a guide for the comparison workflow. Reference existing SBOM detail page documentation and package/advisory data model docs.

## Acceptance Criteria
- [ ] Comparison endpoint (`GET /api/v2/sbom/compare`) is documented with request parameters, response shape, and example responses
- [ ] Comparison UI workflow is documented: how to select SBOMs, trigger comparison, and interpret diff sections
- [ ] Documentation references existing SBOM detail page documentation and data model docs for context
- [ ] Error responses (400, 404) are documented with example error payloads

## Test Requirements
- [ ] Documentation accurately reflects the implemented endpoint path and query parameters
- [ ] Response shape in documentation matches the actual `SbomComparisonResult` type
- [ ] UI workflow documentation matches the actual page flow

## Dependencies
- Depends on: Task 3 — Backend comparison endpoint
- Depends on: Task 7 — Frontend comparison page
