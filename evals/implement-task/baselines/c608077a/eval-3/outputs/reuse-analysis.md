# Reuse Analysis — TC-9203

The task lists three Reuse Candidates. **All three are used. No duplicate filtering,
parsing, or join logic gets written.** Each one would be confirmed with
`mcp__serena_backend__find_symbol(include_body=true)` before implementation.

## 1. `common/src/db/query.rs::apply_filter` — used directly

- **What it provides**: parses a comma-separated multi-value query parameter and generates
  the SQL condition (`col = v` for one value, `col IN (v1, v2, ...)` for several).
- **How it is used**: in `PackageService::list`
  (`modules/fundamental/src/package/service/mod.rs`), after the join on `package_license`:
  ```rust
  if let Some(license) = license {
      select = apply_filter(select, package_license::Column::License, license)?;
  }
  ```
  The exact call shape (whether it takes a `Select<E>` or returns a `Condition`, and whether
  it is fallible) would be copied from how `AdvisoryService::list` calls it for `severity`.
- **What it replaces**: there will be no hand-written `split(',')`, no hand-written
  `Expr::col(...).is_in(...)`, and no special-casing of single versus multiple values.
- **Visibility and dependency**: `common` is already a dependency of
  `modules/fundamental`, because the advisory module uses it. If `apply_filter` turns out to
  be private, the skill's "Reuse over duplication" rule applies: make it `pub` instead of
  copying it, and flag that change because `common/src/db/query.rs` is outside the listed files.
- **Validation**: if `apply_filter` already rejects empty tokens, the 400 case for empty or
  malformed input comes for free. If it does not, the endpoint does a small SPDX-syntax check
  and still calls `apply_filter` for the parsing and SQL work. The check is not a second
  parser. First I would search for an existing license or SPDX validator and use it if one
  exists.

## 2. `modules/fundamental/src/advisory/endpoints/list.rs` — pattern followed

- **What it provides**: a working example of an optional, comma-separated filter
  (`severity`) on a list endpoint.
- **How it is used**: as the template for `modules/fundamental/src/package/endpoints/list.rs`:
  - the same Query struct shape: an `Option<String>` field with the same serde and
    `IntoParams` derives and the same way of flattening pagination
  - the same handler flow: extract `Query<...>`, pass `as_deref()` to the service, return
    `Result<Json<PaginatedResults<_>>, AppError>` with `.context()`
  - the same utoipa `params(...)` documentation style, if present
- **Not copied**: no code moves out of the advisory module. It is only a structural
  reference, so the two endpoints stay consistent (sibling parity).
- **Paired reference**: the advisory service method (`advisory/service/advisory.rs`) shows
  how the endpoint value gets to `apply_filter`. That is the pattern for
  `PackageService::list`.

## 3. `entity/src/package_license.rs` — used for the JOIN

- **What it provides**: the SeaORM entity for the package to license mapping table
  (`Entity`, `Column::License`, `Column::PackageId`, and `Relation`s).
- **How it is used**: in `PackageService::list`, join with the SeaORM relation API
  (`.inner_join(package_license::Entity)` or
  `.join(JoinType::InnerJoin, package::Relation::PackageLicense.def())`), and pass
  `package_license::Column::License` to `apply_filter`. There is **no raw SQL**.
- **Dedup handling**: packages with several licenses can match more than one row, so the
  query uses `.distinct()` (or groups by package id) to keep `PaginatedResults` items and
  totals correct.
- **Check before use**: confirm that `entity/src/package.rs` declares the
  `Related<package_license::Entity>` relation. If it does not, use
  `package_license::Relation::Package.def().rev()` rather than editing the entity file,
  which is out of scope.

## Additional reuse (not listed as candidates)

| Existing code | Use |
|---|---|
| `common/src/model/paginated.rs::PaginatedResults<T>` | Return type stays as is. The response shape does not change. |
| `common/src/error.rs::AppError` | Its existing bad-request variant produces the 400. No new error type. |
| Existing pagination/sort helpers in `common/src/db/query.rs` | Package list keeps using them. Only the filter step is added. |
| `tests/api/advisory.rs` setup helpers | The new test file reuses the same test-DB and client setup and seeding approach instead of creating new fixtures. If those helpers live in a shared test-utility module, import them. |

## Symbol deduplication check

Before declaring anything new (for example a `PackageListQuery` struct or a license-validation
helper), grep the `fundamental` and `common` crates for `PackageListQuery`, `PackageQuery`,
`license`, and `spdx`. If the package endpoint already has a Query struct, add the `license`
field to it instead of creating a new struct.

## Planned new code

- One `Option<String>` field on the package Query struct, plus its doc comment
- One new parameter on `PackageService::list`, plus the conditional join and `apply_filter` call
- A minimal SPDX-syntax validation, only if neither `apply_filter` nor an existing helper
  already covers it
- The new integration test file
