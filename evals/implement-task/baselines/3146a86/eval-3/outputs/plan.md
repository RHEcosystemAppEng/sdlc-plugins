# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Summary

This task adds an optional `license` query parameter to `GET /api/v2/package`. The parameter
accepts a single SPDX identifier or a comma-separated list of SPDX identifiers and filters
results to packages whose declared license matches any of the provided values. The response
shape (`PaginatedResults<PackageSummary>`) is unchanged.

## Files to Modify

### `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Handles `GET /api/v2/package` with pagination/sorting query parameters.
No filtering by license.

**Changes:**

1. Add a `Query` struct (following the advisory endpoint pattern from
   `modules/fundamental/src/advisory/endpoints/list.rs`) with an optional `license` field:

   ```rust
   /// Query parameters accepted by the package list endpoint.
   #[derive(Debug, Deserialize, IntoParams)]
   pub struct PackageListQuery {
       pub license: Option<String>,
       // existing pagination/sorting fields remain unchanged
   }
   ```

2. Extract the `license` field from the deserialized query struct in the handler function
   and pass it down to the service layer:

   ```rust
   pub async fn list_packages(
       State(service): State<PackageService>,
       Query(params): Query<PackageListQuery>,
       // ... existing extractor parameters
   ) -> Result<Json<PaginatedResults<PackageSummary>>, AppError> {
       let result = service
           .list(params.license, /* existing params */)
           .await
           .context("listing packages")?;
       Ok(Json(result))
   }
   ```

3. Update OpenAPI parameter annotations (utoipa `#[utoipa::path]` macro or equivalent)
   to document the new optional `license` query parameter.

**Reuse:** The `Query` struct pattern and the handler's extraction of the optional filter
field are copied directly from
`modules/fundamental/src/advisory/endpoints/list.rs::AdvisoryListQuery` (Reuse Candidate 2).
No new parsing logic is introduced here — parsing is delegated to `apply_filter` in the
service layer.

---

### `modules/fundamental/src/package/service/mod.rs`

**Current state:** `PackageService::list` builds a SeaORM query for packages with pagination
and sorting. It does not join `package_license` and accepts no license filter argument.

**Changes:**

1. Update the `list` method signature to accept an optional license filter:

   ```rust
   pub async fn list(
       &self,
       license: Option<String>,
       // ... existing pagination/sorting parameters
   ) -> Result<PaginatedResults<PackageSummary>, AppError>
   ```

2. When `license` is `Some(...)`, join the `package_license` entity and apply the filter
   using `apply_filter` from `common/src/db/query.rs`:

   ```rust
   use common::db::query::apply_filter;
   use entity::package_license;

   // inside list():
   let mut query = entity::package::Entity::find();

   if let Some(license_param) = license {
       // apply_filter parses comma-separated values and appends an IN-clause condition
       query = query
           .join(JoinType::InnerJoin, package_license::Relation::Package.def())
           .filter(apply_filter(
               package_license::Column::LicenseSpdxId,
               &license_param,
           ));
   }
   ```

   - The join uses the `package_license` entity (Reuse Candidate 3) so no raw SQL is
     written.
   - `apply_filter` (Reuse Candidate 1) handles the comma-separated multi-value parsing
     and builds the SQL `IN` clause; no new parsing utility is created.

3. Add a documentation comment to the updated `list` method explaining the `license`
   parameter and its `None` / `Some(csv)` semantics.

4. Verify that callers of `PackageService::list` (if any exist beyond the endpoint handler)
   are updated to pass `None` for the new parameter, maintaining backward compatibility.

---

## Files to Create

### `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the new `license` query parameter. Tests run against
a real PostgreSQL test database, following the conventions observed in
`tests/api/advisory.rs` and `tests/api/sbom.rs`.

**Test functions:**

```
test_list_packages_single_license_filter
test_list_packages_multi_license_filter
test_list_packages_no_license_filter
test_list_packages_invalid_license_returns_400
```

**Structure of each test** (following sibling test conventions):

- Use `assert_eq!(resp.status(), StatusCode::OK)` for success cases, `StatusCode::BAD_REQUEST`
  for the invalid-license case.
- Deserialize the response body into `PaginatedResults<PackageSummary>`.
- Assert on specific item values (SPDX identifiers on returned packages), not just counts,
  so test failures identify *what* changed rather than just *how many* results appeared.
- Use given-when-then section comments inside each non-trivial test body.
- Every test function has a `///` doc comment describing what it verifies.

**Example sketch:**

```rust
/// Verifies that filtering by a single license SPDX ID returns only matching packages.
#[tokio::test]
async fn test_list_packages_single_license_filter() {
    // Given: a test database containing packages with MIT and Apache-2.0 licenses
    let app = setup_test_app().await;
    seed_packages_with_licenses(&app.db, &[("pkg-a", "MIT"), ("pkg-b", "Apache-2.0")]).await;

    // When: requesting packages filtered to MIT
    let resp = app.get("/api/v2/package?license=MIT").await;

    // Then: only the MIT-licensed package is returned
    assert_eq!(resp.status(), StatusCode::OK);
    let body: PaginatedResults<PackageSummary> = resp.json().await;
    assert_eq!(body.items.len(), 1);
    assert_eq!(body.items[0].name, "pkg-a");
}

/// Verifies that a comma-separated license list returns packages matching any listed license.
#[tokio::test]
async fn test_list_packages_multi_license_filter() { ... }

/// Verifies that omitting the license parameter returns all packages without filtering.
#[tokio::test]
async fn test_list_packages_no_license_filter() { ... }

/// Verifies that an invalid (non-SPDX) license value returns 400 Bad Request.
#[tokio::test]
async fn test_list_packages_invalid_license_returns_400() { ... }
```

The new test file must be registered in `tests/Cargo.toml` (and any integration test
harness entry point if one exists) following the pattern used by `advisory.rs` and
`sbom.rs`.

---

## How Existing Code is Reused

See `reuse-analysis.md` for the detailed breakdown. In brief:

| Reuse Candidate | Applied In |
|---|---|
| `common/src/db/query.rs::apply_filter` | `package/service/mod.rs` — comma-separated license parsing and IN-clause generation |
| `modules/fundamental/src/advisory/endpoints/list.rs` | `package/endpoints/list.rs` — Query struct shape and optional-filter extraction pattern |
| `entity/src/package_license.rs` | `package/service/mod.rs` — JOIN target for the package-license relationship |

## Data-Flow Trace

```
HTTP request: GET /api/v2/package?license=MIT,Apache-2.0
  → package/endpoints/list.rs  : deserialize PackageListQuery; extract license: Some("MIT,Apache-2.0")
  → package/service/mod.rs     : receive Option<String>; join package_license; call apply_filter
  → common/db/query.rs         : parse CSV; emit IN clause: license_spdx_id IN ('MIT','Apache-2.0')
  → PostgreSQL                 : execute query with JOIN + WHERE
  → service/mod.rs             : map rows → Vec<PackageSummary>; wrap in PaginatedResults
  → endpoint handler           : return Json(PaginatedResults<PackageSummary>)
HTTP response: 200 OK, body unchanged in shape
```

All stages are connected — the flow is complete end-to-end.

## Out-of-Scope

- No changes to `entity/src/package_license.rs` — the entity is reused as-is.
- No changes to `common/src/db/query.rs` — `apply_filter` is called, not modified.
- No changes to `modules/fundamental/src/advisory/` — that module is read as a reference only.
- No database migrations — the `package_license` table already exists.
- Response shape (`PaginatedResults<PackageSummary>`) is unchanged.
