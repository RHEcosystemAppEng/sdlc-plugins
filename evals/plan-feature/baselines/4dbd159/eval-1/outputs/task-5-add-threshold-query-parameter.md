# Task 5 -- Add optional threshold query parameter to advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add support for an optional `?threshold=critical` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the response filters severity counts to include only levels at or above the specified threshold (e.g., `?threshold=high` returns counts for `critical` and `high` only, with `medium` and `low` as zero). This supports alerting integrations that need to check for critical or high-severity advisories without processing all severity levels.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` -- add `threshold` query parameter extraction and filtering logic
- `modules/fundamental/src/sbom/service/sbom.rs` -- optionally extend `get_advisory_summary` to accept a threshold filter parameter, or handle filtering at the endpoint layer

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={severity}` -- MODIFY: add optional `threshold` query parameter; accepted values: `critical`, `high`, `medium`, `low`; when provided, severity counts below the threshold are returned as zero

## Implementation Notes
- **Severity ordering**: Define a severity hierarchy: Critical > High > Medium > Low. When `threshold=high`, return counts for Critical and High; set Medium and Low to zero in the response. The `total` field should reflect only the counted (above-threshold) advisories.
- **Query parameter extraction**: Use Axum's `Query` extractor to parse the optional `threshold` parameter. Define a `AdvisorySummaryParams` struct (or add to the existing handler params) with `threshold: Option<String>` (or an enum `SeverityThreshold`).
- **Validation**: Return 400 Bad Request if an invalid threshold value is provided (e.g., `?threshold=unknown`). Use the same error handling pattern as other endpoints.
- **Filtering approach**: Two options -- filter at the SQL query level (add a `WHERE severity IN (...)` clause) or filter at the application level after aggregation (zero out below-threshold counts). The SQL approach is more efficient but either is acceptable given the small result set.
- Follow the pattern for query parameter handling in existing list endpoints, e.g., `modules/fundamental/src/sbom/endpoints/list.rs` for how query parameters are extracted and validated.
- This is a non-MVP requirement. It should be implemented as a backward-compatible addition -- the endpoint must continue to work without the parameter.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference for query parameter extraction patterns using Axum's `Query` extractor
- `common/src/db/query.rs` -- shared query helpers for filtering; may contain patterns for enum-based query parameters
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- contains the severity field definition; reference for how severity values are represented

## Acceptance Criteria
- [ ] `?threshold=critical` returns only critical count (high, medium, low are zero)
- [ ] `?threshold=high` returns critical and high counts (medium, low are zero)
- [ ] `?threshold=medium` returns critical, high, and medium counts (low is zero)
- [ ] `?threshold=low` returns all counts (equivalent to no threshold)
- [ ] Omitting the threshold parameter returns all counts (backward compatible)
- [ ] Invalid threshold values return 400 Bad Request
- [ ] `total` field reflects only the above-threshold advisory count

## Test Requirements
- [ ] Integration test: `?threshold=critical` filters correctly
- [ ] Integration test: `?threshold=high` filters correctly
- [ ] Integration test: no threshold parameter returns all counts (backward compatible)
- [ ] Integration test: invalid threshold value returns 400

## Verification Commands
- `cargo test --package fundamental -- sbom::endpoints::test_advisory_summary_threshold` -- threshold filtering tests pass
- `curl -s "http://localhost:8080/api/v2/sbom/{id}/advisory-summary?threshold=critical" | jq .` -- returns only critical count

## Dependencies
- Depends on: Task 3 -- Add GET /api/v2/sbom/{id}/advisory-summary endpoint
