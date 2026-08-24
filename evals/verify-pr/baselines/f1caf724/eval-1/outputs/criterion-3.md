# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

This criterion requires that invalid SPDX license identifiers are rejected with a 400 Bad Request status code and an informative error message.

### Code Evidence

**Validation Logic (`modules/fundamental/src/package/endpoints/list.rs`):**

The `validate_license_param` function validates each identifier using the `spdx` crate:

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

Key observations:
1. `spdx::Expression::parse(id)` performs the validation. `INVALID-999` is not a valid SPDX expression and will cause a parse error.
2. The error is mapped to `AppError::BadRequest` with a descriptive message that includes the invalid identifier: `"Invalid SPDX license identifier: INVALID-999"`.
3. The `?` operator causes early return on the first invalid identifier, preventing any database query from executing.

**Error Propagation:**

The handler calls `validate_license_param` with the `?` operator:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

If validation fails, `AppError::BadRequest` is returned directly to the caller. Per the repository conventions, `AppError` implements `IntoResponse` (documented in `common/src/error.rs`), which converts `BadRequest` to HTTP 400 status.

**Test Coverage (`tests/api/package.rs`):**

The test `test_list_packages_invalid_license_returns_400` sends `?license=INVALID-999` and asserts:

```rust
assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
```

This directly validates the 400 status code. The error message content is not explicitly asserted in the test, but the implementation includes a descriptive message per the criterion requirement.

### Conclusion

The implementation validates license identifiers using the standard `spdx` crate parser, returns `AppError::BadRequest` with a descriptive error message for invalid identifiers, and the test confirms the 400 status code response.
