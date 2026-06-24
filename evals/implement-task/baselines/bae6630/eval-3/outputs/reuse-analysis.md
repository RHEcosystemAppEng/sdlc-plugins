# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** A shared utility function that accepts a raw query parameter string (potentially comma-separated), splits it into individual values, and generates a SQL `IN (...)` clause compatible with SeaORM's query builder. It handles edge cases such as trimming whitespace, deduplicating values, and producing a single-value equality check when only one value is provided.

**How it would be applied:** The `license` query parameter arrives as a raw `Option<String>` from the HTTP request. When present, the value is passed directly to `apply_filter`, which:

1. Splits `"MIT,Apache-2.0"` into `["MIT", "Apache-2.0"]`
2. Generates a `column IN ('MIT', 'Apache-2.0')` condition
3. Returns a SeaORM `Condition` that is appended to the query builder

This eliminates any need to write custom parsing logic for comma-separated values. The license filter reuses `apply_filter` identically to how the advisory severity filter uses it — no wrapper functions, no custom splitting, no new utility code. The function is called in the service layer (`modules/fundamental/src/package/service/mod.rs`) when building the filtered query.

**Why reuse is appropriate:** Writing a new comma-separated parser or SQL IN clause builder would directly duplicate `apply_filter`'s functionality. The function was designed as a shared utility in the `common` crate precisely for this cross-module reuse pattern. Every list endpoint that supports multi-value filtering should go through `apply_filter` to maintain consistency in parsing behavior and SQL generation.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** A complete, working implementation of a list endpoint with optional query parameter filtering. The advisory list endpoint supports a `severity` query parameter that filters advisories by severity level, using the same single-value and comma-separated multi-value pattern required for the license filter.

**How it would be applied:** This file serves as the structural guide — not called directly, but followed as a pattern template. The implementation mirrors its architecture in three specific ways:

1. **Query struct pattern:** The advisory endpoint defines a `Query` struct with an `Option<String>` field for `severity`. The package endpoint's `Query` struct in `list.rs` adds an analogous `Option<String>` field for `license`. The struct derives the same Axum extractor traits (`Deserialize`, `IntoParams`).

2. **Handler-to-service flow:** The advisory handler checks if `query.severity` is `Some`, then passes the parsed filter to `AdvisoryService::list()`. The package handler follows the same conditional flow — check `query.license`, pass to `PackageService::list()`.

3. **Service-layer integration:** The advisory service calls `apply_filter` with the severity value and adds the resulting condition to the SeaORM query. The package service does the same with the license value, adding the `package_license` join before applying the filter condition.

**Why reuse is appropriate:** Following the advisory endpoint's structure ensures the license filter is implemented consistently with existing filters in the codebase. Inventing a different pattern (e.g., a middleware-based filter, a macro-generated filter, or a different query parameter extraction approach) would create an inconsistency that makes the codebase harder to maintain. The advisory pattern has been validated in production and represents the project's established convention for list endpoint filtering.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:** The SeaORM entity definition for the `package_license` join table, which maps packages to their declared licenses. This entity includes:

- The `Model` struct with typed fields (package ID, license identifier, and any metadata columns)
- `Relation` definitions that establish foreign key relationships to the `package` table and any license reference table
- Column enum for type-safe column references in queries
- Standard SeaORM trait implementations (`EntityTrait`, `ActiveModelTrait`, etc.)

**How it would be applied:** When the license filter is active, the package list query needs to JOIN through the `package_license` table to access the license identifier column. The entity is used in two ways:

1. **JOIN construction:** In `PackageService::list()`, when a license filter is provided, the SeaORM query builder adds a `.join()` call referencing `package_license::Relation::Package` (or the reverse relation from `package` to `package_license`). This produces a `JOIN package_license ON package.id = package_license.package_id` clause without writing raw SQL.

2. **Column reference for filtering:** The `apply_filter` result is applied against `package_license::Column::License` (or the equivalent column name), providing a type-safe reference to the license identifier column. This ensures compile-time verification that the column exists and has the correct type.

**Why reuse is appropriate:** The `package_license` entity already exists and encodes the correct table schema, column names, and relationships. Writing raw SQL joins or defining inline column references would bypass SeaORM's type safety and diverge from how other join tables (`sbom_package`, `sbom_advisory`) are used elsewhere in the codebase. Using the entity maintains the project's convention of leveraging SeaORM entities for all database interactions.

---

## Summary

| Reuse Candidate | Role in Implementation | Reuse Type |
|---|---|---|
| `common/src/db/query.rs::apply_filter` | Comma-separated value parsing and SQL IN clause generation | Direct function call |
| `modules/fundamental/src/advisory/endpoints/list.rs` | Structural template for Query struct, handler flow, and service integration | Pattern replication |
| `entity/src/package_license.rs` | SeaORM entity for JOIN query and type-safe column reference | Entity/model reuse |

No new utility functions are created. All comma-separated parsing goes through `apply_filter`. The advisory endpoint pattern is followed rather than reinvented. The existing `package_license` entity provides the JOIN without raw SQL.
