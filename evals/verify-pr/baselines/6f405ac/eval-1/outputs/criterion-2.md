# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` splits the license parameter on commas:

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

This produces a `Vec<String>` containing `["MIT", "Apache-2.0"]`. Each identifier is individually validated as a valid SPDX expression.

The service layer in `modules/fundamental/src/package/service/mod.rs` uses `Condition::any()` with `is_in()`:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

The `is_in` clause generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` condition, which returns the union of packages matching either license. The `Condition::any()` wrapper ensures OR semantics.

The integration test `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), queries with `?license=MIT,Apache-2.0`, and asserts that exactly 2 packages are returned, all having either MIT or Apache-2.0 license.

## Evidence

- `list.rs`: `license.split(',')` handles comma-separated values
- `list.rs`: `.map(|s| s.trim().to_string())` trims whitespace around identifiers
- `service/mod.rs`: `is_in(licenses.iter().cloned())` with `Condition::any()` provides OR/union semantics
- `tests/api/package.rs`: `test_list_packages_multi_license_filter` verifies union behavior with 3 seeded packages
