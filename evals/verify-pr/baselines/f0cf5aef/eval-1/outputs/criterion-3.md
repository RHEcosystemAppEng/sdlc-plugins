# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

The implementation satisfies this criterion through SPDX validation that short-circuits before any database query:

### 1. SPDX Validation (list.rs)

The `validate_license_param` function validates each identifier against the `spdx` crate's `Expression::parse`:
```rust
for id in &identifiers {
    Expression::parse(id).map_err(|_| {
        AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
    })?;
}
```

When `Expression::parse("INVALID-999")` fails (because `INVALID-999` is not a valid SPDX license identifier), the `map_err` converts the parse error into `AppError::BadRequest` with a descriptive error message including the invalid identifier.

### 2. Early Return via Error Propagation

The `?` operator in `validate_license_param` propagates the `AppError::BadRequest` immediately, and the handler's `?` on `validate_license_param(license)?` returns the error to the HTTP layer before any database interaction occurs. Since the handler returns `Result<Json<...>, AppError>`, the `AppError::BadRequest` is converted into an HTTP 400 response by the framework's `IntoResponse` implementation for `AppError`.

### 3. Error Message Content

The error message follows the format: `"Invalid SPDX license identifier: INVALID-999"`, providing clear context about which identifier was invalid.

### 4. Test Coverage

The test `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts:
- HTTP 400 (BAD_REQUEST) status code

This directly verifies the criterion.

## Evidence

- `Expression::parse(id)` validates against the SPDX standard
- `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))` produces the 400 response with an error message
- Error propagation via `?` ensures no database query is executed for invalid input
- Test `test_list_packages_invalid_license_returns_400` validates the 400 response
