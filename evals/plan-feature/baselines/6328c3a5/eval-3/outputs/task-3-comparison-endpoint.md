## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Create the `GET /api/v2/sbom/compare` REST endpoint that accepts two SBOM IDs as query parameters and returns a structured comparison result. This endpoint delegates to the `SbomComparisonService` (Task 2) and exposes the comparison functionality over HTTP. Add integration tests that validate the endpoint against a real PostgreSQL test database.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler for `GET /api/v2/sbom/compare?left={id1}&right={id2}`
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route in the SBOM route group
- `server/src/main.rs` — Ensure SBOM module routes are mounted (likely already done; verify)

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparisonResult` JSON with six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Implementation Notes
Per CONVENTIONS.md §Module Pattern: register the route in `endpoints/mod.rs` following the pattern of existing routes (`list.rs`, `get.rs`).
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's endpoints/ directory scope.

Per CONVENTIONS.md §Error Handling: the handler must return `Result<Json<SbomComparisonResult>, AppError>` with `.context()` wrapping for all internal errors.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database using the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/sbom_compare.rs` matching the convention's integration test scope.

**Endpoint design:**
- Route: `GET /api/v2/sbom/compare`
- Query parameters: `left` (UUID, required), `right` (UUID, required)
- Response: `200 OK` with `SbomComparisonResult` JSON body
- Error responses: `400 Bad Request` (missing/invalid query params), `404 Not Found` (SBOM not found)
- Note: this endpoint returns a single comparison result, NOT `PaginatedResults<T>` (the comparison is a computed diff, not a paginated list)

**Route registration pattern** (follow `modules/fundamental/src/sbom/endpoints/mod.rs`):
```rust
.route("/compare", get(compare::handler))
```

**Non-functional:** p95 response time < 1s for SBOMs with up to 2000 packages each.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing endpoint handler; follow its pattern for extracting path/query params and calling the service
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing endpoint; reference for route registration pattern
- `common/src/db/query.rs` — shared query helpers; may not be needed since comparison is not paginated
- `common/src/error.rs::AppError` — standard error type for handler return types

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns `200 OK` with correct `SbomComparisonResult` JSON
- [ ] Returns `400 Bad Request` when `left` or `right` query parameter is missing
- [ ] Returns `400 Bad Request` when `left` or `right` is not a valid UUID
- [ ] Returns `404 Not Found` when either SBOM ID does not exist in the database
- [ ] Response JSON matches the expected shape: `{ added_packages: [...], removed_packages: [...], version_changes: [...], new_vulnerabilities: [...], resolved_vulnerabilities: [...], license_changes: [...] }`
- [ ] Route is registered under the `/api/v2/sbom` route group

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences and verify correct diff result
- [ ] Integration test: verify 400 response when query parameters are missing
- [ ] Integration test: verify 404 response when an SBOM ID does not exist
- [ ] Integration test: compare two identical SBOMs and verify all diff arrays are empty
- [ ] Integration test: verify new vulnerabilities include correct severity values

## Verification Commands
- `cargo test --test api sbom_compare` — run comparison endpoint integration tests
- `cargo clippy --all-targets` — verify no linting warnings in new code

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Implement SBOM comparison service and model
