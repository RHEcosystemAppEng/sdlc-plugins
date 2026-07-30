# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

### What was checked

This criterion requires that the endpoint accepts a `license` query parameter and returns only packages matching the specified license identifier.

### Evidence from the diff

**1. Query parameter parsing (`modules/fundamental/src/package/endpoints/list.rs`):**

The `PackageListParams` struct now includes a `license` field:

```rust
pub struct PackageListParams {
    pub offset: Option<i64>,
    pub limit: Option<i64>,
    pub license: Option<String>,
}
```

This means `GET /api/v2/package?license=MIT` will deserialize the `license` query parameter into `params.license = Some("MIT")`.

**2. Validation (`modules/fundamental/src/package/endpoints/list.rs`):**

The `validate_license_param` function parses each identifier through `spdx::Expression::parse`, ensuring only valid SPDX identifiers are accepted. "MIT" is a valid SPDX identifier, so it passes validation.

**3. Filter application (`modules/fundamental/src/package/service/mod.rs`):**

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

This joins the `package_license` table and filters to rows where the license column matches one of the provided identifiers. For a single license like "MIT", this effectively returns only MIT-licensed packages.

**4. Test coverage (`tests/api/package.rs`):**

The test `test_list_packages_single_license_filter` directly verifies this criterion:
- Seeds packages with MIT and Apache-2.0 licenses
- Requests `GET /api/v2/package?license=MIT`
- Asserts response status is 200 OK
- Asserts exactly 2 items returned (the two MIT packages)
- Asserts all returned items have `license == "MIT"`

### Conclusion

The code correctly parses the `license` query parameter, validates it as a valid SPDX identifier, applies an inner join filter on the package-license relationship, and returns only matching packages. The test provides direct verification of this behavior. Criterion satisfied.
