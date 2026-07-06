## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint and license policy configuration for compliance officers and CI/CD pipeline integrators. This is a New Content documentation task as specified in the feature's Documentation Considerations section. The documentation should cover: how to configure the license policy JSON file, how to call the `GET /api/v2/sbom/{id}/license-report` endpoint, how to interpret the response (license groups with compliance flags), and how to integrate the endpoint into automated compliance gates in CI/CD pipelines. Reference the SPDX license list for standard license identifiers.

## Acceptance Criteria
- [ ] Documentation explains the license policy JSON configuration format (allowed_licenses, denied_licenses)
- [ ] Documentation describes the `GET /api/v2/sbom/{id}/license-report` endpoint including request parameters and response schema
- [ ] Documentation includes at least one example request and response showing license grouping with compliant and non-compliant entries
- [ ] Documentation covers how to use the endpoint as an automated compliance gate in CI/CD pipelines
- [ ] Documentation references the SPDX license list for standard license identifiers

## Test Requirements
- [ ] Verify documentation is accurate by comparing endpoint description against the actual implementation
- [ ] Verify example request/response matches the actual API behavior
- [ ] Verify license policy configuration instructions are complete and actionable

## Dependencies
- Depends on: Task 3 -- Add license compliance report REST endpoint
- Depends on: Task 4 -- Add integration tests for license compliance report
