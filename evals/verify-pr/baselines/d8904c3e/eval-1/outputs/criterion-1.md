# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

### What the criterion requires

The endpoint must accept a `license` query parameter and, when a single license identifier such as `MIT` is provided, return only packages whose license matches that identifier.

### Evidence from the diff

**1. Query parameter parsing (list.rs)**

The `PackageListParams` struct adds a new optional field:

```rust
pub license: Option<String>,
```

This means Axum's `Query` extractor will automatically parse `?license=MIT` from the URL into `params.license = Some("MIT")`.

**2. License validation (list.rs)**

The `validate_license_param` function splits the parameter on commas, trims whitespace, and validates each identifier against the SPDX expression parser:

```rust
fn validate_license_param(license: &str) -> Result<Vec<String>, AppError> {
    let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
    for id in &identifiers {
        Expression::parse(id).map_err(|_| {
            AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
        })?;
    }
    Ok(identifiers)
}
```

For a single value like `MIT`, this produces `vec!["MIT"]`.

**3. Filter application (service/mod.rs)**

The `PackageService::list` method now accepts `license_filter: Option<&[String]>` and applies a filter when present:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

For `["MIT"]`, the `is_in` clause restricts results to packages whose associated `package_license` record has `license = 'MIT'`. The inner join ensures only packages with a matching license row are included.

**4. Handler wiring (list.rs)**

The `list_packages` handler converts the validated filter into the service call:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
let results = PackageService::new(&db)
    .list(params.offset, params.limit, license_filter.as_deref())
    .await
    .context("Failed to list packages")?;
```

**5. Test coverage (tests/api/package.rs)**

The test `test_list_packages_single_license_filter` directly verifies this criterion:
- Seeds packages with MIT and Apache-2.0 licenses
- Calls `GET /api/v2/package?license=MIT`
- Asserts the response status is 200 OK
- Asserts exactly 2 items are returned (the two MIT packages)
- Asserts all returned items have `license == "MIT"`

### Conclusion

The full chain is implemented: query parameter extraction, SPDX validation, database filtering via inner join with `is_in`, and a dedicated integration test that verifies the exact behavior described in the criterion. The criterion is satisfied.
