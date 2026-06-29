# Task 6: Add threshold query parameter support (Non-MVP)

## Repository

trustify-backend

## Target Branch

main

## Description

Add an optional `?threshold=<severity>` query parameter to `GET /api/v2/sbom/{id}/advisory-summary` that filters the severity counts to only include severities at or above the specified threshold. For example, `?threshold=high` would return counts for critical and high only, with medium and low as zero. The total should reflect only the filtered counts. This supports the alerting integration use case (UC-2) where external systems poll for critical advisories.

## Files to Modify

- `modules/fundamental/src/sbom/model/advisory_summary.rs` — Add a threshold query parameter struct (e.g., `AdvisorySummaryQuery`) for Axum's `Query` extractor
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Add query parameter extraction and pass threshold to service
- `modules/fundamental/src/sbom/service/sbom.rs` — Extend `advisory_summary` method to accept an optional threshold parameter and filter the aggregation accordingly

## API Changes

- `GET /api/v2/sbom/{id}/advisory-summary?threshold=<severity>` — MODIFY: add optional `threshold` query parameter. Valid values: `critical`, `high`, `medium`, `low`. When specified, only severities at or above the threshold are included in counts. Returns 400 for invalid threshold values.

## Implementation Notes

- Add a query parameter struct (e.g., `AdvisorySummaryQuery { threshold: Option<String> }`) in `modules/fundamental/src/sbom/model/advisory_summary.rs`, deriving `Deserialize` and `IntoParams` for OpenAPI.
- In the handler in `modules/fundamental/src/sbom/endpoints/advisory_summary.rs`, extract the query parameter using Axum's `Query<AdvisorySummaryQuery>` extractor.
- Define the severity ordering: critical > high > medium > low. When a threshold is specified, zero out the count fields for severities below the threshold, and adjust the total accordingly.
- The filtering can be done either in SQL (add a `WHERE severity >= threshold` using a CASE expression or severity rank) or in application code after the aggregation query returns (simpler, and acceptable given the small result set of 4 severity levels).
- Validate the threshold value; return 400 (`AppError::BadRequest`) for unrecognized values.
- Update the OpenAPI attributes on the handler to document the new query parameter.
- Per CONVENTIONS.md §Error handling: return `AppError::BadRequest` for invalid threshold values, using `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler file scope.
- Per CONVENTIONS.md §Endpoint registration: ensure the query parameter is properly documented in the route's OpenAPI attributes.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint handler scope.

## Reuse Candidates

- `common/src/error.rs::AppError` — `AppError::BadRequest` for invalid threshold values
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Extend existing handler from Task 3
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::advisory_summary` — Extend existing service method from Task 2
- `modules/fundamental/src/sbom/endpoints/list.rs` — Reference for query parameter extraction pattern using Axum's `Query` extractor

## Acceptance Criteria

- [ ] `?threshold=critical` returns only critical count (high, medium, low are zero), total equals critical count
- [ ] `?threshold=high` returns critical and high counts, medium and low are zero
- [ ] `?threshold=medium` returns critical, high, and medium counts, low is zero
- [ ] `?threshold=low` returns all counts (same as no threshold)
- [ ] Omitting the threshold parameter returns all counts (backward compatible)
- [ ] Invalid threshold value returns 400 with a descriptive error message
- [ ] OpenAPI docs are updated to include the query parameter

## Test Requirements

- [ ] Integration test: verify each threshold level returns correctly filtered counts
- [ ] Integration test: verify omitting threshold returns full counts (backward compatibility)
- [ ] Integration test: verify invalid threshold value returns 400
- [ ] Unit test: verify severity ordering logic

## Dependencies

- Depends on: Task 1 — Add AdvisorySeveritySummary response model
- Depends on: Task 2 — Add advisory summary aggregation to SbomService
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint

## Verification Commands

- `cargo check -p trustify-module-fundamental` — verify compilation
- `cargo test -p trustify-module-fundamental -- advisory_summary` — run unit tests
- `cargo test --test api -- sbom_advisory_summary` — run integration tests

## Documentation Updates

- REST API reference documentation — update the `GET /api/v2/sbom/{id}/advisory-summary` endpoint documentation to include the optional `threshold` query parameter, valid values, severity ordering, and filtering behavior
