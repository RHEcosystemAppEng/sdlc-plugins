## Repository
trustify-backend

## Target Branch
main

## Description
Document the new license compliance report endpoint and license policy configuration. The Feature's Documentation Considerations section indicates **New Content** is needed: document the endpoint usage, response format, and how to configure license policies for compliance checking. This documentation supports compliance officers who need to understand how to configure policies and interpret reports.

## Acceptance Criteria
- [ ] Documentation covers the `GET /api/v2/sbom/{id}/license-report` endpoint: URL, method, path parameters, response schema
- [ ] Documentation explains the license policy configuration format (JSON structure with allowed, denied, and review lists)
- [ ] Documentation includes example request and response
- [ ] Documentation references the SPDX license list for valid license identifiers
- [ ] Documentation explains the compliance flag semantics (per-group and overall)

## Test Requirements
- [ ] Documentation accurately reflects the implemented API behavior
- [ ] Example request/response in documentation matches actual endpoint behavior
- [ ] License policy configuration format matches the implemented `LicensePolicy` struct

## Dependencies
- Depends on: Task 4 — License report endpoint
- Depends on: Task 5 — Integration tests
