## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint and the license policy
configuration. The Feature's Documentation Considerations specify "New Content"
covering the endpoint usage and policy configuration for compliance officers.

Doc impact type: **New Content**

Documentation should cover:
- The `GET /api/v2/sbom/{id}/license-report` endpoint: request format, response
  shape, HTTP status codes, and example usage
- License policy configuration: JSON file format, allowed/denied license lists,
  default mode (allow/deny), and how to customize policies per organization
- How to use the endpoint in CI/CD pipelines as an automated compliance gate
- Reference to the SPDX license list for valid license identifiers

Reference material: SPDX license list, existing package data model documentation.
User purpose: Compliance officers need to understand how to configure policies and
interpret reports.

Feature reference: TC-9004

## Acceptance Criteria
- [ ] Endpoint documentation covers request format, response shape, and status codes
- [ ] License policy configuration format is documented with example JSON
- [ ] CI/CD integration use case is documented with example pipeline usage
- [ ] Documentation is accurate and consistent with the implemented feature behavior

## Test Requirements
- [ ] Documentation accurately reflects the implemented endpoint path and response shape
- [ ] Example JSON policy configuration is valid and parseable
- [ ] All documented HTTP status codes match the actual endpoint behavior

## Dependencies
- Depends on: Task 1 -- Add license report model types and policy configuration
- Depends on: Task 2 -- Implement license compliance report service
- Depends on: Task 3 -- Add license compliance report REST endpoint
- Depends on: Task 4 -- Add integration tests for license compliance report
