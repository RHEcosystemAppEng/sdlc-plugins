## Repository
trustify-backend

## Target Branch
main

## Description
Expose the SBOM diff from Task 1 over HTTP as `GET /api/v2/sbom/compare?left={id1}&right={id2}` (TC-9003). This endpoint is the backend contract consumed by the trustify-ui comparison page. It must validate both query parameters, return 404 when either SBOM is missing, and meet the p95 < 1s latency target for SBOMs with up to 2000 packages each.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/compare` route (before the `/api/v2/sbom/{id}` route so `compare` is not captured as an `{id}`)
- `tests/api/sbom.rs` — add integration tests for the compare endpoint
- `README.md` — add the new endpoint to the API overview

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler: extracts `left` and `right` query parameters, calls the compare service from Task 1, returns `Json<SbomComparison>`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns a `SbomComparison` JSON object with `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`. Errors: 400 when `left` or `right` is missing/malformed, 404 when either SBOM does not exist.

## Implementation Notes
- Follow the handler structure of `modules/fundamental/src/sbom/endpoints/get.rs` (single-resource GET returning a model struct) and the route registration style in `modules/fundamental/src/sbom/endpoints/mod.rs`. `server/src/main.rs` already mounts the SBOM module routes, so no change there is needed unless route mounting is per-endpoint.
- Define a `CompareQuery { left: String, right: String }` struct (use the same ID type as `get.rs` uses for `{id}`) and extract it with `axum::extract::Query`. Missing parameters must produce a 400 response, not a panic or a 500.
- **Route ordering:** Axum matches static segments before captures, but verify explicitly with a test that `GET /api/v2/sbom/compare?...` does not hit the `get.rs` handler.
- **Response is not paginated:** unlike `list.rs`, do not wrap in `PaginatedResults<T>` (`common/src/model/paginated.rs`) — the Figma design and feature spec expect one diff object.
- **Caching:** the route builder in `endpoints/mod.rs` configures `tower-http` caching middleware; apply the same cache configuration used for the `get.rs` route (diff of immutable SBOM contents is cacheable per `left`/`right` pair).
- **Observability:** add a `tracing` span/instrument on the handler (matching sibling handlers) so the endpoint appears in latency metrics feeding the Grafana API latency dashboard (dashboard change itself is out of scope — see impact map "Excluded requirements").
- **Per CONVENTIONS.md §Endpoint registration:** register the route in `modules/fundamental/src/sbom/endpoints/mod.rs`; see the existing `list.rs`/`get.rs` registration in the same file.
  Applies: task modifies modules/fundamental/src/sbom/endpoints/mod.rs matching the convention's Rust endpoint-registration `endpoints/mod.rs` scope.
- **Per CONVENTIONS.md §Error handling:** the handler returns `Result<Json<SbomComparison>, AppError>` with `.context()` wrapping, as in `modules/fundamental/src/sbom/endpoints/get.rs`.
  Applies: task modifies modules/fundamental/src/sbom/endpoints/compare.rs matching the convention's Rust handler `.rs` scope.
- **Per CONVENTIONS.md §Caching:** configure `tower-http` caching in the compare route builder the same way as the existing SBOM routes in `endpoints/mod.rs`.
  Applies: task modifies modules/fundamental/src/sbom/endpoints/mod.rs matching the convention's endpoint route builder scope.
- **Per CONVENTIONS.md §Testing:** add integration tests in `tests/api/sbom.rs` against the real PostgreSQL test database, asserting with `assert_eq!(resp.status(), StatusCode::OK)`.
  Applies: task modifies tests/api/sbom.rs matching the convention's `tests/api/` integration test scope.
- **Constraints (docs/constraints.md):** §2 commits (Conventional Commits, `Implements <task-key>` footer, `Assisted-by:` trailer); §3 PRs (`--base main`, PR link posted on Jira task); §5 code changes (scoped to listed files, inspect first, no duplication, data-flow trace, sibling parity with `get.rs`/`list.rs` for error handling, tracing and caching); §1.4/1.5 implement-task scope rules.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — template for a single-object GET handler with not-found handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route builder and caching middleware config to extend
- `common/src/error.rs::AppError` — maps not-found/bad-request to HTTP responses via `IntoResponse`
- `tests/api/sbom.rs` — existing SBOM integration test setup (fixture ingestion, test client) to reuse for the new tests

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with the `SbomComparison` JSON shape
- [ ] Missing `left` or `right` returns 400
- [ ] Unknown `left` or `right` SBOM ID returns 404 (not 200 with empty arrays)
- [ ] `GET /api/v2/sbom/{id}` behaviour is unchanged
- [ ] Endpoint is registered in `modules/fundamental/src/sbom/endpoints/mod.rs` with the same caching configuration as sibling SBOM routes
- [ ] p95 latency < 1s for two SBOMs with 2000 packages each (measured locally against the test database)
- [ ] README lists the new endpoint

## Test Requirements
- [ ] Integration test: ingest two SBOM fixtures that differ by an added package, a removed package, a version change, a license change, a new advisory and a resolved advisory; assert each array contains exactly the expected entry
- [ ] Integration test: comparing an SBOM with itself returns 200 and six empty arrays
- [ ] Integration test: unknown SBOM ID returns 404 (fail-closed — guards against silently returning an empty diff)
- [ ] Integration test: missing query parameter returns 400
- [ ] Integration test: existing `GET /api/v2/sbom/{id}` test still passes (route ordering regression)
- [ ] Performance test (ignored by default, `#[ignore]`) generating two 2000-package SBOMs and asserting response time < 1s

## Verification Commands
- `cargo test --test api sbom` — compare integration tests pass
- `curl -s "http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=<id2>" | jq 'keys'` — prints the six diff keys

## Documentation Updates
- `README.md` — add `GET /api/v2/sbom/compare` with query parameters and a response example

## Dependencies
- Depends on: Task 1 — Add SBOM comparison diff model and service
