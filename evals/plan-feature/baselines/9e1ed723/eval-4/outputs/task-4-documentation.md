## Repository
trustify-backend

## Target Branch
main

## Description
Document the license compliance report feature delivered by TC-9004 (Add license compliance report endpoint).

Doc impact type: **New Content** — document the `GET /api/v2/sbom/{id}/license-report` endpoint and the license policy configuration (`license-policy.json`).

Details from the Feature's Documentation Considerations:
- User purpose: compliance officers need to understand how to configure policies and interpret reports.
- Reference material: SPDX license list, existing package data model documentation.
- Customer considerations: license policy configuration must be documented, and organizations may have different compliance policies (cover how to customize the policy file).

The documentation should cover: the endpoint request/response shape, the meaning of each group's `compliant` flag, how packages without license data are reported (`NOASSERTION`), how to author and point the server at a custom policy, and how to use the endpoint as an automated CI/CD compliance gate (UC-2), including that error responses (e.g. 404) must be treated as gate failures.

## Acceptance Criteria
- [ ] Documentation describes `GET /api/v2/sbom/{id}/license-report`, its response format, and error responses
- [ ] Documentation explains license policy configuration (file format, allowed/denied lists, unknown-license handling, configuring the file path)
- [ ] Documentation explains how to interpret the report and use it as a CI/CD gate
- [ ] Documentation references the SPDX license list for valid identifiers

## Test Requirements
- [ ] Verify documented request/response examples match the actual endpoint behavior
- [ ] Verify the documented policy file format matches the shipped `license-policy.json` and loader behavior
- [ ] Verify the documentation is complete with respect to the Documentation Considerations scope

## Dependencies
- Depends on: Task 1 — Add configurable license compliance policy
- Depends on: Task 2 — Implement license report aggregation service
- Depends on: Task 3 — Add license report REST endpoint
