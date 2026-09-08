## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` REST endpoint that accepts two SBOM IDs as query parameters and returns a structured diff using the SbomComparisonService created in Task 2. Register the route in the SBOM endpoint module and add integration tests.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — add route registration for the comparison endpoint
- `server/src/main.rs` — verify comparison route is mounted (should be automatic via SBOM module registration)
- `tests/api/sbom.rs` — add integration tests for the comparison endpoint

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — GET /api/v2/sbom/compare handler function

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: accepts two SBOM IDs as query parameters, returns SbomComparisonResult JSON with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes

## Implementation Notes
- Follow the existing endpoint pattern: see `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure.
- The handler should:
  1. Parse `left` and `right` query parameters (both required)
  2. Validate both IDs exist (return 404 if either SBOM is not found)
  3. Call `SbomComparisonService::compare(left_id, right_id)`
  4. Return the `SbomComparisonResult` as JSON with 200 OK
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing SBOM routes. See the existing route registration pattern in that file.
- Error responses: 400 for missing query parameters, 404 if either SBOM ID does not exist, 500 for internal errors.
- Per CONVENTIONS.md: handler returns `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` endpoint handler scope.
- Per CONVENTIONS.md: follow the endpoint registration pattern in `endpoints/mod.rs`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Performance: the non-functional requirement specifies p95 < 1s for SBOMs with up to 2000 packages. The service layer (Task 2) handles the optimization; the endpoint layer should not add significant overhead.

**Relevant constraints from docs/constraints.md:**
- Commit rules (section 2): every commit must reference TC-9003, follow Conventional Commits, include AI attribution trailer
- PR rules (section 3): branch named after Jira issue ID, PR link posted to Jira task
- Code change rules (section 5): changes scoped to listed files, inspect code before modifying, follow referenced patterns

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM GET handler, reference for handler structure and error handling pattern
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing SBOM list handler, reference for query parameter parsing
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration, follow the same pattern for the compare route
- `common/src/error.rs::AppError` — error type for handler responses

## Acceptance Criteria
- [ ] GET /api/v2/sbom/compare?left={id1}&right={id2} returns 200 with SbomComparisonResult JSON
- [ ] Missing left or right query parameter returns 400 Bad Request
- [ ] Non-existent SBOM ID for left returns 404 Not Found
- [ ] Non-existent SBOM ID for right returns 404 Not Found
- [ ] Response JSON shape matches: { added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes }
- [ ] Route is registered in the SBOM endpoint module and accessible from the server
- [ ] Integration tests cover happy path and error cases

## Test Requirements
- [ ] Integration test: compare two existing SBOMs returns 200 with valid comparison result
- [ ] Integration test: missing left parameter returns 400
- [ ] Integration test: missing right parameter returns 400
- [ ] Integration test: non-existent left SBOM ID returns 404
- [ ] Integration test: non-existent right SBOM ID returns 404
- [ ] Integration test: comparing an SBOM with itself returns empty diff (all arrays empty)

## Verification Commands
- `cargo test --test api sbom::compare` — run comparison endpoint integration tests, expect all pass
- `cargo run & curl "http://localhost:8080/api/v2/sbom/compare?left=1&right=2"` — manual verification returns JSON response

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main (trustify-backend)
- Depends on: Task 2 — Add SBOM comparison diff model and service
