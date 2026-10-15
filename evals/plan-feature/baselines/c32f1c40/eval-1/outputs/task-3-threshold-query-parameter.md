## Repository
trustify-backend

## Target Branch
main

## Description
Add an optional `?threshold=critical` query parameter to the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the response filters severity counts to only include severities at or above the specified threshold. This supports alerting integrations that only need to know about critical or high-severity advisories (UC-2 from the feature description).

This is a non-MVP requirement that enhances the advisory-summary endpoint for alerting use cases.

Severity ordering (highest to lowest): critical > high > medium > low.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Add optional `threshold` query parameter extraction and severity filtering logic
- `tests/api/sbom.rs` — Add integration tests for threshold query parameter

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={severity}` — MODIFY: Add optional `threshold` query parameter that filters counts to only include severities at or above the specified level (critical, high, medium, low)

## Implementation Notes
Add a `threshold` query parameter to the existing advisory-summary endpoint handler. Parse the value as a severity enum and filter the response to only include counts for severities at or above the threshold.

Per CONVENTIONS.md: all handlers must return `Result<T, AppError>` with `.context()` wrapping for error propagation.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md: integration tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/sbom.rs` matching the convention's `.rs` test file scope.

**Query parameter implementation:**
- Use Axum's `Query<ThresholdParams>` extractor with an `Option<Severity>` field
- Define severity ordering: Critical=4, High=3, Medium=2, Low=1
- When threshold is provided, zero out counts for severities below the threshold
- When threshold is not provided, return all counts (backward compatible)
- Invalid threshold values should return 400 Bad Request
- Recalculate `total` to reflect only the included severity counts

**Example behavior:**
- `?threshold=high` returns counts for critical and high only; medium and low are 0
- `?threshold=critical` returns count for critical only; high, medium, low are 0
- No threshold parameter returns all counts (existing behavior)

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the severity field; reference for severity enum values and ordering
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — The endpoint handler created in Task 1; extend with threshold filtering

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only the critical count with high, medium, low set to 0
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts with medium, low set to 0
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium counts with low set to 0
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (equivalent to no threshold)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all counts (backward compatible)
- [ ] Invalid threshold value returns 400 Bad Request
- [ ] `total` field reflects only the included severity counts when threshold is applied

## Test Requirements
- [ ] Integration test: threshold=critical returns only critical count, others are 0
- [ ] Integration test: threshold=high returns critical and high counts
- [ ] Integration test: threshold=medium returns critical, high, and medium counts
- [ ] Integration test: threshold=low returns all counts
- [ ] Integration test: no threshold returns all counts (backward compatibility)
- [ ] Integration test: invalid threshold value returns 400

## Verification Commands
- `cargo test --test api sbom::advisory_summary_threshold` — Run threshold-specific integration tests
- `cargo build` — Verify compilation

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model, service, and endpoint
