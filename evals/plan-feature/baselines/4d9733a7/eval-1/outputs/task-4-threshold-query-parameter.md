## Repository
trustify-backend

## Target Branch
main

## Description
Add support for the optional `?threshold=critical` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the response filters severity counts to only include severities at or above the specified threshold level. The severity ordering from highest to lowest is: critical, high, medium, low. For example, `?threshold=high` returns counts for critical and high only, with medium, low, and total adjusted accordingly. This is a non-MVP requirement intended for alerting integrations that need to check for advisories above a severity threshold.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add query parameter extraction for `threshold` and pass it to the service method
- `modules/fundamental/src/sbom/service/sbom.rs` — extend `advisory_severity_summary` to accept an optional threshold parameter and filter counts accordingly

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={level}` — MODIFY: add optional `threshold` query parameter accepting values `critical`, `high`, `medium`, `low`; when set, only severity levels at or above the threshold are included in the response, and `total` reflects the filtered sum

## Implementation Notes
- Add a query parameter struct (e.g., `AdvisorySummaryQuery`) with an optional `threshold` field. Use Axum's `Query` extractor pattern, following the pattern in `modules/fundamental/src/sbom/endpoints/list.rs` for query parameter handling.
- Define a severity ordering: critical > high > medium > low. When threshold is set, zero out counts for severities below the threshold and recalculate `total`.
- The threshold filter can be applied after the aggregation query returns full counts — no need to modify the database query itself.
- Invalid threshold values should return 400 Bad Request with a descriptive error message.
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` for validation errors on the threshold parameter.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing endpoint with query parameter extraction; follow its pattern for `Query` extractor
- `common/src/db/query.rs` — query builder with filtering helpers

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only the critical count and total
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts with adjusted total
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)
- [ ] Invalid threshold values return 400 Bad Request

## Test Requirements
- [ ] Integration test: threshold=critical returns only critical count with correct total
- [ ] Integration test: threshold=high returns critical and high counts with correct total
- [ ] Integration test: threshold=medium returns critical, high, and medium counts with correct total
- [ ] Integration test: no threshold parameter returns all counts (backward compatibility)
- [ ] Integration test: invalid threshold value returns 400 Bad Request

## Dependencies
- Depends on: Task 2 — Add advisory-summary endpoint with caching
