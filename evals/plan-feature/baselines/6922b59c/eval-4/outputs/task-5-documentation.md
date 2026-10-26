# Task 5 — Document license report endpoint and policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Document the new `GET /api/v2/sbom/{id}/license-report` endpoint and the license policy configuration format. The feature description indicates "New Content" documentation impact: compliance officers need to understand how to configure license policies and interpret compliance reports. Documentation should cover the endpoint request/response format, the license policy JSON schema, and how to set up automated compliance gates in CI/CD pipelines.

Reference: Feature TC-9004 — Add license compliance report endpoint.

Doc impact type: **New Content**

Documentation Considerations details:
- User purpose: Compliance officers need to understand how to configure policies and interpret reports
- Reference material: SPDX license list, existing package data model documentation

## Acceptance Criteria
- [ ] Endpoint documentation covers the `GET /api/v2/sbom/{id}/license-report` request path, parameters, and response schema
- [ ] License policy configuration format is documented with example JSON showing denied and allowed license lists
- [ ] Documentation explains how to interpret the compliance flags in the report response
- [ ] CI/CD integration guidance is provided (how to use the endpoint as an automated compliance gate)
- [ ] Documentation references the SPDX license list for valid license identifiers

## Test Requirements
- [ ] Documentation accurately reflects the implemented endpoint behavior and response schema
- [ ] Example policy JSON in the documentation is valid and can be used as-is
- [ ] All API paths and response fields mentioned in the documentation match the actual implementation

## Dependencies
- Depends on: Task 1 — Add license report model types and policy configuration
- Depends on: Task 2 — Implement license compliance report service
- Depends on: Task 3 — Add license report endpoint and register route
- Depends on: Task 4 — Add integration tests for license report endpoint
