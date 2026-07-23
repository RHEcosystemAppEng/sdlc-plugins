## Repository
trustify-backend

## Target Branch
main

## Description
Add support for an optional `?threshold=<severity>` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the endpoint filters severity counts to include only levels at or above the specified threshold. Valid threshold values are `critical`, `high`, `medium`, `low`. This is a non-MVP enhancement for TC-9001 that supports alerting integrations that only need to know about advisories above a certain severity level.

Severity ordering (highest to lowest): critical > high > medium > low.

Example: `?threshold=high` returns counts for `critical` and `high` only, with `medium` and `low` omitted or zeroed.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add `threshold` query parameter extraction, validate the value, and filter the `AdvisorySeveritySummary` before returning
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — add a `Severity` enum (`Critical`, `High`, `Medium`, `Low`) with ordering support, and add a filtering method on `AdvisorySeveritySummary` that zeroes out counts below the threshold

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=<severity>` — MODIFY: optional query parameter `threshold` accepts `critical`, `high`, `medium`, `low`. When set, counts for severity levels below the threshold are omitted (set to 0) and `total` reflects only the included levels. Returns 400 Bad Request for invalid threshold values.

## Implementation Notes
- Define a `Severity` enum in the model file with variants `Critical`, `High`, `Medium`, `Low` that implements `Ord` for comparison. Use Axum's query parameter extraction (`Query<ThresholdParams>`) with a struct `ThresholdParams { threshold: Option<Severity> }`.
- Per Key Conventions §Error handling: return `AppError::BadRequest` (or equivalent) with a descriptive message when the threshold value is not one of the valid severity levels.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust endpoint file scope.
- The filtering should happen at the response level (after the service returns the full summary), not at the query level. This keeps the service method simple and allows the cache to work on the full summary regardless of threshold.
- Consider the `total` field: when a threshold is applied, `total` should reflect the sum of only the included severity levels, not the original total.
- Follow the query parameter patterns used by existing list endpoints (see `common/src/db/query.rs` for shared query patterns, though this is a simpler single-parameter filter).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — the base endpoint handler (from Task 2) being extended
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — the model struct (from Task 1) being extended with filtering
- `common/src/db/query.rs` — shared query parameter patterns; reference for Axum query extraction conventions

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only `critical` count (other levels zeroed), with `total` equal to `critical`
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns `critical` and `high` counts, with `total` as their sum
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns `critical`, `high`, and `medium` counts
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (equivalent to no threshold)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all counts (backward compatible)
- [ ] Invalid threshold value returns 400 Bad Request with descriptive error message

## Test Requirements
- [ ] Integration test: `?threshold=critical` returns only critical count with correct total
- [ ] Integration test: `?threshold=high` returns critical and high counts with correct total
- [ ] Integration test: no threshold returns all severity counts (backward compatibility)
- [ ] Integration test: invalid threshold value (e.g., `?threshold=urgent`) returns 400

## Verification Commands
- `curl http://localhost:8080/api/v2/sbom/{id}/advisory-summary?threshold=critical` — verify only critical count returned
- `curl http://localhost:8080/api/v2/sbom/{id}/advisory-summary?threshold=invalid` — verify 400 response

## Dependencies
- Depends on: Task 2 — Add advisory-summary endpoint with caching
