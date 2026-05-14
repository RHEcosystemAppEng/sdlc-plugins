# Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint `GET /api/v2/sbom/{id}/license-report` that returns a license compliance report for a given SBOM. The endpoint delegates to the license report service (Task 2) and returns the structured compliance report as JSON. This is the user-facing API that compliance teams and CI/CD pipelines will call.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/license_report.rs` — Axum handler for GET /api/v2/sbom/{id}/license-report

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new license-report route alongside existing SBOM routes
- `server/src/main.rs` — No changes expected if SBOM module routes are already mounted; verify this during implementation

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns a license compliance report for the specified SBOM. Response shape: `{ groups: [{ license: string, packages: [{ name: string, version: string, transitive: bool }], compliant: bool }], summary: { total_packages: number, compliant_count: number, non_compliant_count: number } }`

## Implementation Notes
- Follow the existing endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` — the handler should:
  1. Extract the SBOM ID from the path using Axum's `Path` extractor
  2. Extract the license policy from Axum shared state
  3. Call the license report service to generate the report
  4. Return the report as `Json<LicenseComplianceReport>`
  5. Handle errors using `Result<Json<LicenseComplianceReport>, AppError>` with `.context()` wrapping
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for existing routes (e.g., `get.rs`, `list.rs`). The route should be nested under the existing `/api/v2/sbom` prefix as `/{id}/license-report`.
- See `modules/fundamental/src/advisory/endpoints/mod.rs` for a second example of route registration in a different module — consistency across modules is important.
- The endpoint must NOT require new database tables per the non-functional requirements.
- Per docs/constraints.md section 2 (Commit Rules): commits must reference TC-9004, follow Conventional Commits, and include the `Assisted-by: Claude Code` trailer.
- Per docs/constraints.md section 3 (PR Rules): feature branch must be named after the Jira issue ID; PR link must be posted to Jira.
- Per docs/constraints.md section 5 (Code Change Rules): inspect existing code before modifying, follow patterns in Implementation Notes, do not duplicate existing functionality.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — GET /api/v2/sbom/{id} handler pattern (path extraction, service call, JSON response)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Route registration pattern for SBOM sub-routes
- `common/src/error.rs` — AppError for error response handling

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/license-report` returns 200 with a valid LicenseComplianceReport JSON body
- [ ] Response groups packages by license type with correct `compliant` flags
- [ ] Transitive dependency licenses are included in the report
- [ ] Non-existent SBOM ID returns 404 with an appropriate error message
- [ ] Response time is within the p95 < 500ms budget for SBOMs with up to 1000 packages

## Test Requirements
- [ ] Integration test: valid SBOM ID returns 200 with expected report structure
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: SBOM with mixed compliant and non-compliant licenses returns correct compliance flags
- [ ] Integration test: SBOM with no packages returns an empty report (200, empty groups)
- [ ] Integration test: response Content-Type is application/json

## Verification Commands
- `cargo test --test api license_report` — all license report integration tests pass

## Documentation Updates
- `README.md` — Add the new license-report endpoint to the API endpoint listing if one exists

## Dependencies
- Depends on: Task 2 — Add license report model and service logic
