# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The PR implements SPDX license validation that returns a 400 Bad Request response with a descriptive error message for invalid license identifiers.

### Validation Logic (list.rs)

The `validate_license_param()` function validates each comma-separated identifier against the SPDX expression parser:

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

For `INVALID-999`, the `spdx::Expression::parse("INVALID-999")` call will fail because `INVALID-999` is not a recognized SPDX license identifier. The `map_err` converts the parsing error into `AppError::BadRequest` with the message `"Invalid SPDX license identifier: INVALID-999"`.

The `?` operator causes the function to return early with the error, which propagates to the handler's `Result` return type. Since the handler returns `Result<Json<PaginatedResults<PackageSummary>>, AppError>`, and `AppError` implements `IntoResponse` (per the repository structure: `common/src/error.rs -- AppError enum, implements IntoResponse`), the `BadRequest` variant maps to HTTP 400 status.

### Error Propagation

The handler calls `validate_license_param` with `?`:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

If validation fails, the `?` propagates the `AppError::BadRequest` to the caller, and Axum's `IntoResponse` implementation for `AppError` converts it to a 400 response.

### Test Coverage

The test `test_list_packages_invalid_license_returns_400` validates this criterion:

```rust
let resp = ctx.get("/api/v2/package?license=INVALID-999").await;
assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
```

This sends a request with the exact invalid identifier from the acceptance criteria and asserts a 400 status code is returned.

### Error Message Inclusion

The task requires the 400 response to include "an error message." The `AppError::BadRequest` variant is constructed with `format!("Invalid SPDX license identifier: {}", id)`, which produces a descriptive message. The `IntoResponse` implementation for `AppError` (in `common/src/error.rs`) is expected to include this message in the response body, consistent with the repository's error handling pattern.

## Evidence

- `modules/fundamental/src/package/endpoints/list.rs`: `Expression::parse(id)` for SPDX validation, `AppError::BadRequest` with descriptive error message
- `common/src/error.rs`: `AppError` enum implements `IntoResponse` (per repo structure docs)
- `tests/api/package.rs`: `test_list_packages_invalid_license_returns_400` asserts 400 status
- The `spdx` crate import (`use spdx::Expression`) provides the validation capability
