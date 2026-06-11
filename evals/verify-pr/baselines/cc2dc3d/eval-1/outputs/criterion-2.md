# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Result: PASS

## Evidence

### Comma-Separated Parsing (`modules/fundamental/src/package/endpoints/list.rs`)

The `validate_license_param` function handles comma-separated values:

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

For the input `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`. Each identifier is validated individually against the SPDX expression parser. The `trim()` call also handles whitespace around commas (e.g., `MIT, Apache-2.0`).

### Service Layer Union Query (`modules/fundamental/src/package/service/mod.rs`)

The filter uses `Condition::any()` with `is_in()`:

```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```

`is_in` with multiple values produces `WHERE license IN ('MIT', 'Apache-2.0')`, which returns the union of packages matching either license. The `Condition::any()` wrapping is consistent with OR semantics.

### Test Verification (`tests/api/package.rs`)

The test `test_list_packages_multi_license_filter` verifies this:

- Seeds 3 packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (GPL-3.0-only)
- Queries `GET /api/v2/package?license=MIT,Apache-2.0`
- Asserts `StatusCode::OK`
- Asserts `body.items.len() == 2` (MIT and Apache-2.0 packages; GPL-3.0-only excluded)
- Asserts `body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0")`

The test confirms that the comma-separated filter correctly returns the union of matching packages while excluding packages with other licenses (GPL-3.0-only).

## Conclusion

The comma-separated license parsing is correctly implemented with proper trimming and individual SPDX validation. The service layer generates an `IN` clause that returns the union of matching packages. The test validates the behavior with 3 different licenses and asserts the correct 2-package result set.
