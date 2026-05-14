# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

### What It Provides

The `apply_filter` function is the codebase's standard utility for handling query parameter filtering. It accepts a comma-separated string value and produces the corresponding SeaORM filter condition: an equality check for a single value, or an `IN` clause for multiple comma-separated values. This encapsulates all parsing, splitting, and SQL generation logic in one reusable location.

### How It Applies to TC-9203

The `license` query parameter must support both `?license=MIT` (single value) and `?license=MIT,Apache-2.0` (comma-separated multi-value). This is exactly the functionality that `apply_filter` already provides. In the `PackageService::list` method, when a license filter string is present, it will be passed directly to `apply_filter` along with the target column reference from the package-license entity. The function will return the correct filter condition to chain onto the query.

### Why Direct Reuse Is Required

Writing new code to split comma-separated values and build `IN` clauses would duplicate `apply_filter` line-for-line. The existing function is already tested, handles edge cases (single value, multiple values, whitespace trimming), and is used consistently across the codebase. Creating any new parsing utility would violate DRY and introduce a maintenance burden where two functions must be kept in sync.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

### What It Provides

The advisory list endpoint implements a severity filter using an optional field on a `Query` struct. The pattern is: define `severity: Option<String>` on the `Query` struct, extract it via Axum's query parameter deserialization, and pass it through to the corresponding service method. The service method then conditionally applies the filter when the value is `Some`. This is the established structural pattern for optional list filters across the codebase.

### How It Applies to TC-9203

The license filter is structurally identical to the severity filter. In `modules/fundamental/src/package/endpoints/list.rs`, an optional `license: Option<String>` field will be added to the `Query` struct following the same declaration pattern. The handler will forward `query.license` to `PackageService::list` in the same way the advisory handler forwards `query.severity` to its service. This ensures consistency in how endpoints expose optional filters.

### Why Following This Pattern Is Required

Diverging from the established `Query` struct pattern would create inconsistency in the API layer. Every list endpoint in the codebase uses the same approach: an optional field on a `Query` struct, Axum deserialization, and pass-through to the service. Inventing an alternative mechanism (e.g., manual header parsing, middleware extraction, or a different struct layout) would confuse future maintainers and break the principle of least surprise. The advisory severity filter is the direct structural template to follow.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

### What It Provides

The `package_license` entity is an existing SeaORM entity that models the join table between packages and licenses. It defines the table schema, column mappings, and relationships needed to query the package-license association. This entity is already part of the project's entity crate and participates in SeaORM's relation and query-building infrastructure.

### How It Applies to TC-9203

Filtering packages by license requires joining the packages table with the package-license join table and applying a condition on the license identifier column. The `package_license` entity provides the SeaORM `Entity`, `Column`, and `Relation` definitions needed to construct this JOIN using SeaORM's query builder API (e.g., `find().join(...)` or `find_also_related(...)`). The license column on this entity is the target column passed to `apply_filter` for the filter condition.

### Why Using the Existing Entity Is Required

Writing raw SQL for the JOIN would bypass SeaORM's type safety, relation validation, and query composition. Creating a new entity for the same join table would produce a duplicate definition that conflicts with the existing one and violates the single-source-of-truth principle for schema definitions. The `package_license` entity already exists, is correct, and is the proper SeaORM building block for any query involving the package-license relationship.

---

## Summary

All three reuse candidates are mandatory for this implementation. Together they eliminate the need for any new utility functions, raw SQL, or new entity definitions. The implementation reduces to wiring existing components together following an established pattern:

1. **`apply_filter`** handles all comma-separated value parsing and SQL condition generation.
2. **Advisory severity filter pattern** provides the exact structural template for the endpoint layer.
3. **`package_license` entity** provides the join table definition for the database query.
