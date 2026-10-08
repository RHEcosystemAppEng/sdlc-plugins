## Repository
trustify-backend

## Target Branch
main

## Description
Add documentation for the new license compliance report endpoint introduced by TC-9004. The documentation should cover:

- The `GET /api/v2/sbom/{id}/license-report` endpoint: request format, response shape, status codes, and usage examples
- License policy configuration: how to create and customize the `license-policy.json` file, the structure of allowed/denied license lists, and how the policy affects compliance flags
- Use case guidance for compliance officers: how to generate a compliance report, interpret the grouped results, and identify non-compliant licenses
- Use case guidance for CI/CD pipelines: how to integrate the license report endpoint as an automated compliance gate

**Doc impact type**: New Content
**Reference material**: SPDX license list, existing package data model documentation

## Acceptance Criteria
- [ ] Endpoint documentation describes `GET /api/v2/sbom/{id}/license-report` with request parameters, response shape, and status codes
- [ ] License policy configuration is documented with a complete example `license-policy.json`
- [ ] Documentation explains how compliance flags are determined (allowed vs denied lists)
- [ ] CI/CD integration guide shows how to use the endpoint as an automated compliance gate
- [ ] Documentation references the SPDX license identifier list for valid license names

## Test Requirements
- [ ] Documentation accurately reflects the implemented endpoint behavior and response shape
- [ ] Example requests and responses in the documentation are valid and match the actual API contract
- [ ] License policy configuration example is valid JSON that the service can load

## Dependencies
- Depends on: Task 1 -- Add license policy model and compliance report data structures
- Depends on: Task 2 -- Add license compliance report service with transitive dependency resolution
- Depends on: Task 3 -- Add license report endpoint and route registration
- Depends on: Task 4 -- Add integration tests for license compliance report
