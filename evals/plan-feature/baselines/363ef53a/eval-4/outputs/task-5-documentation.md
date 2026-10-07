## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint and license policy configuration for the license compliance report feature (TC-9004). The documentation should cover:

- The `GET /api/v2/sbom/{id}/license-report` endpoint: purpose, request format, response shape, and example responses
- License policy configuration: how to create and customize the `config/license-policy.json` file, available fields (allowed_licenses, denied_licenses), and how the policy affects compliance flags in the report
- Use cases: generating a compliance report for an SBOM, integrating the endpoint into CI/CD pipelines as a compliance gate

**Doc impact type:** New Content
**User purpose:** Compliance officers need to understand how to configure policies and interpret reports
**Reference material:** SPDX license list, existing package data model documentation

This documentation task was generated from the Documentation Considerations section of feature TC-9004.

## Acceptance Criteria
- [ ] The license report endpoint is documented with request/response examples
- [ ] The license policy configuration format is documented with field descriptions
- [ ] Use case examples are provided for manual compliance review and CI/CD integration
- [ ] Documentation references the SPDX license identifier standard for valid license values
- [ ] Documentation is consistent with the implemented endpoint behavior

## Test Requirements
- [ ] Verify the documented endpoint path and response shape match the actual implementation
- [ ] Verify the documented configuration file format matches the actual `config/license-policy.json` schema
- [ ] Verify all documented examples produce the expected results when tested against the running service

## Dependencies
- Depends on: Task 1 -- Add license policy configuration and report models
- Depends on: Task 2 -- Add license report service with dependency tree walking
- Depends on: Task 3 -- Add license report REST endpoint
- Depends on: Task 4 -- Add license report integration tests
