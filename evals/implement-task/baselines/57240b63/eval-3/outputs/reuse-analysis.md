# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides**: The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL `IN` clause generation. It takes a raw query parameter string (e.g., `"MIT,Apache-2.0"`), splits it on commas, and produces the appropriate filter clause -- a simple equality check for single values, or an `IN (...)` clause for multiple values.

**How it would be applied**: This function would be called directly in `modules/fundamental/src/package/service/mod.rs` when the `license` query parameter is present. Instead of writing custom code to split the comma-separated string and build SQL conditions, the service method passes the raw license parameter string to `apply_filter`, which handles all parsing and clause generation.

**Justification for reuse**: The license filter requirement -- "support both single-value and comma-separated multi-value filtering" -- is exactly what `apply_filter` was designed for. Writing new parsing logic would duplicate this existing, tested functionality. By reusing `apply_filter`, the implementation inherits correct handling of edge cases (trailing commas, whitespace, etc.) that the shared utility already addresses.

**Risk**: None. This is a direct application of the function's intended purpose.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides**: The advisory list endpoint implements a `severity` query parameter filter using a pattern of: (1) an optional field on the Query struct that deserializes from query parameters, (2) passing that field to the service layer, and (3) conditionally applying the filter in the service when the value is present. This is a complete, working example of the exact pattern needed for the license filter.

**How it would be applied**: This file serves as the structural guide for the implementation. Specifically:

- The Query struct pattern (adding `pub license: Option<String>` to the package endpoint's Query struct) mirrors how the advisory endpoint's Query struct carries `pub severity: Option<String>`.
- The handler function pattern (extracting the optional field and passing it to the service) mirrors the advisory handler's flow.
- The service integration pattern (conditionally building a filter clause when the parameter is `Some`) mirrors how the advisory service applies the severity filter.

The implementation follows this file's structure step-by-step, adapting field names and entity references for the package/license domain.

**Justification for reuse**: This pattern has already been validated in production for the advisory module. Following the same structure ensures consistency across endpoints, makes the codebase easier to navigate (developers familiar with the advisory filter will immediately understand the package filter), and reduces the risk of architectural mistakes.

**Risk**: None. The advisory severity filter and the package license filter are structurally identical -- both are optional query parameters that filter a list endpoint by an exact-match string field via a join table.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides**: This is the existing SeaORM entity definition for the `package_license` join table, which maps packages to their declared licenses. It defines the table schema, column mappings, and relation definitions (linking back to the package entity and to the license entity) that SeaORM uses for type-safe query building.

**How it would be applied**: In `modules/fundamental/src/package/service/mod.rs`, the license filter query requires joining the packages table to the licenses table to match on SPDX identifiers. Instead of writing raw SQL (`JOIN package_license ON ...`), the implementation uses the existing `package_license` entity's relation definitions to construct the join via SeaORM's query builder API:

```rust
use entity::package_license;

// Use the entity's defined relation for a type-safe join
query = query.join(JoinType::InnerJoin, package_license::Relation::Package.def().rev());
```

The entity's column definitions are also used to reference the license identifier column in the filter clause, ensuring type safety and consistency with the database schema.

**Justification for reuse**: The entity already exists and correctly models the package-to-license relationship. Creating a new entity or writing raw SQL for this join would be redundant and would diverge from the project's established pattern of using SeaORM entities for all database interactions. Using the existing entity also means that any future schema migrations that update the join table will automatically be reflected in this query.

**Risk**: None. The entity is a stable, existing part of the data model.

---

## Summary

All three reuse candidates are applied directly. No new utility functions, entity definitions, or parsing logic are created that would duplicate existing functionality. The implementation is essentially a composition of these three existing components, adapted to the package/license domain.
