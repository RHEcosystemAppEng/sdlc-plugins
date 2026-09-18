## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint (`GET /api/v2/sbom/{id}/license-report`) and the license policy configuration format. The feature documentation should cover:
- Endpoint usage, request parameters, and response format
- License policy JSON configuration schema and examples
- How transitive dependencies are handled in the report
- Compliance flag interpretation

Doc impact type: New Content. The documentation targets compliance officers who need to understand how to configure policies and interpret reports. Reference material includes the SPDX license list and existing package data model documentation.

Feature reference: TC-9004 -- Add license compliance report endpoint.

## Acceptance Criteria
- [ ] License report endpoint is documented with request/response examples
- [ ] License policy configuration format is documented with a complete JSON schema example
- [ ] Transitive dependency behavior is explained
- [ ] Compliance flag semantics are documented (what compliant: true/false means)
- [ ] Documentation is accurate and consistent with the implemented feature behavior

## Test Requirements
- [ ] Documentation accurately reflects the API endpoint path, method, and response shape
- [ ] Configuration examples are valid JSON that can be parsed by the LicensePolicy struct
- [ ] All documented behaviors match the actual implementation

## Dependencies
- Depends on: Task 1 -- Add license report model types and policy configuration
- Depends on: Task 2 -- Implement license report service with transitive dependency resolution
- Depends on: Task 3 -- Add GET /api/v2/sbom/{id}/license-report endpoint
- Depends on: Task 4 -- Add integration tests for license report endpoint
