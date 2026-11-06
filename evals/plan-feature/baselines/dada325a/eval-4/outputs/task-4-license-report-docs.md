## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report feature from TC-9004 ("Add license compliance report endpoint").

**What changed:** a new endpoint, `GET /api/v2/sbom/{id}/license-report`, returns the packages in an SBOM, including transitive dependencies, grouped by license. Each group has a `compliant` flag computed from a configurable license policy stored as a JSON config file (`license-policy.json`) in the repository.

**Doc impact type:** New Content. Document the endpoint and the license policy configuration.

**Details from Documentation Considerations:**
- User purpose: compliance officers need to understand how to configure policies and how to interpret reports
- Reference material: SPDX license list, existing package data model documentation
- Customer considerations: the license policy configuration must be documented, and organizations may have different compliance policies, so explain how to customize the allow/deny lists and the unknown-license behavior

Also cover the CI/CD compliance-gate use case (UC-2). Explain that a pipeline should fail when any group has `compliant: false`. Explain that the endpoint returns 404 for unknown SBOMs and reports packages without license data under a non-compliant `NOASSERTION` group, so these cases are not treated as passing.

Reference: TC-9004

## Acceptance Criteria
- [ ] The documentation describes `GET /api/v2/sbom/{id}/license-report`, including the path parameter, the response shape (`groups[].license`, `groups[].packages`, `groups[].compliant`), and the error responses (404 for unknown SBOM)
- [ ] The documentation explains the `license-policy.json` format (allowed list, denied list, `unknown_license` setting), where the file lives, and how to point the server at a custom policy
- [ ] The documentation explains how to interpret the report, including the `NOASSERTION` group and multi-licensed packages
- [ ] The documentation includes an example of using the endpoint as a CI/CD compliance gate
- [ ] The documentation references the SPDX license list for valid license identifiers

## Test Requirements
- [ ] Check that the documented endpoint path, response fields, and status codes match the implemented behavior from Tasks 1–3
- [ ] Check that the documented policy file format matches the `LicensePolicy` struct and the shipped default `license-policy.json`
- [ ] Check that the example requests/responses and the CI gate example are accurate when run against a running server

## Dependencies
- Depends on: Task 1 — Add configurable license policy and compliance evaluator
- Depends on: Task 2 — Implement license compliance report aggregation service
- Depends on: Task 3 — Expose GET /api/v2/sbom/{id}/license-report endpoint
