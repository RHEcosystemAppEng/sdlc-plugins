## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report feature (TC-9004). The documentation should cover the GET /api/v2/sbom/{id}/license-report endpoint, including request parameters, response format, and error responses. It should also document the license policy configuration file format, how to customize it for different organizational compliance policies, and how to use the endpoint for automated compliance gates in CI/CD pipelines.

Doc impact type: New Content. Reference: Feature TC-9004 — Add license compliance report endpoint.

Details from Documentation Considerations:
- User purpose: Compliance officers need to understand how to configure policies and interpret reports
- Reference material: SPDX license list, existing package data model documentation

## Acceptance Criteria
- [ ] Endpoint documentation covers the request format (GET with SBOM ID path parameter), response schema (ComplianceReport with LicenseGroup array), and error handling (404 for missing SBOM)
- [ ] License policy configuration format is documented with a complete JSON schema example including allowed-licenses, denied-licenses, and default-compliance fields
- [ ] Documentation explains how organizations can customize the policy for their specific compliance requirements
- [ ] CI/CD integration use case is documented with example pipeline steps for automated compliance gating
- [ ] Documentation references the SPDX license list for valid license identifiers

## Test Requirements
- [ ] Verify documentation accurately reflects the implemented endpoint behavior and response format
- [ ] Verify policy configuration examples are valid JSON that the system can successfully parse

## Dependencies
- Depends on: Task 4 — Add integration tests for the license compliance report endpoint
