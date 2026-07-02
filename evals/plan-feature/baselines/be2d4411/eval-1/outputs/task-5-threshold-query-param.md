## Repository
trustify-backend

## Target Branch
main

## Description
Add support for the optional `?threshold=critical` query parameter on the advisory-summary endpoint. When provided, the response includes only counts for severity levels at or above the specified threshold. For example, `?threshold=high` returns counts for Critical and High while zeroing out Medium and Low. The `total` field reflects the sum of the included (non-zeroed) counts. When the parameter is omitted, all counts are returned (backward compatible).

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add optional `threshold` query parameter extraction via Axum's `Query` extractor and pass to service method
- `modules/fundamental/src/sbom/service/sbom.rs` — add `threshold` parameter to `get_advisory_severity_summary` method signature and apply filtering logic
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — add `SeverityThreshold` enum (Critical, High, Medium, Low) for the query parameter deserialization

## Implementation Notes
- Define a `SeverityThreshold` enum in `modules/fundamental/src/sbom/model/advisory_summary.rs` with variants: `Critical`, `High`, `Medium`, `Low`. Derive `Deserialize` for query parameter parsing. Use `#[serde(rename_all = "lowercase")]` so URL values are lowercase (e.g., `?threshold=critical`).
- Add an optional `Query<ThresholdParams>` extractor to the endpoint handler in `advisory_summary.rs`, where `ThresholdParams` is a struct with `threshold: Option<SeverityThreshold>`.
- Modify `SbomService::get_advisory_severity_summary` to accept an `Option<SeverityThreshold>` parameter. When `Some`, zero out severity counts below the threshold and recompute `total` as the sum of the remaining counts. The severity ordering for threshold filtering is: Critical > High > Medium > Low.
- Return `AppError::BadRequest` with a descriptive message when the `threshold` parameter value is not a valid severity level. Axum's `Query` extractor will handle most validation, but add a fallback error for unexpected values.
- Ensure backward compatibility: when `threshold` is `None` (parameter omitted), behavior is identical to the endpoint without this change.

Per CONVENTIONS.md §Error Handling: return `AppError::BadRequest` for invalid threshold values with `.context()` wrapping for descriptive error messages.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` handler file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — existing handler to extend with query parameter
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for how severity is represented as a field, useful for aligning the threshold enum values with existing severity strings

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only the critical count; high, medium, low are 0; total equals critical
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts; medium, low are 0; total equals critical + high
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium counts; low is 0; total equals critical + high + medium
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (equivalent to no threshold)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all counts (backward compatible)
- [ ] Invalid threshold value (e.g., `?threshold=unknown`) returns HTTP 400 Bad Request

## Test Requirements
- [ ] Integration test: `?threshold=critical` returns only critical count with others zeroed
- [ ] Integration test: `?threshold=high` returns critical and high counts with medium and low zeroed
- [ ] Integration test: `?threshold=medium` returns critical, high, and medium with low zeroed
- [ ] Integration test: no threshold parameter returns all counts (backward compatibility)
- [ ] Integration test: invalid threshold value returns 400

## Dependencies
- Depends on: Task 2 — Create GET /api/v2/sbom/{id}/advisory-summary endpoint with caching

---

[sdlc-workflow] Description digest: sha256-md:049d4de36595c80faf18d84e8a059f1ffc7f31a6b62f64f339db1b53b64d4ed2
