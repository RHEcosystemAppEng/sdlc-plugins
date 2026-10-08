# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

This document details how each Reuse Candidate from the task description is used in the
implementation, following the skill's "Reuse first" and "Reuse over duplication" guidance.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source**: `common/src/db/query.rs`

**What it provides**: Handles comma-separated multi-value query parameter parsing and SQL
`IN` clause generation. Takes a raw query string like `"MIT,Apache-2.0"` and a SeaORM
column reference, then returns a `Condition` that matches any of the parsed values.

**How it is reused**: Called directly in `PackageService::list()` (in
`modules/fundamental/src/package/service/mod.rs`) when the `license` parameter is present.
No modifications to `apply_filter` are needed -- it is used as-is.

```rust
// In PackageService::list()
if let Some(license) = license {
    let condition = apply_filter(entity::package_license::Column::License, &license)?;
    query = query.filter(condition);
}
```

**Reuse decision rationale**: `apply_filter` is in `common/src/db/query.rs`, which is a
shared crate already depended upon by `modules/fundamental` (it is the standard query
helper used across all modules). No new dependency is introduced. Direct reuse is the
correct choice -- writing custom comma-parsing or `IN` clause generation would duplicate
this existing utility.

**What is NOT duplicated**: Comma-separated value parsing logic, SQL `IN` clause
construction, input validation for filter values. All of this is handled by `apply_filter`.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Source**: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides**: The severity filter implementation demonstrates the complete pattern
for adding an optional filter query parameter to a list endpoint. It shows:
1. How to declare an optional filter field in the Axum `Query` struct
2. How to extract and validate the parameter in the handler
3. How to pass it to the service layer
4. How the service layer integrates it into the SeaORM query

**How it is reused**: Used as a structural template (not code copy). The license filter
follows the identical pattern:

| Advisory severity filter | Package license filter |
|---|---|
| `Query` struct has `severity: Option<String>` | `PackageQuery` struct gets `license: Option<String>` |
| Handler extracts `query.severity` | Handler extracts `query.license` |
| Handler passes severity to `AdvisoryService::list()` | Handler passes license to `PackageService::list()` |
| Service calls `apply_filter` on severity column | Service calls `apply_filter` on license column |

**Reuse decision rationale**: This is pattern reuse, not code copying. The advisory list
endpoint is the canonical reference for "how to add a filter to a list endpoint in this
codebase." Following the same structural approach ensures consistency across modules and
avoids inventing a new pattern. The advisory severity filter in a sibling module establishes
the convention for:
- Field declaration style (optional String in Query struct)
- Validation approach (handled by `apply_filter`'s error return)
- Service layer parameter passing convention
- SeaORM query composition pattern

**What is NOT duplicated**: No code is copied from the advisory module. The pattern is
followed structurally, but the implementation targets different entities (package vs
advisory) and different columns (license vs severity).

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Source**: `entity/src/package_license.rs`

**What it provides**: The existing SeaORM entity definition for the package-license mapping
table. This entity defines the table schema, column types, and relations (linking packages
to their SPDX license identifiers).

**How it is reused**: Used directly in the SeaORM query within `PackageService::list()` for:

1. **JOIN clause**: The entity's relation definition is used to join the `package` table
   with the `package_license` table:
   ```rust
   query = query.join(
       JoinType::InnerJoin,
       entity::package_license::Relation::Package.def().rev()
   );
   ```

2. **Column reference**: The entity's `Column::License` enum variant is passed to
   `apply_filter` to generate the filter condition on the correct column:
   ```rust
   apply_filter(entity::package_license::Column::License, &license)
   ```

**Reuse decision rationale**: The entity already exists and maps the exact table needed for
the license filter JOIN. Using the SeaORM entity ensures type-safe column references and
relation-based JOINs rather than writing raw SQL strings. The entity crate is already a
dependency of `modules/fundamental` -- no new dependency is introduced.

**What is NOT duplicated**: No raw SQL is written for the JOIN. No manual table/column name
strings are used. The existing entity's relation and column definitions handle all of this
through SeaORM's type system.

---

## Summary

| Reuse Candidate | Reuse Type | New Dependency Required? | Code Modified? |
|---|---|---|---|
| `apply_filter` | Direct function call | No (already a dependency) | No |
| Advisory list severity filter | Structural pattern template | N/A (pattern, not import) | No |
| `package_license` entity | Direct entity reference (JOIN + column) | No (already a dependency) | No |

All three reuse candidates are used as specified in the task description. No new code is
written that duplicates existing functionality. The implementation composes existing building
blocks (query helper, entity, endpoint pattern) rather than creating new infrastructure.
