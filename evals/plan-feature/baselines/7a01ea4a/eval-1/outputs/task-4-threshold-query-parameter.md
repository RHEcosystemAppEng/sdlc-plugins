## Repository
trustify-backend

## Target Branch
main

## Description
Add an optional `?threshold` query parameter to the `GET /api/v2/sbom/{id}/advisory-summary` endpoint that filters severity counts to include only severities at or above the specified threshold. This supports alerting integrations that need to check for critical advisories without retrieving the full severity breakdown. The threshold values are `critical`, `high`, `medium`, and `low` (case-insensitive). This is a non-MVP enhancement.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add `threshold` query parameter extraction using Axum's `Query` extractor; filter the response to include only severities at or above the threshold
- `modules/fundamental/src/sbom/service/sbom.rs` — extend `get_advisory_summary` to accept an optional threshold parameter, or add a separate method `get_advisory_summary_filtered` that applies the threshold filter to the aggregated counts

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — MODIFY: add optional `threshold` query parameter. When provided, only severity levels at or above the threshold are included in the response. Valid values: `critical`, `high`, `medium`, `low`. Invalid values return 400 Bad Request.

## Implementation Notes
- Use Axum's `Query<ThresholdParams>` extractor to parse the optional query parameter. Define a `ThresholdParams` struct with `threshold: Option<String>`.
- Define severity ordering: critical > high > medium > low. When threshold is `high`, return counts for `critical` and `high` only, setting `medium` and `low` to 0 (or omitting them). Recalculate `total` to reflect only the included severities.
- The filtering can be applied at the service layer (modify the SQL query to filter by severity) or at the handler layer (filter the `AdvisorySeveritySummary` after the full aggregation). The handler-layer approach is simpler and sufficient given the small response size.
- Return 400 Bad Request for invalid threshold values. Use `AppError` from `common/src/error.rs` for the error response.
- Per Key Conventions (Error handling): all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — the handler created in Task 2, which this task extends with query parameter support
- `common/src/db/query.rs` — shared query builder helpers that may include parameter validation patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical count and total
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts and total
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium counts and total
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (equivalent to no filter)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all counts (backward compatible)
- [ ] Invalid threshold value returns 400 Bad Request
- [ ] Threshold values are case-insensitive

## Test Requirements
- [ ] Integration test: each threshold level returns the correct subset of severity counts
- [ ] Integration test: total is recalculated to reflect only included severities
- [ ] Integration test: invalid threshold value returns 400
- [ ] Integration test: no threshold parameter returns full counts (backward compatibility)
- [ ] Integration test: threshold values are accepted case-insensitively

## Verification Commands
- `cargo test --test api threshold` — threshold-related integration tests pass
- `curl http://localhost:8080/api/v2/sbom/{id}/advisory-summary?threshold=critical` — returns filtered counts

## Dependencies
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
