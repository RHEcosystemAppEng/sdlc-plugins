## Repository
trustify-backend

## Target Branch
main

## Description
Implement the filtering logic in the SearchService so that filter parameters parsed by the endpoint (Task 3) are applied to the database query. This task connects the `SearchFilters` struct to actual database query conditions, using the shared query builder helpers to compose filter predicates.

## Files to Modify
- `modules/search/src/service/mod.rs` — Extend SearchService to accept `SearchFilters` and apply filter conditions to the database query: severity filtering on advisory results, date range filtering on entity timestamps, package name text matching, and license equality matching
- `common/src/db/query.rs` — Add shared filter predicate helpers for date range filtering and multi-value equality filtering, reusable across modules

## Implementation Notes
Extend the SearchService in `modules/search/src/service/mod.rs` to accept the `SearchFilters` struct (defined in Task 3 at `modules/search/src/model/mod.rs`) as a parameter to the search method.

Use the shared query builder helpers in `common/src/db/query.rs` to compose SQL WHERE clauses. The existing helpers handle pagination and sorting; add new helpers for:
- Multi-value equality: `WHERE severity IN (...)` using the severity values from the filter
- Date range: `WHERE created_at >= date_from AND created_at <= date_to`
- Text contains: `WHERE package_name ILIKE '%{pattern}%'`
- Equality: `WHERE license = '{value}'`

The filter conditions should be composed with AND semantics -- all specified filters must match for a result to be included. When a filter field is `None`, the condition is omitted.

Reference the entity definitions for column names:
- `entity/src/advisory.rs` for severity column
- `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs` for date columns
- `entity/src/package.rs` for package name column
- `entity/src/package_license.rs` for license join/column

Use the `limiter.rs` connection pool limiter in `common/src/db/limiter.rs` if the filter queries risk exhausting the connection pool under load.

**Assumption (pending clarification):** Filters combine with AND semantics (all conditions must match). The feature does not specify whether filters should use AND or OR semantics.

## Reuse Candidates
- `common/src/db/query.rs` — Existing query builder helpers for pagination and sorting; extend with filter predicate composition
- `common/src/db/limiter.rs` — Connection pool limiter for protecting against expensive filtered queries

## Acceptance Criteria
- [ ] Severity filter restricts advisory results to matching severity values only
- [ ] Date range filter restricts results to entities created/published within the range
- [ ] Package name filter performs case-insensitive partial matching
- [ ] License filter performs exact match on license type
- [ ] Multiple filters combine with AND semantics
- [ ] Omitted filters do not affect query results

## Test Requirements
- [ ] Unit test for each filter predicate builder function in `common/src/db/query.rs`
- [ ] Integration test combining severity + date range filters on advisory search
- [ ] Integration test verifying package name filter returns partial matches
- [ ] Integration test verifying license filter returns exact matches only

## Dependencies
- Depends on: Task 3 — Add filter parameters to search endpoint

[sdlc-workflow] Description digest: sha256-md:c9d3e7f1a5b028463578abcdef9876543210fedc9876543210fedcba98765432
