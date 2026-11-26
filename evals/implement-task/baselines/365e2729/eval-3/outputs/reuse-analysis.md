# Reuse Analysis — TC-9203

The task lists three Reuse Candidates. The plan uses all three, and none of their logic is duplicated.

## 1. `common/src/db/query.rs::apply_filter` — USED DIRECTLY

- **What it does:** parses a comma-separated query parameter (single or multiple values) and builds the SQL `IN (...)` condition, or `=` for a single value.
- **How it is used:** `PackageService::list` in `modules/fundamental/src/package/service/mod.rs` calls `apply_filter(query, entity::package_license::Column::License, license_param)` after joining `package_license`. This one call covers both `?license=MIT` and `?license=MIT,Apache-2.0`.
- **What is not written:** no new comma-splitting code and no hand-built `IN` clause.
- **Verification first:** `find_symbol("apply_filter", include_body=true)` confirms the signature (it may take a `Select<E>` and a column, or work as a `Condition` builder) and that it is `pub`.
- **Dependency check:** `modules/fundamental` already depends on `common`, because it uses `PaginatedResults` and `AppError`, so no new crate dependency is needed. If `apply_filter` is not exported, the skill's "Reuse over duplication" rule applies: make it `pub` instead of copying it, and say so in the PR description.
- **Note:** the handler's validation step (400 for empty segments or non-SPDX characters) only checks the input. It does not parse values into the filter. Splitting and filtering stay inside `apply_filter`. If `apply_filter` already returns an error on malformed input, the handler maps that error to 400 and does not repeat the check.

## 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter) — USED AS THE PATTERN

- **What it is:** the advisory list endpoint's optional `severity` query parameter. It is built the same way as the license filter this task needs.
- **How it is used:** the package list endpoint copies its structure:
  - an `Option<String>` field (`license`) on the package list Query struct, with the same derives, `IntoParams`/utoipa annotations and doc-comment style as `severity`
  - the same extraction in the handler (`Query<...>`) and the same way of passing the value into the service
  - the same error-handling style (`Result<_, AppError>` with `.context()`)
- **Service layer too:** `advisory/service/advisory.rs` is the reference for how the service receives the filter and calls `apply_filter`, so the package service signature matches it.
- **Tests:** `tests/api/advisory.rs` (the severity filter tests, if present) is the template for setup and assertion style in `tests/api/package_license_filter.rs`.

## 3. `entity/src/package_license.rs` — USED FOR THE JOIN

- **What it is:** the SeaORM entity for the package-to-license mapping table.
- **How it is used:** the service joins through the entity's relation, `.join(JoinType::InnerJoin, entity::package::Relation::PackageLicense.def())`, or the reverse relation defined in `package_license.rs`. It filters on `entity::package_license::Column::License` (the actual column name is confirmed with `get_symbols_overview`).
- **What is not written:** no raw SQL and no new entity or migration.
- **Duplicate rows:** `.distinct()` (or a group by on package id) stops a package with several matching licenses from appearing twice and skewing the pagination totals.
- **Missing relation:** if `entity/src/package.rs` does not declare a `Related<package_license::Entity>` impl, the plan uses `JoinType::InnerJoin` with the `package_license` relation defined from that side. Adding a relation to `package.rs` would be out of scope and would be flagged for approval.

## Other reuse checks (Step 4 / Step 9)

- **`PaginatedResults<PackageSummary>`** (`common/src/model/paginated.rs`): the response type is reused unchanged, which satisfies the "response shape unchanged" criterion.
- **`AppError`** (`common/src/error.rs`): an existing variant that maps to 400 is used for invalid licenses. No new error type is added.
- **SPDX validation:** before writing a license-ID validator, search `common/` and `modules/` for an existing SPDX or license validator, for example in the ingestor, which parses SBOM license fields. Reuse it if found. Otherwise add a small private helper in `endpoints/list.rs`.
- **Test fixtures:** reuse the existing test DB and app setup helpers from `tests/api/` (as used in `advisory.rs` and `sbom.rs`) instead of writing new bootstrap code.

## Summary

| Candidate | Decision | Where it is used |
|---|---|---|
| `common::db::query::apply_filter` | Call directly | `package/service/mod.rs` |
| Advisory `severity` filter | Follow its structure | `package/endpoints/list.rs`, service signature, tests |
| `entity::package_license` | Use for the SeaORM join | `package/service/mod.rs` |
