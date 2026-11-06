# Task 3 — Expose GET /api/v2/sbom/compare endpoint

**Summary:** Add GET /api/v2/sbom/compare endpoint with integration tests
**Epic:** TC-9003: SBOM diff API

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Expose the SBOM diff from Task 2 at `GET /api/v2/sbom/compare?left={id1}&right={id2}`. The frontend comparison page (TC-9003, Tasks 4–5) calls this endpoint to render the side-by-side diff.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/compare` route alongside the existing list (`/api/v2/sbom`) and get (`/api/v2/sbom/{id}`) routes
- `tests/api/sbom.rs` — add integration tests for the compare endpoint
- `README.md` — add the new endpoint to the API overview

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler: extracts the `left` and `right` query params, calls `SbomService::compare`, returns `Json<SbomComparison>`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparison` (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes). 400 if either param is missing or malformed. 404 if either SBOM does not exist.

## Implementation Notes
- Model the handler on `modules/fundamental/src/sbom/endpoints/get.rs`: the same state/service extraction and the same `Result<Json<_>, AppError>` return. Use a `#[derive(Deserialize)] struct CompareParams { left: String, right: String }` with `axum::extract::Query` (match the ID type used by `get.rs`).
- **Route ordering:** `/api/v2/sbom/compare` shares a prefix with `/api/v2/sbom/{id}`. Axum's router gives a static segment priority over a path parameter. Still, add an integration test proving that `compare` is not routed to the get-by-id handler.
- Leave the response unpaginated. Unlike list endpoints, it does not use `PaginatedResults<T>`, because the Figma contract is a single object of six arrays. Document this in the handler doc comment.
- **Caching:** per the repo's `tower-http` caching convention, set cache configuration in the route builder. SBOMs are immutable once ingested, so a cacheable response keyed on the full query string is acceptable. Follow whatever the existing get route does.
- **Fail-closed:** a missing `left` or `right` parameter must return 400 (Axum `Query` rejection, mapped through `AppError` if the project wraps rejections). A non-existent ID must return 404. Neither case may return 200 with empty lists.
- If the existing endpoints register OpenAPI docs via `utoipa::path`, annotate the new handler the same way.
- Monitoring: the request to add the endpoint to the Grafana API latency dashboard is excluded from this task (see the impact map: no dashboard repository is registered). Still give the handler a stable route name / tracing span, matching the existing handlers, so the dashboard can pick it up later.

**Conventions:**
- Per CONVENTIONS.md §Endpoint registration: register the route in `modules/fundamental/src/sbom/endpoints/mod.rs`. `server/src/main.rs` already mounts the SBOM module, so it needs no change. See how `list.rs` and `get.rs` are wired in `endpoints/mod.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration (`endpoints/mod.rs`) scope.
- Per CONVENTIONS.md §Error handling: return `Result<Json<SbomComparison>, AppError>` and wrap service calls with `.context()`, matching `get.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust handler (`.rs`) scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/sbom.rs` against the real PostgreSQL test database, using the `assert_eq!(resp.status(), StatusCode::OK)` pattern of the existing SBOM tests.
  Applies: task modifies `tests/api/sbom.rs` matching the convention's integration test (`tests/api/`) scope.
- Per CONVENTIONS.md §Caching: set cache configuration in the compare route builder using the existing `tower-http` caching middleware.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route builder scope.

**Project constraints (docs/constraints.md):**
- §2: Conventional Commits; the footer references the Jira task (`Implements TC-XXXX`); include the `Assisted-by:` trailer.
- §3: Open the PR with `gh pr create --base TC-9003` and post the PR link on the Jira task.
- §5: Change only the files listed here. Reuse the Task 2 service method rather than reimplementing the diff. Check parity with sibling handlers (error handling, caching, OpenAPI, tracing).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference handler for extraction, error mapping, and response.
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route builder and cache configuration.
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::compare` — added in Task 2.
- `tests/api/sbom.rs` — existing SBOM test fixtures and ingestion helpers for seeding two SBOMs.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with a JSON body matching the documented `SbomComparison` shape
- [ ] A missing `left` or `right` query param returns 400
- [ ] A non-existent `left` or `right` SBOM ID returns 404, not 200 with empty lists (fail-closed)
- [ ] `/api/v2/sbom/compare` is not captured by the `/api/v2/sbom/{id}` route
- [ ] Existing `GET /api/v2/sbom` and `GET /api/v2/sbom/{id}` behavior is unchanged
- [ ] p95 response time is under 1s when comparing two SBOMs of about 2000 packages each in the test environment
- [ ] README documents the new endpoint

## Test Requirements
- [ ] Integration test: seed two SBOMs that differ in packages, versions, licenses, and advisories, and assert each of the six lists contains exactly the expected entries
- [ ] Integration test: compare an SBOM with itself and assert 200 with six empty arrays
- [ ] Integration test: an unknown `right` ID returns 404, and the body is not an empty diff (fail-closed path)
- [ ] Integration test: a missing `right` param returns 400
- [ ] Integration test: a request to `/api/v2/sbom/compare` does not hit the get-by-id handler (route precedence)
- [ ] Performance test or benchmark (may be `#[ignore]`d in CI): two SBOMs of 2000 packages each compare in under 1s

## Verification Commands
- `cargo test --test api sbom` (adjust to the test crate name in `tests/Cargo.toml`) — all SBOM tests pass, including the new compare tests
- `curl -s "http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=<id2>" | jq 'keys'` — returns the six diff keys
- `curl -s -o /dev/null -w "%{http_code}" "http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=does-not-exist"` — prints `404`

## Documentation Updates
- `README.md` — add `GET /api/v2/sbom/compare` to the API section: query params, response shape, and error codes (400/404)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model and diff service
