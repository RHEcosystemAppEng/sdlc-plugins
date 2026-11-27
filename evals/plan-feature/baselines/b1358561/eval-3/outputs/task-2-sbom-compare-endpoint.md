# Task 2 — Add GET /api/v2/sbom/compare endpoint

**Summary:** TC-9003: Add GET /api/v2/sbom/compare endpoint
**Issue type:** Task
**Parent (Epic):** Epic 1 — TC-9003: SBOM comparison diff API
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003)

---

## Repository
trustify-backend

## Target Branch
main

## Description
Expose the SBOM diff from Task 1 over HTTP as `GET /api/v2/sbom/compare?left={id1}&right={id2}`.
This is the endpoint the frontend comparison page (TC-9003) calls, and it is also usable by
API consumers directly. The endpoint validates its query parameters, delegates to the
comparison service, and returns the `SbomComparison` JSON.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/compare` route alongside the existing list/get routes; ensure it is registered so that `compare` is not captured by the `/api/v2/sbom/{id}` path parameter route
- `tests/api/sbom.rs` — add integration tests for the compare endpoint

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler: parses `left` and `right` query params, calls the comparison service, returns `Json<SbomComparison>`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns a structured diff (`added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`) between two SBOMs. `400 Bad Request` if `left` or `right` is missing/malformed; `404 Not Found` if either SBOM does not exist.

## Implementation Notes
- Follow the handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id}) for extractor usage, service injection and response type; follow `modules/fundamental/src/sbom/endpoints/list.rs` for query-parameter extraction (`Query<…>` struct with `serde::Deserialize`).
- Define a `CompareQuery { left: <SBOM id type>, right: <SBOM id type> }` struct using the same ID type the `get.rs` handler uses for `{id}` so that malformed IDs are rejected by the extractor with 400.
- **Route ordering:** `/api/v2/sbom/compare` must be matched before `/api/v2/sbom/{id}`; with Axum's router, a static segment takes precedence over a capture, but add an integration test to prove `compare` is not parsed as an ID.
- **Fail-closed:** missing params must return 400 and unknown IDs must return 404 (propagated from the Task 1 service `AppError`), never `200` with an empty diff. Guard site: `compare.rs` handler (param extraction) and `service/compare.rs::compare` (existence check).
- **Caching:** the repository uses `tower-http` caching middleware configured in endpoint route builders. The diff is derived from immutable ingested SBOM data, so a cache policy consistent with the existing `get.rs` route is acceptable; do not enable caching that could outlive SBOM deletion without matching the existing routes' policy.
- **Observability (Customer Information/Supportability):** emit a `tracing` span on the handler including `left`, `right`, package counts and elapsed time so slow comparisons (>2000 packages) are visible in logs/metrics. (Grafana dashboard wiring is out of scope for this repo — see impact map Excluded requirements.)
- Per CONVENTIONS.md §Endpoint registration: register the route in the module's `endpoints/mod.rs`; `server/src/main.rs` already mounts the sbom module, so no change to `main.rs` is expected — verify during implementation.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `endpoints/mod.rs` route-registration scope.
- Per CONVENTIONS.md §Error handling: the handler returns `Result<Json<SbomComparison>, AppError>` and uses `.context()` wrapping; see `modules/fundamental/src/sbom/endpoints/get.rs`.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust handler `.rs` scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit the real PostgreSQL test database and assert with `assert_eq!(resp.status(), StatusCode::OK)`; follow existing tests in `tests/api/sbom.rs`.
  Applies: task modifies `tests/api/sbom.rs` matching the convention's `tests/api/*.rs` integration-test scope.
- Constraints (docs/constraints.md): §5.1 scope to listed files; §5.2 inspect before modifying; §5.8 parity with sibling handlers (`get.rs`, `list.rs`) on error handling, logging and caching; §2.1–2.3 commit rules; §3.3 PR `--base main`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — sibling single-resource handler; copy extractor/error/response pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — sibling handler with query-parameter extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration for `/api/v2/sbom`
- `tests/api/sbom.rs` — existing SBOM integration test setup (fixture ingestion, client helpers)

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns `200` with the `SbomComparison` JSON shape defined in Task 1
- [ ] Missing `left` or `right` returns `400 Bad Request`
- [ ] A non-existent `left` or `right` SBOM ID returns `404 Not Found` — not `200` with an empty diff
- [ ] `GET /api/v2/sbom/compare` is not routed to the `/api/v2/sbom/{id}` handler
- [ ] Existing `/api/v2/sbom` and `/api/v2/sbom/{id}` endpoints behave unchanged
- [ ] p95 latency < 1s when comparing two SBOMs with ~2000 packages each in the test environment

## Test Requirements
- [ ] Integration test: ingest two SBOM fixtures with known differences; assert each of the six lists contains exactly the expected entries
- [ ] Integration test: compare an SBOM with itself → `200` and all lists empty
- [ ] Integration test: missing `right` param → `400`
- [ ] Integration test: unknown SBOM ID → `404` (fail-closed: asserts the response is not a `200` empty diff)
- [ ] Integration test: existing `GET /api/v2/sbom/{id}` still returns `200` for a valid ID (route-ordering regression)
- [ ] Performance check (can be an ignored/bench test): two ~2000-package SBOMs compare in < 1s

## Verification Commands
- `cargo test -p tests sbom` — all SBOM integration tests pass, including new compare tests
- `curl -s "http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=<id2>" | jq 'keys'` — returns the six diff category keys
- `curl -s -o /dev/null -w '%{http_code}' "http://localhost:8080/api/v2/sbom/compare?left=<id1>"` — returns `400`

## Documentation Updates
- `README.md` — add `GET /api/v2/sbom/compare` to the API endpoint overview (full reference docs are covered by Task 8)

## Dependencies
- Depends on: Task 1 — Add SBOM comparison model and diff service
