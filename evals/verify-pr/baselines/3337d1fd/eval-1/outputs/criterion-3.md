## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Verdict: PASS

### Reasoning

This criterion requires that invalid SPDX license identifiers are rejected with a 400 Bad Request response containing an error message.

**Validation logic (`list.rs`):**
The `validate_license_param` function iterates over each identifier and attempts to parse it using `spdx::Expression::parse(id)`:
```rust
for id in &identifiers {
    Expression::parse(id).map_err(|_| {
        AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
    })?;
}
```
When `Expression::parse` fails (returns `Err`), the error is mapped to `AppError::BadRequest` with a descriptive message that includes the invalid identifier. The `?` operator propagates this error, causing the handler to return the error response immediately.

**Error response:**
The `AppError::BadRequest` variant (from `common/src/error.rs` per the repo structure) implements `IntoResponse`, which the Axum framework uses to generate a 400 status code response with the error message in the body.

**Handler integration (`list.rs`):**
The validation runs before the database query:
```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```
If validation fails, the `?` operator returns the `AppError::BadRequest` immediately, and `PackageService::list` is never called. This follows the fail-fast pattern described in the implementation notes.

**Test coverage (`tests/api/package.rs`):**
The test `test_list_packages_invalid_license_returns_400` sends `GET /api/v2/package?license=INVALID-999` and asserts:
- Response status is `StatusCode::BAD_REQUEST` (400)

The test confirms the error response. Note that the test asserts the status code but does not explicitly verify the error message body. However, the code clearly includes the error message via the `format!` macro, and the `AppError::BadRequest` type is designed to serialize this message in the response body per the project's error handling conventions.

### Evidence

- `list.rs`: `Expression::parse(id).map_err(|_| AppError::BadRequest(...))` validates SPDX identifiers
- `list.rs`: Error message format: `"Invalid SPDX license identifier: {id}"`
- `list.rs`: `?` operator in handler ensures early return on validation failure
- `tests/api/package.rs`: `test_list_packages_invalid_license_returns_400` asserts 400 status for `INVALID-999`
