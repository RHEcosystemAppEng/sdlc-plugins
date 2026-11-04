# Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint and integration tests

**Feature**: TC-9004 · **Labels**: ai-generated-jira · **Priority**: Major · **Fix Versions**: RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
Expose the license compliance report as `GET /api/v2/sbom/{id}/license-report` so compliance officers (UC-1) and CI/CD pipelines (UC-2) can get a grouped license report with policy violation flags in one call. The handler calls `SbomService::license_report` (Task 2) with the loaded `LicensePolicy` (Task 1) and returns the `LicenseReport` JSON.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/{id}/license-report` route in the existing `/api/v2/sbom` route builder and add the `LicensePolicy` state
- `server/src/main.rs` — load `LicensePolicy` at startup (fail startup if loading fails) and pass it into the SBOM module's router state
- `tests/api/sbom.rs` — integration tests for the new endpoint

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `200` with `{ groups: [{ license: string, packages: PackageSummary[], compliant: boolean }] }`; `404` when the SBOM does not exist

## Implementation Notes
- Follow the handler shape in `modules/fundamental/src/sbom/endpoints/get.rs` (path extraction of `{id}`, service call, `Result<Json<_>, AppError>`). Map `Ok(None)` from the service to the same not-found `AppError` variant `get.rs` uses.
- **Fail-closed gate (UC-2 CI gate)**: the endpoint must never return `200` with an empty or all-compliant report when it cannot actually evaluate the SBOM. An unknown SBOM returns `404`, and a DB failure returns `5xx` via `AppError`. A policy-load failure stops server startup in `server/src/main.rs` and must never become a permissive default. The guards belong in `license_report.rs` (handler) and in the policy wiring in `server/src/main.rs`.
- Caching: the report depends on mutable ingestion data and on the policy. Configure the `tower-http` caching for this route in the route builder in `endpoints/mod.rs` so a stale report is not served after re-ingestion (no-cache, or short-lived and consistent with how `get.rs` is configured).
- Register only the `/{id}/license-report` route. Add no other routes in this change (in particular no debug, exec, eval, or admin endpoints).
- Performance: the endpoint must meet p95 < 500ms for SBOMs with up to 1000 packages. Rely on the single-query aggregation from Task 2.
- Per CONVENTIONS.md §Endpoint registration: register the route in the module's `endpoints/mod.rs`; `server/src/main.rs` mounts modules. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope. Example: existing `list`/`get` registration in `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Per CONVENTIONS.md §Error handling: the handler returns `Result<T, AppError>` with `.context()`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust handler scope. Example: `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Testing: integration tests go in `tests/api/` against the real PostgreSQL test DB using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/sbom.rs` matching the convention's integration test scope. Example: existing tests in `tests/api/sbom.rs`.
- Per CONVENTIONS.md §Caching: cache configuration lives in the endpoint route builders. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's route builder scope. Example: `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Constraints (docs/constraints.md): §2.1–2.3, §3.1–3.3, §5.1–5.4, §5.6 (trace the request → service → response lifecycle end to end), §5.8 (parity with the sibling `get.rs` handler on error handling and caching), §5.11–5.12 (doc comments and given-when-then comments on tests).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — handler pattern for `/api/v2/sbom/{id}`, including not-found handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route builder and caching configuration to extend
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::license_report` (from Task 2) — report generation
- `tests/api/sbom.rs` — existing SBOM integration test setup and fixtures (SBOM ingestion helpers)

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns `200` with `{ groups: [{ license, packages, compliant }] }` for an ingested SBOM
- [ ] Non-compliant licenses under the configured policy are returned with `compliant: false`
- [ ] Transitive dependency packages appear in the report
- [ ] A nonexistent SBOM id returns `404`, never `200` with empty groups (fail closed)
- [ ] The server refuses to start when the license policy cannot be loaded (fail closed)
- [ ] The route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`, and existing `/api/v2/sbom` routes are unchanged
- [ ] No other new routes are added (no debug, exec, eval, or admin endpoints)
- [ ] p95 response time < 500ms for an SBOM with 1000 packages

## Test Requirements
- [ ] Integration test: an ingested SBOM with mixed licenses returns `200` and the expected groups and flags
- [ ] Integration test: an SBOM whose licenses are all allowed returns every group with `compliant: true`
- [ ] Integration test: transitive dependency packages are present in the response
- [ ] Integration test (fail-closed): an unknown SBOM id returns `404`
- [ ] Integration test (fail-closed): a package without license data is reported in a group with `compliant: false`
- [ ] Integration test: the response JSON shape matches `{ groups: [{ license, packages, compliant }] }`
- [ ] Performance check: an SBOM fixture with 1000 packages is generated within the 500ms budget (benchmark or timed test)

## Verification Commands
- `cargo test --test api sbom` — SBOM integration tests, the new license-report tests included, pass
- `curl -s http://localhost:8080/api/v2/sbom/<id>/license-report | jq '.groups[] | {license, compliant}'` — returns grouped licenses with compliance flags
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/api/v2/sbom/does-not-exist/license-report` — returns `404`

## Documentation Updates
- `README.md` — add the new endpoint to the API overview (full docs are in Task 4)

## Dependencies
- Depends on: Task 2 — Add license report models and aggregation service
