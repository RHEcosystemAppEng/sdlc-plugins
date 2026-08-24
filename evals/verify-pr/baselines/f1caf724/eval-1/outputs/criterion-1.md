# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Analysis

This criterion requires that a single-license filter query parameter correctly filters the package list to return only packages matching the specified SPDX license identifier.

### Code Evidence

**Parameter Parsing (`modules/fundamental/src/package/endpoints/list.rs`):**

The `PackageListParams` struct now includes an optional `license` field:

```rust
pub struct PackageListParams {
    pub offset: Option<i64>,
    pub limit: Option<i64>,
    pub license: Option<String>,
}
```

When the `license` parameter is present, `validate_license_param` is called, which splits on comma and validates each identifier against the SPDX expression parser. For a single value like `MIT`, this produces a `Vec<String>` containing one element: `["MIT"]`.

**Query Filtering (`modules/fundamental/src/package/service/mod.rs`):**

The `PackageService::list` method now accepts `license_filter: Option<&[String]>`. When populated, it applies a filter:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

The `is_in` condition with a single-element list produces a SQL `WHERE license IN ('MIT')` clause, and the `InnerJoin` on `PackageLicense` ensures only packages with a license record are included. This correctly filters to only MIT-licensed packages.

**Test Coverage (`tests/api/package.rs`):**

The test `test_list_packages_single_license_filter` seeds three packages (two with MIT, one with Apache-2.0), queries `?license=MIT`, and asserts:
- Response status is 200 OK
- Exactly 2 items are returned
- All returned items have `license == "MIT"`

This directly validates the criterion's expected behavior.

### Conclusion

The implementation correctly parses the license query parameter, validates it as a valid SPDX identifier, and applies it as a database filter. The test confirms the expected behavior with concrete assertions on both count and license values.
