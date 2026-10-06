## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint and license policy configuration. The Feature's Documentation Considerations indicate **New Content** is needed:

- **Doc impact type:** New Content
- **User purpose:** Compliance officers need to understand how to configure license policies and interpret compliance reports
- **Reference material:** SPDX license list, existing package data model documentation

Documentation should cover:
1. The `GET /api/v2/sbom/{id}/license-report` endpoint — request format, response structure, and usage examples
2. The license policy configuration file — JSON schema, allowed/denied license lists, SPDX identifier format
3. How transitive dependency licenses are included in the report
4. How to integrate the endpoint into a CI/CD compliance gate

Reference feature: TC-9004

## Acceptance Criteria
- [ ] Endpoint documentation covers the request format (`GET /api/v2/sbom/{id}/license-report`) and response schema
- [ ] License policy configuration documentation explains the JSON structure and supported fields
- [ ] Documentation includes at least one example request and response
- [ ] SPDX license identifier format is referenced
- [ ] CI/CD integration use case is documented (automated compliance gate)
- [ ] Documentation is consistent with the implemented endpoint behavior

## Test Requirements
- [ ] Documentation accurately reflects the endpoint's actual request/response format
- [ ] Policy configuration examples are valid JSON that can be deserialized by the application
- [ ] All documented features match the implemented behavior from Tasks 1-4

## Dependencies
- Depends on: Task 4 — Add license report integration tests (documentation should be written after implementation is complete)
