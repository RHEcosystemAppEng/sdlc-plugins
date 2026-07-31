## Repository
trustify-backend

## Target Branch
main

## Priority
Major

## Fix Versions
RHTPA 1.5.0

## Description
Document the new `GET /api/v2/sbom/{id}/license-report` endpoint and the license policy configuration in the REST API reference. This covers endpoint usage, request/response format, license policy JSON schema, and configuration instructions for compliance officers.

## Acceptance Criteria
- [ ] REST API reference documents the `GET /api/v2/sbom/{id}/license-report` endpoint with request parameters and response schema
- [ ] License policy JSON configuration format is documented with examples of allow-list and deny-list policies
- [ ] Documentation includes example request and response payloads
- [ ] Error responses (404 for missing SBOM) are documented

## Test Requirements
- [ ] Documentation review confirms endpoint URL, method, and path parameters are accurate
- [ ] Documentation review confirms response schema matches the implemented `LicenseReport` structure
- [ ] Documentation review confirms license policy configuration examples are valid JSON

## Dependencies
- Depends on: Task 3 — Add license report endpoint
