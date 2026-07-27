## Repository
trustify-backend

## Target Branch
main

## Description
Add optional `?threshold=critical` query parameter support to the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When the threshold parameter is provided, the endpoint filters severity counts to include only severities at or above the specified threshold level. The severity hierarchy is: critical > high > medium > low. For example, `?threshold=high` returns counts for critical and high only, with medium and low set to 0. This supports alerting integrations that need to check for advisories above a specific severity level (UC-2 in TC-9001). This is a non-MVP requirement.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add `Query<ThresholdParams>` extractor to the handler; filter response fields based on threshold
- `modules/fundamental/src/sbom/service/sbom.rs` — add optional `threshold` parameter to `advisory_severity_summary` method signature to push filtering to the query level

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={severity}` — MODIFY: add optional query parameter `threshold` accepting values `critical`, `high`, `medium`, `low`; when set, only counts at or above the threshold severity are included (lower severities return 0)

## Implementation Notes
- Define a `ThresholdParams` struct with `threshold: Option<SeverityThreshold>` and derive `Deserialize` for Axum's `Query` extractor. Define `SeverityThreshold` as an enum with variants `Critical`, `High`, `Medium`, `Low` and implement custom deserialization for case-insensitive matching.
- The threshold filtering can be applied either at the SQL level (add a `WHERE severity >= threshold` clause) or at the application level (zero out fields below the threshold). Prefer SQL-level filtering for consistency with the caching layer — different threshold values should be cached separately.
- When `threshold` is `None` (parameter not provided), return all severity counts unchanged (backward-compatible).
- Follow the query parameter extraction pattern from list endpoints like `modules/fundamental/src/sbom/endpoints/list.rs` which use Axum's `Query` extractor for pagination parameters.
- Per CONVENTIONS.md §Error Handling: return `Result<Json<AdvisorySeveritySummary>, AppError>` from the handler; return 400 Bad Request for invalid threshold values.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Endpoint Registration: the route is already registered; only the handler signature changes.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint registration scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for `Query` extractor usage with Axum
- `common/src/db/query.rs` — shared query builder helpers for adding filter conditions
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — the handler being extended (from Task 2)

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical count (high, medium, low are 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts (medium, low are 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium counts (low is 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (equivalent to no threshold)
- [ ] Omitting the threshold parameter returns all counts (backward compatible)
- [ ] Invalid threshold values return 400 Bad Request

## Test Requirements
- [ ] Integration test: `?threshold=critical` returns only critical count with other severities zeroed
- [ ] Integration test: `?threshold=high` returns critical and high counts
- [ ] Integration test: no threshold parameter returns all severity counts (backward compatibility)
- [ ] Integration test: invalid threshold value returns 400

## Verification Commands
- `cargo build -p fundamental` — compiles without errors
- `cargo test --test api -- sbom_advisory_summary` — all tests pass including new threshold tests

## Dependencies
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
