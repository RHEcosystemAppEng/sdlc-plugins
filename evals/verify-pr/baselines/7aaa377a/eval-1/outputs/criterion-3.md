## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict: PASS**

### Analysis

This criterion requires that invalid SPDX license identifiers are rejected with a 400 Bad Request response containing an error message.

### Evidence from the PR diff

**1. Validation logic (list.rs)**

The `validate_license_param` function validates each license identifier using the `spdx` crate's `Expression::parse`:

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

When `Expression::parse("INVALID-999")` fails (because "INVALID-999" is not a recognized SPDX license expression), the error is mapped to `AppError::BadRequest` with a descriptive message: `"Invalid SPDX license identifier: INVALID-999"`.

**2. Error propagation (list.rs)**

In the `list_packages` handler, the validation result is propagated with the `?` operator:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

If validation fails, the `AppError::BadRequest` is returned immediately, short-circuiting the handler before any database query executes. The `AppError` enum (documented in `common/src/error.rs` per the repo structure) implements `IntoResponse`, converting `BadRequest` to an HTTP 400 response.

**3. Integration test coverage (tests/api/package.rs)**

The test `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts:

```rust
assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
```

This directly validates the 400 response for invalid identifiers.

### Conclusion

The implementation validates license identifiers against the SPDX standard using the `spdx` crate before querying. Invalid identifiers produce a 400 Bad Request response with a clear error message identifying the offending identifier. The test confirms this behavior.
