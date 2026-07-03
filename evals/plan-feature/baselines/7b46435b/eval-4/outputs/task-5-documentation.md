# Task 5 — Document license report endpoint and policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Document the new `GET /api/v2/sbom/{id}/license-report` endpoint and the license policy configuration for compliance officers and API consumers. This is new documentation content covering:

- The license report endpoint: request format, response schema, HTTP status codes, and usage examples
- The license policy configuration: file format, how to customize the non-compliant license list, and where the configuration file is located
- Use case guidance: how compliance officers can use the endpoint for one-click license audits, and how CI/CD pipelines can use it as an automated compliance gate

**Doc impact type**: New Content (from Feature TC-9004 Documentation Considerations)

**User purpose**: Compliance officers need to understand how to configure policies and interpret reports.

**Reference material**: SPDX license list, existing package data model documentation.

## Acceptance Criteria
- [ ] Endpoint documentation covers request format (`GET /api/v2/sbom/{id}/license-report`), response schema, and HTTP status codes (200, 404)
- [ ] License policy configuration documentation explains the JSON config file format and how to customize it
- [ ] Documentation includes at least one usage example (curl command or equivalent)
- [ ] Documentation explains the compliance flag semantics (`compliant: true/false` per license group)
- [ ] Documentation references the SPDX license list for valid license identifiers

## Test Requirements
- [ ] Verify documentation accurately reflects the implemented endpoint behavior (request/response shapes match actual API)
- [ ] Verify the license policy configuration example in docs matches the actual `config/license-policy.json` format
- [ ] Verify any curl examples return the documented response structure when run against a running instance

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
- Depends on: Task 4 — Add integration tests for license report endpoint
