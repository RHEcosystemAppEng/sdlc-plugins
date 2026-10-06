## Repository
trustify-backend

## Target Branch
main

## Description
Add support for the optional `?threshold` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the endpoint filters severity counts to include only levels at or above the specified threshold. This enables alerting integrations to check for critical-or-above advisories without processing all severity levels.

Severity hierarchy (highest to lowest): Critical > High > Medium > Low.

Examples:
- `?threshold=critical` returns only `{ "critical": N, "total": N }`
- `?threshold=high` returns `{ "critical": N, "high": N, "total": N }`
- `?threshold=medium` returns `{ "critical": N, "high": N, "medium": N, "total": N }`
- No threshold parameter returns all four levels (existing behavior)

This is a non-MVP enhancement.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add `threshold` query parameter extraction and validation
- `modules/fundamental/src/sbom/service/advisory_summary.rs` — add threshold filtering to the aggregation method or add a post-query filter

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={level}` — MODIFY: add optional `threshold` query parameter accepting values `critical`, `high`, `medium`, `low`; invalid values return 400 Bad Request

## Implementation Notes
- Add a `ThresholdQuery` struct with an optional `threshold` field for Axum query parameter extraction. Use `#[serde(default)]` for the optional field.
- Define a severity ordering (Critical=4, High=3, Medium=2, Low=1) to determine which levels are "at or above" the threshold.
- The threshold filter can be applied either at the database query level (more efficient, filters rows before aggregation) or as a post-query filter on the `AdvisorySeveritySummary` struct (simpler, zero fields below threshold). Choose the approach that aligns with the existing query pattern from Task 1.
- When levels are filtered out, they should be omitted from the response entirely (not set to 0). The `total` field should reflect only the counts of included severity levels.
- Return 400 Bad Request for unrecognized threshold values.
- Follow existing query parameter patterns in `modules/fundamental/src/sbom/endpoints/list.rs` for parameter extraction and validation.
- Per repo conventions: use shared filtering/pagination helpers from `common/src/db/query.rs` if applicable.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — query parameter extraction pattern for Axum handlers
- `common/src/db/query.rs` — shared query builder helpers for filtering

## Acceptance Criteria
- [ ] `?threshold=critical` returns only critical count and total
- [ ] `?threshold=high` returns critical and high counts and total
- [ ] `?threshold=medium` returns critical, high, and medium counts and total
- [ ] `?threshold=low` returns all four severity levels (equivalent to no threshold)
- [ ] No threshold parameter returns all four severity levels (backward compatible)
- [ ] Invalid threshold value returns 400 Bad Request
- [ ] `total` reflects only the sum of included severity levels

## Test Requirements
- [ ] Integration test: each valid threshold value returns the correct subset of severity levels
- [ ] Integration test: no threshold returns all levels (backward compatibility)
- [ ] Integration test: invalid threshold value returns 400
- [ ] Integration test: total field correctly sums only included levels

## Verification Commands
- `cargo test --test api -- advisory_summary` — run integration tests including threshold scenarios

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and severity aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache
