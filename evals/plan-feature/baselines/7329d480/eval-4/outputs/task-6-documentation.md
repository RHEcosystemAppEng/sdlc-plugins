## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint and license policy configuration. This is new content covering the API endpoint usage, response format, policy file structure, and how to customize the license policy for different organizational requirements.

## Files to Create
- `docs/license-compliance.md` — Documentation for the license report endpoint and policy configuration

## Implementation Notes
- Document the `GET /api/v2/sbom/{id}/license-report` endpoint: URL, method, path parameters, response schema with example JSON output.
- Document the `config/license-policy.json` configuration file: structure, license categories (approved, restricted, prohibited), how to customize for different organizational policies, and the SPDX license identifier format.
- Include a usage example showing the automated compliance gate use case (CI/CD pipeline calling the endpoint and checking for `compliant: false` groups).
- Document the behavior for unknown licenses (not listed in policy) and the default-deny approach.
- Per CONVENTIONS.md §Module pattern: organize documentation consistent with the module structure and reference the relevant source paths. Applies: convention has no file-type restriction (broadly applicable).

## Acceptance Criteria
- [ ] Endpoint documentation covers URL, method, path parameters, and full response schema
- [ ] License policy configuration is documented with structure and customization instructions
- [ ] Example JSON response is included showing grouped licenses with compliance flags
- [ ] CI/CD integration use case is documented
- [ ] Unknown license handling behavior is documented

## Dependencies
- Depends on: Task 4 — License report endpoint

## additional_fields
```json
{ "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```
