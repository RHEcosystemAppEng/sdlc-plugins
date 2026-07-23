# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

### Comma-Separated Parsing

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

For the input `"MIT,Apache-2.0"`, `split(',')` produces `["MIT", "Apache-2.0"]`. Each is validated individually via `Expression::parse`, and both are valid SPDX identifiers, so validation passes. The function returns `vec!["MIT".to_string(), "Apache-2.0".to_string()]`.

### Union (OR) Filtering

In `modules/fundamental/src/package/service/mod.rs`, the filter uses `Condition::any()` which produces a SQL `OR` condition:

```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```

The `is_in` with `Condition::any()` generates a SQL `WHERE package_license.license IN ('MIT', 'Apache-2.0')` clause. This returns packages whose license matches ANY of the provided identifiers -- an OR/union semantic, which is exactly what the criterion requires.

### Test Coverage

The test `test_list_packages_multi_license_filter` in `tests/api/package.rs` verifies this criterion directly:

1. Seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (GPL-3.0-only)
2. Sends `GET /api/v2/package?license=MIT,Apache-2.0`
3. Asserts response status is 200 OK
4. Asserts `body.items.len() == 2` (MIT and Apache-2.0 packages, not GPL-3.0-only)
5. Asserts `body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0")` -- confirms union semantics

### Evidence

- **Splitting**: `license.split(',')` in `validate_license_param` correctly splits comma-separated values.
- **Trimming**: `.map(|s| s.trim().to_string())` handles optional whitespace around values.
- **Per-value validation**: Each identifier is validated individually, so mixed valid/invalid inputs are caught.
- **OR semantics**: `Condition::any()` with `is_in` produces union filtering.
- **Test assertion**: The test seeds three licenses but expects only the two requested ones, confirming exclusion of non-matching packages.

## Conclusion

The implementation correctly parses comma-separated license values, validates each independently, and applies an OR filter via `Condition::any()` + `is_in`. The test confirms that only packages matching either specified license are returned, and packages with other licenses are excluded. Criterion satisfied.
