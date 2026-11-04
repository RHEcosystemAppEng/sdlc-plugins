# Reuse Analysis — TC-9203

The task lists three Reuse Candidates. All three are used. No new filtering, parsing or join logic
is written where these already provide it.

## 1. `common/src/db/query.rs::apply_filter`: reused directly

- **What it provides**: parses a comma-separated query value (`"MIT,Apache-2.0"`) into separate
  values and builds a SQL `IN (...)` clause (or `=` for a single value) on a given column.
- **How it is used**: in `PackageService::list` (`modules/fundamental/src/package/service/mod.rs`),
  when `license` is `Some`, call `apply_filter` on the `Select<package::Entity>` with the
  `package_license` license column and the raw license string. This covers both acceptance criteria
  (single and multi-value) without a hand-written `split(',')` or IN-clause builder.
- **Visibility / dependency check**: `common` is already a dependency of the `fundamental` crate,
  because the advisory module uses this helper. If `apply_filter` were not `pub`, the plan would be
  to make it `pub` (the dependency already exists) and not duplicate it, and to note the change in
  the PR description. It is expected to be public already.
- **Before writing code**: `find_symbol(apply_filter, include_body=true)` confirms the exact
  signature: generic over the entity/select, the column argument, a `Result` return type, and how it
  handles empty items. If it already returns an `AppError` that maps to 400 for malformed input, the
  handler relies on that and does not re-implement it.

## 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter): followed as the structural template

- **What it provides**: the established pattern for an optional, comma-separated filter on a list
  endpoint. That pattern is an optional `Option<String>` field on a `Deserialize` Query struct,
  extracted next to pagination, passed to the service with `.context()`, and documented in the
  utoipa `params`.
- **How it is used**: `modules/fundamental/src/package/endpoints/list.rs` copies this structure.
  It adds `license: Option<String>` to the package Query struct with the same derives, serde
  attributes, extractor placement, error wrapping and OpenAPI annotation. The matching service-side
  reference is `AdvisoryService::list` in `advisory/service/advisory.rs`, which shows how severity
  is handed to `apply_filter`. `PackageService::list` follows it.
- **Not reused verbatim**: the severity field may be validated against a fixed enum. License
  values are open SPDX identifiers, so validation is a syntax check (allowed characters, no empty
  items), not an enum match. This is the only deliberate difference from the template.

## 3. `entity/src/package_license.rs`: used for the JOIN

- **What it provides**: the SeaORM entity for the package-to-license mapping, with `Column`,
  `Relation` and the `Related<package::Entity>` definitions.
- **How it is used**: `PackageService::list` joins `package` to `package_license` with the entity's
  relation (`.join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())` or
  `.inner_join(package_license::Entity)` if `Related` is implemented). It filters on
  `package_license::Column::<License>`. No raw SQL and no new entity or relation.
- **Additional care**: `.distinct()` is applied when the join is active. Packages with several
  matching licenses then appear once, and the pagination `total` stays correct. The
  `PaginatedResults<PackageSummary>` response shape is unchanged.

## Additional reuse (not listed as candidates, found through conventions)

- **`common/src/error.rs::AppError`**: the existing bad-request variant is used for the 400
  response. No new error type.
- **`common/src/model/paginated.rs::PaginatedResults<T>`**: still the response wrapper, unchanged.
- **Test helpers in `tests/api/advisory.rs`** (and any shared test context/fixture setup): reused
  for DB setup, client creation and seeding in `tests/api/package_license_filter.rs`.
- **Symbol deduplication**: before declaring anything license-related (SPDX regex, license
  constants), grep `common/` and `modules/` for `license`/`spdx`/`SPDX`. If a validator exists, it
  is imported, not redeclared.

## What is deliberately NOT created

- No new comma-splitting or IN-clause helper, because `apply_filter` covers it.
- No raw SQL join, because the `package_license` entity covers it.
- No new endpoint, route, or response model. The route registration in `package/endpoints/mod.rs`
  stays unchanged.
