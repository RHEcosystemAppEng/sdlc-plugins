## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Document the new SBOM comparison endpoint and comparison UI workflow. Add API reference documentation for `GET /api/v2/sbom/compare` covering request parameters, response schema, and error codes. Include a user-facing guide for the comparison workflow.

## Documentation Updates
- `README.md` — Add a section documenting the SBOM comparison endpoint: request parameters (left and right SBOM IDs as query params), response schema (six diff categories with field definitions), error codes (400 for missing parameters, 404 for nonexistent SBOM), and performance characteristics (p95 < 1s for SBOMs up to 2000 packages). Reference existing SBOM detail endpoint documentation for data model context.

## Acceptance Criteria
- [ ] Comparison endpoint documented with request parameters and example response
- [ ] Error codes (400, 404) and their conditions documented
- [ ] Comparison UI workflow described for end users
- [ ] Performance characteristics noted
