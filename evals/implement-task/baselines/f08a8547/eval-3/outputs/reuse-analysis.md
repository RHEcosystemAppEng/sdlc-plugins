# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

## Overview

The task description identifies three Reuse Candidates. All three are directly applicable
and should be reused rather than writing new code. No additional reusable code was
discovered beyond what was listed. This analysis details how each candidate is used and
the rationale for reuse.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source**: `common/src/db/query.rs`
**Symbol**: `apply_filter` function
**Purpose**: Parses comma-separated multi-value query parameter strings and generates SQL
`IN` clause values.

### How it is reused

The `apply_filter` function is called in `PackageService::list()` (in
`modules/fundamental/src/package/service/mod.rs`) to transform the raw `license` query
parameter string into a collection of individual license values suitable for a SeaORM
`.is_in()` filter clause.

**Usage pattern:**

```rust
use common::db::query::apply_filter;

// In PackageService::list(), when license filter is present:
if let Some(license_filter) = license {
    let license_values = apply_filter(license_filter);
    query = query
        .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
        .filter(package_license::Column::License.is_in(license_values));
}
```

### Rationale

- **Dependency already exists**: The `common` crate is already a dependency of
  `modules/fundamental` (it provides `AppError`, `PaginatedResults`, and the existing
  query helpers). No new dependency is introduced.
- **DRY principle**: `apply_filter` already handles the comma-split-and-trim logic, edge
  cases (empty strings, whitespace), and produces the correct type for SeaORM filter
  methods. Reimplementing this logic would duplicate ~10-15 lines of parsing code and
  create a maintenance burden where bug fixes would need to be applied in two places.
- **Consistency**: The advisory endpoint's severity filter uses the same function. Using
  it for the license filter ensures identical parsing behavior across all list endpoints.

### Verification steps

1. Inspect `apply_filter` signature and return type to confirm compatibility with
   `Column::is_in()`.
2. Verify it handles edge cases: empty string input, trailing commas, whitespace around
   values.
3. Confirm the `common` crate is in `modules/fundamental/Cargo.toml` dependencies.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Source**: `modules/fundamental/src/advisory/endpoints/list.rs`
**Symbol**: The advisory list endpoint's `Query` struct and handler pattern (specifically
the severity filter implementation)
**Purpose**: Provides the structural template for adding an optional filter parameter to
a list endpoint.

### How it is reused

This is a **pattern reference** rather than direct code import. The advisory endpoint's
severity filter is structurally identical to the license filter needed for the package
endpoint. The implementation follows the same three-layer pattern:

1. **Endpoint layer** (`list.rs`): Add `license: Option<String>` to the `Query` struct,
   mirroring how `severity: Option<String>` is declared in the advisory Query struct.
   Pass it to the service layer in the same manner.

2. **Service layer** (`service/mod.rs`): Accept `license: Option<&str>` as a parameter,
   mirroring how the advisory service accepts `severity: Option<&str>`. Apply the filter
   conditionally using `apply_filter` + entity JOIN, following the same conditional
   pattern.

3. **Entity JOIN**: Use the entity relation definition for the JOIN, just as the advisory
   endpoint JOINs through its related entity for severity filtering.

**Specific patterns borrowed from the advisory endpoint:**

| Pattern | Advisory (severity) | Package (license) |
|---|---|---|
| Query struct field | `pub severity: Option<String>` | `pub license: Option<String>` |
| Service parameter | `severity: Option<&str>` | `license: Option<&str>` |
| Filter application | `apply_filter(severity)` + entity JOIN | `apply_filter(license)` + `package_license` JOIN |
| Conditional guard | `if let Some(severity_filter) = severity` | `if let Some(license_filter) = license` |

### Rationale

- **Convention conformance**: Following an existing sibling endpoint's pattern ensures
  the new filter integrates consistently with the codebase's established architecture.
  Reviewers can verify correctness by comparing against the known-working advisory
  implementation.
- **Reduced risk**: The advisory severity filter is already tested and deployed. Mirroring
  its structure minimizes the chance of architectural mistakes (wrong layer for filtering,
  incorrect parameter passing, missed error handling).
- **No code duplication**: This reuse is structural (following the same design pattern),
  not copying code. Each endpoint has its own Query struct and service method -- they just
  follow the same shape.

### Verification steps

1. Read the advisory `Query` struct to confirm the pattern for optional filter fields
   (derive macros, serde attributes, documentation).
2. Read the advisory handler function to confirm how the filter is extracted and passed
   to the service.
3. Read the advisory service's list method to confirm the `apply_filter` + JOIN + filter
   pattern.
4. Identify any advisory-specific logic that should NOT be copied (e.g., severity-specific
   validation that does not apply to licenses).

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Source**: `entity/src/package_license.rs`
**Symbol**: The `package_license` SeaORM entity (model, columns, relations)
**Purpose**: Provides the ORM entity for the package-to-license join table, enabling
type-safe JOINs and column references in the filter query.

### How it is reused

The `package_license` entity is used in the `PackageService::list()` method to:

1. **JOIN the package-license table**: Use the entity's relation definition to create a
   type-safe JOIN from the `package` table to the `package_license` table. This avoids
   raw SQL and ensures the JOIN is validated at compile time.

   ```rust
   query = query.join(
       JoinType::InnerJoin,
       package_license::Relation::Package.def().rev()
   );
   ```

2. **Filter on the license column**: Use the entity's `Column` enum to reference the
   license column in the WHERE clause, again with compile-time type safety.

   ```rust
   .filter(package_license::Column::License.is_in(license_values))
   ```

### Rationale

- **Entity already exists**: The `package_license.rs` entity is already defined in the
  `entity` crate. Creating a new entity or using raw SQL would be both unnecessary and
  inconsistent with the project's SeaORM conventions.
- **Type safety**: Using the SeaORM entity provides compile-time verification of column
  names and relation paths. Raw SQL string references to table/column names would bypass
  this safety and be fragile to schema changes.
- **Dependency already exists**: The `entity` crate is already a dependency of
  `modules/fundamental` (it uses `package`, `sbom`, and other entities). No new
  dependency is introduced.

### Verification steps

1. Read `entity/src/package_license.rs` to confirm the column names (expected: `package_id`
   and `license` or similar).
2. Verify the entity defines a `Relation::Package` (or equivalent) that can be used for
   the reverse JOIN from packages to package_license.
3. Confirm the `entity` crate is in `modules/fundamental/Cargo.toml` dependencies.
4. Check if the entity is already imported/used elsewhere in the `fundamental` module to
   confirm the import path.

---

## Summary Table

| Reuse Candidate | Reuse Type | Location Used | New Code Avoided |
|---|---|---|---|
| `apply_filter` | Direct function call | `PackageService::list()` | ~15 lines of comma-split parsing + IN clause logic |
| Advisory list endpoint pattern | Structural pattern | `list.rs` handler + `Query` struct + `service/mod.rs` | Architectural design decisions; ensures consistent filter pattern |
| `package_license` entity | Direct entity import | `PackageService::list()` JOIN + filter | ~20 lines of raw SQL or manual table/column references |

## Additional Reuse Discovery

No additional reusable code was discovered beyond the three candidates listed in the task
description. The existing candidates fully cover the implementation needs:

- **Parsing**: handled by `apply_filter`
- **Pattern**: provided by the advisory endpoint
- **Data access**: provided by the `package_license` entity

No symbol deduplication issues were identified -- the license filter does not introduce
any new constants, enums, or type aliases that might already exist elsewhere.
