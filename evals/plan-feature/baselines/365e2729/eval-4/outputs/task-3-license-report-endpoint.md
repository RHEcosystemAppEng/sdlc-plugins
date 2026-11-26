## Repository
trustify-backend

## Target Branch
main

## Description
Expose the license compliance report for TC-9004 as `GET /api/v2/sbom/{id}/license-report`. Register the route in the SBOM module, wire it to the service from Task 2, and add endpoint integration tests that cover the compliance officer flow (UC-1) and the CI/CD gate flow (UC-2).

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/{id}/license-report` route under `/api/v2/sbom`
- `server/src/main.rs` — load the `LicensePolicy` at startup (failing startup if it is invalid) and make it available to the handler as shared state. No new module mount is needed, because the route lives in the existing SBOM router
- `tests/api/sbom.rs` — add integration tests for the new endpoint

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `{ "groups": [ { "license": "MIT", "packages": [PackageSummary...], "compliant": true } ] }`. Returns 404 when the SBOM does not exist.

## Implementation Notes
- Model the handler on `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`): same path extractor, same database/service state, same `Result<Json<_>, AppError>` return type.
- Register the route the same way `list.rs` and `get.rs` are registered in `modules/fundamental/src/sbom/endpoints/mod.rs`.
- The route uses the same authentication and authorization middleware as the other `/api/v2/sbom` routes. Do not add any unauthenticated route.
- **Fail-closed startup (gate site: policy loading in `server/src/main.rs`).** If `LicensePolicy` fails to load, the server refuses to start or the endpoint returns 500. It never serves reports against a permissive fallback policy.
- Caching: if the cache configuration in the SBOM route builder is applied, make sure cached reports are invalidated or kept short-lived, because a policy file change must be reflected in the report. Prefer no caching for this route unless profiling shows it is needed.
- Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes and `server/main.rs` mounts modules. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration (`endpoints/mod.rs`) scope. See the existing registrations in that file for `list.rs` and `get.rs`.
- Per CONVENTIONS.md §Error handling: the handler returns `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust handler (`.rs`) scope. See `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/sbom.rs` matching the convention's integration test (`tests/api/*.rs`) scope. See the existing tests in `tests/api/sbom.rs`.
- Constraints (docs/constraints.md): §5.1 keep changes to the files listed above; §5.2 inspect existing code before modifying it; §5.8 match sibling endpoints (`get.rs`, `list.rs`) on error handling, auth, and logging; §2.1–2.3 commit rules; §3.1–3.3 PR rules.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — handler pattern for `/api/v2/sbom/{id}`
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — the service entry point (`license_report` method added in Task 2)
- `tests/api/sbom.rs` — existing SBOM integration test setup and fixtures

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a body matching `{ groups: [{ license, packages, compliant }] }`
- [ ] The endpoint returns 404 for a nonexistent SBOM ID
- [ ] The endpoint is protected by the same auth middleware as other `/api/v2/sbom` routes
- [ ] The server does not serve reports when the license policy fails to load (fail-closed)
- [ ] p95 latency is under 500ms for an SBOM with up to 1000 packages

## Test Requirements
- [ ] Integration test: a valid SBOM returns 200 with grouped licenses and correct `compliant` flags (UC-1)
- [ ] Integration test: an SBOM containing a non-compliant license has at least one group with `compliant: false` (UC-2 gate signal)
- [ ] Integration test: a nonexistent SBOM ID returns 404, not 200 with empty groups
- [ ] Integration test: an unauthenticated request is rejected the same way as on `GET /api/v2/sbom/{id}`
- [ ] Integration test: transitive dependency packages appear in the response

## Verification Commands
- `cargo test --test api sbom` — SBOM integration tests, including the license report tests, pass
- `curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8080/api/v2/sbom/<id>/license-report | jq '.groups[] | {license, compliant}'` — lists the license groups with their compliance flags

## Documentation Updates
- `README.md` — add the new endpoint to the API overview and point to the license policy configuration (full documentation is covered by Task 4)

## Dependencies
- Depends on: Task 2 — Implement license report aggregation service
