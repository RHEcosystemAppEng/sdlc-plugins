# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document details the three Reuse Candidates identified in the task description and how each would be applied during implementation. Following SKILL.md constraint 5.4 ("Reuse first"), no new utility functions are created that duplicate existing functionality.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** `apply_filter` is a shared query builder helper that accepts a string value (potentially comma-separated, e.g., `"MIT,Apache-2.0"`), splits it on commas, and generates a SQL `IN` clause for use with SeaORM queries. It handles both single-value and multi-value cases uniformly.

**How it would be reused:** In `modules/fundamental/src/package/service/mod.rs`, when the `license` parameter is `Some`, the service calls `apply_filter` directly with the raw license string from the query parameter. `apply_filter` handles all parsing and SQL condition generation. No new comma-splitting logic, no new `IN` clause builder, no new utility function is written. The function is already publicly exported from the `common` crate, and `modules/fundamental` already depends on `common` (as evidenced by its existing use of `PaginatedResults` from `common/src/model/paginated.rs` and other query helpers from `common/src/db/`).

**Why reuse is correct:** Writing a custom parser for comma-separated license values would directly duplicate `apply_filter`'s functionality. The function is designed for exactly this use case -- it is the project's standard mechanism for multi-value query parameter filtering. Reusing it ensures consistent behavior across all list endpoints and avoids introducing a second code path for the same logic.

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:** The advisory list endpoint already implements a query parameter filter using the same structural pattern needed for the license filter. Specifically:
- A Query struct with an optional filter field (`severity: Option<String>`)
- Extraction of the filter value from the Query struct in the handler
- Passing the filter value to the service layer
- The service layer using `apply_filter` to build the database condition

**How it would be used as a structural guide:** The implementation in `modules/fundamental/src/package/endpoints/list.rs` follows this pattern exactly:
1. Add `license: Option<String>` to the package endpoint's Query struct, mirroring the `severity: Option<String>` field in the advisory endpoint's Query struct.
2. Extract `query.license` in the handler and pass it to `PackageService::list()`, mirroring how the advisory handler extracts `query.severity` and passes it to `AdvisoryService::list()`.
3. In the service layer, apply the filter conditionally (only when `Some`), mirroring the advisory service's conditional severity filtering.

**Why this guide is correct:** The advisory severity filter is structurally identical to the needed license filter -- both are optional query parameters that support comma-separated multi-value filtering on a specific column. Following this established pattern ensures consistency across the codebase's list endpoints and avoids inventing a new approach where a proven one already exists. The advisory endpoint is in the same `modules/fundamental` module, making it the closest sibling for convention conformance.

## Reuse Candidate 3: `entity/src/package_license.rs` (package-license entity)

**What it provides:** A SeaORM entity definition that maps the `package_license` database table. This table represents the many-to-many relationship between packages and their declared SPDX license identifiers. The entity defines the table's columns (including the license identifier column and the foreign key to the package table) and its SeaORM relations to other entities.

**How it would be reused:** In `modules/fundamental/src/package/service/mod.rs`, the license filter query joins through the `package_license` entity to find packages matching the specified license(s). The JOIN is expressed using SeaORM's typed relation API:

```rust
Package::find()
    .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
    .filter(/* apply_filter condition on package_license::Column::License */)
```

The entity's `Column` enum provides the typed column reference for the filter condition, and its `Relation` enum provides the typed JOIN definition. No raw SQL is written for the JOIN or the filter condition.

**Why reuse is correct:** The `package_license` entity already encodes the table schema, column names, and foreign key relationships. Writing raw SQL for the JOIN would bypass SeaORM's type safety, risk column name mismatches, and not benefit from schema evolution (if columns are renamed or relations change, the entity is updated in one place). The entity exists precisely to provide a typed, maintainable interface to this table.

## Summary

| Reuse Candidate | Location | Role in Implementation |
|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Comma-separated value parsing and SQL IN clause generation -- called directly, no new parsing logic written |
| Severity filter pattern | `modules/fundamental/src/advisory/endpoints/list.rs` | Structural template for Query struct field, handler extraction, and service-layer conditional filtering |
| `package_license` entity | `entity/src/package_license.rs` | SeaORM entity for the JOIN query -- used for typed column references and relation definitions instead of raw SQL |

No new utility functions, parsing helpers, or query builders are created. All filtering logic flows through the existing `apply_filter` function, and all database access flows through the existing `package_license` entity.
