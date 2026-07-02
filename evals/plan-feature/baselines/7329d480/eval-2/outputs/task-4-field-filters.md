# Task 4: Add field-based filters to search API

additional_fields: { "labels": ["ai-generated-jira"], "priority": {"name": "Normal"}, "fixVersions": [{"name": "RHTPA 1.6.0"}] }

## Repository
trustify-backend

## Target Branch
main

## Description
Add field-based filter parameters to the search endpoint, enabling users to narrow results by severity (for advisories) and date range. The feature TC-9002 requires "add filters" with "some kind of filtering capability" but provides no filter specification.

**Assumption**: The initial field-based filters are severity (matching the `severity` field on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`) and date range (created_at/updated_at). These are the most useful filters given the data model. Additional filters (e.g., license for packages from `entity/src/package_license.rs`) can be added in a follow-up once the product owner clarifies requirements. This assumption is pending clarification.

**Assumption**: Severity filter accepts standard CVSS severity levels (none, low, medium, high, critical). Date range filter accepts ISO 8601 date strings via `from_date` and `to_date` parameters.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add `severity`, `from_date`, and `to_date` query parameters
- `modules/search/src/service/mod.rs` — Extend SearchService to apply field-based filter clauses to search queries
- `common/src/db/query.rs` — Add date-range filter helper if not already present

## Implementation Notes
In the search endpoint (`modules/search/src/endpoints/mod.rs`):
- Add optional query parameters: `severity` (string, e.g., `high`), `from_date` (ISO 8601 date), `to_date` (ISO 8601 date)
- Validate severity against known values; return 400 via `AppError` for invalid values
- Parse date strings; return 400 for malformed dates
- Pass validated filters to the service layer

In the SearchService (`modules/search/src/service/mod.rs`):
- When `severity` is present, add a WHERE clause filtering advisory results by severity
- When `from_date` and/or `to_date` are present, add date range conditions
- Severity filter should only apply when advisory entity type is in scope (combine logically with entity-type filter from Task 3)

In `common/src/db/query.rs`:
- Add a reusable date-range filter builder function if one does not already exist, following the pattern of existing filter helpers in that module
- Extend the existing shared query builder helpers for the severity filter

Reference `modules/fundamental/src/advisory/model/summary.rs` for the `severity` field definition on `AdvisorySummary`. Reference `entity/src/advisory.rs` for the advisory entity column names.

Per CONVENTIONS.md §Module pattern: Maintain the model/ + service/ + endpoints/ structure. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's modules directory scope.

Per CONVENTIONS.md §Error handling: Return Result<T, AppError> with .context() wrapping for validation errors. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust syntax scope.

Per CONVENTIONS.md §Query helpers: Extend shared filtering utilities in common/src/db/query.rs for date-range and severity filters. Applies: task modifies `common/src/db/query.rs` matching the convention's file path scope (common/src/db/query.rs).

## Reuse Candidates
- `common/src/db/query.rs::filtering helpers` — Extend existing filter infrastructure for new filter types
- `common/src/error.rs::AppError` — Use for validation error responses
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference the severity field definition

## Dependencies
- Depends on: Task 3 — Add entity-type filter to search API (field filters should compose with entity-type filter)

## Acceptance Criteria
- [ ] Search endpoint accepts optional `severity` query parameter (values: none, low, medium, high, critical)
- [ ] Search endpoint accepts optional `from_date` and `to_date` query parameters (ISO 8601 format)
- [ ] Invalid severity values return 400 Bad Request
- [ ] Malformed date values return 400 Bad Request
- [ ] Severity filter applies only to advisory results
- [ ] Date range filter applies across all entity types
- [ ] Filters compose correctly with each other and with the entity-type filter from Task 3
- [ ] When no field filters are provided, behavior is unchanged (backward compatible)

## Test Requirements
- [ ] Search with `severity=high` returns only high-severity advisory results
- [ ] Search with `from_date` and `to_date` returns only results within the date range
- [ ] Search with `severity=high&entity_type=advisory` correctly combines both filters
- [ ] Invalid severity value returns 400
- [ ] Malformed date returns 400
- [ ] Omitting all field filters returns unfiltered results

## Verification Commands
- `cargo test -p modules-search` — search module compiles and tests pass
- `cargo test -p common` — common crate tests pass (new query helpers)
- `cargo test -p tests --test search` — integration tests pass

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional `severity` query parameter (values: none, low, medium, high, critical)
- `GET /api/v2/search` — MODIFY: Add optional `from_date` and `to_date` query parameters (ISO 8601 dates)
