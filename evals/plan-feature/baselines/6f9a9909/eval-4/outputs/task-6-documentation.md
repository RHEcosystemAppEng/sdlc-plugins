## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint and license policy configuration. This is a New Content documentation task -- the feature introduces a new API endpoint (`GET /api/v2/sbom/{id}/license-report`) and a configurable license policy mechanism that both require documentation for compliance officers and platform users.

**Doc impact type**: New Content

**Documentation scope** (from Feature's Documentation Considerations):
- Document the license report endpoint: URL, HTTP method, request parameters, response shape, status codes
- Document the license policy configuration: JSON file format, supported license categories (allowed, denied, review_required), how to customize the policy for different organizations
- User purpose: Compliance officers need to understand how to configure policies and interpret reports
- Reference material: SPDX license list, existing package data model documentation

## Acceptance Criteria
- [ ] License report endpoint is documented with URL, method, parameters, response schema, and example response
- [ ] License policy configuration format is documented with a complete example JSON file
- [ ] Documentation explains how organizations can customize the policy for their compliance requirements
- [ ] Documentation references the SPDX license list for standard license identifiers
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify the documented endpoint URL matches the implemented endpoint
- [ ] Verify the documented response schema matches the actual API response
- [ ] Verify the documented policy configuration format matches what the service accepts
- [ ] Verify example requests in the documentation return expected responses when run against a live instance

## Dependencies
- Depends on: Task 1 -- Add license report response model types
- Depends on: Task 2 -- Add license policy configuration
- Depends on: Task 3 -- Add license compliance report service
- Depends on: Task 4 -- Add license report REST endpoint
- Depends on: Task 5 -- Add license report integration tests
