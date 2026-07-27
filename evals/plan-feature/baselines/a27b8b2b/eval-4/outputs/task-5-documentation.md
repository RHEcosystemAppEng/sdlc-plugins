## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint and license policy configuration. The feature (TC-9004) introduces a new API endpoint `GET /api/v2/sbom/{id}/license-report` and a configurable license policy file.

**Doc impact type:** New Content

**Documentation scope** (from Feature's Documentation Considerations):
- Document the endpoint: request format, response shape, and usage examples
- Document the license policy configuration: JSON format, allowed/denied license lists, how to customize for different organizational policies
- User purpose: Compliance officers need to understand how to configure policies and interpret reports
- Reference material: SPDX license list, existing package data model documentation

## Acceptance Criteria
- [ ] API endpoint documentation covers `GET /api/v2/sbom/{id}/license-report` with request parameters and response schema
- [ ] License policy configuration documentation covers the JSON config file format with field descriptions
- [ ] Documentation includes at least one usage example showing how to call the endpoint and interpret the response
- [ ] Documentation explains how to customize the license policy for different compliance requirements
- [ ] Documentation references SPDX license identifiers as the canonical format

## Test Requirements
- [ ] Verify the documented endpoint path and response shape match the actual implementation
- [ ] Verify the documented policy configuration format matches the actual JSON schema
- [ ] Verify all documented examples are accurate and produce the described output

## Dependencies
- Depends on: Task 1 — Add license report model and policy types
- Depends on: Task 2 — Add license report service with transitive dependency resolution
- Depends on: Task 3 — Add license report endpoint and route registration
- Depends on: Task 4 — Add license report integration tests
