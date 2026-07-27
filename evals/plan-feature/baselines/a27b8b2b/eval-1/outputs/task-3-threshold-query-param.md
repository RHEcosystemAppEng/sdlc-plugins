# Task 3 — Add threshold query parameter to advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add support for an optional `?threshold=critical|high|medium|low` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the response filters severity counts to include only severities at or above the specified threshold level (e.g., `?threshold=high` returns counts for `critical` and `high` only, with `medium`, `low` set to zero and `total` reflecting the filtered sum). This enables alerting integrations to poll for critical/high severity advisories without processing the full breakdown.

Note: This is a non-MVP requirement — it serves alerting integration use cases.

## Files to Modify
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — add a `SeverityThreshold` enum (`Critical`, `High`, `Medium`, `Low`) with ordering/comparison support, and add a method on `AdvisorySeveritySummary` to filter counts by threshold
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add `threshold` as an optional Axum query parameter, apply filtering to the service response before returning
- `modules/fundamental/src/sbom/service/sbom.rs` — optionally accept a threshold parameter in the `advisory_summary` method signature, or filter at the endpoint layer after the full query

## Implementation Notes
- Define a `SeverityThreshold` enum in the model file. Implement `Deserialize` for URL query parsing (Axum uses serde for query parameter deserialization). The enum values should be case-insensitive for user convenience (e.g., `Critical`, `critical`, `CRITICAL` all accepted).
  Applies: task modifies `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's Rust model scope.
- Use Axum's `Query<ThresholdParams>` extractor with an `Option<SeverityThreshold>` field. See existing list endpoints (e.g., `modules/fundamental/src/sbom/endpoints/list.rs`) for the query parameter extraction pattern.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust endpoint scope.
- The threshold filtering can be applied either at the database query level (more efficient — only count matching severities) or at the application level (simpler — query all, then zero out below-threshold counts). Given the performance requirement (p95 < 200ms), either approach is acceptable for up to 500 advisories. Choose the simpler application-level approach unless profiling indicates otherwise.
- Severity ordering for threshold comparison: Critical > High > Medium > Low. When `threshold=high`, include Critical and High counts; set Medium and Low to 0; recalculate `total`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates Axum query parameter extraction pattern using `Query<T>` extractor
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field type; reference for severity level values

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical count (high, medium, low are 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts (medium, low are 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium counts (low is 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (same as no threshold)
- [ ] `total` field reflects the sum of the filtered (non-zero) counts
- [ ] Omitting the `threshold` parameter returns all counts (backward compatible)
- [ ] Invalid threshold value returns 400 Bad Request

## Test Requirements
- [ ] Integration test: `?threshold=critical` returns only critical count
- [ ] Integration test: `?threshold=high` returns critical + high counts
- [ ] Integration test: no threshold returns all counts (backward compatibility)
- [ ] Integration test: invalid threshold value (e.g., `?threshold=unknown`) returns 400

## Verification Commands
- `cargo build -p fundamental` — compiles without errors
- `cargo test -p fundamental -- advisory_summary` — all tests pass including threshold tests

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
