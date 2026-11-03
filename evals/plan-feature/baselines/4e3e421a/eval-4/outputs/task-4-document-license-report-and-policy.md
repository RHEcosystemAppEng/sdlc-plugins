## Repository
trustify-backend

## Target Branch
main

## Description
Document the new SBOM license compliance report capability delivered by TC-9004.

- **What changed:** a new endpoint `GET /api/v2/sbom/{id}/license-report` returns all packages of an SBOM (including transitive dependencies) grouped by license, with a `compliant` flag per group derived from a configurable JSON license policy (`license-policy.json`).
- **Doc impact type:** New Content — document the endpoint and the license policy configuration.
- **User purpose:** compliance officers need to understand how to configure policies and interpret reports; CI/CD maintainers need to know how to gate builds on `compliant: false`.
- **Reference material:** SPDX license list; existing package data model documentation.
- **Feature reference:** TC-9004.

Content to cover: endpoint path, parameters, response shape and status codes (200/404/5xx); policy file format (`allowed`/`denied` SPDX identifiers), location and how to override it; default-deny semantics for unlisted and unknown (`NOASSERTION`) licenses; an example CI gate that fails the build when any group has `compliant: false`.

## Acceptance Criteria
- [ ] Documentation describes `GET /api/v2/sbom/{id}/license-report`, its response shape, and status codes accurately
- [ ] Documentation explains the license policy file format, location, and override mechanism
- [ ] Documentation explains how compliance flags are computed, including default-deny for unknown licenses
- [ ] Documentation includes a CI/CD gate example matching UC-2
- [ ] Documentation references the SPDX license list

## Test Requirements
- [ ] Verify every documented field, status code, and config key matches the implemented behavior
- [ ] Verify the example request and CI gate snippet work against a running instance
- [ ] Verify the documentation covers all items listed under Documentation Considerations in TC-9004

## Dependencies
- Depends on: Task 1 — License policy configuration and report model
- Depends on: Task 2 — License report aggregation service
- Depends on: Task 3 — License report REST endpoint
