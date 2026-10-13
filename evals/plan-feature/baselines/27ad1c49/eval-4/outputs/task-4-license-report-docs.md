## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint and the license policy configuration. This covers API usage for compliance officers and CI/CD pipeline integration, as well as how to configure the license policy JSON file.

## Files to Modify
- `README.md` — add a section documenting the license report endpoint (request/response format, example usage) and license policy configuration (JSON schema, allowed/denied license lists, file location)

## Documentation Updates
- `README.md` — add "License Compliance Report" section covering:
  - Endpoint: GET /api/v2/sbom/{id}/license-report
  - Response format with example JSON
  - License policy configuration file format and location
  - Usage for CI/CD compliance gates (checking `compliant: false`)

## Acceptance Criteria
- [ ] README documents the GET /api/v2/sbom/{id}/license-report endpoint
- [ ] README documents the license policy JSON configuration format
- [ ] README includes example response payload
- [ ] README includes guidance for CI/CD pipeline integration

## Dependencies
- Depends on: Task 3 — Add license report endpoint and route registration
