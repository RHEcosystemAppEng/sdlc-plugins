# Task 3 — Expose GET /api/v2/sbom/compare endpoint

**Summary:** Add GET /api/v2/sbom/compare endpoint with integration tests
**Epic:** TC-9003: SBOM diff API
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003)

---

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Expose the SBOM diff service from Task 2 as a REST endpoint: `GET /api/v2/sbom/compare?left={id1}&right={id2}`. The frontend comparison page (TC-9003, UC-1 step 4) calls this endpoint, and the UI depends on its response contract.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/compare` route alongside the existing list (`/api/v2/sbom`) and get (`/api/v2/sbom/{id}`) routes
- `tests/api/sbom.rs` — add integration tests for the compare endpoint
- `README.md` — add the compare endpoint to the API reference (see Documentation Updates)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — `compare` Axum handler: extracts the `left` and `right` query params, calls `SbomService::compare`, returns `Json<SbomComparison>`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns the structured diff `SbomComparison` (`added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`)
  - 400 when `left` or `right` is missing or malformed
  - 404 when either SBOM does not exist

## Implementation Notes
- **Handler.** Follow the existing handler shape in `modules/fundamental/src/sbom/endpoints/get.rs` (single-resource fetch) and `list.rs` (query-param extraction).
  - Define a `CompareParams { left: <SbomId type>, right: <SbomId type> }` struct with `#[derive(Deserialize)]` and extract it with `Query<CompareParams>`.
  - Use the same ID type that `get.rs` uses for `{id}`.
- **Route ordering.** `/api/v2/sbom/compare` sits next to `/api/v2/sbom/{id}`. Register it so that the literal `compare` segment is never captured as `{id}`. Axum's router gives static segments priority, but add an integration test (below) that proves `GET /api/v2/sbom/compare?...` does not reach the `get` handler.
- **Response type.** This is a single-object response. Do not wrap it in `PaginatedResults<T>` (`common/src/model/paginated.rs`), because the feature requires the whole diff in one payload. The frontend virtualizes long lists.
- **Caching.** The diff of two immutable SBOM IDs is deterministic until new advisories are correlated. If the route builder in `endpoints/mod.rs` applies `tower-http` caching middleware to sibling routes, apply the same configuration to this route. Do not invent a new caching policy.
- **Errors.** Map not-found from `SbomService::compare` to 404 via the existing `AppError` `IntoResponse` implementation (`common/src/error.rs`). Do not add a new error type.
- **Observability.** The Grafana dashboard update is out of scope (see "Excluded requirements" on TC-9003). Keep the handler compatible with the existing per-route latency metrics middleware, if one is mounted in `server/src/main.rs`, so the route can be added to the dashboard later.
- Per CONVENTIONS.md §Endpoint registration: register the route in the module's `endpoints/mod.rs`. `server/src/main.rs` already mounts the SBOM module, so it should not need changes; verify this at implementation time. See `modules/fundamental/src/sbom/endpoints/mod.rs` for the established pattern.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `endpoints/mod.rs` route-registration scope.
- Per CONVENTIONS.md §Error handling: the handler returns `Result<Json<SbomComparison>, AppError>` and wraps service calls with `.context()`. See `modules/fundamental/src/sbom/endpoints/get.rs`.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust handler scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/sbom.rs` against the real PostgreSQL test database, using the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern. See the existing tests in `tests/api/sbom.rs`.
  Applies: task modifies `tests/api/sbom.rs` matching the convention's `tests/api/` integration test scope.
- Constraints (docs/constraints.md):
  - §2 Commit rules: Conventional Commits format, a `Implements TC-<task-key>` footer, and an `Assisted-by:` trailer.
  - §3 PR rules: use `--base TC-9003` and post the PR link on the Jira task. If the `TC-9003` branch does not yet exist in `trustify-backend`, create it from `main` first (the bookend Task 1 only covers `trustify-ui`).
  - §5 Code change rules: stay within the listed files; inspect before modifying; no duplicate functionality.
  - §1.4/§1.5: no unrelated refactoring.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing single-SBOM handler; mirror its extractor, service invocation, and error mapping
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing query-param extraction pattern
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::compare` — added in Task 2; the handler is a thin wrapper around it
- `tests/api/sbom.rs` — existing SBOM integration test setup (fixture ingestion, test client); reuse it to ingest two SBOM fixtures with overlapping packages

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with a JSON body containing all six diff keys
- [ ] The response for two ingested fixture SBOMs correctly lists added, removed, version-changed, and license-changed packages, plus new and resolved vulnerabilities
- [ ] A missing `left` or `right` query param returns 400
- [ ] A non-existent SBOM ID in either param returns 404, not 200 with an empty diff
- [ ] `GET /api/v2/sbom/{id}` and `GET /api/v2/sbom` keep working unchanged (no route collision with `compare`)
- [ ] p95 response time is below 1s for two SBOMs of up to 2000 packages each (measured locally against the test DB with a generated fixture)

## Test Requirements
- [ ] Integration test: ingest two SBOMs that differ by one added package, one removed package, one version upgrade, one license change, one new advisory, and one resolved advisory; assert 200 and the exact contents of each category
- [ ] Integration test: compare an SBOM with itself → 200 with all arrays empty
- [ ] Integration test: missing `right` param → 400
- [ ] Integration test: unknown `left` ID → 404 (fail-closed; must not return an empty diff)
- [ ] Integration test: the existing `GET /api/v2/sbom/{id}` test still passes, and a request to `/api/v2/sbom/compare?...` is handled by the compare handler (response contains `added_packages`)
- [ ] Integration (or `#[ignore]`-gated benchmark) test with two generated 2000-package SBOMs that asserts completion under 1s

## Verification Commands
- `cargo test --test api sbom` — all SBOM integration tests pass (adjust to the test target defined in `tests/Cargo.toml`)
- `curl -s "http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=<id2>" | jq 'keys'` — prints the six diff keys

## Documentation Updates
- `README.md` — add `GET /api/v2/sbom/compare` to the API endpoint list, with its query parameters, response shape, and error codes (400/404)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison response model and on-the-fly diff computation in SbomService
