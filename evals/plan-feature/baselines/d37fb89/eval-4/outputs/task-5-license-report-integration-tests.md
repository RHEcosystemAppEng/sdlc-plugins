## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint. Tests should cover the full request/response cycle against a real PostgreSQL test database, validating correct grouping, compliance flagging, transitive dependency inclusion, and error handling.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `tests/Cargo.toml` — Add any necessary test dependencies if not already present

## Implementation Notes
Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
- Tests hit a real PostgreSQL test database (not mocked)
- Use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern
- Set up test data by ingesting an SBOM with packages that have known licenses before calling the report endpoint
- Include packages with a mix of compliant and non-compliant licenses to test flagging
- Include packages with transitive dependencies to verify full dependency tree traversal

Test scenarios:
1. **Basic report**: Ingest SBOM with 3 packages (MIT, Apache-2.0, GPL-3.0), call report, verify grouping and compliance flags
2. **Transitive dependencies**: Ingest SBOM where package A depends on B which depends on C, verify C's license appears in the report
3. **All compliant**: Ingest SBOM with only permissive licenses, verify `non_compliant_count: 0`
4. **Non-existent SBOM**: Call report with invalid ID, verify 404 response
5. **Empty SBOM**: Ingest SBOM with no packages, verify empty report with zero counts
6. **CI/CD gate scenario**: Verify that a report with non-compliant licenses returns `compliant: false` on the relevant groups, enabling pipeline decisions

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration test patterns for test setup, database initialization, and assertion style
- `tests/api/advisory.rs` — additional reference for integration test structure and data setup

## Acceptance Criteria
- [ ] All 6 test scenarios pass against the PostgreSQL test database
- [ ] Tests validate response status codes (200, 404)
- [ ] Tests validate JSON response structure and field values
- [ ] Tests verify compliance flags match expected policy evaluation
- [ ] Tests verify transitive dependency licenses are included

## Test Requirements
- [ ] Integration test: basic report with mixed licenses produces correct grouping
- [ ] Integration test: transitive dependencies appear in report
- [ ] Integration test: all-compliant SBOM produces zero non-compliant count
- [ ] Integration test: non-existent SBOM returns 404
- [ ] Integration test: empty SBOM returns valid empty report
- [ ] Integration test: non-compliant licenses are flagged correctly for CI/CD gating

## Dependencies
- Depends on: Task 4 — Add license report endpoint and route registration

[sdlc-workflow] Description digest: sha256-md:212e514c28f0149f6bdd61cca23daaaa1211099d363cfdcb387833465e61946a
