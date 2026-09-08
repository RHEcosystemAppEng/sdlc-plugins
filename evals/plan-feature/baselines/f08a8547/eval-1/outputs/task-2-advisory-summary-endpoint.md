## Repository
trustify-backend

## Target Branch
main

## Description
Add the `GET /api/v2/sbom/{id}/advisory-summary` REST endpoint that returns aggregated advisory severity counts for a given SBOM (TC-9001). The endpoint calls the `SbomService::advisory_severity_counts` method (from Task 1) and returns the result as JSON. It includes a 5-minute cache TTL using `tower-http` caching middleware and supports an optional `?threshold=<severity>` query parameter to filter counts at or above a given severity level.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `advisory-summary` route under `/api/v2/sbom/{id}`

## Files to Create
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — handler for `GET /api/v2/sbom/{id}/advisory-summary` with optional `threshold` query parameter and 5-minute cache configuration

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` as JSON
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — NEW: filters counts to severity levels at or above the given threshold (non-MVP)

## Implementation Notes
- Follow the pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure: extract path parameters, call the service method, return JSON response.
- Define a `ThresholdQuery` struct (deriving `Deserialize`) with an optional `threshold` field for the query parameter. Parse severity values as case-insensitive enum variants.
- When `threshold` is provided, filter the `AdvisorySeverityCounts` response to include only severity levels at or above the threshold. The severity hierarchy is: Critical > High > Medium > Low. For example, `?threshold=high` returns `critical`, `high`, and `total` (recalculated for the filtered levels), with `medium` and `low` set to 0 or omitted.
- Configure a 5-minute cache TTL using `tower-http` `CacheControl` or the project's existing cache configuration pattern in endpoint route builders.
- Return 404 via `AppError` when the SBOM ID does not exist.
- Per CONVENTIONS.md §Endpoint Registration: register the new route in `endpoints/mod.rs` using the same pattern as existing routes (`list.rs`, `get.rs`). See `modules/fundamental/src/sbom/endpoints/mod.rs` for the registration pattern.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Error Handling: the handler must return `Result<T, AppError>` and use `.context()` wrapping on fallible operations.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler scope.
- Per CONVENTIONS.md §Caching: use `tower-http` caching middleware with cache configuration in the endpoint route builder. See existing endpoint route builders for the pattern.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing `GET /api/v2/sbom/{id}` handler; follow the same structure for path parameter extraction, service invocation, and JSON response
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern; use the same `Router` method chain to add the new route
- `common/src/error.rs::AppError` — error handling; use `AppError::NotFound` (or equivalent) for missing SBOM

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with JSON body `{ critical: N, high: N, medium: N, low: N, total: N }` for a valid SBOM
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns 404 when the SBOM ID does not exist
- [ ] Response includes appropriate cache headers (5-minute TTL)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical count and adjusted total (non-MVP)
- [ ] Severity counts reflect only unique advisories (deduplication by advisory ID)

## Test Requirements
- [ ] Test that the endpoint returns 200 with correct JSON shape for a valid SBOM
- [ ] Test that the endpoint returns 404 for a non-existent SBOM ID
- [ ] Test that the `threshold` query parameter filters severity counts correctly
- [ ] Test that cache headers are present in the response

## Verification Commands
- `cargo test --test api -- advisory_summary` — run advisory-summary integration tests
- `curl -i http://localhost:8080/api/v2/sbom/{id}/advisory-summary` — verify response shape and cache headers

## Dependencies
- Depends on: Task 1 — Add advisory severity count model and service method
