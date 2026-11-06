# Reuse Analysis — TC-9203

The task lists three Reuse Candidates. I would use all three. No new filtering, parsing, or SQL helpers would be written.

## 1. `common/src/db/query.rs::apply_filter` — USE DIRECTLY

- **What it provides:** parses a comma-separated multi-value query parameter and generates the SQL condition (`=` for one value, `IN (...)` for several).
- **How I would use it:** in `PackageService::list` (`modules/fundamental/src/package/service/mod.rs`), when `license` is `Some`, call `apply_filter` against `package_license::Column::License` on the joined select. Both acceptance criteria (single `MIT` and multi `MIT,Apache-2.0`) come from this one call.
- **What I would avoid:** no hand-written `split(',')`, no manual `Condition::any()` loop, and no `IN` clause construction in the package module.
- **Things to check before coding** (`find_symbol include_body=true`):
  - The exact signature (generic over the column, and whether it takes `&str` or `Option<&str>`).
  - Whether it trims whitespace and rejects empty tokens. If it already returns an error for bad input, that error carries the 400 criterion and no extra validator is needed. If it does not, add a small validation step in the endpoint only.
  - Visibility. It should be `pub`, since advisory already uses it. If it is not exported, `common` is already a dependency of `fundamental`, so the rule is to make it `pub` rather than duplicate it. That edit is outside the listed files, so it would be flagged for approval.

## 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter) — FOLLOW AS PATTERN

- **What it provides:** a working example of an optional comma-separated filter on a list endpoint. It covers the Query struct field (`severity: Option<String>`), serde and OpenAPI param annotations, how invalid values become an `AppError` 400, and how the value is passed to the service layer.
- **How I would use it:** mirror it in `modules/fundamental/src/package/endpoints/list.rs`:
  - Add `license: Option<String>` with the same derives and attributes (`#[serde(default)]`, `IntoParams` doc) to the package Query struct.
  - Pass `query.license.as_deref()` to `PackageService::list` the same way severity reaches `AdvisoryService`.
  - Use the same `AppError` variant and `.context()` style for validation failures.
- **Companion reference:** `advisory/service/advisory.rs` shows how the service calls `apply_filter`. The package service change copies that call shape.
- **Tests:** `tests/api/advisory.rs` (the severity filter tests) is the template for setup, client usage, and assertion style in `tests/api/package_license_filter.rs`. Per skill guidance, I would strengthen it with value-based assertions on package names and licenses, `///` doc comments, and Given/When/Then sections.

## 3. `entity/src/package_license.rs` — USE FOR THE JOIN

- **What it provides:** the SeaORM entity for the package-to-license mapping table, with its `Column` enum and `Relation` to `package`.
- **How I would use it:** `package::Entity::find().join(JoinType::InnerJoin, <package -> package_license relation>.def())`, then apply `apply_filter` on `package_license::Column::License`. Add `.distinct()` so a package with several matching licenses appears only once and pagination totals stay correct.
- **What I would avoid:** raw SQL, `Statement::from_string`, or a newly declared join entity. The join is only added when `license` is `Some`, so the unfiltered query (the no-regression criterion) is unchanged.
- **Check:** confirm the `Related<package::Entity>` / `Relation` definition exists. If it does not, `JoinType::InnerJoin` with `package_license::Relation::Package.def().rev()` covers it, still without raw SQL.

## Additional reuse (found during Step 4 analysis, not listed in the task)

- `common/src/model/paginated.rs::PaginatedResults<T>`: keep it as the response type. Nothing new is created, so the response shape is unchanged.
- `common/src/error.rs::AppError`: reuse its existing bad-request variant for invalid license values. No new error type is created.
- Symbol deduplication: before adding any SPDX validation helper or license constant, run `search_for_pattern` for `license`, `spdx`, and `SPDX` across `common/` and `modules/`. If a validator exists (for example one used by ingestion), import it instead of writing one.

## Summary

| Candidate | Decision | Used in |
|---|---|---|
| `common/src/db/query.rs::apply_filter` | Reuse directly | `package/service/mod.rs` |
| advisory `endpoints/list.rs` severity filter | Follow as structural pattern | `package/endpoints/list.rs`, tests |
| `entity/src/package_license.rs` | Reuse for SeaORM JOIN | `package/service/mod.rs` |
| `PaginatedResults`, `AppError` (extra) | Reuse unchanged | endpoint and service |

The only new logic written is the optional field, passing the value through to the service, the conditional join, and (only if `apply_filter` does not already do it) input validation that returns 400.
