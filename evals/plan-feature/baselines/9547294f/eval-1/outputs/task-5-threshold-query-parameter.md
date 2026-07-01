## Repository
trustify-backend

## Target Branch
main

## Description
Add optional `?threshold=<severity>` query parameter support to the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the endpoint filters severity counts to only include levels at or above the specified threshold (e.g., `?threshold=critical` returns only the critical count). This enables alerting integrations to poll for critical advisories without retrieving all severity levels. This is a non-MVP enhancement.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add query parameter extraction and pass threshold to service method
- `modules/fundamental/src/sbom/service/sbom.rs` — add optional threshold parameter to `advisory_severity_summary` method; filter aggregation query by severity level when provided

## Implementation Notes
- Add an optional query parameter struct using Axum's `Query<T>` extractor. Define a struct like `AdvisorySummaryParams { threshold: Option<SeverityLevel> }` where `SeverityLevel` is an enum or string matching the severity values used in the advisory model.
- The threshold filter should follow severity ordering: Critical > High > Medium > Low. When `?threshold=high` is provided, return counts for High and Critical only (severities at or above the threshold).
- Modify the service method signature to accept an optional threshold parameter: `advisory_severity_summary(&self, sbom_id: Id, threshold: Option<SeverityLevel>) -> Result<AdvisorySeveritySummary, AppError>`.
- When no threshold is provided, return all severity counts (backward compatible with the MVP endpoint behavior from Task 2).
- Use the severity type from `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` for consistent severity representation.
- Follow the query parameter pattern used by existing endpoints — check `modules/fundamental/src/sbom/endpoints/list.rs` and `common/src/db/query.rs` for query parameter extraction and filtering patterns.
- Per CONVENTIONS.md: shared filtering via `common/src/db/query.rs`. Follow the established query parameter pattern.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service file scope.

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold=<severity>` — MODIFY: add optional `threshold` query parameter. Accepted values: `critical`, `high`, `medium`, `low`. When provided, response includes only severity levels at or above the threshold. Counts for excluded severity levels are set to 0.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering; may contain patterns for enum-based query parameter filtering
- `modules/fundamental/src/sbom/endpoints/list.rs` — shows query parameter extraction pattern with Axum's `Query<T>` extractor
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity field definition; reuse the same severity type

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical count (other levels set to 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts (medium and low set to 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)
- [ ] Invalid threshold values return 400 Bad Request

## Test Requirements
- [ ] Integration test: `?threshold=critical` returns only critical count, other severities are 0
- [ ] Integration test: `?threshold=high` returns critical and high counts
- [ ] Integration test: `?threshold=medium` returns critical, high, and medium counts
- [ ] Integration test: `?threshold=low` returns all counts (equivalent to no threshold)
- [ ] Integration test: no threshold parameter returns all severity counts (backward compatibility)
- [ ] Integration test: invalid threshold value returns 400

## Verification Commands
- `cargo test --test api advisory_summary` — run all advisory summary integration tests including threshold tests

## Dependencies
- Depends on: Task 2 — Add advisory summary endpoint with caching

---

> [sdlc-workflow] Description digest: (simulated) The digest would be posted as a Jira comment after task creation per the description-digest-protocol. Format: `[sdlc-workflow] Description digest: sha256-md:<64-hex-chars>`
