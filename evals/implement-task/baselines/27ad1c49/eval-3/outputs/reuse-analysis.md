# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

## Reuse Candidates from Task Description

The task description identifies three Reuse Candidates. All three are applicable and would be used in the implementation.

---

### 1. `common/src/db/query.rs::apply_filter`

**What it provides:** Handles comma-separated multi-value query parameter parsing and SQL IN clause generation.

**How it would be applied:**

The `apply_filter` function is reused directly in `modules/fundamental/src/package/service/mod.rs` when building the license filter query. When `PackageService::list()` receives a license filter string like `"MIT,Apache-2.0"`, it passes the raw string to `apply_filter`, which:

- Splits the comma-separated string into individual values
- Trims whitespace from each value
- Generates a SQL `IN ('MIT', 'Apache-2.0')` clause (or equivalent SeaORM filter expression)

This eliminates the need to write any custom parsing or splitting logic for multi-value parameters. The function already exists in the `common` crate, which is a dependency of the `fundamental` module, so no new dependency is required -- it can be imported directly.

**Decision:** Reuse directly. No new utility function is created for comma-separated parsing. This follows the DRY principle and ensures any future improvements to `apply_filter` (e.g., escaping, validation) automatically apply to the license filter.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides:** A structurally identical filter implementation (the `severity` query parameter) that demonstrates the pattern for adding optional filters to list endpoints.

**How it would be applied:**

This file serves as a structural template -- the code is not imported, but its pattern is replicated in the package endpoint. Specifically:

- **Query struct pattern:** The advisory list endpoint defines a Query struct with an optional `severity` field. The package list endpoint replicates this by adding an optional `license` field to its own Query struct (or extending it if one already exists).
- **Handler flow:** The advisory handler extracts the severity value from the Query struct and passes it to the advisory service method. The package handler follows the same flow: extract the license value and pass it to `PackageService::list()`.
- **Service integration:** The advisory service method applies the severity filter conditionally (only when `Some`). The package service method follows the same conditional pattern for the license filter.

By following the advisory endpoint as a template, the implementation maintains consistency across the codebase: both filters use the same handler-to-service data flow, the same query struct conventions, and the same conditional filtering approach. This makes the codebase predictable for future maintainers.

**Decision:** Follow as a structural pattern. No code is copied or imported -- the same architectural approach is applied to the package module.

---

### 3. `entity/src/package_license.rs`

**What it provides:** The existing SeaORM entity definition for the package-license join table, which maps packages to their declared licenses.

**How it would be applied:**

The `package_license` entity is used in `PackageService::list()` to build a JOIN query that connects packages to their licenses:

- **JOIN construction:** The service method references `package_license::Entity`, `package_license::Column`, and `package_license::Relation` to construct a SeaORM join from the `package` table to the `package_license` table. The join key is the package ID foreign key.
- **Filter application:** After the JOIN, the `apply_filter` output is applied to `package_license::Column::LicenseId` (or the equivalent SPDX identifier column) to filter for the requested license values.
- **No raw SQL:** By using the existing entity, the query is built entirely through SeaORM's type-safe query builder. This avoids raw SQL strings, ensures compile-time verification of column names, and maintains consistency with how other join queries are constructed throughout the codebase.

The `entity` crate is already a dependency of the `fundamental` module (since `PackageService` already queries the `package` entity), so importing `package_license` requires no new dependency.

**Decision:** Reuse directly. The existing entity provides all necessary columns and relations for the JOIN query. No new entity, migration, or raw SQL is needed.

---

## Summary

| Reuse Candidate | Reuse Type | Location Used | New Code Avoided |
|---|---|---|---|
| `apply_filter` | Direct function reuse | `package/service/mod.rs` | Custom comma-separated parsing and SQL IN clause generation |
| `advisory/endpoints/list.rs` | Structural pattern | `package/endpoints/list.rs` | Ad-hoc filter design; maintains codebase consistency |
| `package_license.rs` | Direct entity reuse | `package/service/mod.rs` | Raw SQL joins; new entity definitions |

All three candidates are used as described in the task. No new utility functions, entities, or query helpers are created that would duplicate existing functionality.
