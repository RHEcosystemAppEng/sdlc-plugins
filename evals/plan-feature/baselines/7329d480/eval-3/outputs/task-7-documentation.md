## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Create documentation for the SBOM comparison feature covering the new `GET /api/v2/sbom/compare` endpoint reference and the comparison UI workflow. This addresses the feature's Documentation Considerations ("New Content") to support API consumers who need the endpoint reference and UI users who need a guide for the comparison workflow.

## Files to Modify
- `README.md` — add a section documenting the SBOM comparison endpoint under the existing API reference area

## Documentation Updates
- `README.md` — add "SBOM Comparison" section covering: endpoint URL and method, query parameters (left, right), response schema with all six diff categories, example request/response, error responses (400 for missing params, 404 for unknown SBOM), and performance notes (p95 < 1s for up to 2000 packages)

## Acceptance Criteria
- [ ] README documents the GET /api/v2/sbom/compare endpoint with full parameter and response schema
- [ ] Documentation includes an example curl request and JSON response
- [ ] Error responses (400, 404) are documented
- [ ] Performance characteristics are noted

## Test Requirements
- [ ] Verify documentation renders correctly in Markdown preview
- [ ] Verify example curl command executes successfully against a running instance

## Dependencies
- Depends on: Task 3 — Backend comparison endpoint (endpoint must be implemented to document accurately)
