# Criterion 1: Single License Filter

**Criterion:** `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict: PASS**

## What was checked

Inspected the PR diff for:
1. Query parameter parsing for a single `license` value
2. Filter application in the database query
3. Test coverage for single license filtering

## Code-level evidence

### Parameter parsing (list.rs)

The `PackageListParams` struct adds a `license` field:
```rust
pub license: Option<String>,
```

In `list_packages`, the license parameter is extracted and validated:
```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

### Validation (list.rs)

`validate_license_param` parses the license string. For a single value like `MIT`, `split(',')` produces a single-element vec. `Expression::parse(id)` validates it as a valid SPDX identifier:
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

### Filter application (service/mod.rs)

The `list` method receives `license_filter: Option<&[String]>` and applies it:
```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

For a single license like `MIT`, `is_in` receives a single-element iterator, effectively filtering to only MIT-licensed packages.

### Test coverage (tests/api/package.rs)

`test_list_packages_single_license_filter` seeds packages with MIT and Apache-2.0 licenses, queries `?license=MIT`, and asserts:
```rust
assert_eq!(body.items.len(), 2);
assert!(body.items.iter().all(|p| p.license == "MIT"));
```

This confirms only MIT-licensed packages are returned.
