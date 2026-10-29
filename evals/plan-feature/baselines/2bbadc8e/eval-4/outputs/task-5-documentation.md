## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint (`GET /api/v2/sbom/{id}/license-report`) and the license policy configuration for the SBOM license compliance report feature (TC-9004). The Documentation Considerations section of the feature specifies "New Content" doc impact: compliance officers need to understand how to configure policies and interpret reports. Reference material includes the SPDX license list and existing package data model documentation.

## Acceptance Criteria
- [ ] API endpoint documentation covers the license report endpoint path, HTTP method, path parameters, response schema, and example response
- [ ] License policy configuration is documented: JSON config file format, allowlist/denylist modes, and how to customize for different compliance policies
- [ ] Documentation includes guidance for compliance officers on interpreting report results (what compliant/non-compliant flags mean)
- [ ] Documentation references the SPDX license list as the license identifier standard

## Test Requirements
- [ ] Verify documentation accurately reflects the implemented API endpoint path and response schema
- [ ] Verify license policy configuration examples match the actual JSON config format
- [ ] Verify documentation is consistent with the endpoint behavior implemented in Tasks 1-4

## Dependencies
- Depends on: Task 1 — Add license report model and policy configuration
- Depends on: Task 2 — Add license report service with transitive dependency resolution
- Depends on: Task 3 — Add license report endpoint and route registration
- Depends on: Task 4 — Add integration tests for license report endpoint
