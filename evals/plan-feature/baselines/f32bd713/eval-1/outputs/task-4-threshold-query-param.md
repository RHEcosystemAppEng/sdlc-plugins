## Repository
trustify-backend

## Target Branch
main

## Description
Add support for the optional `?threshold=critical` query parameter on the GET /api/v2/sbom/{id}/advisory-summary endpoint. When the threshold parameter is provided, the response includes only severity counts at or above the specified severity level. For example, `?threshold=high` returns counts for critical and high only (medium and low are omitted or zero). This supports alerting integrations that poll for advisories above a severity threshold. This is a non-MVP enhancement.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` -- add optional `threshold` query parameter extraction using Axum's `Query<>` extractor; pass the threshold to the service method; filter or zero out severity levels below the threshold in the response
- `modules/fundamental/src/sbom/service/sbom.rs` -- extend `get_advisory_summary` to accept an optional threshold parameter and filter the aggregation query or post-filter the counts
- `tests/api/sbom.rs` -- add integration tests for threshold filtering behavior

## Implementation Notes
- Define a severity ordering: Critical > High > Medium > Low. When `?threshold=high` is specified, include only Critical and High counts; set Medium, Low to zero or omit them. The total should reflect only the included severities.
- Parse the threshold parameter as a case-insensitive string matching one of: "critical", "high", "medium", "low". Return 400 Bad Request for invalid values.
- Follow the query parameter extraction pattern used in `modules/fundamental/src/sbom/endpoints/list.rs` for optional query parameters. Use Axum's `Query<ThresholdParams>` extractor with an `Option<String>` field for the threshold.
- The filtering can happen at the service layer (modify the aggregation SQL to exclude lower severities) or at the endpoint layer (post-filter the AdvisorySeveritySummary). Prefer service-layer filtering for efficiency.
- Per CONVENTIONS.md §Error Handling: return a 400 Bad Request via AppError when an invalid threshold value is provided. See `common/src/error.rs` for existing error variants. Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler file scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/sbom.rs` for threshold filtering. Applies: task modifies `tests/api/sbom.rs` matching the convention's test file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` -- demonstrates optional query parameter extraction with Axum Query<> extractor
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- contains the severity field type and possible enum values for severity ordering

## Acceptance Criteria
- [ ] GET /api/v2/sbom/{id}/advisory-summary?threshold=critical returns only the critical count and total
- [ ] GET /api/v2/sbom/{id}/advisory-summary?threshold=high returns critical and high counts and total
- [ ] GET /api/v2/sbom/{id}/advisory-summary?threshold=medium returns critical, high, and medium counts and total
- [ ] GET /api/v2/sbom/{id}/advisory-summary?threshold=low returns all counts (same as no threshold)
- [ ] GET /api/v2/sbom/{id}/advisory-summary without threshold parameter returns all counts (backward compatible)
- [ ] GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid returns 400 Bad Request
- [ ] The total field reflects only the included severity levels when threshold is applied

## Test Requirements
- [ ] Integration test: call with `?threshold=critical` on an SBOM with advisories at all severity levels; verify only critical count is non-zero and total matches critical count
- [ ] Integration test: call with `?threshold=high`; verify critical and high counts are present, medium and low are zero
- [ ] Integration test: call without threshold parameter; verify all severity counts are returned (backward compatibility)
- [ ] Integration test: call with `?threshold=invalid`; verify 400 Bad Request response

## Dependencies
- Depends on: Task 2 -- Add advisory-summary endpoint with caching
