# Reuse Analysis — TC-9203

The task lists three Reuse Candidates, and all three are used. No new filtering, parsing,
or SQL-building logic is written. The only code that may be new is input validation for
the 400 case, and only if no existing helper covers it.

## 1. `common/src/db/query.rs::apply_filter`: reused directly

- **What it provides:** it parses a query value that may be comma-separated (`"MIT,Apache-2.0"`)
  and produces a SeaORM condition. One value becomes `col = v`. Several values become `col IN (v1, v2)`.
- **How it is used:** it is called once in `PackageService::list`
  (`modules/fundamental/src/package/service/mod.rs`) on the column
  `package_license::Column::License`, with the raw `license` string from the request:
  ```rust
  if let Some(license) = license {
      select = apply_filter(
          select.join(JoinType::InnerJoin, package::Relation::PackageLicense.def()).distinct(),
          package_license::Column::License,
          license,
      );
  }
  ```
- **What is NOT written:** no `split(',')` in the service, no hand-built `IN` clause, no
  per-value `OR` loop. Both acceptance criteria for single and multiple values are handled by
  this one helper.
- **Verification before use:** read its body with `mcp__serena_backend__find_symbol`
  (`include_body=true`) to confirm:
  - the exact signature (generic over `Select<E>`? does it take a `Column` or an expression?)
  - whitespace trimming
  - whether it returns `Result` for invalid or empty input. If it does, propagate that error
    as the 400 instead of writing a separate validator.
- **Visibility:** `common` is already a dependency of `modules/fundamental`, because list
  endpoints already use the pagination helpers from `query.rs`. If `apply_filter` turned out
  to be non-`pub`, the "Reuse over duplication" rule applies: make it `pub` rather than copy
  it. That edit is outside the listed files, so it is flagged for approval.

## 2. `modules/fundamental/src/advisory/endpoints/list.rs`: pattern to follow (severity filter)

- **What it provides:** the reference structure for an optional filter on a list endpoint:
  - a Query struct with `severity: Option<String>`
  - extraction via Axum `Query<...>`
  - the value passed into `AdvisoryService::list`, which calls `apply_filter`
- **How it is used:** the change in `package/endpoints/list.rs` mirrors it one-to-one:
  - add `license: Option<String>` to the package list Query struct, using the same derives,
    serde attributes, and OpenAPI `IntoParams` annotations as `severity`
  - pass `query.license.as_deref()` to `PackageService::list`, using the same parameter
    position and style as the advisory handler, which keeps caller-site parity
  - use the same error handling (`Result<_, AppError>` with `.context(...)`)
- Also inspect `advisory/service/advisory.rs`, so the service-level signature change
  (`Option<&str>` vs a filter struct) matches the advisory service exactly.
- **Gap compared with the pattern:** the task requires **400 for invalid license values**.
  If the advisory endpoint already validates `severity` (for example against an enum), copy
  that validation shape. A license is free-form SPDX, so the equivalent check is: no empty
  elements and only SPDX identifier characters. Search the codebase first (see the next
  section). Only add a small private, documented `validate_license_ids` in
  `package/endpoints/list.rs` if nothing exists.

## 3. `entity/src/package_license.rs`: used for the join

- **What it provides:** the SeaORM entity for the package-to-license mapping table, with its
  `Column::License` / `Column::PackageId` and its relation to `package::Entity`.
- **How it is used:**
  - join from `package::Entity` to `package_license::Entity` through the SeaORM relation
    (`package::Relation::PackageLicense.def()`, or `.inner_join(package_license::Entity)`
    if `Related` is implemented)
  - filter on `package_license::Column::License` using `apply_filter`
  - apply `.distinct()` so a package that matches several requested licenses is returned
    once and pagination totals stay correct
- **What is NOT written:** no raw SQL, no new entity, no migration.
- **Verification:** `find_symbol` on `package_license::Relation` and on
  `package::Relation` / `impl Related`. If the relation is defined only on the
  `package_license` side, join from that side
  (`package_license::Relation::Package.def().rev()`) instead of editing `entity/src/package.rs`.
  Editing that file would be out of scope.

## Additional reuse (found through the skill's reuse-first checks)

| Existing code | Reuse |
|---|---|
| Pagination and sorting helpers in `common/src/db/query.rs` | kept as they are in `PackageService::list`, and applied after the license filter so count and paging respect it |
| `PaginatedResults<T>` (`common/src/model/paginated.rs`) | unchanged response wrapper, which satisfies "response shape unchanged" |
| `AppError` bad-request variant (`common/src/error.rs`) | used for the 400. No new error type |
| Test harness, fixtures, and HTTP client helpers used by `tests/api/advisory.rs` / `sbom.rs` | reused in `tests/api/package_license_filter.rs`, along with the `assert_eq!(resp.status(), StatusCode::OK)` style |

## Symbol deduplication searches (before declaring anything new)
- `search_for_pattern` for `spdx|SPDX|license` in `common/` and `modules/`, looking for an
  existing license validator or parser.
- Search for `validate_` helpers in `common/src/db/query.rs`.
- Search for any existing `LicenseFilter`, `PackageListQuery`, or `PackageQuery` struct, so
  the existing struct is extended instead of a new one being created.

## Duplication check (Step 9)
After implementation, grep the diff for `split(','`, `is_in(`, and `Condition::any()`. None
should appear in the new code, because all multi-value handling must go through `apply_filter`.
