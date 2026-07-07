## Repository
trustify-backend

## Target Branch
main

## Description
Add optional `?threshold=critical` query parameter support to the GET /api/v2/sbom/{id}/advisory-summary endpoint. When provided, the response filters advisory counts to only include advisories at or above the specified severity level. This is a non-MVP enhancement that builds on the core endpoint functionality. Valid threshold values are: low, medium, high, critical. When omitted, all severity levels are included (existing behavior).

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — add query parameter extraction and pass threshold to the service method
- `modules/fundamental/src/advisory/service/advisory.rs` — extend `get_severity_summary_for_sbom` to accept an optional threshold parameter and filter results accordingly

## Implementation Notes
Add a query parameter struct with an optional `threshold` field using Axum's `Query` extractor, following sibling endpoint patterns in `modules/fundamental/src/sbom/endpoints/mod.rs`. The threshold should be an enum with variants `Critical`, `High`, `Medium`, `Low` that implements `Deserialize`. When a threshold is specified, the service method should zero out severity counts below the threshold and recalculate the total. For example, `?threshold=high` would set `low` and `medium` to 0 and total to `critical + high`.
Per CONVENTIONS.md §Framework: use Axum HTTP query parameter extraction conventions. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint scope.
Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` for invalid threshold values. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint scope.

## Acceptance Criteria
- [ ] `?threshold=critical` returns only critical count (high, medium, low are 0)
- [ ] `?threshold=high` returns critical and high counts (medium, low are 0)
- [ ] `?threshold=medium` returns critical, high, and medium counts (low is 0)
- [ ] `?threshold=low` returns all counts (same as no threshold — existing behavior)
- [ ] Omitting the threshold parameter returns all severity counts (backward compatible)
- [ ] Invalid threshold value returns 400 Bad Request
- [ ] Total reflects only the counted severity levels when threshold is applied

## Test Requirements
- [ ] Integration test for each threshold level verifying correct filtering
- [ ] Integration test verifying backward compatibility when threshold is omitted
- [ ] Integration test verifying 400 response for invalid threshold value

## Dependencies
- Depends on: Task 5 — Integration tests
