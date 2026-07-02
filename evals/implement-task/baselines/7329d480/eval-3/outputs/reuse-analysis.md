# Reuse Analysis for TC-9203

## Summary

All three Reuse Candidates identified in the task description are directly applicable and will be used. No new utility functions or parsing logic need to be written -- the existing codebase provides everything required for the license filter implementation.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides:** The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL IN clause generation. It takes a raw query parameter string (e.g., `"MIT,Apache-2.0"`), splits it on commas, and produces the appropriate SeaORM filter condition (equivalent to `WHERE column IN ('MIT', 'Apache-2.0')`). It also handles the single-value case transparently.

**How it will be reused:** In `modules/fundamental/src/package/endpoints/list.rs`, when the `license` query parameter is present, pass its value directly to `apply_filter` to parse the comma-separated string and generate the filter condition. This avoids writing any custom string splitting, validation, or SQL generation logic.

**Why reuse instead of writing new code:** Writing a new parser for comma-separated values would duplicate the exact logic already in `apply_filter`. The function already handles edge cases (trimming whitespace, empty segments, single values) and produces correctly typed SeaORM conditions. Duplicating this would violate DRY and risk introducing inconsistencies with how other filters in the codebase work.

**Integration point:** Called from the endpoint handler in `list.rs` after extracting the `license` query parameter from the request. The result is passed to `PackageService::list()` as a filter condition or as parsed values.

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:** The advisory list endpoint implements a structurally identical filter pattern -- it accepts an optional `severity` query parameter, parses it (including comma-separated multi-value support via `apply_filter`), and applies it as a filter condition on the advisory query. The endpoint defines a Query struct with optional filter fields, extracts them in the handler, and passes them to the service layer.

**How it will be reused:** The `list.rs` file in the package endpoints module will follow the same structural pattern:

1. **Query struct**: Add an `Option<String>` field named `license` to the existing query parameter struct, mirroring how `severity` is declared as `Option<String>` in the advisory Query struct.
2. **Handler flow**: In the handler function, check if `license` is `Some`, and if so, call `apply_filter` on the value -- exactly as the advisory handler does with `severity`.
3. **Service call**: Pass the parsed filter to `PackageService::list()` using the same parameter pattern that `AdvisoryService::list()` uses for severity.

**Why follow this pattern:** The advisory severity filter is a proven, reviewed, and tested implementation of the exact same filtering concept. Following it ensures consistency across the codebase and reduces the risk of subtle differences in behavior. It also makes the code easier for reviewers to evaluate since they can compare the new license filter against the existing severity filter.

**Specific elements to mirror:**
- Query struct field declaration and serde attributes
- `apply_filter` invocation in the handler
- Error handling for invalid filter values (returning 400 via `AppError`)
- Passing the filter to the service layer

---

## Reuse Candidate 3: `entity/src/package_license.rs` (package-license join entity)

**What it provides:** The SeaORM entity definition for the `package_license` join table, which maps packages to their declared licenses. It defines the table columns (`package_id`, `license`, and any additional fields), the `Model` struct, the `Relation` enum linking to the `package` and potentially `license` tables, and the `ActiveModel` for inserts/updates.

**How it will be reused:** In `modules/fundamental/src/package/service/mod.rs`, the `PackageService::list()` method will use this entity to construct a JOIN query:

1. **JOIN construction**: Use SeaORM's query builder to add an `InnerJoin` (or `LeftJoin` depending on the desired semantics) from the `package` entity to `package_license` using the relation defined in `entity/src/package_license.rs`. This is done via `.join(JoinType::InnerJoin, entity::package_license::Relation::Package.def().rev())` or equivalent SeaORM API.
2. **Filter application**: After joining, apply a `WHERE package_license.license IN (...)` condition using the parsed license values from `apply_filter`.
3. **No raw SQL**: By using the entity's relation definitions, the JOIN is expressed entirely through SeaORM's type-safe query builder. This avoids raw SQL strings, ensures column names stay in sync with the entity definition, and benefits from compile-time type checking.

**Why reuse instead of raw SQL:** The entity already encodes the table name, column names, and relationships. Using it directly ensures that if the schema changes (e.g., a column rename in a migration), the compiler will catch the discrepancy. Writing raw SQL would bypass these safety guarantees and introduce a maintenance burden.

---

## Reuse Verification Checklist

| Reuse Candidate | Used? | New code replacing it? |
|---|---|---|
| `apply_filter` from `common/src/db/query.rs` | Yes -- called directly for parsing | No -- no custom parsing logic written |
| Severity filter pattern from `advisory/endpoints/list.rs` | Yes -- structural pattern followed | No -- no alternative pattern invented |
| `package_license` entity from `entity/src/package_license.rs` | Yes -- used for JOIN query | No -- no raw SQL written |
