# Task 6 — Add optional threshold query parameter to advisory summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add support for the optional `?threshold=critical` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When the threshold parameter is provided, the response should only include severity counts at or above the specified severity level. For example, `?threshold=high` would return counts for `critical` and `high` only, with `medium` and `low` set to zero (or omitted). This supports alerting integrations that only care about advisories above a certain severity threshold. This is a non-MVP enhancement.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add query parameter extraction and pass threshold to the service method
- `modules/fundamental/src/sbom/service/sbom.rs` — modify `advisory_summary` method to accept an optional threshold parameter and filter severity counts accordingly

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={severity}` — MODIFY: add optional `threshold` query parameter. Valid values: `critical`, `high`, `medium`, `low`. When specified, counts for severity levels below the threshold are zeroed out. Without the parameter, behavior is unchanged (all severity counts returned).

## Implementation Notes
- Define severity ordering: critical > high > medium > low. When `threshold=high`, include counts for `critical` and `high`; zero out `medium` and `low`. Adjust `total` to reflect only the filtered counts.
- Extract the `threshold` query parameter using Axum's `Query` extractor. The parameter is optional — when absent, the endpoint behaves identically to the base implementation (all severity counts returned).
- The threshold filtering can be applied either at the database query level (by adding a WHERE clause to filter severities) or at the application level (by zeroing out counts below the threshold after the query). Database-level filtering is preferred for efficiency.
- Validate the threshold parameter value. If an invalid severity level is provided, return 400 Bad Request with a descriptive error message.
- Update the `utoipa` OpenAPI annotations on the handler to document the new query parameter.
- Per docs/constraints.md Section 5 (Code Change Rules): changes must be scoped to the files listed; code must not be modified without first inspecting it; implementation must follow the patterns referenced in these notes.
- Per docs/constraints.md Section 2 (Commit Rules): every commit must reference TC-9001, follow Conventional Commits, and include the AI assistance trailer.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — the existing endpoint handler to extend with query parameter support
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates query parameter extraction patterns (e.g., pagination, sorting parameters)
- `common/src/db/query.rs` — shared query helpers that may include patterns for optional filtering

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only the critical count (high, medium, low are zero)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts (medium and low are zero)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium counts (low is zero)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all severity counts (equivalent to no threshold)
- [ ] `total` field reflects the sum of only the filtered severity counts
- [ ] Endpoint without `threshold` parameter behaves identically to before (backward compatible)
- [ ] Invalid threshold value returns 400 Bad Request

## Test Requirements
- [ ] Integration test: `?threshold=critical` returns only critical count with other levels zeroed
- [ ] Integration test: `?threshold=high` returns critical and high counts
- [ ] Integration test: `?threshold=medium` returns critical, high, and medium counts
- [ ] Integration test: `?threshold=low` returns all counts (same as no threshold)
- [ ] Integration test: no threshold parameter returns all counts (backward compatibility)
- [ ] Integration test: invalid threshold value (e.g., `?threshold=invalid`) returns 400 Bad Request
- [ ] Integration test: total field is correctly computed as the sum of filtered counts only

## Verification Commands
- `cargo build` — full project compiles
- `cargo test --test api advisory_summary` — advisory summary tests pass
- `cargo test --test api` — all integration tests pass

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 5 — Add integration tests for advisory summary endpoint
