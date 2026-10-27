## Repository
trustify-backend

## Target Branch
main

## Description
Add support for the optional `?threshold=critical` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the endpoint filters severity counts to include only severities at or above the specified threshold level. The severity ordering is: critical > high > medium > low. For example, `?threshold=high` returns counts for critical and high only, with medium and low set to 0. This supports alerting integrations that need to check for advisories above a specific severity.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add `Query<ThresholdParams>` extractor to parse the optional `threshold` query parameter, apply filtering to the response before returning
- `modules/fundamental/src/sbom/service/sbom.rs` — optionally extend the `advisory_severity_summary` method to accept a threshold parameter, or handle filtering at the endpoint handler level

## Implementation Notes
Use Axum's `Query` extractor to parse optional query parameters. Define a `ThresholdParams` struct:

```rust
#[derive(Deserialize)]
struct ThresholdParams {
    threshold: Option<String>, // "critical", "high", "medium", "low"
}
```

Severity ordering for threshold filtering: critical (4) > high (3) > medium (2) > low (1). When threshold is set:
- Zero out counts for severity levels below the threshold
- Recalculate `total` as the sum of remaining non-zero counts

Follow the pattern of existing query parameter handling in list endpoints (e.g., `modules/fundamental/src/sbom/endpoints/list.rs` for pagination parameters).

Per CONVENTIONS.md §Error Handling: return a 400 Bad Request via `AppError` if an invalid threshold value is provided.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates query parameter extraction pattern with Axum's `Query` extractor
- `common/src/error.rs::AppError` — for returning 400 on invalid threshold values

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical count (high, medium, low are 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts (medium, low are 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium counts (low is 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (equivalent to no filter)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all counts (backward compatible)
- [ ] Invalid threshold value returns 400 Bad Request
- [ ] `total` field is recalculated to reflect only the included severity levels

## Test Requirements
- [ ] Integration test for each threshold level verifying correct filtering
- [ ] Integration test for missing threshold parameter (backward compatibility)
- [ ] Integration test for invalid threshold value returning 400

## Verification Commands
- `cargo test --test api` — run integration tests including threshold filter tests

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint
