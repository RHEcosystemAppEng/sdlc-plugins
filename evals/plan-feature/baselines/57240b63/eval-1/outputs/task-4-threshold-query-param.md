## Repository
trustify-backend

## Target Branch
main

## Description
Add support for the optional `?threshold=critical` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the response filters severity counts to include only severities at or above the specified threshold level (e.g., `?threshold=high` returns counts for critical and high only, with medium and low set to zero). This enables alerting integrations to quickly check whether an SBOM has any advisories above a given severity without processing the full breakdown.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add `Query<ThresholdParams>` extractor to the handler; define `ThresholdParams` struct with an optional `threshold` field; apply threshold filtering to the summary before returning
- `modules/fundamental/src/sbom/service/sbom.rs` — optionally extend the aggregation method to accept a threshold parameter, or apply filtering at the endpoint layer after retrieving the full summary

## Implementation Notes
- Define a `ThresholdParams` struct with `#[derive(Deserialize)]` containing `threshold: Option<SeverityThreshold>` where `SeverityThreshold` is an enum with variants `Critical`, `High`, `Medium`, `Low` (derive `Deserialize` with `#[serde(rename_all = "lowercase")]`).
- Use Axum's `Query<ThresholdParams>` extractor alongside the existing `Path<Uuid>` extractor in the handler function signature.
- Threshold filtering logic: when `threshold` is `Some(level)`, zero out severity counts below the threshold. The severity hierarchy is: Critical > High > Medium > Low. For `?threshold=high`, set `medium = 0` and `low = 0`; recalculate `total` as the sum of non-zeroed fields.
- Filtering can be applied at the endpoint layer (post-query) rather than modifying the SQL query — this keeps the service method simple and the filter logic testable independently.
- Follow the query parameter extraction pattern from `modules/fundamental/src/sbom/endpoints/list.rs` which already uses `Query<>` extractors for pagination and filtering.
- Per Key Conventions §Error handling: return `Result<T, AppError>` and handle invalid threshold values gracefully (Axum's query deserialization returns 400 automatically for invalid enum values). Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for `Query<>` extractor usage pattern in an endpoint handler
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — the endpoint handler created in Task 3, to be extended with the new parameter

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only the critical count (high, medium, low are zero)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts (medium, low are zero)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium counts (low is zero)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (no filtering, equivalent to omitting the parameter)
- [ ] Omitting the threshold parameter returns the full severity breakdown (backward compatible)
- [ ] Invalid threshold values return 400 Bad Request
- [ ] `total` field is recalculated to reflect only the non-zeroed counts

## Test Requirements
- [ ] Integration test: verify each threshold level filters counts correctly
- [ ] Integration test: verify omitting the parameter returns full counts
- [ ] Integration test: verify invalid threshold value returns 400

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-tests -- advisory_summary` — tests pass

## Dependencies
- Depends on: Task 3 — Implement GET /api/v2/sbom/{id}/advisory-summary endpoint with caching

## Jira Fields
- **Labels:** ai-generated-jira
- **Priority:** Major
- **Fix Versions:** RHTPA 1.5.0

[sdlc-workflow] Description digest: sha256-md:9a9a39cc94ebd5ece130be05064fc2b99ebd335d82dee9815a2a538668e02a3d
