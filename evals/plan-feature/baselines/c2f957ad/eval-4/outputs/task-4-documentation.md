**Summary:** TC-9004: Document license compliance report endpoint and policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Document the license compliance report feature delivered by TC-9004.

- **What changed:** a new endpoint `GET /api/v2/sbom/{id}/license-report` returns an SBOM's packages (including transitive dependencies) grouped by license, with a `compliant` flag per group computed from a configurable JSON license policy stored in the repository.
- **Doc impact type:** New Content — document the endpoint and the license policy configuration.
- **User purpose:** compliance officers need to understand how to configure policies and interpret reports; CI/CD users need to know how to gate builds on `compliant: false`.
- **Reference material:** SPDX license list; existing package data model documentation.
- **Customer considerations:** license policy configuration must be documented; organizations may have different compliance policies (cover how to supply a custom policy file).
- Feature reference: TC-9004.

## Acceptance Criteria
- [ ] Documentation describes the endpoint path, method, path parameter, response shape, and error responses (404 for unknown SBOM)
- [ ] Documentation explains the license policy file format (allowed/denied SPDX identifiers), its default location, and how to configure a custom path
- [ ] Documentation explains how unknown / missing licenses are treated (non-compliant)
- [ ] Documentation explains how to interpret the report and includes a CI/CD gating example (fail build when any group has `compliant: false`)
- [ ] Documentation references the SPDX license list for valid identifiers

## Test Requirements
- [ ] Verify the documented request/response examples match the implemented endpoint behavior
- [ ] Verify the documented policy file format matches the shipped `license-policy.json` and loader behavior
- [ ] Verify the CI/CD gating example works against a running instance

## Dependencies
- Depends on: Task 1 — Add configurable license compliance policy (JSON config + loader)
- Depends on: Task 2 — Implement license report model and service with transitive dependency walk
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
