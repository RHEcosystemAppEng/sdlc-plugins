# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

This document explains how each Reuse Candidate identified in the task description is
applied in the implementation. All three candidates are used directly; no duplicating
utility functions are created.

---

## Candidate 1: `common/src/db/query.rs::apply_filter`

**Purpose of the existing utility:**
`apply_filter` is a shared query-builder helper in the `common` crate. It accepts a
SeaORM column reference and a raw query-parameter string. Internally it splits the string
on commas, trims whitespace from each token, and constructs a SeaORM `Condition` that
translates to a SQL `IN` clause (e.g., `license_spdx_id IN ('MIT', 'Apache-2.0')`). When
only one token is present it produces a simple equality condition. The function already
handles the exact multi-value comma-separated semantics required by the new `license`
parameter.

**How it is applied:**
In `modules/fundamental/src/package/service/mod.rs`, the `list` method checks whether
the incoming `license: Option<String>` is `Some`. When it is, `apply_filter` is called
with the `package_license::Column::LicenseSpdxId` column and the raw parameter string:

```rust
use common::db::query::apply_filter;

if let Some(license_param) = license {
    query = query
        .join(JoinType::InnerJoin, package_license::Relation::Package.def())
        .filter(apply_filter(
            package_license::Column::LicenseSpdxId,
            &license_param,
        ));
}
```

**What is NOT done:**
No new function is written to split or parse the comma-separated license string. No custom
`IN`-clause builder is introduced. The call to `apply_filter` is the only filtering logic
added, which is the correct reuse-first behavior required by the task.

---

## Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` — severity filter pattern

**Purpose of the existing code:**
The advisory list endpoint already implements an optional `severity` query parameter using
a typed `Query` struct deserialized by Axum. The struct has an optional `severity: Option<String>`
field. The handler extracts the value and passes it to `AdvisoryService::list`. This pattern
is structurally identical to what the package endpoint needs for `license`.

**How it is applied:**
The advisory `Query` struct shape and handler pattern are followed verbatim when modifying
`modules/fundamental/src/package/endpoints/list.rs`:

1. A `PackageListQuery` struct is introduced with an `license: Option<String>` field,
   mirroring the advisory struct's `severity: Option<String>` field.
2. The Axum `Query<PackageListQuery>` extractor is added to the `list_packages` handler
   signature at the same position as the advisory handler's extractor.
3. The extracted `params.license` value is passed directly to `PackageService::list`,
   exactly as `params.severity` is passed to `AdvisoryService::list` in the advisory
   endpoint.
4. OpenAPI/utoipa annotations follow the same approach used in the advisory endpoint for
   documenting the optional query parameter.

**Benefit:**
Because the pattern is copied rather than invented, the package endpoint immediately
inherits the correct deserialization behavior (empty string vs. absent parameter), the
correct OpenAPI documentation placement, and alignment with the project's established
endpoint conventions — all without requiring a convention review beyond the existing
advisory code.

---

## Candidate 3: `entity/src/package_license.rs` — package-license join table entity

**Purpose of the existing entity:**
`entity/src/package_license.rs` is a SeaORM entity that models the `package_license`
join table, which maps packages to their declared licenses. It defines:

- The table name
- Column definitions (including `LicenseSpdxId` — the column that stores the SPDX
  identifier string)
- Relation definitions connecting back to the `package` entity

**How it is applied:**
In `modules/fundamental/src/package/service/mod.rs`, the entity is imported and used
as the JOIN target when a license filter is present:

```rust
use entity::package_license;

// Inside list():
query = query
    .join(JoinType::InnerJoin, package_license::Relation::Package.def())
    .filter(apply_filter(
        package_license::Column::LicenseSpdxId,
        &license_param,
    ));
```

The `package_license::Relation::Package` definition gives SeaORM all the information it
needs (foreign key columns, join direction) to emit the correct SQL JOIN without any raw
SQL strings. The `package_license::Column::LicenseSpdxId` column reference provides a
type-safe handle for `apply_filter` to build the WHERE condition.

**What is NOT done:**
No raw SQL join strings are written. No new struct or migration is created to represent
the join table — the existing entity is sufficient. The entity file itself
(`entity/src/package_license.rs`) is not modified; it is only imported and used.

---

## Summary Table

| Reuse Candidate | Applied In | How Used |
|---|---|---|
| `common/src/db/query.rs::apply_filter` | `package/service/mod.rs` | Parses comma-separated license values and generates SQL IN clause — no custom parsing written |
| `modules/fundamental/src/advisory/endpoints/list.rs` | `package/endpoints/list.rs` | Query struct shape and optional-filter extraction pattern copied exactly |
| `entity/src/package_license.rs` | `package/service/mod.rs` | JOIN target and column reference for the license filter — no raw SQL or new entity |

All three candidates are reused directly. No new utility functions that duplicate their
functionality are introduced anywhere in the implementation.
