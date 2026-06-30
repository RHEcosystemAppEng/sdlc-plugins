## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add integration tests for the SBOM comparison endpoint. Tests exercise the full request lifecycle through the Axum server against a real PostgreSQL test database, covering success cases, error cases, and edge cases like identical SBOMs and large package sets. These tests follow the existing integration test patterns in `tests/api/`.

## Files to Create
- `tests/api/sbom_compare.rs` — Integration tests for `GET /api/v2/sbom/compare`

## Files to Modify
- `tests/Cargo.toml` — Add test module reference if needed (depends on test harness configuration)

## Implementation Notes
Follow the integration test pattern in `tests/api/sbom.rs`. Tests should:

1. Set up test data: ingest two SBOMs with known package sets via `IngestorService` from `modules/ingestor/src/service/mod.rs`
2. Make HTTP requests to `GET /api/v2/sbom/compare?left={id1}&right={id2}` using the test HTTP client
3. Assert response status codes and JSON body structure using `assert_eq!(resp.status(), StatusCode::OK)` pattern
4. Parse response JSON into `SbomComparison` to verify field values

Test cases to implement:
- **Happy path**: Two SBOMs with overlapping but different package sets; verify all six diff categories
- **Identical SBOMs**: Same SBOM ID for left and right; all diff vectors should be empty
- **Missing SBOM**: Non-existent ID returns 404
- **Missing parameters**: Omit `left` or `right` query param, expect 400
- **Vulnerability diff**: Two SBOMs where the right has a package with a linked advisory not in the left; verify `new_vulnerabilities` is populated
- **License change**: Package with different license between SBOMs; verify `license_changes`

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/sbom_compare.rs` matching the convention's `tests/api/` directory scope.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for SBOM endpoint test setup and assertion patterns
- `tests/api/advisory.rs` — reference for advisory-related test data setup
- `modules/ingestor/src/service/mod.rs::IngestorService` — for ingesting test SBOMs and advisories

## Acceptance Criteria
- [ ] Integration tests cover: happy path, identical SBOMs, missing SBOM 404, missing params 400, vulnerability diff, license changes
- [ ] All tests pass against a real PostgreSQL test database
- [ ] Tests follow existing patterns in `tests/api/sbom.rs`

## Test Requirements
- [ ] All listed test cases are implemented and passing
- [ ] Tests are isolated and do not depend on external state or ordering

## Verification Commands
- `cargo test --test api -- sbom_compare` — all integration tests pass
- `cargo test --test api` — full API test suite still passes (no regressions)

## Dependencies
- Depends on: Task 1 — create-branch
- Depends on: Task 4 — backend-comparison-endpoint

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

[sdlc-workflow] Description digest: sha256-md:2878252a481b1716b2cd81e9a9adb134dd75648b6110f60d65f98b885d7d9381
