**Summary:** Document license report endpoint and license policy configuration
**Epic:** TC-9004: License compliance documentation
**Labels:** ai-generated-jira | **Priority:** Major | **Fix Versions:** RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
Feature TC-9004 adds `GET /api/v2/sbom/{id}/license-report`, which returns an SBOM's packages (including transitive dependencies) grouped by license, each group flagged `compliant: true/false` against a configurable license policy stored as a JSON config file in the repository.

**Doc impact type:** New Content — document the endpoint and the license policy configuration.

**Details from Documentation Considerations:**
- User purpose: compliance officers need to understand how to configure policies and interpret reports.
- Reference material: SPDX license list; existing package data model documentation.

Content should cover: endpoint request/response format with an example; meaning of the `compliant` flag and the `UNKNOWN` group; policy file location, schema (`allowed`/`denied` SPDX IDs), default-deny semantics, and how to override the policy path; how to use the endpoint as a CI/CD compliance gate (UC-2: fail the build when any group has `compliant: false`); behavior when the policy is missing or invalid (fail-closed).

## Acceptance Criteria
- [ ] Documentation describes `GET /api/v2/sbom/{id}/license-report` request, response shape, and error responses (404, policy failure)
- [ ] Documentation explains the license policy file schema, default location, path override, and default-deny semantics with SPDX identifier references
- [ ] Documentation explains how to interpret `compliant` flags and the `UNKNOWN` group
- [ ] Documentation includes a CI/CD gate example
- [ ] Documentation matches the implemented behavior of Tasks 1–3

## Test Requirements
- [ ] Verify every documented field, path, and status code against the implemented endpoint and policy loader
- [ ] Verify the example policy file and example response are valid and reproducible against a running service
- [ ] Verify the documentation is complete for the scope in Documentation Considerations (endpoint + policy configuration)

## Dependencies
- Depends on: Task 1 — Add configurable license policy and loader
- Depends on: Task 2 — Add license report models and aggregation service
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint and integration tests
