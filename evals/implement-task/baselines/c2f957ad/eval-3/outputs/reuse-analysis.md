# Reuse Analysis — TC-9203

The task lists three Reuse Candidates. The plan uses all three, so the license filter needs no new parsing, SQL or join code.

## 1. `common/src/db/query.rs::apply_filter` — USED DIRECTLY

- **What it provides:** it parses a single or comma-separated query-param value and builds the matching SeaORM condition: `=` for one value, `IN (...)` for several.
- **How it is used:** in `PackageService::list` (`modules/fundamental/src/package/service/mod.rs`), it is applied to the select after joining `package_license`:
  ```rust
  if let Some(license) = license {
      select = apply_filter(select, package_license::Column::License, license)?;
  }
  ```
  The exact signature and return type are confirmed first with `mcp__serena_backend__find_symbol("apply_filter", include_body=true)`, and the call is adapted if it takes a `Condition` or returns `Result`.
- **What is avoided:**
  - hand-written `split(',')`, trim and `is_in(...)` logic in the package module
  - a second, slightly different multi-value parser
- **Visibility:**
  - `common` is already a dependency of `modules/fundamental` (the advisory module uses this helper), so no new crate dependency is needed.
  - If `apply_filter` were somehow not `pub`, the skill's "reuse over duplication" rule applies: the dependency already exists, so the right move is to make it `pub`, not copy it. That edit is outside the file scope, so it would be flagged for approval.
- **Validation:** if `apply_filter` already rejects empty segments with an error that maps to 400, the endpoint relies on it. A license-specific charset check is added in `list.rs` only for what `apply_filter` does not cover, such as invalid SPDX characters.

## 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter) — USED AS THE STRUCTURAL TEMPLATE

- **What it provides:** a working example of an optional, comma-separated filter param on a list endpoint. It covers:
  - the `Query` struct with an `Option<String>` field
  - `IntoParams` / utoipa docs
  - validation that returns `AppError` (400)
  - passing the value into the service
- **How it is used in `modules/fundamental/src/package/endpoints/list.rs`:**
  - Add `license: Option<String>` to the package list query struct, with the same derives, serde attributes and doc-comment style as `severity`.
  - Validate it the same way severity is validated, with the same `AppError::BadRequest` variant and `.context()` style.
  - Thread it to the service the way severity is threaded to `AdvisoryService` (a positional `Option<&str>` or a filter struct, whichever the sibling uses).
  - Add the `license` entry to the `#[utoipa::path]` params like the severity entry.
- **Service side:** the advisory service list method (`advisory/service/advisory.rs`) is read too, to copy how it calls `apply_filter`. This keeps both services consistent (sibling parity).
- **Tests:** `tests/api/advisory.rs` severity-filter tests serve as the template for the fixture setup and the request/assert style in `tests/api/package_license_filter.rs`.

## 3. `entity/src/package_license.rs` — USED FOR THE JOIN

- **What it provides:** the SeaORM entity for the package-license mapping table, with columns such as `package_id` and `license`, plus `Relation` definitions to `package`.
- **How it is used:** in `PackageService::list`, when a license filter is present:
  ```rust
  select = select
      .join(JoinType::InnerJoin, package::Relation::PackageLicense.def())
      .distinct();
  ```
  Then `apply_filter` is called on `package_license::Column::License`.
- **Why it matters:**
  - no raw SQL
  - the join stays type-safe
  - `.distinct()` stops packages with several matching licenses from being duplicated or inflating the pagination total
- **Check first:** confirm that `package::Relation` / `Related<package_license::Entity>` exists. If only the reverse relation is defined, join with `package_license::Relation::Package.def().rev()` so no entity file needs editing (it is out of scope).

## Additional reuse found / planned checks

- **`PaginatedResults<T>`** (`common/src/model/paginated.rs`): stays the response type, with no change, so the response shape is preserved.
- **`AppError`** (`common/src/error.rs`): its existing BadRequest variant provides the 400 response. No new error type.
- **Existing pagination/sort helpers** in `query.rs`: still applied after the filter, so a filtered query paginates the same way as an unfiltered one.
- **Symbol deduplication:** before declaring anything new (for example a license-id regex or a constant), grep `common/` and `modules/` for an existing SPDX or license validator (`spdx`, `LICENSE_`, `validate_license`). If one exists, reuse it.

## Not reused / not needed

- No new query helper, no new entity and no migration: the `package_license` table already exists.
