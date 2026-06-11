# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Result: PASS

## Evidence

### Endpoint Layer (`modules/fundamental/src/package/endpoints/list.rs`)

The `PackageListParams` struct now includes an optional `license` field:

```rust
pub struct PackageListParams {
    pub offset: Option<i64>,
    pub limit: Option<i64>,
    pub license: Option<String>,
}
```

When `license` is present, `validate_license_param` is called, which splits the value by comma and validates each identifier via `spdx::Expression::parse()`. For a single value like `MIT`, this produces a `Vec<String>` containing `["MIT"]`.

The validated identifiers are passed to the service layer:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

### Service Layer (`modules/fundamental/src/package/service/mod.rs`)

The `list` method now accepts `license_filter: Option<&[String]>`. When present, it applies:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

This adds an `INNER JOIN` to the `package_license` table and a `WHERE license IN ('MIT')` clause. The `InnerJoin` ensures only packages that have a matching license record are returned. Packages without a license in the filter set are excluded.

### Test Verification (`tests/api/package.rs`)

The test `test_list_packages_single_license_filter` directly verifies this criterion:

- Seeds 3 packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (MIT)
- Queries `GET /api/v2/package?license=MIT`
- Asserts `StatusCode::OK`
- Asserts `body.items.len() == 2` (only the 2 MIT packages)
- Asserts `body.items.iter().all(|p| p.license == "MIT")` (all returned packages have MIT license)

This test confirms that the filter correctly excludes non-matching packages (Apache-2.0 pkg-b is not returned) and includes all matching packages.

## Conclusion

The implementation correctly filters packages by a single SPDX license identifier using parameterized SQL via SeaORM, and the test validates the expected behavior with specific assertions on result count and license values.
