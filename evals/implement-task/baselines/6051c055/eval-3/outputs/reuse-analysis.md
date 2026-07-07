# Reuse Analysis — TC-9203: Add package license filter to list endpoint

## Reuse Candidates Evaluation

### 1. `common/src/db/query.rs::apply_filter`

**Decision:** Reuse directly. No wrapper, no reimplementation.

**How it is reused:**

`apply_filter` is the sole mechanism for parsing and applying the license filter value. It is called in `modules/fundamental/src/package/service/mod.rs` when the `license` query parameter is present. Specifically:

- **Comma-separated parsing:** `apply_filter` already splits a comma-separated string (e.g., `"MIT,Apache-2.0"`) into individual values. The license filter passes the raw query parameter string directly to `apply_filter` without any pre-processing. No new splitting or parsing logic is written.

- **SQL IN clause generation:** For multi-value inputs, `apply_filter` generates a SQL `WHERE column IN (...)` clause. For single values, it generates a `WHERE column = ...` clause. This covers both `?license=MIT` and `?license=MIT,Apache-2.0` requirements.

- **Error handling:** `apply_filter` validates its input and returns errors for malformed values. These errors are propagated as HTTP 400 responses, satisfying the "invalid license values return 400" acceptance criterion.

**Why no new utility functions are needed:** `apply_filter` already provides the exact functionality required — comma parsing, IN clause generation, and input validation. Writing a new helper would duplicate this functionality and diverge from the established codebase pattern.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs`

**Decision:** Use as a structural template. No code is copied; the pattern is followed.

**How it is reused:**

The advisory list endpoint's severity filter is structurally identical to the license filter being implemented. It serves as the reference for:

- **Query struct pattern:** The advisory endpoint defines a `Query` struct (or equivalent) with optional filter fields. The package endpoint's `Query` struct in `modules/fundamental/src/package/endpoints/list.rs` is extended with a `license: Option<String>` field following this same pattern.

- **Handler-to-service delegation:** The advisory handler extracts filter values from the Query struct and passes them to the service layer without performing any parsing or validation itself. The package handler follows the same thin-handler approach — it passes `query.license` directly to `PackageService::list()`.

- **Service-layer filter application:** The advisory service calls `apply_filter` conditionally when a filter parameter is present. The package service follows the same `if let Some(value) = &filter { query = apply_filter(...) }` pattern.

- **Error propagation:** The advisory endpoint maps `apply_filter` errors to HTTP 400 responses. The package endpoint uses the same error-handling approach.

This candidate is used as a structural guide, not as code to import or call. The value is consistency: the license filter will be immediately familiar to anyone who has worked on the advisory filters.

---

### 3. `entity/src/package_license.rs`

**Decision:** Reuse directly for the JOIN query.

**How it is reused:**

The `package_license` entity defines the SeaORM model for the `package_license` join table, which maps packages to their declared licenses. It is used in `modules/fundamental/src/package/service/mod.rs` as follows:

- **JOIN clause:** When the license filter is present, the service adds a JOIN from the package table to `package_license` using SeaORM's relation-based API (e.g., `.join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())`). The entity's existing `Relation` definitions provide the foreign key mappings — no raw SQL is written.

- **Column reference:** The `apply_filter` call references `package_license::Column::License` (or the equivalent column name defined in the entity) as the column to filter on. This ensures the filter targets the correct column in the joined table.

- **No new entity is created.** The `package_license` entity already has the model, columns, and relations needed. Creating a duplicate or simplified entity would be unnecessary and would create a maintenance burden.

---

## Summary

| Reuse Candidate | Reuse Type | Used In |
|----------------|-----------|---------|
| `common/src/db/query.rs::apply_filter` | Direct function call | `package/service/mod.rs` — parsing comma values, building SQL filter |
| `advisory/endpoints/list.rs` | Structural pattern | `package/endpoints/list.rs` — Query struct, handler delegation, error handling |
| `entity/src/package_license.rs` | Direct entity import | `package/service/mod.rs` — JOIN and column reference |

All three reuse candidates are used. No new utility functions are introduced that would duplicate `apply_filter` functionality. No new entities are created. No raw SQL is written.
