# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

### Validation Logic

In `modules/fundamental/src/package/endpoints/list.rs`, the `validate_license_param` function validates each license identifier against the SPDX standard using the `spdx` crate:

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

`INVALID-999` is not a valid SPDX license expression. `Expression::parse("INVALID-999")` will return `Err(...)`, which is mapped to `AppError::BadRequest` with the message `"Invalid SPDX license identifier: INVALID-999"`.

### Error Propagation

The handler calls `validate_license_param` with the `?` operator:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

When validation fails, the `AppError::BadRequest` propagates via `?` and the Axum framework converts it to a 400 Bad Request HTTP response (as documented in the repo structure -- `common/src/error.rs` contains `AppError` which implements `IntoResponse`).

### Error Message

The error message format is: `"Invalid SPDX license identifier: INVALID-999"`. This satisfies the "with an error message" part of the criterion -- the response body contains a descriptive error explaining what went wrong.

### Test Coverage

The test `test_list_packages_invalid_license_returns_400` in `tests/api/package.rs` verifies this criterion directly:

1. Sends `GET /api/v2/package?license=INVALID-999`
2. Asserts `resp.status() == StatusCode::BAD_REQUEST`

The test confirms the 400 status code response for invalid input.

### Evidence

- **Validation**: `Expression::parse(id)` from the `spdx` crate performs SPDX standard validation.
- **Error mapping**: `.map_err(|_| AppError::BadRequest(...))` converts parse failures to 400 responses.
- **Error message**: `format!("Invalid SPDX license identifier: {}", id)` provides a descriptive error message.
- **Import**: `use spdx::Expression;` is added to bring in the SPDX validation capability.
- **Test**: Directly asserts `StatusCode::BAD_REQUEST` for the `INVALID-999` input.

## Conclusion

The implementation validates license identifiers against the SPDX standard using the `spdx` crate. Invalid identifiers like `INVALID-999` fail parsing and are mapped to `AppError::BadRequest` with a descriptive error message. The Axum framework returns this as a 400 Bad Request HTTP response. The integration test confirms the expected status code. Criterion satisfied.
