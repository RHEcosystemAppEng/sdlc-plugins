## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint and license policy configuration. The Feature's Documentation Considerations indicate "New Content" is needed: compliance officers need to understand how to configure license policies and interpret the compliance report output.

Documentation should cover:
- The `GET /api/v2/sbom/{id}/license-report` endpoint: request format, response shape, and usage examples
- License policy configuration: how to customize the `license-policy.json` file to define approved, restricted, and banned licenses
- Integration with CI/CD pipelines: how to use the endpoint as an automated compliance gate
- Reference to the SPDX license list for license identifiers

Doc impact type: **New Content**

## Acceptance Criteria
- [ ] API endpoint documentation covers request/response format with examples
- [ ] License policy configuration documentation explains the JSON format and customization options
- [ ] CI/CD integration guide shows how to use the endpoint as a compliance gate
- [ ] Documentation references the SPDX license list for valid license identifiers
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify documented request/response examples match the actual API behavior
- [ ] Verify license policy configuration examples are valid and produce expected results
- [ ] Verify all documented endpoints and paths are correct

## Dependencies
- Depends on: Task 1 — Add license policy configuration and license report models
- Depends on: Task 2 — Add license report service with transitive dependency resolution
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
- Depends on: Task 4 — Add integration tests for license report endpoint
