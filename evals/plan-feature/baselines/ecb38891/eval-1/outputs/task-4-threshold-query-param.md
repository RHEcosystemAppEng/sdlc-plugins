## Repository
trustify-backend

## Target Branch
main

## Description
Add support for the optional `?threshold=critical` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When the threshold parameter is provided, the response filters severity counts to include only severities at or above the specified threshold level. The severity hierarchy is: Critical > High > Medium > Low. For example, `?threshold=high` returns counts for Critical and High only, with Medium and Low counts set to 0. This is a non-MVP requirement intended for alerting integrations that need to filter by severity level.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add query parameter extraction and threshold filtering logic
- `modules/fundamental/src/sbom/service/sbom.rs` — add optional `threshold` parameter to `get_advisory_summary` method signature

## Implementation Notes
- Add a query parameter struct (e.g., `AdvisorySummaryParams`) with an optional `threshold` field of type `Option<SeverityThreshold>` where `SeverityThreshold` is an enum with variants `Critical`, `High`, `Medium`, `Low`.
- Parse the threshold from the query string using Axum's `Query` extractor. The threshold value should be case-insensitive (accept "critical", "Critical", "CRITICAL").
- Define the severity hierarchy: Critical (4) > High (3) > Medium (2) > Low (1). When a threshold is set, zero out counts for severities below the threshold level.
- The total count should reflect only the non-zeroed severities when a threshold is applied.
- Per repo Key Conventions §Error handling: return a 400 Bad Request with a descriptive error message if the threshold value is not a recognized severity level.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — the existing endpoint handler created in Task 2
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for how severity is represented in the existing advisory model
- `common/src/db/query.rs` — query helper patterns for parameter extraction

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns counts only for Critical severity (High, Medium, Low are 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for Critical and High (Medium, Low are 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns counts for Critical, High, and Medium (Low is 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (equivalent to no threshold)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all counts (backward compatible)
- [ ] `total` field reflects the sum of non-zeroed severities when threshold is applied
- [ ] Invalid threshold value returns 400 Bad Request with descriptive error message
- [ ] Threshold parameter is case-insensitive

## Test Requirements
- [ ] Integration test for each threshold level (critical, high, medium, low) verifying correct filtering
- [ ] Integration test verifying backward compatibility when no threshold is provided
- [ ] Integration test verifying 400 response for invalid threshold value (e.g., `?threshold=unknown`)
- [ ] Integration test verifying case-insensitive threshold parsing (e.g., `?threshold=Critical`, `?threshold=CRITICAL`)

## Verification Commands
- `cargo build --workspace` — project compiles without errors
- `cargo test -p fundamental` — fundamental module tests pass

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service
- Depends on: Task 2 — Add advisory summary endpoint with caching
