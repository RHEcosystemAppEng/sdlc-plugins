## Repository
trustify-backend

## Target Branch
main

## Description
Document the license compliance report feature delivered by TC-9004.

**Doc impact type:** New Content. Document the endpoint and the license policy configuration.

What changed:
- New endpoint `GET /api/v2/sbom/{id}/license-report`. It returns the packages in an SBOM, including transitive dependencies, grouped by license, with a `compliant` flag on each group.
- New JSON license policy file (`license-policy.json`) that declares allowed and denied SPDX licenses and how unknown licenses are treated. Its path is configurable.

Details from the Documentation Considerations section:
- **User purpose:** compliance officers need to understand how to configure policies and interpret reports.
- **Reference material:** SPDX license list, existing package data model documentation.
- **Customer considerations:** organizations may have different compliance policies, so the documentation must explain how to customize the policy.

The documentation should also cover how to use the report as a CI/CD gate (UC-2): fail the build when any group has `compliant: false`. It must state that unknown or missing licenses are non-compliant by default and that a nonexistent SBOM returns 404.

Reference: Feature TC-9004.

## Acceptance Criteria
- [ ] The documentation describes the endpoint path, method, auth requirement, response schema, and error responses (404)
- [ ] The documentation describes the license policy file format, its default location, how to override the path, and the allow/deny/unknown semantics
- [ ] The documentation explains how to interpret the report, including the `UNKNOWN` group and the `compliant` flag
- [ ] The documentation includes a CI/CD gate example
- [ ] The documentation references the SPDX license list for valid identifiers

## Test Requirements
- [ ] Check that the documented request and response examples match the actual endpoint output
- [ ] Check that the documented policy file example parses and is accepted by the loader
- [ ] Check that the documented defaults (unknown is non-compliant, 404 behavior) match the implemented behavior

## Dependencies
- Depends on: Task 1 — Add configurable license policy and evaluator
- Depends on: Task 2 — Implement license report aggregation service
- Depends on: Task 3 — Add license report endpoint and integration tests
