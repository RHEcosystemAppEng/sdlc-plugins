## Repository
trustify-backend

## Target Branch
main

## Description
Expose the SBOM license compliance report via a new REST endpoint `GET /api/v2/sbom/{id}/license-report` (TC-9004). The handler loads the license policy, calls `SbomService::license_report`, and returns the grouped report as JSON. This satisfies UC-1 (compliance officer report) and UC-2 (CI/CD pipeline gate checking for `compliant: false`).

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/license-report` route alongside existing SBOM routes
- `tests/api/sbom.rs` — add integration tests for the new endpoint

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — `GET /api/v2/sbom/{id}/license-report` handler

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `{ "groups": [ { "license": "<SPDX id>", "packages": [PackageSummary...], "compliant": <bool> } ] }`; 404 when the SBOM does not exist; 500 when the license policy cannot be loaded

## Implementation Notes
- Model the handler on `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`): same path-parameter extraction, service injection, and `Result<Json<_>, AppError>` return type.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` next to the existing `get` route. The SBOM router is already mounted by `server/src/main.rs`, so no change to the server is required.
- The response is a single report object, not a list — do not wrap it in `PaginatedResults<T>`.
- Load `LicensePolicy` (Task 1) once at router construction / application state and share it with the handler; a policy load failure must surface as an error response, never as an all-compliant report (fail-closed for the UC-2 CI gate).
- Per CONVENTIONS.md §Endpoint registration: register the new route in the SBOM module's `endpoints/mod.rs`. Applies: task modifies modules/fundamental/src/sbom/endpoints/mod.rs matching the convention's `endpoints/mod.rs` route registration scope. Example: existing `get` route registration in `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Per CONVENTIONS.md §Error handling: the handler returns `Result<T, AppError>` with `.context()` wrapping. Applies: task creates modules/fundamental/src/sbom/endpoints/license_report.rs matching the convention's Rust handler (`.rs`) scope. Example: `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Caching: configure caching for the new route in the route builder consistently with the existing SBOM detail route; keep cache lifetime short or disabled so policy changes are reflected. Applies: task modifies modules/fundamental/src/sbom/endpoints/mod.rs matching the convention's endpoint route builder scope. Example: route builder in `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/` against the PostgreSQL test database using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies tests/api/sbom.rs matching the convention's `tests/api/` integration test scope. Example: existing tests in `tests/api/sbom.rs`.
- Constraints (docs/constraints.md): Conventional Commits with Jira footer and `Assisted-by: Claude Code` trailer (§2.1–2.3); PR `--base main`, link posted to Jira (§3.2–3.3); scope to listed files, inspect before modifying, no duplicated logic (§5.1–5.4); compare the new handler against sibling SBOM handlers for parity in error handling, logging, and caching (§5.8); test functions get doc comments and given-when-then comments where non-trivial (§5.11–5.12).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing `GET /api/v2/sbom/{id}` handler; template for path extraction and error mapping
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing SBOM route registration and caching configuration
- `tests/api/sbom.rs` — existing SBOM integration test setup/fixtures

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with the documented `groups` JSON shape for an existing SBOM
- [ ] Non-compliant license groups are returned with `compliant: false`
- [ ] Unknown SBOM id returns 404
- [ ] Policy load failure returns an error status (5xx), never a 200 with all groups compliant (fail-closed)
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`; no other new routes are added
- [ ] p95 response time < 500ms for an SBOM with 1000 packages

## Test Requirements
- [ ] Integration test: 200 and correct grouping for an ingested SBOM with mixed licenses
- [ ] Integration test: denied license group has `compliant: false` (UC-2 gate condition)
- [ ] Integration test: unknown SBOM id returns 404
- [ ] Integration test: missing/invalid policy configuration yields an error response rather than an all-compliant 200 (fail-closed path)
- [ ] Integration test: package without license data is reported in a non-compliant unknown group
- [ ] Performance test: SBOM with 1000 packages completes within the 500ms p95 budget

## Verification Commands
- `cargo test -p tests sbom` — SBOM integration tests, including license-report tests, pass
- `curl -s http://localhost:8080/api/v2/sbom/<id>/license-report | jq '.groups[] | {license, compliant}'` — returns grouped licenses with compliance flags

## Documentation Updates
- `README.md` — mention the new license report endpoint and the `license-policy.json` configuration file

## Dependencies
- Depends on: Task 2 — License report aggregation service
