# Task 3 — Add GET /api/v2/sbom/compare endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Expose the SBOM diff from Task 2 as `GET /api/v2/sbom/compare?left={id1}&right={id2}` for TC-9003 (SBOM comparison view). The frontend comparison page calls this endpoint. The URL takes both SBOM IDs as query parameters so comparisons can be shared and bookmarked (UC-2). Responses must stay under p95 1s for SBOMs with up to 2000 packages each.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/compare` route on the `/api/v2/sbom` router
- `tests/api/sbom.rs` — add integration tests for the compare endpoint
- `README.md` — add the compare endpoint to the API reference

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler: parses and validates the `left`/`right` query params, calls `SbomService::compare`, and returns JSON `SbomComparison`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparison` with `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`. 400 if a parameter is missing or malformed; 404 if either SBOM does not exist.

## Implementation Notes
- **Handler pattern**: copy the structure of `modules/fundamental/src/sbom/endpoints/get.rs`.
  - Use an `axum::extract::Query<CompareParams { left: String, right: String }>` extractor (use the same ID type `get.rs` uses for `{id}`).
  - Inject `SbomService` the way `get.rs` does.
- **Route precedence**: register `/compare` in `endpoints/mod.rs` next to the existing `/{id}` route. Axum's router prefers static segments over captures, but add an integration test that confirms `/api/v2/sbom/compare` does not reach the `get` handler.
- **Response**: return a plain `Json<SbomComparison>`. This is not `PaginatedResults`, because the Figma spec calls for one full diff with client-side virtualization instead of pagination.
- **Fail-closed validation** (gate site: `compare.rs` handler):
  - A missing `left` or `right` returns 400 via `AppError`.
  - An unknown ID returns 404, passed up from `SbomService::compare`.
  - The handler must never return 200 with empty arrays for unresolvable IDs.
- **Caching**: SBOM content is immutable once ingested, so the compare response for an ID pair can use the same `tower-http` caching configuration as the `get` route builder in `endpoints/mod.rs`.
- **Observability**:
  - Add a `tracing` span on the handler that records the `left`/`right` IDs and package counts. This provides the timing data needed for the supportability items (Grafana latency / timeout monitoring).
  - The dashboard and alert configuration itself is out of scope; see the "Excluded requirements" section of the impact map.
- Per CONVENTIONS.md §Endpoint registration: register the route in the module's `endpoints/mod.rs`. `server/main.rs` already mounts the SBOM module, so no server change is needed. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route registration scope. Example: the `list.rs`/`get.rs` registration in the same file.
- Per CONVENTIONS.md §Error handling: the handler returns `Result<Json<SbomComparison>, AppError>` with `.context()`. Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's HTTP handler scope. Example: `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Testing: integration tests go in `tests/api/` against the real PostgreSQL test DB and use `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/sbom.rs` matching the convention's integration test scope. Example: the existing tests in `tests/api/sbom.rs`.
- Constraints (docs/constraints.md):
  - §2: Conventional Commits, Jira footer, `Assisted-by` trailer
  - §3: `gh pr create --base TC-9003`, and post the PR link to Jira
  - §5: scoped changes, inspect code before modifying it, reuse, trace the data flow end to end (query params -> service -> JSON)

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — handler shape, service injection, and ID parsing for SBOM IDs
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route builder with existing caching middleware configuration
- `common/src/error.rs::AppError` — 400/404 mapping via `IntoResponse`
- `tests/api/sbom.rs` — existing SBOM fixtures and ingestion helpers for setting up two SBOMs

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with a JSON body matching the documented `SbomComparison` shape (snake_case field names)
- [ ] A missing `left` or `right` parameter returns 400
- [ ] An unknown `left` or `right` ID returns 404, not 200 with an empty diff
- [ ] `/api/v2/sbom/compare` is not captured by the `/api/v2/sbom/{id}` route
- [ ] The existing `GET /api/v2/sbom` and `GET /api/v2/sbom/{id}` behavior is unchanged
- [ ] p95 response time is under 1s for two SBOMs with 2000 packages each (measured in a local benchmark or test)
- [ ] The README documents the endpoint, its parameters, response shape, and error codes

## Test Requirements
- [ ] Integration test: ingest two SBOMs with known differences and assert each of the six arrays contains exactly the expected entries
- [ ] Integration test: missing query parameter returns `StatusCode::BAD_REQUEST`
- [ ] Integration test: nonexistent SBOM ID returns `StatusCode::NOT_FOUND`, and the body is not an empty diff (fail-closed)
- [ ] Integration test: the same ID on both sides returns 200 with all arrays empty
- [ ] Integration test: a request to `/api/v2/sbom/compare` is not routed to the get-by-ID handler
- [ ] Performance check: a test or benchmark with 2000 packages per SBOM finishes under 1s

## Verification Commands
- `cargo test -p tests sbom` — all SBOM integration tests pass, including the new compare tests
- `curl -s "http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=<id2>" | jq 'keys'` — prints the six diff keys
- `curl -s -o /dev/null -w "%{http_code}" "http://localhost:8080/api/v2/sbom/compare?left=does-not-exist&right=<id2>"` — prints `404`

## Documentation Updates
- `README.md` — add `GET /api/v2/sbom/compare` to the API endpoint list: query params, response shape, and 400/404 semantics

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison diff model and service
