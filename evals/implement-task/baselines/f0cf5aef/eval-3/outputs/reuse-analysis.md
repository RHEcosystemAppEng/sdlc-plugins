# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

## Overview

The task description provides three Reuse Candidates. All three are reused directly in the implementation -- no new utility functions are created that would duplicate existing functionality.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** A shared query builder helper that handles comma-separated multi-value query parameter parsing and SQL IN clause generation. It takes a raw query string value (e.g., `"MIT,Apache-2.0"`) and produces a filter condition suitable for use in SeaORM queries.

**How it is reused:** Called directly in `modules/fundamental/src/package/endpoints/list.rs` to parse the `license` query parameter. The handler extracts the optional `license` string from the query struct and passes it to `apply_filter`, which returns the parsed filter values. This avoids writing custom comma-splitting logic or building SQL IN clauses manually.

**Why direct reuse is appropriate:**
- `common` is already a dependency of the `fundamental` module (it provides `PaginatedResults`, `AppError`, and other shared types used by the package endpoints)
- `apply_filter` is a public function designed for exactly this use case
- The advisory module's severity filter already uses `apply_filter` the same way, confirming the pattern is established

**What is NOT done:** No new wrapper function is created around `apply_filter`. No custom string-splitting or parameter-parsing logic is written. The function is called as-is with no modifications to `query.rs`.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** A structurally identical filter implementation -- the advisory list endpoint supports a `severity` query parameter using the same filtering approach needed for the license filter. It demonstrates the complete pattern: Query struct with optional filter field, `apply_filter` call, and pass-through to the service layer.

**How it is reused:** The advisory endpoint's pattern is followed as a structural template for the package endpoint changes:

1. **Query struct pattern:** The advisory endpoint defines a Query struct with `severity: Option<String>`. The package endpoint's Query struct gains a `license: Option<String>` field following the same convention.

2. **Handler pattern:** The advisory handler calls `apply_filter` on the severity field and passes the result to `AdvisoryService::list()`. The package handler follows the same sequence: extract `license` from query, call `apply_filter`, pass to `PackageService::list()`.

3. **Service integration pattern:** The advisory service accepts the parsed filter and applies it to the database query. The package service follows the same approach for the license filter, adding a JOIN to `package_license` (which is specific to the license domain but follows the same query-building conventions).

**Why pattern-following is appropriate:** The advisory and package modules are sibling modules within `modules/fundamental/` sharing the same `model/ + service/ + endpoints/` structure. Implementing the license filter differently from the severity filter would introduce inconsistency without justification.

**What is NOT done:** The advisory code is not copied wholesale -- it serves as a structural reference. The license filter has its own domain-specific concerns (the JOIN through `package_license`) but the endpoint-layer pattern is identical.

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides:** An existing SeaORM entity that maps the `package_license` database table -- the join table linking packages to their declared licenses. It defines the entity's columns, relations, and model struct, enabling type-safe ORM queries.

**How it is reused:** Used in `modules/fundamental/src/package/service/mod.rs` to build the JOIN query when a license filter is active. Instead of writing raw SQL (`JOIN package_license ON ...`), the implementation uses the SeaORM entity to express the join:

- The `package_license::Entity` is used in a `.join()` call on the package query
- The `package_license::Column::LicenseSpdx` (or equivalent column name) is used in the `.filter()` call with `ColumnTrait::is_in(license_values)`
- The relation between `package` and `package_license` defined in the entity is used for the join condition

**Why entity reuse is appropriate:**
- `entity` is already a dependency of the `fundamental` module (other entities like `package.rs` are already used by `PackageService`)
- The entity encapsulates the table schema, column names, and relations -- using it ensures type safety and avoids hardcoded SQL strings
- If the `package_license` table schema changes in the future, the entity definition is the single source of truth and all consumers benefit from the update

**What is NOT done:** No raw SQL is written for the join. No new entity or model is created for the package-license relationship. The existing entity at `entity/src/package_license.rs` is used without modification.

---

## Duplication Avoidance Summary

| Potential duplication | Avoided by |
|----------------------|------------|
| Custom comma-separated parameter parsing | Reusing `apply_filter` from `common/src/db/query.rs` |
| Custom SQL IN clause generation | Reusing `apply_filter` which handles this |
| New endpoint filter pattern | Following the established pattern from `advisory/endpoints/list.rs` |
| Raw SQL JOIN for package-license | Using the existing SeaORM entity `entity/src/package_license.rs` |
| New join table entity/model | Using the existing `package_license` entity as-is |

No new utility functions, helpers, or shared modules are proposed. All implementation logic is scoped to the two files being modified and the one test file being created, leveraging the three reuse candidates for all shared concerns.
