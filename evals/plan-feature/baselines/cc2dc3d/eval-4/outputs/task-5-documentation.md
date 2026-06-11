## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint and license policy configuration. This task covers updating the project README and adding API documentation so that compliance officers and CI/CD pipeline integrators can understand how to use the endpoint and configure license policies.

## Files to Modify
- `README.md` — add a section describing the license compliance report feature, the endpoint, and a link to the policy configuration documentation

## Files to Create
- `docs/license-policy.md` — documentation for the license policy configuration file format, with examples of common policies (permissive-only, deny-specific-licenses, etc.)

## Implementation Notes
- Document the `GET /api/v2/sbom/{id}/license-report` endpoint with its request parameters and response schema.
- Include an example response showing the `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }` structure.
- Document the `config/license-policy.json` configuration file format, including:
  - How to specify denied license identifiers
  - How to specify allowed license identifiers (optional allowlist)
  - Examples of common policies (e.g., deny all copyleft, allow only permissive licenses)
- Reference the SPDX license list for valid license identifiers.
- Document the CI/CD integration use case: how a pipeline can call the endpoint and check for `compliant: false` groups to gate builds.

## Documentation Updates
- `README.md` — add License Compliance Report section under API features
- `docs/license-policy.md` — new file documenting policy configuration format and examples

## Acceptance Criteria
- [ ] README.md includes a section about the license compliance report feature
- [ ] `docs/license-policy.md` exists with complete policy configuration documentation
- [ ] Endpoint documentation includes request format, response schema, and example response
- [ ] Policy configuration documentation includes at least two example policies
- [ ] CI/CD integration use case is documented with a step-by-step example

## Test Requirements
- [ ] Documentation review: verify all file paths and endpoint paths mentioned in the docs match the actual implementation
- [ ] Verify example JSON in the documentation is valid JSON

## Dependencies
- Depends on: Task 3 — Add license report endpoint
