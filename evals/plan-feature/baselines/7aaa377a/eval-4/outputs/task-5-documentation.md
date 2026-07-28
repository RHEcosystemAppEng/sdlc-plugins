# Task 5 — Document license compliance report endpoint and policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Document the new `GET /api/v2/sbom/{id}/license-report` endpoint and the license policy configuration system. The feature's Documentation Considerations specify "New Content" doc impact: compliance officers need to understand how to configure license policies and interpret the compliance report output.

Documentation should cover:
- The license report endpoint: path, method, request parameters, response shape, and example responses
- The license policy configuration: file format, location, how to define allowed/denied licenses using SPDX identifiers
- Use cases: generating a one-click compliance audit, integrating with CI/CD pipelines for automated compliance gates

**Doc impact type:** New Content
**User purpose:** Compliance officers need to understand how to configure policies and interpret reports
**Reference material:** SPDX license list, existing package data model documentation
**Feature reference:** TC-9004

## Acceptance Criteria
- [ ] Endpoint documentation includes the path, HTTP method, request parameters, and complete response schema
- [ ] At least one example request/response pair is included
- [ ] License policy configuration documentation explains the JSON config format, file location, and how to define rules
- [ ] Documentation covers both the one-click audit use case (UC-1) and the CI/CD pipeline integration use case (UC-2)
- [ ] Documentation references the SPDX license list for valid license identifiers

## Test Requirements
- [ ] Documentation accurately reflects the implemented endpoint behavior
- [ ] Example request/response pairs are valid and match the actual API response shape
- [ ] License policy configuration examples are valid JSON that can be loaded by the policy loader
- [ ] All referenced paths and configuration file locations are correct

## Dependencies
- Depends on: Task 3 -- Add GET /api/v2/sbom/{id}/license-report endpoint
- Depends on: Task 4 -- Add integration tests for license report endpoint
