# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Reuse Candidates from Task Description

The task description includes three Reuse Candidates. Each is analyzed below for how it would be used during implementation.

---

### 1. `common/src/db/query.rs::apply_filter`

**What it provides:** Handles comma-separated multi-value query parameter parsing and SQL IN clause generation.

**How it would be reused:** Called directly in `modules/fundamental/src/package/service/mod.rs` to implement the license filter logic. When the `license` query parameter contains a value like `"MIT,Apache-2.0"`, `apply_filter` would:
1. Parse the comma-separated string into individual values: `["MIT", "Apache-2.0"]`
2. Generate a SQL `IN` clause: `WHERE package_license.license IN ('MIT', 'Apache-2.0')`

**Reuse type:** Direct invocation -- no modification to `apply_filter` needed. The function is already in the `common` crate, which is a dependency of `modules/fundamental` (verified by the project's workspace structure where fundamental modules import common query helpers).

**Why reuse over writing new code:** Writing custom comma-separation parsing and IN clause generation would duplicate the exact logic already in `apply_filter`. The function is designed for this use case and is already used by the advisory endpoint for the severity filter. Using it ensures consistent behavior (same delimiter handling, same SQL generation, same edge case handling for empty values).

**Integration point:** Inside `PackageService::list()` method, after extracting the license parameter:
```rust
if let Some(license) = license {
    apply_filter(&mut query, "package_license", "license", &license)?;
}
```
(Exact API depends on the actual `apply_filter` signature, which would be verified in Step 4.)

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides:** The severity filter implementation is structurally identical to the license filter needed. It demonstrates the Query struct pattern with an optional field for filtering.

**How it would be reused:** Used as a structural template (not called directly). The advisory endpoint's pattern would be replicated for the package endpoint:

1. **Query struct pattern**: The advisory endpoint defines a Query struct with an optional `severity` field:
   ```rust
   #[derive(Deserialize)]
   struct Query {
       // ... other fields (pagination, sorting)
       severity: Option<String>,
   }
   ```
   The package endpoint's Query struct would add an analogous `license: Option<String>` field.

2. **Handler-to-service parameter passing**: The advisory handler extracts `query.severity` and passes it to `AdvisoryService::list()`. The package handler would do the same with `query.license` and `PackageService::list()`.

3. **Service-layer integration**: The advisory service's `list()` method accepts an optional severity parameter, calls `apply_filter` when present, and returns the filtered results. The package service would follow the same pattern.

**Reuse type:** Structural pattern reuse (template). The advisory code is not imported or called -- its structure is followed to ensure consistency across endpoints.

**Why reuse over inventing a new pattern:** Using the same structural approach across all list endpoints ensures:
- Consistent developer experience (finding and understanding filters works the same way everywhere)
- Consistent API behavior (all filters use comma-separated syntax, same error responses)
- Reduced review friction (reviewers recognize the established pattern)

**Specific elements replicated from advisory:**
- Query struct field declaration with `Option<String>` type
- Serde deserialization attributes on the Query struct
- Handler function extracting the optional field and passing to service
- Service method signature accepting `Option<String>` filter parameter
- Conditional filter application (`if let Some(val) = filter { ... }`)

---

### 3. `entity/src/package_license.rs` (package-license entity)

**What it provides:** Existing SeaORM entity for the package-license join table. Maps the database relationship between packages and their licenses.

**How it would be reused:** Used for the JOIN query in the service layer instead of writing raw SQL. When filtering by license:

1. **JOIN construction**: The SeaORM entity provides the `Relation` definitions that enable type-safe JOINs:
   ```rust
   query = query.join(
       JoinType::InnerJoin,
       entity::package_license::Relation::Package.def().rev()
   );
   ```

2. **Column reference**: The entity's `Column` enum provides type-safe column references for the WHERE clause:
   ```rust
   entity::package_license::Column::License
   ```

**Reuse type:** Direct usage -- the entity is imported and used for query building. No modification to `entity/src/package_license.rs` needed.

**Why reuse over raw SQL:** Using the SeaORM entity for JOINs provides:
- Type safety: column names are checked at compile time
- Consistency: follows the project's convention of using SeaORM entities everywhere (as seen in advisory and SBOM modules)
- Maintainability: if the join table schema changes, the entity definition is updated in one place

---

## Additional Reuse Opportunities (discovered during analysis)

### 4. `common/src/model/paginated.rs::PaginatedResults<T>`

**What it provides:** Generic response wrapper for paginated list endpoints.

**How it would be reused:** Already used by the package list endpoint for its response type. The license filter does not change the response shape -- it only adds input filtering. No modification needed. This confirms acceptance criterion #4 (response shape unchanged).

### 5. `common/src/error.rs::AppError`

**What it provides:** Centralized error enum implementing Axum's `IntoResponse` trait.

**How it would be reused:** Used for validation errors (400 Bad Request) when invalid license values are provided. The package endpoint handler would use `AppError` with `.context()` wrapping, consistent with all other endpoints in the project.

---

## Reuse Summary

| Candidate | Reuse Type | Modification Needed | Location Used |
|-----------|-----------|---------------------|---------------|
| `apply_filter` (query.rs) | Direct invocation | None | `package/service/mod.rs` |
| Advisory severity filter pattern | Structural template | N/A (pattern, not code) | `package/endpoints/list.rs`, `package/service/mod.rs` |
| `package_license` entity | Direct usage (JOIN) | None | `package/service/mod.rs` |
| `PaginatedResults<T>` | Already in use | None | `package/endpoints/list.rs` (unchanged) |
| `AppError` | Already in use | None | `package/endpoints/list.rs` (validation errors) |

## Code Duplication Avoided

By reusing these candidates, the implementation avoids duplicating:
1. **Comma-separated parameter parsing logic** (estimated 15-20 lines) -- handled by `apply_filter`
2. **SQL IN clause generation** (estimated 10-15 lines) -- handled by `apply_filter`
3. **JOIN table definition** (estimated 20-30 lines) -- already defined in `package_license` entity
4. **Query struct boilerplate** (structural consistency, not line count) -- follows advisory pattern

Total estimated lines of duplicated code avoided: 45-65 lines.
