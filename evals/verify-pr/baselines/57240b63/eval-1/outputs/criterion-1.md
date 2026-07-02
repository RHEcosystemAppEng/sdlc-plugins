# Acceptance Criterion 1: Single License Filter

**Criterion**: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict**: PASS

## Evidence from Diff

### Query Parameter Parsing

In `modules/fundamental/src/package/endpoints/list.rs`, the `PackageListParams` struct now includes an optional `license` field:

```rust
pub struct PackageListParams {
    pub offset: Option<i64>,
    pub limit: Option<i64>,
    pub license: Option<String>,
}
```

This means `?license=MIT` in the URL will be deserialized into `params.license = Some("MIT")`.

### Validation

The `validate_license_param` function parses the license string, splits on commas, trims whitespace, and validates each identifier against the SPDX expression parser:

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

For a single value like `MIT`, this produces `vec!["MIT"]` after validation.

### Handler Logic

The handler calls `validate_license_param` when the license parameter is present and passes the result to the service:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

### Service-Layer Filtering

In `modules/fundamental/src/package/service/mod.rs`, the `list` method now accepts `license_filter: Option<&[String]>` and applies a WHERE clause when present:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

For `license=MIT`, this generates a query that inner-joins `package_license` and filters where `license IN ('MIT')`, ensuring only MIT-licensed packages are returned.

### Test Coverage

The test `test_list_packages_single_license_filter` seeds packages with MIT and Apache-2.0 licenses, then requests `?license=MIT` and asserts:
- Response status is 200 OK
- Exactly 2 items are returned (the 2 MIT packages)
- All returned items have `license == "MIT"`

This directly validates the criterion.
