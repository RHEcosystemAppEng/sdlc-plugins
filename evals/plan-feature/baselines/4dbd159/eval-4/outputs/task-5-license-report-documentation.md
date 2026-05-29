# Task 5 — Document license report endpoint and policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Add documentation for the new license compliance report endpoint and the license policy configuration. This covers the API endpoint usage (request/response), how to configure the license policy JSON file, and how compliance teams can use the report in CI/CD pipelines for automated compliance gating.

## Files to Modify
- `README.md` — add a section or reference to the license compliance report feature

## Files to Create
- `docs/license-compliance.md` — comprehensive documentation for the license report feature including endpoint usage, policy configuration format, and CI/CD integration examples

## Implementation Notes
- Document the endpoint: `GET /api/v2/sbom/{id}/license-report`
  - Path parameters: `id` (SBOM identifier)
  - Response body shape: `{ groups: [{ license: String, packages: [{ name, version, purl }], compliant: bool }] }`
  - HTTP status codes: 200 (success), 404 (SBOM not found)
  - Authentication requirements (same as other SBOM endpoints)
- Document the license policy configuration:
  - JSON file format with `allowed_licenses` and `denied_licenses` arrays
  - How to set the policy file path (environment variable or server configuration)
  - Example policy file for common enterprise use cases (e.g., deny GPL-3.0, allow MIT/Apache-2.0/BSD)
- Document CI/CD integration:
  - How to call the endpoint from a pipeline
  - How to check `compliant: false` groups and fail the build
  - Example shell script or pipeline step
- Reference the SPDX license list for valid license identifiers
- Per docs/constraints.md: commit messages must follow Conventional Commits format (constraint 2.2).

## Documentation Updates
- `README.md` — add reference to the license compliance report feature and link to `docs/license-compliance.md`
- `docs/license-compliance.md` — new document covering endpoint usage, policy configuration, and CI/CD integration

## Acceptance Criteria
- [ ] License report endpoint is documented with request/response examples
- [ ] License policy JSON configuration format is documented with example files
- [ ] CI/CD integration workflow is documented with example pipeline usage
- [ ] README references the new documentation

## Test Requirements
- [ ] Documentation is accurate and consistent with the implemented API
- [ ] Example policy JSON is valid and can be parsed by the policy loader

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
