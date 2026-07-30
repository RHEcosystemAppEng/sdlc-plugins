# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

### What was checked

This criterion requires that invalid SPDX license identifiers are rejected with a 400 Bad Request response containing an error message.

### Evidence from the diff

**1. Validation logic (`modules/fundamental/src/package/endpoints/list.rs`):**

The `validate_license_param` function validates each identifier by attempting to parse it as an SPDX expression:

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

"INVALID-999" is not a valid SPDX expression, so `Expression::parse("INVALID-999")` will return an error. This is mapped to `AppError::BadRequest` with a descriptive error message: `"Invalid SPDX license identifier: INVALID-999"`.

**2. Error propagation in the handler:**

The handler calls `validate_license_param` with the `?` operator:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

The `?` propagates the `AppError::BadRequest` result, which is returned as the handler's error response. Per the repository conventions (`common/src/error.rs`), `AppError` implements `IntoResponse`, so `AppError::BadRequest` renders as HTTP 400.

**3. Error message content:**

The error message includes the specific invalid identifier: `"Invalid SPDX license identifier: INVALID-999"`. This satisfies the requirement for "an error message" in the response.

**4. Test coverage (`tests/api/package.rs`):**

The test `test_list_packages_invalid_license_returns_400` directly verifies this criterion:
- Requests `GET /api/v2/package?license=INVALID-999`
- Asserts response status is `StatusCode::BAD_REQUEST` (400)

### Conclusion

The code validates license identifiers against the SPDX specification using the `spdx` crate, returns `AppError::BadRequest` with a descriptive error message for invalid identifiers, and the handler propagates this as a 400 response. The test provides direct verification. Criterion satisfied.
