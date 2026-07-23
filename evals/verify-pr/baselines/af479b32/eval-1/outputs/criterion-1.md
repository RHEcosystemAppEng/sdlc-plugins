# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

### Endpoint Parameter Parsing

In `modules/fundamental/src/package/endpoints/list.rs`, the `PackageListParams` struct now includes the `license` field:

```rust
pub struct PackageListParams {
    pub offset: Option<i64>,
    pub limit: Option<i64>,
    pub license: Option<String>,
}
```

When `license` is `Some`, the handler calls `validate_license_param(license)` which splits on commas, trims whitespace, and validates each identifier via `spdx::Expression::parse`. For a single value like `MIT`, this produces a `Vec<String>` containing `["MIT"]`.

### Service-Layer Filtering

In `modules/fundamental/src/package/service/mod.rs`, the `list` method now accepts `license_filter: Option<&[String]>`. When present, it applies:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

The `is_in` clause matches rows in the `package_license` table whose `license` column equals any value in the provided list. For a single-element list `["MIT"]`, only packages with MIT license are returned. The `InnerJoin` ensures packages without a license record in `package_license` are excluded.

### Test Coverage

The test `test_list_packages_single_license_filter` in `tests/api/package.rs` verifies this criterion directly:

1. Seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (MIT)
2. Sends `GET /api/v2/package?license=MIT`
3. Asserts response status is 200 OK
4. Asserts `body.items.len() == 2` (only the two MIT packages)
5. Asserts all returned items have `license == "MIT"`

### Evidence

- **Parameter parsing**: `list.rs` line with `pub license: Option<String>` adds the query parameter.
- **Validation**: `validate_license_param` function parses and validates via `spdx::Expression::parse`.
- **Filtering**: `service/mod.rs` applies `is_in` filter on the `package_license::Column::License` column with an inner join.
- **Test assertion**: `assert!(body.items.iter().all(|p| p.license == "MIT"))` confirms only MIT packages are returned.

## Conclusion

The code correctly parses the `license=MIT` query parameter, validates it as a valid SPDX identifier, applies a database filter via `is_in` on the package_license column with an inner join, and returns only matching packages. The integration test confirms the expected behavior end-to-end. Criterion satisfied.
