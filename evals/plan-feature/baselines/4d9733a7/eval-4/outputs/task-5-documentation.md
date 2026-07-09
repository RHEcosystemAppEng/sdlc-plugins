## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint and license policy configuration. The Feature description (TC-9004) indicates a documentation impact type of "New Content" — new documentation pages or sections are needed to cover:

- The `GET /api/v2/sbom/{id}/license-report` endpoint: request parameters, response schema, compliance flag semantics
- License policy configuration: JSON config file format, supported license categories (allowed, denied, review_required), how to customize the policy for different organizational requirements
- Use case examples: generating a compliance report, integrating with CI/CD pipelines for automated compliance gates

Reference: Feature TC-9004 — Add license compliance report endpoint

## Acceptance Criteria
- [ ] API endpoint documentation covers the request path, parameters, response schema, and error responses (404 for nonexistent SBOM)
- [ ] License policy configuration documentation explains the JSON format, supported categories, and customization instructions
- [ ] Documentation includes at least one example request/response pair
- [ ] Documentation references the SPDX license list for valid license identifiers

## Test Requirements
- [ ] Documentation accurately reflects the implemented endpoint behavior and response schema
- [ ] License policy configuration examples are valid JSON that can be loaded by the policy loader
- [ ] All documented endpoint paths match the actual registered routes

## Dependencies
- Depends on: Task 1 — Add license policy configuration model
- Depends on: Task 2 — Add license report model and service
- Depends on: Task 3 — Add license report endpoint
- Depends on: Task 4 — Add integration tests for license report endpoint
