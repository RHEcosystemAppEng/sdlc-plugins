# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

## Reuse Candidates from Task Description

The task description lists three reuse candidates. All three would be used in this implementation.

---

### 1. `common/src/db/query.rs::apply_filter`

**What it provides:**
Handles comma-separated multi-value query parameter parsing and SQL IN clause generation. This is a shared utility already used across the codebase for filtering list endpoints.

**How it would be reused:**
- **Direct reuse** -- call `apply_filter` in the package list handler to parse the `license` query parameter value (e.g., `"MIT,Apache-2.0"`) into individual filter values and generate the corresponding SQL IN clause.
- No modification to `apply_filter` itself is needed. It already supports the exact use case: take a comma-separated string, split it, and produce a database filter condition.
- This avoids writing custom comma-splitting and SQL generation logic in the package endpoint.

**Where in the implementation:**
- Called in `modules/fundamental/src/package/endpoints/list.rs` inside the handler function, after extracting the `license` field from the Query struct.
- The parsed filter values are passed to `PackageService::list` in `modules/fundamental/src/package/service/mod.rs`, which applies them to the SeaORM query.

**Reuse type:** Direct invocation (no modification, no duplication).

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:**
A structurally identical filter implementation -- the advisory list endpoint supports a `severity` query parameter using an optional field on a Query struct, extracted in the handler and passed to the service layer. This serves as the architectural pattern to follow.

**How it would be reused:**
- **Pattern reuse** -- replicate the same structural approach in the package endpoint:
  1. Add an `Option<String>` field named `license` to the package endpoint's `Query` struct, mirroring how `severity` is declared in the advisory Query struct.
  2. In the handler function, extract the `license` field and pass it through the same conditional filtering flow used for `severity`.
  3. Pass the filter to the service layer using the same method signature pattern (optional filter parameter).
- This is not a code copy -- it is following an established convention. The advisory file is the reference implementation that defines the project's standard approach to list endpoint filtering.

**Where in the implementation:**
- `modules/fundamental/src/package/endpoints/list.rs` -- Query struct definition and handler function structure follow the advisory pattern.
- `modules/fundamental/src/package/service/mod.rs` -- service method signature and filter application follow the advisory service pattern.

**Reuse type:** Structural pattern replication (same architecture, different domain entity).

---

### 3. `entity/src/package_license.rs`

**What it provides:**
The existing SeaORM entity definition for the package-license join table. This entity maps packages to their declared licenses and is already part of the data model.

**How it would be reused:**
- **Direct reuse** -- import and use this entity in the `PackageService::list` method to construct the JOIN query for license filtering.
- When the license filter is active, the service builds a SeaORM query that joins the `package` table to the `package_license` table using this entity's relation definitions, then applies the IN clause from `apply_filter`.
- No raw SQL is needed. The entity's SeaORM `Column` enum provides type-safe column references (e.g., `package_license::Column::License`) for the filter condition.
- The entity is not modified -- its existing schema, relations, and column definitions are sufficient for this query.

**Where in the implementation:**
- `modules/fundamental/src/package/service/mod.rs` -- imported and used in the `list` method's query builder to add `.join()` and `.filter()` clauses when the license filter is present.

**Reuse type:** Direct import and use (no modification, no duplication).

---

## Additional Reuse Discovered During Analysis

Beyond the three listed candidates, the following existing code would also be reused:

### `common/src/model/paginated.rs::PaginatedResults<T>`

**What it provides:** The standard response wrapper for list endpoints.

**How it would be reused:** The package list endpoint already returns `PaginatedResults<PackageSummary>`. No changes to this type are needed -- the license filter only affects which packages are included, not the response shape.

### `common/src/error.rs::AppError`

**What it provides:** The standard error enum implementing `IntoResponse` for Axum handlers.

**How it would be reused:** Used to return 400 Bad Request for invalid license parameter values, following the same `.context()` wrapping pattern used throughout the codebase.

---

## Summary

| Reuse Candidate | Reuse Type | Modified? | Location Used |
|----------------|-----------|-----------|---------------|
| `common/src/db/query.rs::apply_filter` | Direct invocation | No | `package/endpoints/list.rs`, `package/service/mod.rs` |
| `advisory/endpoints/list.rs` (severity pattern) | Structural pattern | No | `package/endpoints/list.rs`, `package/service/mod.rs` |
| `entity/src/package_license.rs` | Direct import | No | `package/service/mod.rs` |
| `common/src/model/paginated.rs` | Already in use | No | `package/endpoints/list.rs` (existing) |
| `common/src/error.rs::AppError` | Already in use | No | `package/endpoints/list.rs` (existing) |

**No new shared utilities need to be created.** All required functionality exists in the codebase. The implementation reuses existing code at every level: query parsing (`apply_filter`), architectural pattern (advisory severity filter), data model (`package_license` entity), response wrapping (`PaginatedResults`), and error handling (`AppError`).
