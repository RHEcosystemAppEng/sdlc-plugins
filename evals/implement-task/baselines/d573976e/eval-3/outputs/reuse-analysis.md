# Reuse Analysis for TC-9203: Add package license filter to list endpoint

## Reuse Candidates from Task Description

The task description includes three Reuse Candidates. All three are directly applicable and should be used during implementation.

---

### 1. `common/src/db/query.rs::apply_filter`

**What it provides**: Handles comma-separated multi-value query parameter parsing and SQL IN clause generation.

**How it would be reused**: Called directly from `PackageService::list()` in `modules/fundamental/src/package/service/mod.rs` when the `license` parameter is `Some`. The `apply_filter` function already handles:
- Splitting comma-separated values (e.g., `"MIT,Apache-2.0"` -> `["MIT", "Apache-2.0"]`)
- Generating a SQL `IN` clause for multi-value filters
- Handling single-value filters as a degenerate case of multi-value

**Reuse type**: Direct invocation -- no modification to `apply_filter` is needed. Import and call with the license column and the user-provided filter string.

**Example usage pattern**:
```rust
if let Some(license) = &license_filter {
    apply_filter(&mut query, "license", license);
}
```

**Benefit**: Avoids reimplementing comma-separated parsing and SQL IN clause construction. Ensures consistency with all other filter parameters across the codebase that use the same utility.

---

### 2. `modules/fundamental/src/advisory/endpoints/list.rs` (severity filter pattern)

**What it provides**: A structurally identical filter implementation -- the advisory list endpoint's `severity` query parameter uses the same Query struct pattern with an optional field, validation, and pass-through to the service layer.

**How it would be reused**: Used as a structural template (not called directly) for implementing the license filter in `modules/fundamental/src/package/endpoints/list.rs`. Specifically:

1. **Query struct pattern**: The advisory endpoint defines a Query struct with:
   ```rust
   #[derive(Deserialize)]
   pub struct Query {
       // ... pagination fields ...
       pub severity: Option<String>,
   }
   ```
   The package endpoint's Query struct will add `license: Option<String>` following the same pattern.

2. **Handler wiring pattern**: The advisory handler extracts `query.severity` and passes it to `AdvisoryService::list()`. The package handler will extract `query.license` and pass it to `PackageService::list()` the same way.

3. **Validation pattern**: If the advisory endpoint validates the severity parameter (e.g., rejecting empty strings), the same validation logic will be replicated for the license parameter.

4. **Error response pattern**: The advisory endpoint returns `AppError`-based 400 responses for invalid filter values. The license filter will follow the same error handling approach.

**Reuse type**: Structural pattern reference -- the advisory code serves as the authoritative template for how to add a new filter parameter to a list endpoint. The code is not imported or called; rather, its structure is replicated with license-specific names and semantics.

**Benefit**: Ensures the license filter follows established project conventions for list endpoint filtering. Reduces risk of introducing a novel pattern that deviates from the codebase's expectations.

---

### 3. `entity/src/package_license.rs` (package-license entity)

**What it provides**: The existing SeaORM entity definition for the `package_license` join table, which maps packages to their declared licenses.

**How it would be reused**: Used in `PackageService::list()` to perform a JOIN when filtering by license. Instead of writing raw SQL, the implementation uses SeaORM's relation-based join through the `package_license` entity:

1. **JOIN construction**: When a license filter is active, the package query joins through `package_license` to access the license column:
   ```rust
   use entity::package_license;
   
   // Join package_license when license filter is present
   query = query.join(JoinType::InnerJoin, package_license::Relation::Package.def().rev());
   ```

2. **Column reference**: The `apply_filter` call references the license column from the `package_license` entity rather than a hardcoded string, maintaining type safety:
   ```rust
   apply_filter(&mut query, package_license::Column::License, license_value);
   ```

3. **No raw SQL**: By using the existing entity definition, the implementation avoids raw SQL and benefits from SeaORM's compile-time checking of column names and relations.

**Reuse type**: Direct usage of the existing entity -- imported and used in query construction. No modifications to the entity file are needed.

**Benefit**: Avoids duplicating schema knowledge (table name, column names, relations) and leverages SeaORM's type-safe query building. If the `package_license` table schema changes in the future, the entity file is the single source of truth and the compiler will catch breakages.

---

## Additional Reuse Opportunities Discovered

Beyond the three listed Reuse Candidates, the following existing code would also be leveraged:

### `common/src/model/paginated.rs` - PaginatedResults<T>

The response wrapper `PaginatedResults<PackageSummary>` is already used by the package list endpoint. No changes to this type are needed -- the response shape remains identical with or without the license filter.

### `common/src/error.rs` - AppError

The `AppError` enum and its `IntoResponse` implementation are used for returning 400 Bad Request responses when invalid license values are provided. This follows the same error handling pattern used across all endpoints.

### Sibling test patterns from `tests/api/advisory.rs`

The advisory endpoint integration tests serve as a template for the new `tests/api/package_license_filter.rs` test file. The test setup (database seeding), assertion patterns (`assert_eq!(resp.status(), StatusCode::OK)`), and response deserialization approach will be replicated for the license filter tests.

---

## Summary

| Reuse Candidate | Reuse Type | Modified? | Location Used |
|---|---|---|---|
| `apply_filter` | Direct call | No | `package/service/mod.rs` |
| Advisory severity filter | Structural template | No (reference only) | `package/endpoints/list.rs` |
| `package_license` entity | Direct import/JOIN | No | `package/service/mod.rs` |
| `PaginatedResults<T>` | Existing return type | No | `package/endpoints/list.rs` |
| `AppError` | Error handling | No | `package/endpoints/list.rs` |
| Advisory test patterns | Test structure template | No (reference only) | `tests/api/package_license_filter.rs` |

All three task-specified Reuse Candidates are used. No new utility code needs to be written -- the implementation composes existing building blocks (query helper, entity, error type) following the established advisory filter pattern.
