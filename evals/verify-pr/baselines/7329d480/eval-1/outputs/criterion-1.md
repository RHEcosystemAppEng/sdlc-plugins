## Criterion 1: Single License Filter

**Result: PASS**

`GET /api/v2/package?license=MIT` returns only packages with MIT license.

### Evidence

The diff adds `filter_license` as an optional `String` parameter to `PackageListParams`:

```rust
pub struct PackageListParams {
    pub offset: Option<i64>,
    pub limit: Option<i64>,
    pub license: Option<String>,
}
```

In the handler, the license parameter is extracted and validated:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

The validated identifiers are passed to `PackageService::list`, which applies the filter in the service layer:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

The `is_in` clause generates a SQL `WHERE license IN (...)` condition, and the `InnerJoin` on `PackageLicense` ensures only packages with a matching license row are returned. For a single value like `MIT`, this filters to only MIT-licensed packages.

The integration test `test_list_packages_single_license_filter` confirms this behavior by seeding packages with MIT and Apache-2.0 licenses, filtering by MIT, and asserting only 2 MIT packages are returned.
