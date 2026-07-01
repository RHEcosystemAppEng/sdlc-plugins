# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The implementation correctly handles comma-separated license values and returns the union of matching packages through the following mechanism:

### 1. Comma Splitting and Validation

In `modules/fundamental/src/package/endpoints/list.rs`, the `validate_license_param` function handles comma-separated values:

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

For the input `"MIT,Apache-2.0"`, this produces `["MIT", "Apache-2.0"]`. Each identifier is individually validated against the SPDX expression parser before proceeding.

### 2. OR Semantics via `Condition::any()`

In the service layer (`modules/fundamental/src/package/service/mod.rs`), the filter uses `Condition::any()` combined with `is_in()`:

```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```

`Condition::any()` produces OR semantics in SeaORM, and `is_in` generates a SQL `IN` clause. For `["MIT", "Apache-2.0"]`, this becomes `WHERE package_license.license IN ('MIT', 'Apache-2.0')`, which matches packages with either license.

### 3. Test Coverage

The test `test_list_packages_multi_license_filter` in `tests/api/package.rs` directly verifies this criterion:
- Seeds 3 packages: MIT, Apache-2.0, and GPL-3.0-only
- Queries `GET /api/v2/package?license=MIT,Apache-2.0`
- Asserts response status is 200 OK
- Asserts exactly 2 items are returned (MIT and Apache-2.0, excluding GPL-3.0-only)
- Asserts all returned items have `license == "MIT" || license == "Apache-2.0"`

This confirms union semantics: both MIT and Apache-2.0 packages are included, while GPL-3.0-only is excluded.
