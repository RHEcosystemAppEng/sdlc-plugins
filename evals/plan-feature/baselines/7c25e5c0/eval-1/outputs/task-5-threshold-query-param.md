## Repository
trustify-backend

## Target Branch
main

## Description
Add support for the optional `?threshold=critical` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the endpoint filters severity counts to only include levels at or above the specified threshold. Valid threshold values are: `critical`, `high`, `medium`, `low`. When omitted, all severity levels are returned (default behavior).

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add query parameter extraction and filtering logic
- `modules/fundamental/src/sbom/service/sbom.rs` — add threshold parameter to `advisory_summary` method signature and implement severity-level filtering

## Implementation Notes
- Follow the existing query parameter extraction pattern in `modules/fundamental/src/sbom/endpoints/list.rs` for adding optional query params to an endpoint handler
- Reference `common/src/db/query.rs` for shared query builder helpers that may support filtering patterns
- Define severity ordering: Critical > High > Medium > Low. When `threshold=high`, return counts for Critical and High only (zero out Medium and Low)
- Parse the threshold query param as a case-insensitive string enum
- Return 400 Bad Request if the threshold value is not a valid severity level
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust endpoint scope.

## Acceptance Criteria
- [ ] `?threshold=critical` returns only critical count (high, medium, low are zero)
- [ ] `?threshold=high` returns critical and high counts (medium, low are zero)
- [ ] `?threshold=medium` returns critical, high, and medium counts (low is zero)
- [ ] `?threshold=low` returns all counts (same as no threshold)
- [ ] Omitting the threshold parameter returns all severity counts (backward compatible)
- [ ] Invalid threshold value returns 400 Bad Request

## Test Requirements
- [ ] Test each threshold value produces correct filtered output
- [ ] Test omitted threshold returns full counts
- [ ] Test invalid threshold value returns 400
- [ ] Test case-insensitive threshold values (e.g., `CRITICAL`, `Critical`)

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint with caching
