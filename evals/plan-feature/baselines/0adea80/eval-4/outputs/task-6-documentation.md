# Task 6 — Document license compliance report endpoint and policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Add documentation for the new license compliance report endpoint and the license policy configuration. This covers the API endpoint usage (request/response format), how to configure the license policy JSON file, and how to interpret the compliance report output. This documentation serves compliance officers who need to configure policies and CI/CD pipeline engineers who integrate the endpoint into automated workflows.

## Files to Modify
- `README.md` — Add a section describing the license compliance report feature, including the endpoint path, expected response format, and a link to the policy configuration documentation

## Files to Create
- `docs/license-policy-configuration.md` — Detailed guide for configuring the license policy JSON file, including the schema, default values, SPDX license identifiers, and examples of common configurations (permissive-only, copyleft-allowed, custom deny lists)

## Implementation Notes
- Document the endpoint: `GET /api/v2/sbom/{id}/license-report`
  - Path parameters: `id` (SBOM identifier)
  - Response shape with example JSON
  - HTTP status codes: 200 (success), 404 (SBOM not found)
- Document the license policy configuration:
  - JSON schema for `config/default-license-policy.json`
  - Fields: `allowed_licenses`, `denied_licenses`, `default_policy`
  - How to customize the policy for different organizational needs
  - Reference to the SPDX license list for valid identifiers
- Document the CI/CD integration use case: how to call the endpoint and check for `compliant: false` to fail a build
- Follow existing documentation patterns in the repository (check README.md style and any existing docs/ files)

## Acceptance Criteria
- [ ] README.md includes a section about the license compliance report feature
- [ ] License policy configuration guide explains the JSON schema with examples
- [ ] CI/CD integration workflow is documented with a concrete example
- [ ] All documented endpoint paths and response shapes match the actual implementation

## Test Requirements
- [ ] Manual review: verify all documented paths and response shapes match the implemented endpoint
- [ ] Manual review: verify the license policy JSON examples are valid and parseable

## Dependencies
- Depends on: Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint
- Depends on: Task 1 — Add license policy configuration model and loader
