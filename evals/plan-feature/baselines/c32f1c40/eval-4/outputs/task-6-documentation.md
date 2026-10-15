## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint and the license policy configuration. This is a "New Content" documentation impact — compliance officers need to understand how to configure license policies and interpret the compliance report. Reference the SPDX license list for license identifiers and the existing package data model documentation for context.

The documentation should cover:
- The `GET /api/v2/sbom/{id}/license-report` endpoint: request parameters, response shape, and example responses
- License policy configuration: JSON file format, allowed/denied license lists, default policy behavior
- Use cases: generating compliance reports and integrating with CI/CD pipelines as an automated compliance gate

## Acceptance Criteria
- [ ] Documentation accurately describes the `GET /api/v2/sbom/{id}/license-report` endpoint with request/response examples
- [ ] Documentation explains the license policy JSON configuration format with all fields
- [ ] Documentation covers both `default_policy: "allow"` and `default_policy: "deny"` behaviors
- [ ] Documentation references SPDX license identifiers as the canonical format
- [ ] Documentation includes a use case example for CI/CD pipeline integration (automated compliance gate)
- [ ] Documentation is consistent with the implemented endpoint behavior

## Test Requirements
- [ ] Verify documented endpoint path matches the implemented endpoint
- [ ] Verify documented response shape matches the actual `LicenseReport` struct
- [ ] Verify documented policy configuration format matches the actual `LicensePolicy` struct
- [ ] Verify example requests/responses are valid and reproducible

## Dependencies
- Depends on: Task 1 — Add license compliance report response types
- Depends on: Task 2 — Add license policy configuration
- Depends on: Task 3 — Implement license report service
- Depends on: Task 4 — Add license report endpoint
- Depends on: Task 5 — Integration tests for license report endpoint
