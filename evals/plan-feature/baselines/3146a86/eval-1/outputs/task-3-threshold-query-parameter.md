# Task 3 -- Add optional threshold query parameter to advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add support for an optional `?threshold=<severity>` query parameter to the
`GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the endpoint
filters the severity counts to only include levels at or above the specified
threshold. Valid values are: `critical`, `high`, `medium`, `low`. This enables
alerting integrations to quickly check whether any advisories above a certain
severity level affect a given SBOM.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` -- add query parameter extraction and filtering logic
- `modules/fundamental/src/sbom/service/sbom.rs` -- extend the `advisory_severity_summary` method to accept an optional threshold parameter, or add filtering at the endpoint level

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` -- MODIFY: when `threshold` is provided, only severity levels at or above the threshold are included in the response. Severity ordering: critical > high > medium > low.

## Implementation Notes
- The threshold parameter defines a minimum severity level. The severity ordering is: `critical` (highest) > `high` > `medium` > `low` (lowest).
- When `?threshold=critical`, the response should only include `critical` and `total` counts (high, medium, low are omitted or set to 0).
- When `?threshold=high`, include `critical`, `high`, and `total`.
- When `?threshold=medium`, include `critical`, `high`, `medium`, and `total`.
- When `?threshold=low`, include all fields (equivalent to no filter).
- Use Axum's `Query` extractor to parse the optional query parameter. Follow the query parameter extraction pattern used by existing endpoints like `modules/fundamental/src/sbom/endpoints/list.rs` for reference.
- Consider implementing the filtering at the endpoint/handler level rather than pushing it into the service layer, since the service already returns the full aggregation. This keeps the service method reusable and pushes presentation logic to the endpoint.
- Return 400 Bad Request if the threshold value is not one of the valid severity levels.
- The `total` field should reflect only the counted severities (i.e., the sum of the included severity counts), not the total across all severities.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` -- example of query parameter extraction using Axum's `Query` extractor
- `common/src/db/query.rs` -- shared query helpers; may contain filtering utilities applicable here

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical count and total
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical, high, and total
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, medium, and total
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all severity counts
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)
- [ ] Invalid threshold value returns 400 Bad Request

## Test Requirements
- [ ] Integration test: threshold=critical returns only critical count and correct total
- [ ] Integration test: threshold=high returns critical and high counts with correct total
- [ ] Integration test: threshold=medium returns critical, high, and medium counts with correct total
- [ ] Integration test: no threshold parameter returns all severity counts (regression test)
- [ ] Integration test: invalid threshold value (e.g., ?threshold=none) returns 400

## Verification Commands
- `cargo test --test api -- advisory_summary_threshold` -- run threshold-specific integration tests

## Dependencies
- Depends on: Task 2 -- Add GET /api/v2/sbom/{id}/advisory-summary endpoint
