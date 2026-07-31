# Reuse Analysis: TC-9203 -- Add package license filter to list endpoint

## Reuse-First Principle

The implement-task skill mandates "Reuse first" and "Reuse over duplication": before writing new logic, check whether Implementation Notes list reusable code and use or extend it. All three Reuse Candidates listed in TC-9203 are directly applicable and would be used in the implementation. No new filtering logic, query parameter parsing, or join table handling needs to be written from scratch.

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**What it provides**: The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL IN clause generation. It accepts a raw query string (e.g., `"MIT,Apache-2.0"`), splits it on commas, and produces the appropriate SeaORM condition -- an equality check for single values, or an IN clause for multiple values.

**How it would be reused**: Called directly in `PackageService::list` (in `modules/fundamental/src/package/service/mod.rs`) to apply the license filter to the query. No wrapper, no adaptation, no duplication needed.

```rust
// In PackageService::list:
if let Some(license) = license {
    query = apply_filter(query, package_license::Column::License, license)?;
}
```

**Why reuse is correct here**: The `common` crate is already a dependency of `modules/fundamental` (it must be, since the package module already uses `PaginatedResults` from `common/src/model/paginated.rs` and likely other query helpers). No new dependency is introduced. Per the skill's "Reuse over duplication" rule (Step 6), when the dependency already exists, make the function public and import it rather than duplicating. Since `apply_filter` is already in a shared crate (`common`), it is already designed for cross-module reuse.

**What would happen without reuse**: We would need to write custom comma-splitting logic, parameter validation, and SQL IN clause construction -- duplicating 20-30 lines of logic that already exists and is tested. Any future bug fix to `apply_filter` (e.g., handling edge cases like trailing commas or whitespace) would not apply to the duplicated code.

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**What it provides**: The advisory list endpoint implements a `severity` query parameter filter that is structurally identical to the license filter needed for TC-9203. It demonstrates:
- How to define an optional filter field in the Query struct (`pub severity: Option<String>`)
- How to pass the filter value from the endpoint handler to the service layer
- How the handler delegates all filtering logic to the service rather than implementing it inline

**How it would be reused**: This is a pattern reference, not a direct function call. The package list endpoint's Query struct and handler function would be modified to follow the exact same structure:

1. **Query struct pattern**: Add `pub license: Option<String>` to the package endpoint's Query struct, matching how the advisory endpoint defines `pub severity: Option<String>`.

2. **Handler delegation pattern**: In the package endpoint handler, pass `query.license.as_deref()` to `PackageService::list`, matching how the advisory handler passes `query.severity.as_deref()` to `AdvisoryService::list`.

**Why this is pattern reuse, not code duplication**: Each endpoint has its own Query struct and handler -- these are inherently per-endpoint. Following the same structural pattern ensures consistency across the codebase (sibling parity) without introducing shared abstractions where none are needed. The actual filtering logic is centralized in `apply_filter` (Candidate 1); the endpoint layer only does parameter extraction and delegation.

**Specific elements mirrored from the advisory pattern**:
- Query struct field type: `Option<String>` (not `Option<Vec<String>>` -- the comma parsing is handled by `apply_filter`)
- Handler argument passing: `.as_deref()` to convert `Option<String>` to `Option<&str>`
- Service method signature: `Option<&str>` parameter for the filter
- No endpoint-level validation of the filter value -- validation is handled by `apply_filter` or the service layer

## Reuse Candidate 3: `entity/src/package_license.rs`

**What it provides**: The existing SeaORM entity definition for the `package_license` join table, which maps packages to their SPDX license identifiers. It includes:
- The entity struct and column definitions (including `Column::License` for the SPDX identifier)
- SeaORM relation definitions that link back to the `package` entity
- Any indexes or constraints defined on the table

**How it would be reused**: Used in `PackageService::list` to construct the JOIN query for license filtering. Instead of writing raw SQL joins, the implementation leverages SeaORM's relation system:

```rust
use entity::package_license;

// Join through the existing relation
query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());

// Filter on the license column from the joined table
query = apply_filter(query, package_license::Column::License, license)?;
```

**Why reuse is correct here**: The entity already defines the database schema mapping. Writing raw SQL (`JOIN package_license ON ...`) would bypass SeaORM's type-safe query builder, lose compile-time column name checking, and diverge from how all other modules in trustify-backend perform joins. The skill's convention conformance analysis identifies that SeaORM entities are the standard approach throughout the codebase.

**What would happen without reuse**: We would need to write a raw SQL join clause, manually matching column names to the database schema. This would:
- Break the SeaORM convention used everywhere else in the project
- Lose compile-time validation of column names and types
- Create a maintenance risk if the `package_license` table schema ever changes (the raw SQL would not be updated by SeaORM migrations)

## Summary Table

| Reuse Candidate | Reuse Type | Where Used | Avoids Duplicating |
|---|---|---|---|
| `common/src/db/query.rs::apply_filter` | Direct function call | `PackageService::list` in `service/mod.rs` | Comma-separated parsing, SQL IN clause generation, parameter validation |
| `advisory/endpoints/list.rs` | Structural pattern reference | Query struct and handler in `package/endpoints/list.rs` | Inventing a new parameter extraction/delegation pattern |
| `entity/src/package_license.rs` | Entity import for JOIN query | `PackageService::list` in `service/mod.rs` | Raw SQL joins, manual column name matching |

## Additional Reuse Discovered During Analysis

Beyond the three listed Reuse Candidates, the following existing code would also be reused:

- **`common/src/model/paginated.rs::PaginatedResults<T>`**: The return type for the list method remains `PaginatedResults<PackageSummary>`. No new response wrapper is needed.
- **`common/src/error.rs::AppError`**: All error handling uses the existing `AppError` enum. Invalid license values would be returned as `AppError` variants (likely a 400 Bad Request), following the existing error handling convention. No new error types are created.
- **Test infrastructure from sibling test files** (`tests/api/advisory.rs`, `tests/api/sbom.rs`): Test setup patterns (database seeding, HTTP client construction, response deserialization) would be reused from existing test files rather than written from scratch.
