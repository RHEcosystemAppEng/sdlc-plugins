**Summary:** Add GET /api/v2/sbom/{id}/license-report endpoint and integration tests
**Epic:** TC-9004: License compliance report API
**Labels:** ai-generated-jira | **Priority:** Major | **Fix Versions:** RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
Expose the license compliance report (TC-9004) over HTTP so compliance officers (UC-1) and CI/CD pipelines (UC-2) can retrieve a structured report grouped by license with policy violation flags in a single API call.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/license-report` route
- `server/src/main.rs` — load the license policy at startup (via the Task 1 loader) and provide it to the SBOM module state; fail startup if the policy cannot be loaded

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — `GET /api/v2/sbom/{id}/license-report` handler calling `SbomService::license_report`
- `tests/api/license_report.rs` — integration tests for the endpoint

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `{ groups: [{ license: string, packages: PackageSummary[], compliant: boolean }] }`; 404 when the SBOM does not exist

## Implementation Notes
- Follow the existing handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`) — same path-parameter extraction, service injection, and response serialization.
- The response is a single structured object, not a paginated list — do not wrap it in `PaginatedResults<T>`.
- Endpoint is protected by the same authentication/authorization as the other `/api/v2/sbom` routes; do not add any unauthenticated route.
- **Fail-closed behavior (protects the UC-2 CI gate):** if the policy is unavailable, the endpoint must return a 5xx error — never a 200 with an empty `groups` array or all groups `compliant: true`. Implement by failing server startup in `server/src/main.rs` when the Task 1 loader errors, and by having the handler in `modules/fundamental/src/sbom/endpoints/license_report.rs` return `AppError` rather than a default report.
- Caching: if added, configure it in the route builder per the existing SBOM routes; the cache must not outlive policy changes (policy is loaded at startup, so a per-process cache is acceptable).
- Per CONVENTIONS.md §Endpoint registration: register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside `list.rs` and `get.rs`; `server/src/main.rs` already mounts the SBOM module.
  Applies: task modifies modules/fundamental/src/sbom/endpoints/mod.rs matching the convention's endpoint registration (`endpoints/*.rs`) scope.
- Per CONVENTIONS.md §Error handling: the handler returns `Result<Json<LicenseReport>, AppError>` with `.context()` wrapping; see `common/src/error.rs`.
  Applies: task modifies modules/fundamental/src/sbom/endpoints/license_report.rs matching the convention's Rust handler (`.rs`) scope.
- Per CONVENTIONS.md §Testing: integration tests go in `tests/api/` against the real PostgreSQL test database using the `assert_eq!(resp.status(), StatusCode::OK)` pattern; follow `tests/api/sbom.rs`.
  Applies: task modifies tests/api/license_report.rs matching the convention's integration test (`tests/api/*.rs`) scope.
- Per CONVENTIONS.md §Caching: any caching uses the `tower-http` caching middleware configured in the endpoint route builder, as in `modules/fundamental/src/sbom/endpoints/mod.rs`.
  Applies: task modifies modules/fundamental/src/sbom/endpoints/mod.rs matching the convention's route builder (`endpoints/*.rs`) scope.
- Applicable constraints (docs/constraints.md): §2 commit rules; §3 PR rules (`--base main`); §5 code change rules (5.1 scope, 5.6 data-flow trace, 5.8 sibling parity with `get.rs` for error handling/logging/auth, 5.11–5.13 test doc comments and given-when-then); §1.4/1.5.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — sibling `GET /api/v2/sbom/{id}` handler to mirror
- `tests/api/sbom.rs` — existing SBOM integration test setup (fixture ingestion, client, assertions)
- `common/src/error.rs::AppError` — maps not-found and internal errors to HTTP responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with `{ groups: [{ license, packages, compliant }] }` for an ingested SBOM
- [ ] Non-compliant license groups have `compliant: false`; compliant ones `compliant: true`
- [ ] Unknown SBOM ID returns 404
- [ ] The endpoint requires the same authentication as other `/api/v2/sbom` routes
- [ ] If the license policy cannot be loaded, the service does not serve 200/empty reports (startup fails or endpoint returns 5xx) — fail-closed
- [ ] p95 latency < 500ms for an SBOM with 1000 packages
- [ ] No other new endpoints are introduced

## Test Requirements
- [ ] Integration test: ingest a fixture SBOM with mixed licenses → 200, groups and `compliant` flags match the policy
- [ ] Integration test: transitive dependency package appears in the report
- [ ] Integration test (fail-closed): package without license → `UNKNOWN` group with `compliant: false` in the HTTP response
- [ ] Integration test: unknown SBOM ID → 404
- [ ] Integration test: unauthenticated request → rejected like other SBOM routes
- [ ] Test (fail-closed): invalid/missing policy configuration → server/state construction returns an error (no permissive default)
- [ ] Performance test or benchmark: 1000-package SBOM report completes within the 500ms p95 target

## Verification Commands
- `cargo test -p tests license_report` — integration tests pass
- `curl -H "Authorization: Bearer $TOKEN" http://localhost:8080/api/v2/sbom/<id>/license-report` — returns grouped JSON report

## Documentation Updates
- `README.md` — add a brief mention of the new license report endpoint and the `config/license-policy.json` file (full docs in Task 4)

## Dependencies
- Depends on: Task 2 — Add license report models and aggregation service
