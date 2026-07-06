## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint and the license policy configuration. The feature description indicates a "New Content" documentation impact. Documentation should cover:
- The `GET /api/v2/sbom/{id}/license-report` endpoint: request parameters, response schema, and example responses
- License policy configuration: JSON format, field descriptions, and examples of allow/deny policies
- How compliance officers can use the endpoint for one-click license audits
- How CI/CD pipelines can use the endpoint as an automated compliance gate

Reference: TC-9004 — Add license compliance report endpoint

## Acceptance Criteria
- [ ] Endpoint documentation covers the full request/response contract with examples
- [ ] License policy configuration format is documented with sample JSON
- [ ] Usage guide for compliance officers explains how to interpret the report
- [ ] CI/CD integration guide explains how to use the endpoint as a build gate
- [ ] Documentation is consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify all documented API paths match the actual endpoint implementation
- [ ] Verify documented response schemas match actual API responses
- [ ] Verify documented policy JSON format matches the LicensePolicy struct
- [ ] Verify example commands/curl invocations work against a running instance

## Dependencies
- Depends on: Task 1 — Add license policy configuration model
- Depends on: Task 2 — Add license report model and service
- Depends on: Task 3 — Add license report REST endpoint
- Depends on: Task 4 — Add integration tests for license report endpoint
