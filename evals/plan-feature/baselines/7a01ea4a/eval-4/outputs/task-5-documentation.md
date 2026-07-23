# Task 5 — Document license report endpoint and policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Document the new `GET /api/v2/sbom/{id}/license-report` endpoint and the license policy configuration for compliance officers and API consumers. The Feature description's Documentation Considerations section specifies this is **New Content** — new documentation pages or sections are needed.

**Doc impact type**: New Content

**User purpose**: Compliance officers need to understand how to configure license policies and interpret the compliance report output.

**Reference material**: SPDX license list, existing package data model documentation.

Documentation should cover:
- The license report endpoint (path, method, request parameters, response shape with examples)
- The license policy configuration file format (JSON schema, allowed/denied lists, default disposition)
- How compliance flags are determined
- Use cases: manual compliance audit and CI/CD pipeline integration
- Reference to the SPDX license identifier standard

## Acceptance Criteria
- [ ] Documentation accurately reflects the implemented endpoint behavior
- [ ] License policy configuration format is fully documented with example JSON
- [ ] Response shape is documented with a realistic example showing compliant and non-compliant groups
- [ ] CI/CD integration use case is documented with example pipeline steps
- [ ] SPDX license identifier convention is referenced

## Test Requirements
- [ ] Documentation is accurate and consistent with the implemented feature behavior
- [ ] All endpoint paths, request parameters, and response shapes match the actual implementation
- [ ] Example JSON in the documentation is valid and parses correctly
- [ ] Policy configuration example is complete and usable as a starting point

## Dependencies
- Depends on: Task 1 — Add license policy configuration file and loader
- Depends on: Task 2 — Create license report model structs and service with transitive dependency resolution
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
- Depends on: Task 4 — Add integration tests for license report endpoint
