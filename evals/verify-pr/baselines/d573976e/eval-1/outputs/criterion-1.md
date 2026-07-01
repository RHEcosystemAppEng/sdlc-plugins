# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

The implementation satisfies this criterion through three layers of evidence:

### 1. Query Parameter Parsing (Endpoint Layer)

In `modules/fundamental/src/package/endpoints/list.rs`, the `PackageListParams` struct now includes an optional `license` field:

```rust
pub struct PackageListParams {
    pub offset: Option<i64>,
    pub limit: Option<i64>,
    pub license: Option<String>,
}
```

When the `license` query parameter is present, the handler calls `validate_license_param(license)`, which splits on commas, trims whitespace, and validates each identifier against the `spdx::Expression::parse()` function. For a single value like `MIT`, this produces a `Vec<String>` containing `["MIT"]`.

### 2. Filter Application (Service Layer)

In `modules/fundamental/src/package/service/mod.rs`, the `PackageService::list` method now accepts an optional `license_filter: Option<&[String]>` parameter. When present, it applies:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

This adds an INNER JOIN to the `package_license` table and a WHERE clause filtering by the license column using `is_in`. For a single-element slice `["MIT"]`, this effectively becomes `WHERE package_license.license IN ('MIT')`, ensuring only MIT-licensed packages are returned.

### 3. Test Coverage

The test `test_list_packages_single_license_filter` in `tests/api/package.rs` directly verifies this criterion:
- Seeds 3 packages: 2 with MIT, 1 with Apache-2.0
- Queries `GET /api/v2/package?license=MIT`
- Asserts response status is 200 OK
- Asserts exactly 2 items are returned
- Asserts all returned items have `license == "MIT"`

This provides end-to-end verification that the filter correctly excludes non-matching packages.
