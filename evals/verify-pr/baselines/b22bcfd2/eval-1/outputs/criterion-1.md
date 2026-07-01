# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

The PR diff demonstrates that the single license filter feature is fully implemented across the endpoint, service, and test layers.

### Endpoint Layer (list.rs)

The `PackageListParams` struct now includes an optional `license` field:

```rust
pub license: Option<String>,
```

When present, the license parameter is passed through `validate_license_param()` which parses each identifier as an SPDX expression, then forwarded to the service layer:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

### Service Layer (mod.rs)

`PackageService::list()` now accepts a `license_filter: Option<&[String]>` parameter. When provided, it applies a filter using SeaORM's `Condition::any()` with `is_in()`:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

For a single license value like `MIT`, the comma-split produces a single-element vector `["MIT"]`. The `is_in()` clause generates a SQL `WHERE license IN ('MIT')`, which correctly filters to only MIT-licensed packages. The `InnerJoin` on `PackageLicense` ensures only packages with a matching license row are returned.

### Test Coverage

The test `test_list_packages_single_license_filter` directly validates this criterion:

```rust
ctx.seed_package("pkg-a", "MIT").await;
ctx.seed_package("pkg-b", "Apache-2.0").await;
ctx.seed_package("pkg-c", "MIT").await;

let resp = ctx.get("/api/v2/package?license=MIT").await;

assert_eq!(resp.status(), StatusCode::OK);
let body: PaginatedResults<PackageSummary> = resp.json().await;
assert_eq!(body.items.len(), 2);
assert!(body.items.iter().all(|p| p.license == "MIT"));
```

This seeds 3 packages (2 MIT, 1 Apache-2.0), filters by MIT, and asserts exactly 2 results are returned, all with MIT license.

## Evidence

- `modules/fundamental/src/package/endpoints/list.rs`: `license` field added to `PackageListParams`, `validate_license_param()` splits and validates, filter passed to service
- `modules/fundamental/src/package/service/mod.rs`: `is_in()` filter with `InnerJoin` on `PackageLicense`
- `tests/api/package.rs`: `test_list_packages_single_license_filter` validates end-to-end behavior
