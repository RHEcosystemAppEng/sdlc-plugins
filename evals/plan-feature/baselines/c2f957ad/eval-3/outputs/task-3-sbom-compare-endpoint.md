# Task 3 — Add GET /api/v2/sbom/compare endpoint

**Summary:** Add GET /api/v2/sbom/compare endpoint with integration tests
**Issue type:** Task | **Parent (Epic):** Epic A — TC-9003: SBOM diff API
**Labels:** ai-generated-jira | **Priority:** Critical | **Fix Versions:** RHTPA 1.5.0

---

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Expose the SBOM diff computed by `SbomService::compare` (Task 2) as a REST endpoint: `GET /api/v2/sbom/compare?left={id1}&right={id2}`. The frontend comparison page (trustify-ui, Tasks 4–5) calls this endpoint, and URLs encode the two ids so comparisons are shareable. The endpoint must meet p95 < 1s for SBOMs with up to 2000 packages each.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/compare` route in the `/api/v2/sbom` route builder
- `tests/api/sbom.rs` — add integration tests for the comparison endpoint
- `README.md` — add the comparison endpoint to the API reference section

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler: parse `left`/`right` query params, call `SbomService::compare`, return JSON `SbomComparison`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns the structured diff `{ added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes }` (shape defined in Task 2). `200` on success, `400` when `left` or `right` is missing/malformed, `404` when either SBOM does not exist.

## Implementation Notes
- Follow the handler shape of `modules/fundamental/src/sbom/endpoints/get.rs` (single-resource GET) and the route registration in `modules/fundamental/src/sbom/endpoints/mod.rs`. Use an Axum `Query<CompareParams { left, right }>` extractor; the id type must match the one used by `get.rs` for `{id}`.
- **Route ordering:** `/api/v2/sbom/compare` shares the prefix with `/api/v2/sbom/{id}`. Axum's router prioritizes static segments over path parameters, but add an integration test proving `compare` is not captured as an `{id}` lookup.
- `server/src/main.rs` already mounts the SBOM module routes — no change expected there; verify at implementation time.
- **Fail closed:** missing/invalid query params → `400`; unknown SBOM id → `404` (propagated from Task 2's not-found `AppError`). The handler must never return `200` with empty arrays for an unknown id.
- **Caching:** per the repo's caching convention the route builder configures `tower-http` caching. The diff is derived from two immutable SBOM documents, so it may be cached; keep cache configuration consistent with the `get.rs` route rather than inventing a new policy.
- Per CONVENTIONS.md §Endpoint registration: register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs`; do not mount it directly in `server/src/main.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route-registration (`endpoints/mod.rs`) scope.
- Per CONVENTIONS.md §Error handling: the handler returns `Result<Json<SbomComparison>, AppError>` and wraps service errors with `.context()`, as in `modules/fundamental/src/sbom/endpoints/get.rs`.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust (`.rs`) handler scope.
- Per CONVENTIONS.md §Caching: configure caching for the new route in the endpoint route builder, mirroring the existing SBOM routes.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route-builder scope.
- Per CONVENTIONS.md §Testing: add integration tests to `tests/api/sbom.rs` against the real PostgreSQL test database using the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/sbom.rs` matching the convention's `tests/api/` integration-test scope.
- Constraints (docs/constraints.md): §2.1–2.3 commit rules; §3.1/§3.3/§3.4 PR targets `--base TC-9003`; §5.1–5.8 scope to listed files, reuse, data-flow tracing, sibling parity with `get.rs`/`list.rs` (error handling, logging, caching).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — sibling single-resource handler (extractors, error mapping, response)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route builder and caching configuration
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::compare` — diff logic from Task 2
- `tests/api/sbom.rs` — existing SBOM integration tests and test-data ingestion helpers to seed two SBOMs

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns `200` with the six diff arrays for two existing SBOMs
- [ ] Missing `left` or `right` returns `400`
- [ ] Unknown `left` or `right` id returns `404` (not `200` with empty arrays)
- [ ] `GET /api/v2/sbom/{id}` behaviour is unchanged and `/compare` is not routed to the `{id}` handler
- [ ] p95 response time < 1s for two SBOMs with 2000 packages each
- [ ] README API reference lists the new endpoint, parameters, and response shape

## Test Requirements
- [ ] Integration test: ingest two SBOM fixtures differing by an added package, a removed package, a version change, a license change and an advisory; assert each array's contents
- [ ] Integration test: identical `left` and `right` returns `200` with all arrays empty
- [ ] Integration test: missing query param returns `400`
- [ ] Integration test: non-existent id returns `404`
- [ ] Integration test: existing `GET /api/v2/sbom/{id}` still returns `200` for a valid id (route-ordering regression)
- [ ] Performance check (test or benchmark) with 2000-package SBOMs confirming the < 1s target

## Verification Commands
- `cargo test --test api sbom` — comparison integration tests pass
- `curl -s "http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=<id2>" | jq 'keys'` — returns the six diff keys
- `curl -s -o /dev/null -w '%{http_code}' "http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=does-not-exist"` — prints `404`

## Documentation Updates
- `README.md` — add `GET /api/v2/sbom/compare` to the API section: query parameters, status codes, response shape

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model and diff service
