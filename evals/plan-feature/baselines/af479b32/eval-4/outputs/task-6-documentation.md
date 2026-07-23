# Task 6 — Document license report endpoint and policy configuration

**Summary:** Document the license report endpoint and license policy configuration

**Epic:** TC-9004: Documentation

## Repository
trustify-backend

## Target Branch
main

## Description
Create documentation for the new license compliance report feature. The Feature's Documentation Considerations indicate **New Content** is needed: compliance officers need to understand how to configure license policies and interpret compliance reports.

Documentation should cover:
- The `GET /api/v2/sbom/{id}/license-report` endpoint: request format, response shape, status codes, and usage examples
- The license policy configuration: JSON config file format, how to customize allowed/denied license lists, deny-by-default behavior
- Reference to the SPDX license list for valid license identifiers
- Integration with CI/CD pipelines for automated compliance gates (UC-2 from the feature description)

**Doc impact type:** New Content
**Feature reference:** TC-9004

## Acceptance Criteria
- [ ] Documentation accurately describes the license report endpoint request and response format
- [ ] Documentation explains the license policy JSON configuration file format with examples
- [ ] Documentation describes the deny-by-default compliance behavior
- [ ] Documentation includes at least one example of calling the endpoint and interpreting the response
- [ ] Documentation references the SPDX license list for valid identifiers

## Test Requirements
- [ ] Verify the documentation is accurate and consistent with the implemented endpoint behavior
- [ ] Verify all example requests and responses are valid
- [ ] Verify the policy configuration examples are parseable JSON

## Dependencies
- Depends on: Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint
- Depends on: Task 2 — Add license policy configuration and loader
