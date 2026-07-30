## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint and the license policy configuration. The feature adds `GET /api/v2/sbom/{id}/license-report` and a configurable license policy via `license-policy.json`. Documentation should cover endpoint usage (request/response format, error codes), license policy configuration (JSON schema, allowed/denied lists, default compliance behavior), and integration with CI/CD pipelines for automated compliance gating.

Doc impact type: New Content

Details from Documentation Considerations:
- User purpose: Compliance officers need to understand how to configure policies and interpret reports
- Reference material: SPDX license list, existing package data model documentation
- Add license report endpoint to Grafana dashboard documentation
- Monitor for slow reports on large SBOMs

## Acceptance Criteria
- [ ] Endpoint documentation covers request format, response structure, and error codes for `GET /api/v2/sbom/{id}/license-report`
- [ ] License policy configuration documentation explains the JSON schema, allowlist/denylist fields, and default compliance behavior
- [ ] CI/CD integration guide explains how to use the endpoint as an automated compliance gate
- [ ] Documentation references the SPDX license identifier format

## Test Requirements
- [ ] Verify documentation accurately reflects the implemented endpoint behavior
- [ ] Verify all response fields are documented with correct types and descriptions
- [ ] Verify the license policy configuration example is valid JSON that deserializes correctly

## Dependencies
- Depends on: Task 1 — Add license policy configuration model
- Depends on: Task 2 — Implement license report service
- Depends on: Task 3 — Add license report endpoint
- Depends on: Task 4 — Add integration tests for license report endpoint
