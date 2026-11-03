# Reuse Analysis — TC-9203

The task lists three Reuse Candidates. The plan uses all three, and adds no new logic that
duplicates them.

## 1. `common/src/db/query.rs::apply_filter` — USE DIRECTLY

- **What it provides**: parses a query-parameter value that may be single or
  comma-separated and turns it into a SQL `IN (...)` condition on a given column.
- **How it is used**: in `PackageService::list`
  (`modules/fundamental/src/package/service/mod.rs`), after joining `package_license`:
  ```rust
  if let Some(license) = license {
      select = select.inner_join(package_license::Entity);
      select = apply_filter(select, package_license::Column::License, license)?;
      select = select.distinct();
  }
  ```
  The exact argument order and return type are confirmed with
  `find_symbol("apply_filter", include_body=true)` on `serena_backend` before writing
  the code.
- **What is not written**: no custom `split(',')` loop and no hand-built `IN` clause in
  the package module. Both the single-value form (`MIT`) and the multi-value form
  (`MIT,Apache-2.0`) go through the shared helper.
- **Visibility/dependency check**: `common` is already a dependency of
  `modules/fundamental` (the advisory module uses the helper), so no new crate dependency
  is needed. If `apply_filter` turned out to be non-`pub`, the skill's "reuse over
  duplication" rule applies: the dependency already exists, so the function would be made
  `pub` rather than copied. That edit is outside Files to Modify, so it would be flagged
  for approval.
- **Validation**: if `apply_filter` already rejects empty or invalid tokens with an error,
  map that error to 400 and add no separate validator. Otherwise add only a small token
  check (non-empty, SPDX charset) in the handler, and first search the repo for an
  existing validator to reuse.

## 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter) — FOLLOW AS PATTERN

- **What it provides**: the reference implementation of an optional, comma-separated
  filter parameter on a list endpoint. The task describes it as structurally identical.
- **How it is used**, mirrored in `modules/fundamental/src/package/endpoints/list.rs`:
  - Query struct: add `license: Option<String>` the same way advisory declares
    `severity: Option<String>`, with the same derives, `#[serde(default)]` and
    utoipa/`IntoParams` annotations
  - Handler flow: extract `Query<...>`, pass `query.license.as_deref()` to the service,
    and return `Result<Json<PaginatedResults<PackageSummary>>, AppError>` with `.context()`
  - Error mapping: invalid filter values produce the same `AppError` variant / 400 response
    that the severity path uses
  - Service plumbing: the way `AdvisoryService::list` accepts the severity filter
    (separate argument vs. filter struct) decides how `PackageService::list` accepts
    `license`
  - Tests: `tests/api/advisory.rs` severity tests are the template for
    `tests/api/package_license_filter.rs` (test context setup, request helpers,
    `assert_eq!(resp.status(), StatusCode::OK)`)
- **Difference from severity**: severity is likely a column on `advisory` itself, while
  license lives in a join table. So the package version adds a join (candidate 3) and
  `.distinct()` to avoid duplicate rows. Without it, a package with two matching licenses
  would be counted twice in pagination.

## 3. `entity/src/package_license.rs` — USE FOR THE JOIN

- **What it provides**: the SeaORM entity for the package-to-license mapping table
  (`Column::PackageId`, `Column::License`) and its `Relation` to `package::Entity`.
- **How it is used**: `package::Entity::find().inner_join(package_license::Entity)`, or
  `.join(JoinType::InnerJoin, package::Relation::PackageLicense.def())`, depending on which
  relation is defined (confirmed via `get_symbols_overview` on `entity/src/package.rs` and
  `entity/src/package_license.rs`). `package_license::Column::License` is the column passed
  to `apply_filter`.
- **What is not written**: no raw SQL, no new entity, and no migration. The join table
  already exists.
- **Scope caveat**: if the `package` → `package_license` `Related`/`Relation` impl is
  missing, a manual `RelationDef` built in the service is preferred, because it avoids
  editing `entity/` (out of scope). Adding the relation to the entity would be flagged for
  approval.

## Additional reuse (found through conventions, not listed as candidates)

- `common/src/model/paginated.rs::PaginatedResults<T>`: the existing response wrapper, kept
  unchanged
- `common/src/error.rs::AppError`: the existing error type and its 400 variant. No new error
  type.
- Existing pagination/sort helpers in `common/src/db/query.rs`, already used by
  `PackageService::list`, are left as they are and composed with the new filter.
- Test harness/fixtures used by `tests/api/advisory.rs` are reused for seeding packages and
  licenses.

## Summary

| Candidate | Decision | Where |
|---|---|---|
| `query.rs::apply_filter` | Reuse directly (comma-split + IN clause) | `package/service/mod.rs` |
| advisory `list.rs` severity filter | Follow pattern (Query struct optional field, handler flow, error mapping, tests) | `package/endpoints/list.rs`, `tests/api/package_license_filter.rs` |
| `entity/package_license.rs` | Use entity/relation for the SeaORM join | `package/service/mod.rs` |

New code is limited to the optional query field, the parameter plumbing, the join plus the
`apply_filter` call, a minimal validation step (only if `apply_filter` does not validate),
and the tests.
