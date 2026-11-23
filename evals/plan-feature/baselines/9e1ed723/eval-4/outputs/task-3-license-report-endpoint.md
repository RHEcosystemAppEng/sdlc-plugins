## Repository
trustify-backend

## Target Branch
main

## Description
Expose the license compliance report for TC-9004 as `GET /api/v2/sbom/{id}/license-report`. The endpoint calls `SbomService::license_report` (Task 2) with the configured `LicensePolicy` (Task 1) and returns `{ groups: [{ license, packages, compliant }] }`, enabling compliance officers (UC-1) and CI/CD pipelines (UC-2) to retrieve a structured report in a single call.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/{id}/license-report` route under `/api/v2/sbom`
- `tests/api/sbom.rs` — integration tests for the new endpoint

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `{ groups: [{ license: string, packages: PackageSummary[], compliant: bool }] }`; 404 when the SBOM does not exist

## Implementation Notes
- Follow the handler style of `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`): extract the path ID, call the service, return `Result<Json<LicenseReport>, AppError>`.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing `list.rs` and `get.rs` routes; `server/src/main.rs` already mounts the SBOM module, so no new mount is needed.
- This is a single-resource report, not a list endpoint — do not wrap it in `PaginatedResults<T>`.
- Caching: if `tower-http` caching is applied in the SBOM route builder, ensure the report response is not cached beyond SBOM/policy changes (prefer no caching or a short TTL).
- **Fail-closed response (gate site: handler in `modules/fundamental/src/sbom/endpoints/license_report.rs`)**: errors from the service or policy (unknown SBOM, policy unavailable, query failure) must map to non-2xx responses via `AppError`; the handler must never convert an error into `200 OK` with `groups: []`, since UC-2 pipelines would treat that as compliant.
- The endpoint uses the same authentication/authorization as other `/api/v2/sbom` routes — do not add auth bypasses or alternative auth schemes.
- Per CONVENTIONS.md §Endpoint registration: register the route in the module's `endpoints/mod.rs`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `modules/*/src/*/endpoints/` directory scope.
- Per CONVENTIONS.md §Error handling: handler returns `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust handler source scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` against the PostgreSQL test database using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/sbom.rs` matching the convention's `tests/api/` integration test scope.
- Constraints (docs/constraints.md): commits must reference the Jira task in the footer, follow Conventional Commits, and include an `Assisted-by:` trailer (§2.1–2.3); PR must target `--base main` and its link must be posted on the Jira task (§3.2–3.3); changes must stay within Files to Modify / Files to Create, inspect code before modifying, reuse existing utilities, and match sibling endpoints on error handling and auth (§5.1–5.8).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — sibling `GET /api/v2/sbom/{id}` handler; same path extraction and error mapping
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration for `/api/v2/sbom`
- `tests/api/sbom.rs` — existing SBOM integration test setup and fixtures

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with `{ groups: [{ license, packages, compliant }] }` for an ingested SBOM
- [ ] Groups with policy-violating licenses have `compliant: false`
- [ ] Unknown SBOM ID returns 404, not 200 with empty groups
- [ ] Service/policy failures return a non-2xx error response, never `200` with `groups: []`
- [ ] The endpoint is protected by the same authentication as other `/api/v2/sbom` routes

## Test Requirements
- [ ] Integration test: ingest an SBOM with mixed licenses, call the endpoint, assert 200 and correct grouping/compliance flags
- [ ] Integration test: SBOM containing a denied license yields at least one group with `compliant: false` (UC-2 gate scenario)
- [ ] Integration test (fail-closed): unknown SBOM ID returns 404 and no `groups` body
- [ ] Integration test (fail-closed): a package lacking license data is present in the response under `NOASSERTION` with `compliant: false`
- [ ] Integration test: unauthenticated request is rejected the same way as `GET /api/v2/sbom/{id}`

## Verification Commands
- `cargo test --test api sbom` — SBOM API integration tests pass, including license-report tests
- `curl -s http://localhost:8080/api/v2/sbom/<id>/license-report | jq '.groups[] | {license, compliant}'` — lists license groups with compliance flags

## Documentation Updates
- `README.md` — list the new `GET /api/v2/sbom/{id}/license-report` endpoint

## Dependencies
- Depends on: Task 1 — Add configurable license compliance policy
- Depends on: Task 2 — Implement license report aggregation service
