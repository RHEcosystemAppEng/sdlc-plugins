# Task 5 -- Add license report API and policy configuration documentation

## Repository
trustify-backend

## Target Branch
main

## Description
Add documentation for the license compliance report feature (TC-9004), covering the new API endpoint, license policy configuration, and usage examples. This enables compliance officers and CI/CD pipeline operators to understand how to configure policies and consume the license report API.

## Files to Modify
- `README.md` -- Add a section describing the license compliance report capability and link to detailed documentation

## Files to Create
- `docs/license-compliance.md` -- Comprehensive documentation covering: endpoint usage (`GET /api/v2/sbom/{id}/license-report`), response schema, license policy configuration (`license-policy.json` format), customization guide for allowed/denied license lists, and CI/CD integration examples for automated compliance gating

## Implementation Notes
- Review the existing README.md to understand the documentation style and structure, then add the license compliance section in a consistent format.
- Document the full API contract: endpoint path, HTTP method, path parameters, response schema with field descriptions, and example response JSON.
- Document the `license-policy.json` configuration format: `allowed_licenses`, `denied_licenses`, `default_policy` fields with descriptions and examples.
- Include a CI/CD integration example showing how a pipeline can call the endpoint and check for `compliant: false` groups to fail a build (UC-2 from the feature description).
- Reference the SPDX license list for valid license identifiers.
- Per CONVENTIONS.md (repository conventions): follow existing documentation patterns.
  Applies: convention has no file-type restriction (broadly applicable).

## Acceptance Criteria
- [ ] The license report endpoint is documented with path, method, parameters, and response schema
- [ ] The license policy configuration format is documented with all fields explained
- [ ] A CI/CD integration example is provided
- [ ] The README references the new documentation
- [ ] Documentation is clear and actionable for compliance officers and pipeline operators

## Test Requirements
- [ ] Documentation review: verify all documented field names match the actual API response schema
- [ ] Documentation review: verify the example `license-policy.json` is valid JSON and matches the `LicensePolicy` struct

## Documentation Updates
- `README.md` -- Add a "License Compliance" section with a summary and link to `docs/license-compliance.md`
- `docs/license-compliance.md` -- New file: full documentation for the license report endpoint and policy configuration

## Dependencies
- Depends on: Task 3 -- Add license report endpoint

<!-- [sdlc-workflow] Description digest: sha256-md:96e9a7102a270f6b8a214e782189bdacc8e10487a62762013b8ea191ea6393af -->
