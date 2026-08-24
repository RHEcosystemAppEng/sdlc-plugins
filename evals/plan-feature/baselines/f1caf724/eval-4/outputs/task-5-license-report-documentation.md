## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint and license policy configuration. The Feature's Documentation Considerations indicate "New Content" is needed: document the `GET /api/v2/sbom/{id}/license-report` endpoint, explain the license policy configuration format, and describe how compliance officers can use the report to audit open-source license usage. Reference the SPDX license list and existing package data model documentation as specified in the Feature's reference material.

Doc impact type: New Content
Details: Compliance officers need to understand how to configure license policies and interpret compliance reports. Reference SPDX license list and existing package data model documentation.

Feature reference: TC-9004

## Acceptance Criteria
- [ ] Endpoint documentation covers `GET /api/v2/sbom/{id}/license-report` with request parameters, response shape, and example response
- [ ] License policy configuration format is documented (JSON schema, allowed/denied license lists, default policy)
- [ ] Usage guide explains how compliance officers interpret the report (license groups, compliance flags)
- [ ] CI/CD integration guide explains how to use the endpoint as an automated compliance gate (UC-2)
- [ ] Documentation references the SPDX license list for valid license identifiers

## Test Requirements
- [ ] Documentation accurately reflects the implemented endpoint behavior and response shape
- [ ] License policy configuration examples are valid and can be deserialized by the application
- [ ] All documented endpoint paths and response fields match the actual implementation

## Dependencies
- Depends on: Task 1 -- Add license report model types and policy configuration
- Depends on: Task 2 -- Implement license compliance report service
- Depends on: Task 3 -- Add license report endpoint and route registration
- Depends on: Task 4 -- Add license report integration tests
