# Task 4 — Add threshold query parameter to advisory-summary endpoint (non-MVP)

## Repository
trustify-backend

## Target Branch
main

## Description
Add support for an optional `?threshold=<severity>` query parameter to the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the response includes only severity counts at or above the specified severity level (e.g., `?threshold=high` returns only critical and high counts). This enables alerting integrations to poll for specific severity levels without processing the full breakdown. This is a non-MVP enhancement.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — parse the optional `threshold` query parameter and pass it to the service method
- `modules/fundamental/src/sbom/service/sbom.rs` — extend `get_advisory_severity_summary()` to accept an optional threshold parameter and filter counts accordingly

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` — MODIFY: adds optional query parameter. When `threshold` is set, only counts at or above that severity are included. Valid values: `critical`, `high`, `medium`, `low`. Without the parameter, all severity counts are returned (backward compatible).

## Implementation Notes
- Define a severity ordering: critical > high > medium > low. When threshold is set to a severity level, include counts for that level and all levels above it. For example, `?threshold=high` includes critical and high counts; medium, low are omitted or zeroed.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust endpoint file scope.
- Use Axum's `Query<>` extractor to parse the optional threshold parameter. Define a query params struct (e.g., `AdvisorySummaryParams { threshold: Option<String> }`) following the pattern used by other endpoints with query parameters (see `modules/fundamental/src/sbom/endpoints/list.rs` for pagination query params).
- Validate the threshold value — return 400 Bad Request for invalid severity values. Use `AppError` for consistent error responses.
- The service method signature changes from `get_advisory_severity_summary(sbom_id)` to `get_advisory_severity_summary(sbom_id, threshold: Option<Severity>)`. The filtering can happen either in the SQL query (WHERE severity >= threshold) or in Rust after fetching all counts.
- Ensure backward compatibility: when no threshold is provided, behavior is identical to the current implementation (all severity counts returned).
- Per constraints doc section 5 (Code Change Rules): implementation must follow existing patterns and inspect code before modifying.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — query parameter extraction pattern with Axum's Query<> extractor
- `common/src/db/query.rs` — shared query builder helpers for filtering
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity field type reference

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical count and total
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts and total
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium counts and total
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (same as no threshold)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all counts (backward compatible)
- [ ] Invalid threshold value returns 400 Bad Request

## Test Requirements
- [ ] Integration test: each valid threshold value returns the correct subset of severity counts
- [ ] Integration test: no threshold parameter returns full breakdown (backward compatibility)
- [ ] Integration test: invalid threshold value returns 400
- [ ] Integration test: threshold parameter works correctly with cached responses

## Verification Commands
- `cargo test --package fundamental -- advisory_summary` — all endpoint tests pass including threshold tests
- `cargo check --workspace` — no compilation errors

## Documentation Updates
- `docs/api/` — add threshold query parameter to advisory-summary endpoint documentation

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute caching
