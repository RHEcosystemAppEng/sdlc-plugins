## Repository
trustify-backend

## Target Branch
main

## Description
Document the new `GET /api/v2/sbom/{id}/license-report` endpoint and the license policy configuration. This is a "New Content" documentation task per the feature's Documentation Considerations.

The documentation should cover:
- Endpoint usage: path, method, request parameters, response shape with examples
- License policy configuration: JSON file format, allowed/denied license lists, policy mode
- Use cases: generating a compliance report for a single SBOM, integrating with CI/CD pipelines for automated compliance gates
- Reference material: link to SPDX license list for valid license identifiers

Feature reference: TC-9004 (Add license compliance report endpoint)

## Acceptance Criteria
- [ ] Endpoint documentation covers the `GET /api/v2/sbom/{id}/license-report` path, HTTP method, path parameters, and response shape
- [ ] Response shape example matches the feature specification: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- [ ] License policy configuration format is documented with example JSON files for both allowlist and denylist modes
- [ ] Documentation explains how to configure and deploy a custom license policy
- [ ] CI/CD integration use case is documented (automated compliance gate)
- [ ] Documentation is accurate and consistent with the implemented feature behavior

## Test Requirements
- [ ] Verify documented endpoint path and response shape match the actual implementation
- [ ] Verify documented policy JSON format matches what the policy loader accepts
- [ ] Verify all example requests and responses are valid and reproducible

## Dependencies
- Depends on: Task 1 -- Add license compliance report model and policy configuration
- Depends on: Task 2 -- Add license compliance report service with transitive dependency resolution
- Depends on: Task 3 -- Add license compliance report endpoint
- Depends on: Task 4 -- Add license compliance report integration tests
