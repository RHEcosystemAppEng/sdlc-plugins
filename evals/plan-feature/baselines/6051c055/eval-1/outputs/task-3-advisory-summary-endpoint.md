## Repository
trustify-backend

## Target Branch
main

## Description
Register the new GET /api/v2/sbom/{id}/advisory-summary endpoint that returns aggregated advisory severity counts for a given SBOM. The endpoint delegates to the `AdvisoryService::get_severity_summary_for_sbom` method, applies 5-minute response caching, and returns the `AdvisorySeveritySummary` response as JSON. Returns 404 if the SBOM does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register new GET route for `/api/v2/sbom/{id}/advisory-summary` and implement the handler function

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with 5-minute cache headers

## Implementation Notes
Register the route in the existing SBOM endpoint module at `modules/fundamental/src/sbom/endpoints/mod.rs`, following the pattern of sibling route registrations in the same file. The handler should extract the SBOM ID from the path parameter, call `AdvisoryService::get_severity_summary_for_sbom`, and return the result as JSON. Add `Cache-Control: max-age=300` header for 5-minute caching. Use an in-memory cache (e.g., `HashMap` with expiry timestamps behind a `RwLock` or equivalent concurrency-safe pattern) keyed by SBOM ID to avoid repeated database queries within the TTL window. Return `AppError` 404 from `common/src/error.rs` when the SBOM is not found.
Per CONVENTIONS.md §Framework: use Axum HTTP handler conventions for route registration. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint scope.
Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` for error propagation. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint scope.
Per CONVENTIONS.md §Module pattern: place the endpoint in endpoints/ following the model/ + service/ + endpoints/ module structure. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust module scope.

## Acceptance Criteria
- [ ] GET /api/v2/sbom/{id}/advisory-summary returns JSON `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Response includes `Cache-Control: max-age=300` header
- [ ] In-memory cache prevents repeated database queries within 5-minute TTL
- [ ] Returns 404 with appropriate error body when SBOM ID does not exist
- [ ] Endpoint is registered in the SBOM route group
- [ ] Counts only unique advisories (deduplicated by advisory ID)

## Test Requirements
- [ ] Integration test verifying successful response with known SBOM and advisory data
- [ ] Integration test verifying 404 response for non-existent SBOM ID
- [ ] Integration test verifying response structure matches expected JSON schema
- [ ] Integration test verifying cache header is present in response

## Dependencies
- Depends on: Task 2 — Advisory summary service
