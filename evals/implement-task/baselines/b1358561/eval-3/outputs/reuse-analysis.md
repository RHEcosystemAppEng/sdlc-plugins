# Reuse Analysis — TC-9203

The task lists three Reuse Candidates, and the plan uses all three. No new filtering, parsing, or SQL-generation logic is written. The only new logic is input validation for the 400 case, and that too is reused if an equivalent already exists.

## 1. `common/src/db/query.rs::apply_filter`: reused directly

- **What it does**: parses a single or comma-separated query parameter value and generates the SQL `IN (...)` condition (or `=` for a single value) on a given column.
- **How it is used**: `PackageService::list` (`modules/fundamental/src/package/service/mod.rs`) calls it after joining `package_license`:
  ```rust
  let select = match license {
      Some(value) => apply_filter(
          package::Entity::find()
              .join(JoinType::InnerJoin, package::Relation::PackageLicense.def())
              .distinct(),
          package_license::Column::License,
          value,
      ),
      None => package::Entity::find(),
  };
  ```
  The exact argument order and return type are confirmed with `mcp__serena_backend__find_symbol("apply_filter", include_body=true)` before writing the call.
- **What it avoids**: hand-written `split(',')` and trim logic, and hand-built `Condition::any()` / `is_in` expressions.
- **Visibility and dependency check (skill Reuse rules 1 and 2)**:
  - If `apply_filter` is `pub` (expected, since the advisory module already uses it), import it with `use common::db::query::apply_filter;`.
  - If it is not exported: `common` is already a dependency of `modules/fundamental` (it supplies `PaginatedResults` and `AppError`), so the fix is to make it `pub` rather than copy it. That decision would be recorded in the commit body or PR description.
- **Validation**: if `apply_filter` already rejects empty segments (for example `MIT,,`) and returns an error, that error is mapped to the 400 variant of `AppError` and no separate check is added. Otherwise a small validator is added in the package endpoint. Step 4 first searches for an existing SPDX/license validator (`validate_license`, `spdx`, `SPDX`) and reuses it if found.

## 2. `modules/fundamental/src/advisory/endpoints/list.rs`: pattern followed (structural reuse)

- **What it provides**: the reference implementation of an optional, comma-separated `severity` filter. It has a `Deserialize` Query struct with an `Option<String>` field, passes the field to `AdvisoryService::list`, and rejects invalid values with a 400.
- **How it is used**: this is a pattern to mirror, not code to import. The plan matches it in four places:
  - **Query struct**: `license: Option<String>` with `#[serde(default)]`, added to the package list Query struct next to the existing pagination fields, with the same derives (`Deserialize`, plus `IntoParams` if the advisory struct has it).
  - **Handler flow**: extract `Query<...>`, then validate, then call the service with `query.license.as_deref()`, then return `PaginatedResults<PackageSummary>`. The return type stays the same, so the response shape is unchanged.
  - **Error handling**: the same 400 variant of `AppError` and the same `.context()` usage.
  - **Service parameter**: `PackageService::list(..., license: Option<&str>)` mirrors the shape of the severity parameter on `AdvisoryService::list`.
  - **OpenAPI**: if the advisory endpoint documents `severity` in `#[utoipa::path(params(...))]`, `license` is documented the same way.
- **Tests**: `tests/api/advisory.rs` is the sibling template for the new `tests/api/package_license_filter.rs`, including fixture setup, the HTTP client, and `assert_eq!(resp.status(), StatusCode::OK)`. The new tests also assert on the returned package names by value and carry `///` doc comments with Given/When/Then sections, as the skill rules require.
- **Why not extract a shared helper**: the advisory and package handlers differ only in field name and target column, and `apply_filter` already holds the shared part. A new generic abstraction would expand scope for no benefit.

## 3. `entity/src/package_license.rs`: reused for the JOIN

- **What it provides**: the SeaORM entity for the package-to-license mapping table (`Model`, `Column`, `Relation` to `package`).
- **How it is used**: the license filter joins `package` to `package_license` through the entity's SeaORM relation (`Relation` / `Related` impl), and `package_license::Column::License` is the column handed to `apply_filter`. No raw SQL and no new entity or migration.
- **Check before use**: `get_symbols_overview` on `entity/src/package_license.rs` confirms the column name (`license` vs `spdx_id`) and that a relation to `package` exists. If only the reverse relation exists, `.rev()` is used on it. If no relation is defined at all, adding one to `entity/src/package_license.rs` falls outside the listed files, so it would be flagged for user approval in Step 9 rather than worked around with raw SQL.
- **Duplicate rows**: a package with several licenses could appear more than once after the join, so `.distinct()` is applied when the filter is active to keep `PaginatedResults.total` and the items correct.

## Summary

| Candidate | Reuse type | Where used | New code avoided |
|---|---|---|---|
| `common::db::query::apply_filter` | Direct import | `package/service/mod.rs` | comma parsing, `IN` clause generation |
| `advisory/endpoints/list.rs` severity filter | Pattern mirror | `package/endpoints/list.rs`, tests | redesigning query param, validation, and error flow |
| `entity::package_license` | Direct import (SeaORM entity/relation) | `package/service/mod.rs` | raw SQL join, new entity |

Self-verification check 5 (Duplication) is expected to PASS. The only potentially new function is the license validator, and it is written only if Step 4 finds no existing equivalent and `apply_filter` does not already reject bad input.
