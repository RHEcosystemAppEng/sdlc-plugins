**Summary:** TC-9004: Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Expose the license compliance report via a new REST endpoint `GET /api/v2/sbom/{id}/license-report` (TC-9004). The endpoint calls `SbomService::license_report` (Task 2) with the loaded `LicensePolicy` (Task 1) and returns `{ groups: [{ license, packages, compliant }] }`. This enables compliance officers (UC-1) and CI/CD pipelines (UC-2) to retrieve the report in a single call.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/license-report` route
- `server/src/main.rs` — load the `LicensePolicy` at startup (configurable path, default `license-policy.json`) and make it available to handlers as shared state; fail startup if the policy cannot be loaded
- `tests/api/sbom.rs` — add integration tests for the new endpoint

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — handler for `GET /api/v2/sbom/{id}/license-report`

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `{ groups: [{ license: string, packages: PackageSummary[], compliant: boolean }] }`; 404 when the SBOM does not exist

## Implementation Notes
- Model the handler on `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`): same path-param extraction, service injection, and `Result<Json<_>, AppError>` return.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` next to the existing `list`/`get` routes; `server/src/main.rs` already mounts the SBOM module, so only shared-state wiring for the policy is needed there.
- The endpoint uses the existing authentication/authorization applied to the `/api/v2/sbom` routes — do not add any unauthenticated, debug, or internal routes.
- The response is a single report object, not a list, so it does not use `PaginatedResults<T>`.
- **Fail-closed gate (UC-2):** the handler MUST propagate the not-found error as HTTP 404 and policy/DB errors as 5xx — never return `200` with `{ groups: [] }` for a missing SBOM or a failed aggregation. Guard site: handler in `modules/fundamental/src/sbom/endpoints/license_report.rs`; startup guard for a missing/invalid policy in `server/src/main.rs`.
- Caching: if the SBOM `get` route builder applies `tower-http` caching middleware, apply equivalent configuration here (SBOM contents are immutable after ingestion), but ensure policy changes take effect on restart.
- Per CONVENTIONS.md §Endpoint registration: register the route in the module's `endpoints/mod.rs`; `server/src/main.rs` mounts modules.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Error handling: handler returns `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's handler (`.rs`) scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/sbom.rs` matching the convention's `tests/api/` integration-test scope.
- Commit rules (docs/constraints.md §2), PR rules (§3: `--base main`), code change rules (§5) apply.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing `GET /api/v2/sbom/{id}` handler; template for path extraction and error mapping
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing SBOM route registration
- `tests/api/sbom.rs` — existing SBOM integration tests and fixtures for ingesting a test SBOM

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with `{ groups: [{ license, packages, compliant }] }` for an ingested SBOM
- [ ] Non-compliant license groups are returned with `compliant: false`
- [ ] Unknown SBOM ID returns 404 (not 200 with empty groups)
- [ ] Server fails to start (clear error) when the configured policy file is missing or invalid
- [ ] The endpoint is protected by the same auth as other `/api/v2/sbom` routes
- [ ] p95 latency < 500ms for SBOMs with up to 1000 packages

## Test Requirements
- [ ] Integration test: ingest a test SBOM, call the endpoint, assert 200 and expected groups
- [ ] Integration test: SBOM containing a denied license yields a group with `compliant: false`
- [ ] Integration test: transitive dependency licenses appear in the response
- [ ] Integration test: unknown SBOM ID returns 404 (fail-closed; asserts body is not an empty compliant report)
- [ ] Integration test: unauthenticated request is rejected consistently with other SBOM routes

## Verification Commands
- `cargo test --workspace --test api sbom` — SBOM integration tests pass
- `curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8080/api/v2/sbom/<id>/license-report` — returns JSON with a `groups` array

## Documentation Updates
- `README.md` — mention the new license report endpoint and the license policy configuration option

## Dependencies
- Depends on: Task 1 — Add configurable license compliance policy (JSON config + loader)
- Depends on: Task 2 — Implement license report model and service with transitive dependency walk
