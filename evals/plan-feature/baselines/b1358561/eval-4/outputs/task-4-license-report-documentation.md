## Repository
trustify-backend

## Target Branch
main

## Description
Document the license compliance report feature from TC-9004.

**Doc impact type:** New Content. Document the endpoint and how to configure the license policy.

**What changed:** a new endpoint, `GET /api/v2/sbom/{id}/license-report`, returns an SBOM's packages grouped by license, including transitive dependencies, with a `compliant` flag per group. Compliance is evaluated against a configurable JSON license policy stored in the repository (default `config/license-policy.json`).

**Details from Documentation Considerations:**
- User purpose: compliance officers need to understand how to configure policies and interpret reports.
- Reference material: SPDX license list, existing package data model documentation.
- Customer considerations: the license policy configuration must be documented, and organizations may have different compliance policies, so the docs should show how to customize the allow list, deny list, and default decision.

The documentation should cover:
- The endpoint request and response shape, with example output
- The policy file format (`allowed`, `denied`, `default`) and how to point the server at a custom policy file
- How unknown or missing licenses are treated (fail-closed by default)
- How to use the endpoint as an automated CI/CD compliance gate (UC-2): fail the build when any group has `compliant: false`, and treat non-200 responses as failures

Reference: TC-9004.

## Acceptance Criteria
- [ ] The documentation describes `GET /api/v2/sbom/{id}/license-report`, its response shape, and its error responses (404 for an unknown SBOM)
- [ ] The documentation explains the license policy file format and how to customize it, with SPDX identifiers
- [ ] The documentation explains how to interpret the `compliant` flag, including the default treatment of unknown/NOASSERTION licenses
- [ ] The documentation includes a CI/CD gate example that fails on `compliant: false` and on non-200 responses
- [ ] The documentation matches the implemented behavior

## Test Requirements
- [ ] Verify the example request and response in the docs against a running server built from the implementation tasks
- [ ] Verify the documented policy file format matches what `LicensePolicy::load` accepts (load the documented example successfully)
- [ ] Verify the CI gate example exits non-zero for a report that contains a non-compliant group

## Dependencies
- Depends on: Task 1 — Add configurable license compliance policy
- Depends on: Task 2 — Implement license report aggregation service
- Depends on: Task 3 — Add license report REST endpoint
