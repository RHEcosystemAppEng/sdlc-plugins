## Repository
trustify-backend

## Target Branch
main

## Description
Expose the TC-9004 license compliance report over HTTP at `GET /api/v2/sbom/{id}/license-report`. The handler loads the shared `LicensePolicy` (Task 1) from application state, calls the report service (Task 2), and returns the grouped report as JSON. Compliance officers (UC-1) and CI/CD pipelines (UC-2) use this endpoint to find and block non-compliant licenses.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — `GET /api/v2/sbom/{id}/license-report` handler

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/{id}/license-report` route alongside the existing `list` and `get` routes
- `server/src/main.rs` — load `LicensePolicy` at startup from the configured path (default `config/license-policy.json`) and provide it as shared state. Startup must fail if the policy cannot be loaded.
- `tests/api/sbom.rs` — add integration tests for the new endpoint

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `{ "sbom_id": "<id>", "groups": [{ "license": "MIT", "packages": [PackageSummary, ...], "compliant": true }] }`. Returns 404 when the SBOM does not exist.

## Implementation Notes
- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`): same path extraction, same service invocation style, same `Result<Json<T>, AppError>` return type.
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` the same way `list.rs` and `get.rs` are registered. `server/src/main.rs` already mounts the SBOM module, so only the policy state wiring is added there.
- This endpoint returns a single report object, not a list, so do not wrap it in `PaginatedResults<T>`. The response is the `LicenseReport` model from Task 2.
- Caching: the report changes whenever the policy file changes or the SBOM's packages change. If the existing `tower-http` caching middleware is configured in the SBOM route builder, make sure this route either opts out or uses a short TTL so stale compliance results are not served to the CI gate.
- Fail-closed gate behavior (UC-2 CI gate):
  - Unknown SBOM ID → 404 (from the service's not-found `AppError`), never `200` with an empty `groups` array.
  - Policy load failure → the server refuses to start (in `server/src/main.rs`). It does not serve reports with a missing or permissive policy.
- Authentication and authorization: the endpoint must use the same authentication and authorization as the existing `/api/v2/sbom/{id}` routes. Do not add unauthenticated, debug, internal, or admin routes as part of this task.
- Per CONVENTIONS.md §Endpoint registration: register the route in the module's `endpoints/mod.rs`. `server/main.rs` mounts the modules. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration (`endpoints/mod.rs`) scope. Example: `modules/fundamental/src/sbom/endpoints/mod.rs` (existing `/api/v2/sbom` registration).
- Per CONVENTIONS.md §Error handling: the handler returns `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust source (`.rs`) scope. Example: `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Caching: configure caching in the endpoint route builder. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route builder scope. Example: existing route builder in `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Per CONVENTIONS.md §Testing: put integration tests in `tests/api/` against the real PostgreSQL test database, using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/sbom.rs` matching the convention's integration test (`tests/api/*.rs`) scope. Example: existing tests in `tests/api/sbom.rs`.
- Constraints (docs/constraints.md): §5.1 change only the listed files; §5.8 match sibling SBOM endpoints on error handling, auth, logging, and caching; §2.1–2.3 commit format and trailers; §3.3 `--base main`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — closest sibling handler (`GET /api/v2/sbom/{id}`)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration and cache configuration
- `tests/api/sbom.rs` — existing SBOM integration test setup and fixtures (SBOM ingestion helpers)

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with `{ sbom_id, groups: [{ license, packages, compliant }] }` for an ingested SBOM
- [ ] Groups with policy-violating licenses have `compliant: false`
- [ ] Transitive dependency licenses appear in the response
- [ ] Fail-closed: an unknown SBOM ID returns 404, not 200 with empty `groups`
- [ ] Fail-closed: the server fails to start when the license policy file is missing or invalid
- [ ] The endpoint enforces the same authentication and authorization as the existing SBOM endpoints
- [ ] Report generation for an SBOM with 1000 packages completes with p95 < 500ms
- [ ] No endpoints other than `/api/v2/sbom/{id}/license-report` are added

## Test Requirements
- [ ] Integration test: ingest an SBOM with MIT and GPL-3.0-only packages, call the endpoint, and assert 200 with an MIT group `compliant: true` and a GPL group `compliant: false`
- [ ] Integration test: a transitive-only dependency's license appears in the response
- [ ] Integration test (fail-closed): an unknown SBOM ID returns 404 with no `groups` payload
- [ ] Integration test: an unauthenticated request is rejected the same way as on `GET /api/v2/sbom/{id}`
- [ ] Performance check: a 1000-package SBOM fixture is measured against the 500ms p95 target (benchmark or timed integration test)

## Verification Commands
- `cargo test --test api sbom` — SBOM API integration tests pass, including the license report tests
- `curl -s http://localhost:8080/api/v2/sbom/<id>/license-report | jq '.groups[] | {license, compliant}'` — returns grouped licenses with compliance flags

## Documentation Updates
- `README.md` — mention the new license report endpoint and the `config/license-policy.json` policy file location

## Dependencies
- Depends on: Task 1 — Add configurable license compliance policy
- Depends on: Task 2 — Implement license report aggregation service
