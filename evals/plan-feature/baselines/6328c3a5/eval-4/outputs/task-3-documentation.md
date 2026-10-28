## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint and license policy configuration for feature TC-9004. The feature adds `GET /api/v2/sbom/{id}/license-report` which returns packages grouped by license type with compliance flags based on a configurable policy.

Documentation impact type: **New Content**

This documentation should help compliance officers understand how to:
- Call the license report endpoint and interpret the response
- Configure license policies to match their organization's compliance requirements
- Integrate the endpoint into CI/CD pipelines for automated compliance gating

Reference material: SPDX license list, existing package data model documentation.

Feature issue: TC-9004

## Acceptance Criteria
- [ ] Documentation covers the license report endpoint: path, HTTP method, path parameters, and complete response format with examples
- [ ] Documentation covers license policy configuration: JSON format, configuration file location, allowed/denied license list structure, and customization options
- [ ] Documentation explains how compliance flags are determined (allow-list vs deny-list approach)
- [ ] Documentation includes at least one example request/response pair
- [ ] Documentation references the SPDX license identifier list for valid license values
- [ ] Documentation describes the CI/CD integration use case (automated compliance gate)

## Test Requirements
- [ ] Verify documentation accurately describes the endpoint path and response format matching the implementation
- [ ] Verify policy configuration instructions are complete — a user can follow them to create a working policy file
- [ ] Verify response format examples in documentation match the actual API output
- [ ] Verify all documented configuration options are implemented and functional

## Dependencies
- Depends on: Task 1 — Add license policy configuration and compliance report domain model
- Depends on: Task 2 — Add license compliance report service and endpoint
