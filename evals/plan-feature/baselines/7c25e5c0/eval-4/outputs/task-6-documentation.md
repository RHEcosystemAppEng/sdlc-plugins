## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint and license policy configuration. The feature description indicates "New Content" documentation impact: document the endpoint and license policy configuration for compliance officers who need to understand how to configure policies and interpret reports.

Documentation should cover:
- The `GET /api/v2/sbom/{id}/license-report` endpoint: request parameters, response shape, and example usage
- License policy configuration: format of the `license-policy.json` file, supported fields, and how to customize allowed/denied license lists
- Reference to the SPDX license list for valid license identifiers

Reference: Feature TC-9004

## Acceptance Criteria
- [ ] Documentation accurately describes the license report endpoint path, method, and response structure
- [ ] Documentation explains how to configure the license policy JSON file with examples
- [ ] Documentation references SPDX license identifiers
- [ ] Documentation includes at least one example request/response pair

## Test Requirements
- [ ] Verify documentation is accurate against the implemented endpoint behavior
- [ ] Verify example request/response matches actual API output
- [ ] Verify license policy configuration examples are valid JSON

## Dependencies
- Depends on: Task 4 — License report endpoint
- Depends on: Task 5 — Integration tests
