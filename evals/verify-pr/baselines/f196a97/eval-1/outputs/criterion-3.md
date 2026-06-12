## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict:** PASS

### Reasoning

The `validate_license_param` function validates each license identifier against the SPDX standard:

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

For the input `"INVALID-999"`:
1. The string is split on commas, producing `vec!["INVALID-999"]`
2. `spdx::Expression::parse("INVALID-999")` is called -- since "INVALID-999" is not a valid SPDX license identifier, this returns an error
3. The error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: INVALID-999"))`
4. The `?` operator propagates this error, which Axum converts to an HTTP 400 Bad Request response

The error message is descriptive, indicating which specific identifier was invalid. This follows the project's error handling pattern using `AppError::BadRequest`.

The handler calls `validate_license_param(license)?` early in `list_packages`, so the 400 error is returned before any database query is attempted.

The integration test `test_list_packages_invalid_license_returns_400` sends a request with `license=INVALID-999` and asserts `resp.status() == StatusCode::BAD_REQUEST`.

### Evidence

- `list.rs`: `Expression::parse(id).map_err(|_| AppError::BadRequest(...))` with `?` propagation
- `list.rs`: Error message format: `"Invalid SPDX license identifier: {id}"`
- `common/src/error.rs`: `AppError` enum implements `IntoResponse` (per repo conventions)
- `tests/api/package.rs`: `test_list_packages_invalid_license_returns_400` covers this scenario
