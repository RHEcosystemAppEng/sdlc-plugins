# Task 6 — Update advisory endpoints and integration tests

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoint handlers to work with the new enum-based status column and update all integration tests to verify the new behavior. Ensure the endpoint response shape remains unchanged (status as string) while the underlying queries use the enum column. Remove any remaining references to the `advisory_status` table across the codebase.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if any status-related route parameters reference the old lookup table
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter parameter handling to use enum comparison instead of join-based lookup
- `modules/fundamental/src/advisory/endpoints/get.rs` — update advisory detail response construction to use enum column
- `tests/api/advisory.rs` — update integration tests: remove any test setup that seeds the `advisory_status` table; update assertions to verify status comes from enum column; add test for status filtering with enum values

## Implementation Notes
- Endpoint handlers in `modules/fundamental/src/advisory/endpoints/` return `Result<T, AppError>` using the pattern from `common/src/error.rs`
- List endpoint in `list.rs` uses `PaginatedResults<AdvisorySummary>` from `common/src/model/paginated.rs` — the response wrapper does not change
- Status filter query parameters should accept string values matching the enum variants (New, Analyzing, Fixed, Rejected) — parse them into `AdvisoryStatusEnum` variants before querying
- Integration tests in `tests/api/advisory.rs` follow the pattern in `tests/api/sbom.rs` — use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- The route registration in `modules/fundamental/src/advisory/endpoints/mod.rs` is mounted by `server/src/main.rs` — verify no changes needed there
- Search for any remaining references to `advisory_status` across the codebase (Cargo.toml dependencies, module re-exports, search service) and remove them
- The `modules/search/src/service/mod.rs` may index advisory status — if so, update the search indexing to use the enum column

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for list endpoint pattern without lookup table joins
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for detail endpoint response construction
- `tests/api/sbom.rs` — reference for integration test patterns
- `common/src/db/query.rs` — shared filtering helpers for query parameter parsing

## Acceptance Criteria
- [ ] Advisory list endpoint (`GET /api/v2/advisory`) returns advisories with status from enum column
- [ ] Advisory detail endpoint (`GET /api/v2/advisory/{id}`) returns advisory with status from enum column
- [ ] Status filter parameter works correctly with enum values
- [ ] Response shape is unchanged — status field is still a string value
- [ ] No references to `advisory_status` table remain anywhere in the codebase
- [ ] All integration tests pass with the new schema

## Test Requirements
- [ ] Integration test: `GET /api/v2/advisory` returns list with correct status values
- [ ] Integration test: `GET /api/v2/advisory?status=Fixed` filters correctly using enum
- [ ] Integration test: `GET /api/v2/advisory/{id}` returns detail with correct status
- [ ] Integration test: verify response shape matches previous format (status as string)
- [ ] Verify no test setup code references `advisory_status` table

## Verification Commands
- `cargo test --test api -- advisory` — advisory endpoint integration tests pass
- `cargo test` — full test suite passes with no references to dropped table

## Documentation Updates
- `README.md` — update any architecture or schema documentation that references the `advisory_status` lookup table pattern

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and model to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly

---
Description Digest: sha256-md:53021e58626e72a0bf3650a21a6ee62342c0cb1b0de2436aa81a8ed811df58b6
Priority: High
Fix Versions: RHTPA 2.0.0
