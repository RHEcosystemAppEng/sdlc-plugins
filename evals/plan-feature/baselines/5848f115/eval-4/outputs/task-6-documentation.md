# Task 6 -- Add documentation for license report endpoint and policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Add documentation for the new license compliance report feature. The Feature description's Documentation Considerations section indicates **New Content** is needed: document the `GET /api/v2/sbom/{id}/license-report` endpoint and the license policy configuration mechanism.

**Doc impact type:** New Content

**Details from Documentation Considerations:**
- User purpose: Compliance officers need to understand how to configure license policies and interpret compliance reports
- Reference material: SPDX license list, existing package data model documentation
- The endpoint and policy configuration format should be documented for both API consumers and administrators

**Source:** Feature TC-9004, Documentation Considerations section

## Acceptance Criteria
- [ ] Documentation accurately describes the `GET /api/v2/sbom/{id}/license-report` endpoint, its request parameters, and response shape
- [ ] Documentation explains the license policy configuration format (JSON file structure, allowed/denied lists, default policy behavior)
- [ ] Documentation includes examples of policy configuration for common scenarios
- [ ] Documentation explains how compliance flags are determined (policy evaluation logic)
- [ ] Documentation references the SPDX license list for valid license identifiers
- [ ] Documentation covers the automated compliance gate use case (CI/CD pipeline checking for non-compliant licenses)

## Test Requirements
- [ ] Verify documentation accurately reflects the implemented endpoint behavior
- [ ] Verify example policy configurations are valid JSON that can be deserialized by the LicensePolicy model
- [ ] Verify documented response shapes match the actual API response
- [ ] Verify all documented endpoints and parameters exist in the implementation

## Dependencies
- Depends on: Task 4 -- Add license report endpoint (documentation should reflect the final implemented API)
- Depends on: Task 5 -- Add integration tests for license report endpoint (tests validate the behavior documented)
