# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

The `validate_license_param` function in `list.rs` validates each license identifier against the SPDX specification:

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

When `INVALID-999` is passed, `spdx::Expression::parse("INVALID-999")` fails because it is not a recognized SPDX expression. The error is mapped to `AppError::BadRequest` with a descriptive message including the invalid identifier. The `?` operator propagates this error, causing the handler to return 400 Bad Request.

The test `test_list_packages_invalid_license_returns_400` in `tests/api/package.rs` verifies this:
- Sends `GET /api/v2/package?license=INVALID-999`
- Asserts the response status is `StatusCode::BAD_REQUEST` (400)

## Evidence

- `list.rs`: `Expression::parse(id).map_err(|_| AppError::BadRequest(...))` validates and rejects invalid identifiers
- `list.rs`: Error message includes the invalid identifier: `"Invalid SPDX license identifier: {id}"`
- `tests/api/package.rs`: `test_list_packages_invalid_license_returns_400` asserts 400 response
