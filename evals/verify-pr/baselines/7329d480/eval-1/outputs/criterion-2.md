## Criterion 2: Comma-Separated License Filter

**Result: PASS**

`GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license.

### Evidence

The `validate_license_param` function splits the comma-separated input into individual identifiers:

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

The `split(',')` call parses the comma-separated input, and `trim()` handles whitespace around identifiers. Each identifier is individually validated against SPDX.

In the service layer, the filter uses `Condition::any()` with `is_in`:

```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```

`Condition::any()` produces OR semantics, and `is_in` with the full list of identifiers generates `WHERE license IN ('MIT', 'Apache-2.0')`, returning the union of packages matching any of the specified licenses.

The integration test `test_list_packages_multi_license_filter` confirms this by seeding MIT, Apache-2.0, and GPL-3.0-only packages, filtering by `MIT,Apache-2.0`, and asserting that exactly 2 packages are returned (the GPL package is excluded).
