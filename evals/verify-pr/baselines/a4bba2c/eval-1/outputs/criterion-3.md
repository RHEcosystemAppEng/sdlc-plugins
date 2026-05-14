# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

### What the criterion requires
When a client supplies an invalid SPDX license identifier, the endpoint must return an HTTP 400 Bad Request response with an error message explaining the problem.

### How the implementation satisfies it

**SPDX validation (list.rs):**
The `validate_license_param` function iterates over each identifier and validates it using the `spdx` crate:
```rust
Expression::parse(id).map_err(|_| {
    AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
})?;
```
When `Expression::parse("INVALID-999")` fails (since `INVALID-999` is not a recognized SPDX expression), the error is mapped to `AppError::BadRequest` with a descriptive message including the offending identifier.

**Error propagation (list.rs):**
The `?` operator propagates the `AppError::BadRequest` from `validate_license_param` back through the `list_packages` handler. Since `AppError` implements Axum's `IntoResponse` trait (as noted in the repo structure: `common/src/error.rs`), this produces an HTTP 400 response.

**Error message content:**
The format string `"Invalid SPDX license identifier: {}"` provides a clear, specific error message identifying which identifier was invalid, satisfying the "with an error message" requirement.

**Test coverage:**
`test_list_packages_invalid_license_returns_400` sends `?license=INVALID-999` and asserts:
- Response status is `StatusCode::BAD_REQUEST` (400)

This directly validates the criterion's requirement.

### Evidence
- `modules/fundamental/src/package/endpoints/list.rs`: `Expression::parse(id)` validates SPDX identifiers
- `modules/fundamental/src/package/endpoints/list.rs`: `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))` produces the error
- `common/src/error.rs`: `AppError` enum implements `IntoResponse` (from repo structure)
- `tests/api/package.rs`: `test_list_packages_invalid_license_returns_400` validates the scenario
