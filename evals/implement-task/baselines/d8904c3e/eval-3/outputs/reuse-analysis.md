# Reuse Analysis: TC-9203 — Add package license filter to list endpoint

## Overview

The task description includes three Reuse Candidates. All three are directly applicable and should be reused during implementation. No new filtering or query-building logic needs to be written from scratch — the implementation is a composition of existing patterns and utilities.

---

## Reuse Candidate 1: `common/src/db/query.rs::apply_filter`

**Source**: `common/src/db/query.rs`  
**Symbol**: `apply_filter` function  
**Reuse Type**: Direct invocation (no modification needed)

### What It Provides

The `apply_filter` function handles comma-separated multi-value query parameter parsing and SQL IN clause generation. It takes a raw query string value (e.g., `"MIT,Apache-2.0"`) and returns a parsed collection of individual values suitable for use in a SeaORM `is_in()` filter clause.

### How It Will Be Used

In `modules/fundamental/src/package/service/mod.rs`, when the `license` parameter is `Some`, the service method will call `apply_filter(&license_value)` to split the comma-separated string into individual SPDX identifiers. The resulting values will be passed to a SeaORM `.filter(package_license::Column::License.is_in(values))` clause.

This is the same usage pattern as the advisory endpoint's severity filter, which also calls `apply_filter` to handle comma-separated severity values.

### Justification

Writing custom comma-splitting and SQL IN clause logic would duplicate the exact functionality that `apply_filter` already provides. Using this shared helper ensures:
- Consistent parsing behavior across all list endpoints
- Single point of maintenance for the multi-value filter pattern
- Proven correctness (already tested via the advisory severity filter)

---

## Reuse Candidate 2: `modules/fundamental/src/advisory/endpoints/list.rs`

**Source**: `modules/fundamental/src/advisory/endpoints/list.rs`  
**Reuse Type**: Structural pattern reference (follow the same architecture, do not copy code verbatim)

### What It Provides

The advisory list endpoint implements a `severity` query parameter filter using a `Query` struct with optional filter fields. This struct is deserialized from Axum query parameters. The handler extracts the filter value, passes it to the advisory service layer, and the service applies the filter using `apply_filter` and SeaORM query building.

The key structural elements to replicate:
1. **Query struct pattern**: An optional `String` field on the `Query` struct for the filter parameter
2. **Handler-to-service propagation**: The handler extracts the filter value and passes it as a parameter to the service's `list` method
3. **Service-layer filter application**: The service method conditionally applies the filter when the value is `Some`, using `apply_filter` and a SeaORM join/filter

### How It Will Be Used

The package list endpoint (`modules/fundamental/src/package/endpoints/list.rs`) will follow this identical pattern:

1. Add `pub license: Option<String>` to the existing `Query` struct (mirrors the advisory endpoint's `pub severity: Option<String>`)
2. In the handler function, pass `query.license` to `PackageService::list()` (mirrors how the advisory handler passes `query.severity` to `AdvisoryService::list()`)
3. In `PackageService::list()`, conditionally apply the filter when `license` is `Some` (mirrors the advisory service's severity filter application)

### Justification

Following the advisory endpoint's pattern ensures:
- Consistency across the codebase — all list endpoint filters work the same way
- Maintainability — developers familiar with one filter pattern understand all of them
- Correctness — the pattern is proven to work with Axum's query parameter extraction, SeaORM query building, and the `PaginatedResults` response wrapper

---

## Reuse Candidate 3: `entity/src/package_license.rs`

**Source**: `entity/src/package_license.rs`  
**Reuse Type**: Direct use of existing SeaORM entity (no modification needed)

### What It Provides

The `package_license` entity defines the SeaORM model for the package-license join table in the database. It maps the relationship between packages and their declared licenses. The entity includes:
- Column definitions (including the license SPDX identifier column)
- Relation definitions (linking to the package entity)
- SeaORM derive macros for query building

### How It Will Be Used

In `modules/fundamental/src/package/service/mod.rs`, the license filter query will JOIN through the `package_license` entity to find packages matching the requested license(s):

```rust
// Pseudocode for the SeaORM query
query = query
    .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
    .filter(package_license::Column::License.is_in(license_values));
```

The entity is used as-is — no modifications to the entity definition are needed. The JOIN and filter are expressed through SeaORM's type-safe query builder using the entity's `Column` and `Relation` definitions.

### Justification

Using the existing `package_license` entity instead of writing raw SQL:
- Leverages SeaORM's type safety — column names and relations are checked at compile time
- Maintains consistency with how other join queries are built in the codebase
- Avoids hardcoding table/column names as strings, which are fragile and error-prone
- The entity already exists and defines the exact relationship needed for this filter

---

## Additional Reuse Discovered During Analysis

### `common/src/error.rs::AppError`

**Source**: `common/src/error.rs`  
**Reuse Type**: Direct use for error responses

The existing `AppError` enum implements `IntoResponse` for Axum and includes variants for HTTP error codes (including 400 Bad Request). This will be used for input validation errors when invalid license values are provided, following the same error handling pattern used by all other endpoint handlers in the codebase.

### `common/src/model/paginated.rs::PaginatedResults<T>`

**Source**: `common/src/model/paginated.rs`  
**Reuse Type**: Unchanged response wrapper

The `PaginatedResults<PackageSummary>` response type is already used by the package list endpoint. No changes are needed to this type — the filter only affects which packages are included in the results, not the response shape.

---

## Reuse Summary

| Candidate | File | Reuse Type | Modification Required |
|---|---|---|---|
| `apply_filter` | `common/src/db/query.rs` | Direct invocation | None |
| Advisory severity filter pattern | `modules/fundamental/src/advisory/endpoints/list.rs` | Structural pattern | None (pattern reference only) |
| `package_license` entity | `entity/src/package_license.rs` | Direct use in JOIN query | None |
| `AppError` | `common/src/error.rs` | Direct use for 400 errors | None |
| `PaginatedResults<T>` | `common/src/model/paginated.rs` | Unchanged response type | None |

**Net new code**: Zero new utilities or helpers. The implementation is entirely composed from existing building blocks — a new Query struct field, a service method parameter, and a filter clause using existing functions and entities.
