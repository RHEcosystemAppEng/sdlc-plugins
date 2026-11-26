# Task 3 — Expose GET /api/v2/sbom/compare endpoint

**Summary:** Add GET /api/v2/sbom/compare endpoint with integration tests
**Epic:** TC-9003: SBOM diff API
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003; fixVersion scope = both)

---

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Expose the SBOM diff service from Task 2 over HTTP as `GET /api/v2/sbom/compare?left={id1}&right={id2}`. This endpoint is consumed by the new frontend comparison page (TC-9003, Tasks 4–8) and must also serve URL-shared comparisons (UC-2), so it must be stateless and deterministic for a given pair of IDs.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/compare` route under `/api/v2/sbom`, before/alongside the `/{id}` route, and declare the `compare` module
- `tests/api/sbom.rs` — add integration tests for the compare endpoint

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler: parse `left` and `right` query params, call the compare service, return `Json<SbomComparison>`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns a structured diff (`SbomComparison`) between two SBOMs. `200` with the six diff arrays; `400` when `left` or `right` is missing or malformed; `404` when either SBOM does not exist.

## Implementation Notes
- Follow the existing handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (`GET /api/v2/sbom/{id}`) and `modules/fundamental/src/sbom/endpoints/list.rs`: extract dependencies/state the same way, delegate to the service, and return `Result<Json<_>, AppError>`.
- Use an Axum `Query<CompareParams>` extractor with `left` and `right` fields typed the same as the ID type used by `get.rs`. A missing/invalid param must yield `400`, not a panic and not an empty diff.
- **Route ordering:** `/api/v2/sbom/compare` shares a prefix with `/api/v2/sbom/{id}`. Register `/compare` as a static segment so it is never captured by the `{id}` route (verify against the Axum router version in `Cargo.toml`; Axum's router prioritizes static segments, but add an integration test proving `compare` is not routed to `get`).
- `server/src/main.rs` already mounts the SBOM module's routes; no change is expected there — confirm by inspection.
- Caching: per the repo's tower-http caching convention, cache configuration is set in the endpoint route builder. A comparison of two ingested SBOMs is a pure function of their IDs, but advisory correlation can add `sbom_advisory` rows later; use the same (or a shorter) cache policy as `get.rs` rather than an aggressive long-lived cache.
- NFR: p95 < 1s for SBOMs with up to 2000 packages each. Add a `tracing` span (or the existing request instrumentation pattern) around the handler so the endpoint shows up in the API latency metrics (see Excluded requirements in the impact map regarding the Grafana dashboard itself).
- Fail-closed: the handler must propagate the not-found error from the service as `404`. The gate site is the handler in `modules/fundamental/src/sbom/endpoints/compare.rs` plus the service guard in `modules/fundamental/src/sbom/service/compare.rs` (Task 2).

**Conventions:**
- Per CONVENTIONS.md §Endpoint registration: register the new route in the module's `endpoints/mod.rs`; `server/main.rs` mounts the module. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `endpoints/mod.rs` route-registration scope. Example: existing `list` and `get` registration in the same file.
- Per CONVENTIONS.md §Error handling: handler returns `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust handler (`.rs`) scope. Example: `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` against the PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/sbom.rs` matching the convention's `tests/api/` integration test scope. Example: existing tests in `tests/api/sbom.rs`.
- Per CONVENTIONS.md §Caching: configure caching in the endpoint route builder using the tower-http caching middleware. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route builder scope.

**Project constraints (docs/constraints.md):**
- §2 Commit rules: Conventional Commits, `Implements <task-key>` footer, `Assisted-by:` trailer.
- §3 PR rules: `gh pr create --base TC-9003`; post the PR link on the Jira task.
- §5 Code change rules: scope to listed files; inspect before modifying; follow sibling handler patterns (`get.rs`, `list.rs`) for parity on error handling, logging and caching; doc comments on every new test function and given-when-then comments in non-trivial tests (§5.11, §5.12).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — closest sibling handler (single resource fetch, ID extraction, error mapping)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration and cache configuration pattern
- `common/src/error.rs::AppError` — `IntoResponse` mapping for 400/404
- `tests/api/sbom.rs` — existing SBOM integration test setup (test DB, ingestion of fixture SBOMs, request helpers)

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns `200` with the `SbomComparison` JSON body
- [ ] Response contains exactly the keys `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] Missing `left` or `right` query param returns `400`
- [ ] Fail-closed: a non-existent `left` or `right` ID returns `404`, never `200` with empty arrays
- [ ] `GET /api/v2/sbom/compare` is not captured by the `GET /api/v2/sbom/{id}` route
- [ ] Existing `GET /api/v2/sbom` and `GET /api/v2/sbom/{id}` behavior is unchanged
- [ ] Endpoint responds in < 1s for two SBOMs with ~2000 packages each in the integration environment

## Test Requirements
- [ ] Integration test: ingest two fixture SBOMs differing by an added package, a removed package, a version bump, and a license change; assert each appears in the correct section
- [ ] Integration test: fixture with an advisory linked only to the right SBOM appears in `new_vulnerabilities`; one linked only to the left appears in `resolved_vulnerabilities`
- [ ] Integration test: comparing an SBOM with itself returns `200` with six empty arrays
- [ ] Integration test: missing `right` param returns `400`
- [ ] Fail-closed integration test: non-existent SBOM ID returns `404` and the body is not an empty diff
- [ ] Integration test: request to `/api/v2/sbom/compare?...` is handled by the compare handler (not the `{id}` handler)
- [ ] Regression: existing tests in `tests/api/sbom.rs` still pass

## Verification Commands
- `cargo test --test api sbom` (or the test target defined in `tests/Cargo.toml`) — all SBOM integration tests pass
- `curl -s "http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=<id2>" | jq 'keys'` — prints the six diff keys
- `curl -s -o /dev/null -w "%{http_code}" "http://localhost:8080/api/v2/sbom/compare?left=does-not-exist&right=<id2>"` — prints `404`

## Documentation Updates
- `README.md` — mention the new comparison endpoint in the API overview if the README lists endpoints (full reference is covered by Task 9)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model and diff service
