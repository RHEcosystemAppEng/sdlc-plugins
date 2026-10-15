# Reuse Analysis for TC-9203

This document details how each Reuse Candidate from the task description is used in the
implementation, following constraint 5.4 (reuse existing code rather than duplicating).

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Description from task**: Handles comma-separated multi-value query parameter parsing and SQL IN clause generation.

**How it is reused**: Directly invoked in `modules/fundamental/src/package/service/mod.rs` to parse the `license` query parameter value. When the user provides `license=MIT,Apache-2.0`, `apply_filter` splits the comma-separated string into individual values (`["MIT", "Apache-2.0"]`) and these values are used in a SeaORM `.is_in()` clause to generate a SQL `WHERE ... IN (...)` condition.

**Why reuse is appropriate**: The `common` crate is already a dependency of the `fundamental` module (it provides `PaginatedResults`, `AppError`, and other shared types). No new dependency is needed. The function's behavior -- splitting comma-separated values and producing a collection suitable for SQL IN clauses -- is exactly what the license filter requires. Writing a custom parser would duplicate this logic.

**Alternative considered**: Writing a manual `.split(',')` in the service method. Rejected because `apply_filter` already handles edge cases (trimming whitespace, empty segments) and is the established pattern used by other endpoints (advisory severity filter). Duplicating this logic would violate DRY and diverge from project conventions.

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Description from task**: The severity filter implementation is structurally identical to the license filter needed here; follow the same Query struct pattern with an optional field.

**How it is reused**: Used as the structural template for the package endpoint changes. Specifically:

1. **Query struct pattern**: The advisory list endpoint defines a Query (or similar) struct with an `Option<String>` field for `severity`. The package endpoint's Query struct is extended with an identical `Option<String>` field for `license`, following the same derive macros (`Deserialize`) and field documentation pattern.

2. **Handler flow**: The advisory handler extracts the severity filter from the query struct and passes it to the service layer as `Option<&str>`. The package handler follows the same extraction and forwarding pattern for the license filter.

3. **Service integration**: The advisory service conditionally applies the severity filter when the parameter is `Some`. The package service follows the same conditional pattern for the license filter.

**Why reuse is appropriate**: This is pattern reuse (not code reuse) -- the advisory endpoint is a sibling implementation in the same module (`modules/fundamental`). Following its patterns ensures consistency across endpoints, makes the codebase predictable for reviewers, and aligns with the convention conformance analysis from Step 4.

**No code is copied**: The advisory endpoint code is not duplicated. Instead, its structural pattern (Query struct with optional filter field, conditional filter application in service, use of `apply_filter`) is followed to implement an analogous but distinct feature. The actual filter logic, entity joins, and column references are specific to the package/license domain.

## Reuse Candidate 3: `entity/src/package_license.rs`

**Description from task**: Existing entity for the package-license join table; use for the JOIN query rather than writing raw SQL.

**How it is reused**: The SeaORM entity defined in `entity/src/package_license.rs` is used in the package service's list method to perform the JOIN between the `package` table and the `package_license` table. Specifically:

1. **JOIN definition**: `package_license::Relation::Package.def().rev()` is used with SeaORM's `.join()` method to express the relationship between packages and their licenses. This uses the existing relation definition from the entity rather than writing a raw SQL JOIN.

2. **Column reference**: `package_license::Column::License` is used in the `.filter()` clause with `.is_in()` to filter by license values. This uses the SeaORM column enum generated from the entity definition, ensuring type safety and compile-time verification of column names.

**Why reuse is appropriate**: The `entity` crate is already a dependency of the `fundamental` module. The `package_license` entity already defines the table structure, column mappings, and relations needed for the JOIN. Writing raw SQL (`JOIN package_license ON ...`) would bypass SeaORM's type safety, break if column names change, and violate the project's convention of using SeaORM entities for all database operations.

**Alternative considered**: Writing a raw SQL query with `sea_orm::Statement::from_sql_and_values`. Rejected because:
- It bypasses SeaORM type safety
- It does not benefit from schema migrations that rename columns
- It diverges from how every other query in the codebase is constructed
- The entity already exists and provides everything needed

## Summary

| Reuse Candidate | Reuse Type | New Code Avoided |
|----------------|-----------|-----------------|
| `apply_filter` | Direct function call | Custom comma-separated parser and SQL IN clause builder |
| Advisory `list.rs` | Structural pattern | Novel query parameter extraction and service integration approach |
| `package_license.rs` entity | SeaORM entity for JOIN | Raw SQL JOIN and column references |

All three reuse candidates are used. No new utility functions, parsers, or SQL helpers are created. The implementation relies entirely on existing infrastructure, extended only with the domain-specific license filter logic.
