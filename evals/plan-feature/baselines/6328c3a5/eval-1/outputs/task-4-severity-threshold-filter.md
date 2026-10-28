## Repository
trustify-backend

## Target Branch
main

## Description
Add an optional `?threshold` query parameter to the `GET /api/v2/sbom/{id}/advisory-summary` endpoint that filters severity counts to include only severities at or above the specified threshold level. This enables alerting integrations to efficiently check for advisories above a certain severity without processing the full breakdown (Non-MVP requirement).

Valid threshold values: `critical`, `high`, `medium`, `low`. When the threshold is `critical`, only the `critical` and `total` counts are returned. When `high`, `critical` and `high` counts are included, and so on.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add `threshold` query parameter parsing and response filtering logic
- `modules/fundamental/src/sbom/service/sbom.rs` — update `aggregate_advisory_severity` method to accept an optional threshold parameter and filter results accordingly
- `tests/api/advisory_summary.rs` — add integration tests for threshold filtering scenarios

## Implementation Notes
- Per CONVENTIONS.md §Error Handling: return a 400 Bad Request `AppError` for invalid threshold values. Use `.context()` wrapping for error propagation.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` handler scope.
- Per CONVENTIONS.md §Framework: use Axum's `Query` extractor to parse the optional `threshold` query parameter from the request URL.
  Applies: convention has no file-type restriction (broadly applicable).
- Define a severity ordering: `critical > high > medium > low`. When threshold is set, zero out counts for severities below the threshold level and recalculate the `total` to reflect only the included severities.
- The threshold parameter should be case-insensitive for usability (accept `CRITICAL`, `Critical`, `critical`).
- Consider defining a `Severity` enum with an ordering implementation to make the threshold comparison clean and type-safe.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — the base endpoint handler created in Task 1, which this task extends with query parameter support
- `common/src/db/query.rs` — shared query builder helpers that may provide patterns for adding filter conditions

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only `critical` and `total` counts (other severities zeroed or omitted)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns `critical`, `high`, and `total` counts
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns `critical`, `high`, `medium`, and `total` counts
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all severity counts (equivalent to no threshold)
- [ ] Invalid threshold value (e.g., `?threshold=unknown`) returns 400 Bad Request with a descriptive error message
- [ ] Omitting the threshold parameter returns all severity counts (backward compatible with Task 1 behavior)

## Test Requirements
- [ ] Test each threshold level returns the correct subset of severity counts
- [ ] Test that an invalid threshold value (e.g., `?threshold=unknown`) returns 400
- [ ] Test that omitting the threshold parameter returns the full severity breakdown
- [ ] Test threshold parameter case-insensitivity (e.g., `?threshold=CRITICAL` works the same as `?threshold=critical`)

## Verification Commands
- `cargo test --package tests -- advisory_summary` — run integration tests including threshold scenarios

## Documentation Updates
- REST API reference — document the optional `?threshold` query parameter with valid values and filtering behavior

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation endpoint (the base endpoint must exist before adding the threshold filter)
