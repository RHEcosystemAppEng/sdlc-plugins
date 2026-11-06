## Repository
trustify-backend

## Target Branch
main

## Description
Expose the license compliance report as `GET /api/v2/sbom/{id}/license-report`. Register the route in the SBOM module, load the license policy at server startup, and add integration tests. With this endpoint, compliance officers (UC-1) and CI/CD pipelines (UC-2) can get a grouped license report with policy violation flags in one API call.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for `GET /api/v2/sbom/{id}/license-report` that calls the Task 2 service and returns JSON `LicenseReport`
- `tests/api/license_report.rs` — integration tests for the new endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/{id}/license-report` route under the existing `/api/v2/sbom` router
- `server/src/main.rs` — load `LicensePolicy` at startup (from the configured path, defaulting to `license-policy.json`) and make it available to handlers (e.g., Axum state or an `Extension`). Startup must fail if the policy cannot be loaded.
- `tests/Cargo.toml` — register the new `license_report` integration test target if required by the test harness layout

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: returns `{ "groups": [ { "license": "MIT", "packages": [PackageSummary...], "compliant": true } ] }`. Returns 404 for an unknown SBOM ID.

## Implementation Notes
- Use the existing handlers in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`) as the template for path extraction, DB access, and error mapping.
- Register the route next to the existing ones in `modules/fundamental/src/sbom/endpoints/mod.rs`. `server/src/main.rs` already mounts the SBOM module, so no new mount is needed beyond providing the policy state.
- The response is a single report object, not a list. Do not wrap it in `PaginatedResults<T>` (`common/src/model/paginated.rs`). That wrapper is for list endpoints only. Pagination would also split groups across pages and could hide non-compliant groups from a CI gate.
- Caching: if `tower-http` caching middleware is configured for SBOM routes in the route builder, give this route a short or no cache. A policy change must not serve stale compliance results.
- Fail closed at the HTTP layer: an unknown SBOM must return `404`, and service/policy errors must return a 5xx through `AppError`'s `IntoResponse`. Never return `200` with an empty `groups` array for these cases, because a CI gate checking only for `compliant: false` would pass. The guard belongs in the handler in `modules/fundamental/src/sbom/endpoints/license_report.rs` and in the policy load in `server/src/main.rs`.
- Per CONVENTIONS.md §Endpoint registration: register the route in the module's `endpoints/mod.rs`. `server/src/main.rs` mounts all modules.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration (`modules/*/src/<domain>/endpoints/mod.rs`) scope.
- Per CONVENTIONS.md §Error handling: the handler returns `Result<Json<LicenseReport>, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/license_report.rs` matching the convention's Rust source (`.rs`) scope.
- Per CONVENTIONS.md §Testing: integration tests go in `tests/api/`, run against the PostgreSQL test database, and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern. See `tests/api/sbom.rs` for an example.
  Applies: task modifies `tests/api/license_report.rs` matching the convention's integration test (`tests/api/*.rs`) scope.
- Constraints (docs/constraints.md): Conventional Commits with the Jira ID in the footer and an `Assisted-by:` trailer (§2.1–2.3). PR uses `--base main` (§3.3). Stay within the listed files (§5.1). Compare with sibling handlers (`get.rs`, `list.rs`) for parity in error handling and logging (§5.8).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing `GET /api/v2/sbom/{id}` handler. Follow the same path-param and error-handling pattern.
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration for `/api/v2/sbom`
- `tests/api/sbom.rs` — existing SBOM integration tests. Reuse their fixture/ingestion setup to seed SBOMs with package-license data.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns `200` with `{ groups: [{ license, packages, compliant }] }` for an ingested SBOM
- [ ] Non-compliant licenses (per `license-policy.json`) appear in groups with `compliant: false`
- [ ] Transitive dependency licenses are included in the response
- [ ] An unknown SBOM ID returns `404`, not `200` with empty groups (fail closed)
- [ ] The server refuses to start, with a clear error, if the license policy file is missing or invalid (fail closed)
- [ ] The response is not paginated

## Test Requirements
- [ ] Integration test: ingest an SBOM with mixed licenses, call the endpoint, assert `StatusCode::OK` and the correct grouping and `compliant` flags
- [ ] Integration test: an SBOM containing a denied license returns at least one group with `compliant: false` (UC-2 gate)
- [ ] Integration test: an unknown SBOM ID returns `StatusCode::NOT_FOUND`
- [ ] Integration test: an SBOM whose packages lack license data returns a non-compliant `NOASSERTION` group, not an empty or all-compliant report
- [ ] Integration test: transitive dependencies' licenses appear in the response
- [ ] Integration test: response time for a 1000-package SBOM is within the p95 < 500ms target

## Verification Commands
- `cargo test -p tests license_report` — integration tests pass
- `curl -s http://localhost:8080/api/v2/sbom/<id>/license-report | jq '.groups[] | {license, compliant}'` — returns grouped licenses with compliance flags

## Documentation Updates
- `README.md` — mention the new license report endpoint and the `license-policy.json` configuration file

## Dependencies
- Depends on: Task 2 — Implement license compliance report aggregation service
