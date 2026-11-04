# Task 3 — Backend: GET /api/v2/sbom/compare endpoint and integration tests

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Expose the SBOM diff from Task 2 as `GET /api/v2/sbom/compare?left={id1}&right={id2}`. This endpoint backs the SBOM comparison view of TC-9003 and is called by the frontend comparison page. It returns the structured diff (added/removed packages, version changes, new/resolved vulnerabilities, license changes) and must meet p95 < 1s for SBOMs with up to 2000 packages each.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs`: register the `/api/v2/sbom/compare` route alongside the existing list and get routes
- `tests/api/sbom.rs`: add integration tests for the compare endpoint

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs`: Axum handler that parses the `left`/`right` query params, calls `SbomService::compare` and returns `Json<SbomComparison>`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` is NEW. It returns `SbomComparison` (`added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`). Responses: `200` with the diff, `400` when `left` or `right` is missing or malformed, `404` when either SBOM does not exist.

## Implementation Notes
- Define a `CompareQuery { left: <SBOM id type>, right: <SBOM id type> }` struct and extract it with `axum::extract::Query`. Use the same ID type as the `{id}` path param in `modules/fundamental/src/sbom/endpoints/get.rs`.
- **Route ordering:** register `/compare` so it is not captured by `/{id}`. Axum prefers static segments over parameter segments, but add an integration test that confirms `/api/v2/sbom/compare` does not dispatch to the get-by-id handler.
- **Fail-closed behavior:** a missing or unknown SBOM must produce `404`, and missing params must produce `400`. The handler must never return `200` with empty arrays when a lookup failed. The guard belongs in `compare.rs` (handler), which propagates the not-found `AppError` raised in `SbomService::compare` (`modules/fundamental/src/sbom/service/sbom.rs`).
- **Caching:** both SBOMs are immutable once ingested, so the response can be cached. Follow the existing `tower-http` cache configuration in the SBOM route builder in `modules/fundamental/src/sbom/endpoints/mod.rs`.
- **Response type:** this endpoint returns a single object, not `PaginatedResults<T>`, because the Figma specifies no pagination (open question 2 in the impact map).
- Per CONVENTIONS.md §Endpoint registration: register the route in `modules/fundamental/src/sbom/endpoints/mod.rs`. `server/src/main.rs` already mounts the SBOM module, so no change is needed there. See how `list.rs` and `get.rs` are wired in `endpoints/mod.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration (`endpoints/mod.rs`) scope.
- Per CONVENTIONS.md §Error handling: the handler returns `Result<Json<SbomComparison>, AppError>` and wraps errors with `.context()`. Follow `modules/fundamental/src/sbom/endpoints/get.rs`.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust handler (`.rs`) scope.
- Per CONVENTIONS.md §Caching: configure caching in the endpoint route builder, as the existing SBOM routes do.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route builder scope.
- Per CONVENTIONS.md §Testing: integration tests go in `tests/api/sbom.rs` against the real PostgreSQL test database, using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Follow the existing SBOM endpoint tests in that file.
  Applies: task modifies `tests/api/sbom.rs` matching the convention's integration test (`tests/api/*.rs`) scope.
- Constraints (docs/constraints.md): §1.4/§5.1 scope to the listed files; §5.2 inspect `endpoints/mod.rs`, `get.rs` and `list.rs` before changing them; §5.8 match sibling handlers for error handling, caching and logging; §5.9–5.13 prefer parameterized tests where the project already uses them, add a doc comment to each test, and use given-when-then comments for non-trivial tests; §2.1–2.3 commit format; §3.3 open the PR with `--base TC-9003`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs`: handler pattern (extractor, service call, `AppError` mapping) to mirror
- `modules/fundamental/src/sbom/endpoints/mod.rs`: route registration and cache configuration pattern
- `tests/api/sbom.rs`: existing SBOM integration tests and fixture or ingestion helpers for seeding SBOMs

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns `200` with the `SbomComparison` JSON shape for two existing SBOMs
- [ ] A missing `left` or `right` query param returns `400`
- [ ] A non-existent `left` or `right` SBOM ID returns `404`, never `200` with empty arrays (fail-closed)
- [ ] `/api/v2/sbom/compare` is not routed to the `GET /api/v2/sbom/{id}` handler
- [ ] The existing `GET /api/v2/sbom` and `GET /api/v2/sbom/{id}` behavior is unchanged
- [ ] p95 response time is under 1s for two SBOMs with 2000 packages each

## Test Requirements
- [ ] Integration test: ingest two SBOMs with known differences and assert each of the six response arrays contains the expected entries
- [ ] Integration test: comparing an SBOM with itself returns `200` with six empty arrays
- [ ] Integration test: missing `right` param returns `400`
- [ ] Integration test (fail-closed): an unknown SBOM ID returns `404`, and the body is not an empty diff
- [ ] Integration test: the existing SBOM list and get endpoints still return `200` (route registration regression)
- [ ] Performance test: two seeded SBOMs with 2000 packages each; the compare call completes in under 1s

## Verification Commands
- `cargo test -p tests sbom` — all SBOM integration tests pass, including the new compare tests
- `curl -s "http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=<id2>" | jq 'keys'` — prints the six diff keys
- `curl -s -o /dev/null -w '%{http_code}' "http://localhost:8080/api/v2/sbom/compare?left=does-not-exist&right=<id2>"` — prints `404`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Backend: SBOM comparison model and diff service
