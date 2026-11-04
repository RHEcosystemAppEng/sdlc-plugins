# Task 4 — Document license report endpoint and license policy configuration

**Feature**: TC-9004 · **Labels**: ai-generated-jira · **Priority**: Major · **Fix Versions**: RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
Document the license compliance report feature delivered by TC-9004.

**What changed**: a new endpoint, `GET /api/v2/sbom/{id}/license-report`, returns an SBOM's packages, transitive dependencies included, grouped by license, with each group flagged `compliant: true/false` against a configurable license policy. The policy is a JSON config file in the repository (default `license-policy.json`) with allowed and denied SPDX license identifiers. Licenses that are unlisted or missing are treated as non-compliant.

**Doc impact type**: New Content. Document the endpoint and the license policy configuration.

**Details from Documentation Considerations**:
- User purpose: compliance officers need to understand how to configure policies and interpret reports
- Reference material: SPDX license list, existing package data model documentation
- Customer considerations: the license policy configuration must be documented, and organizations may have different compliance policies, so show how to customize the policy

Cover: the endpoint request and response (including `404` for unknown SBOMs), the meaning of `compliant` and of the `NOASSERTION` group, the policy file format and location, how to supply a custom policy, and an example CI/CD gate (UC-2) that fails the build when any group has `compliant: false`.

Reference: Feature TC-9004.

## Acceptance Criteria
- [ ] Documentation describes `GET /api/v2/sbom/{id}/license-report`, its response shape, and its error responses, and matches the implemented behavior
- [ ] Documentation explains the license policy JSON format, default location, and how to configure a custom policy
- [ ] Documentation explains how to interpret the report (compliance flags, packages with unknown licenses, transitive dependencies)
- [ ] Documentation includes an example automated compliance gate for CI/CD pipelines
- [ ] Documentation references the SPDX license list for valid identifiers

## Test Requirements
- [ ] Verify the documented request and response examples match actual responses from the implemented endpoint
- [ ] Verify the documented policy format loads successfully with the implemented loader
- [ ] Verify the documented CI gate example correctly fails on a non-compliant report and passes on a compliant one

## Dependencies
- Depends on: Task 1 — Add license policy JSON config and loader
- Depends on: Task 2 — Add license report models and aggregation service
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint and integration tests
