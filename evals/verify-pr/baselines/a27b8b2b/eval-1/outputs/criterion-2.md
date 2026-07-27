# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

### Code Implementation Evidence

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

This correctly parses `"MIT,Apache-2.0"` into `["MIT", "Apache-2.0"]`. Each identifier is validated individually against the SPDX specification.

In the service layer (`modules/fundamental/src/package/service/mod.rs`), the filter uses `Condition::any()` with `is_in()`, which generates an SQL `IN` clause. This means a package matches if its license is ANY of the provided values (union semantics), which is the correct behavior for comma-separated filters.

### Test Evidence

The test `test_list_packages_multi_license_filter` verifies this behavior:
- Seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses
- Requests `GET /api/v2/package?license=MIT,Apache-2.0`
- Asserts 2 results are returned (MIT and Apache-2.0 packages)
- Asserts all returned packages have either MIT or Apache-2.0 license
- The GPL-3.0-only package is correctly excluded

### Conclusion

The implementation correctly handles comma-separated license values by parsing them into a list, validating each individually, and using an `IN` clause to return the union of matching packages. Criterion satisfied.
