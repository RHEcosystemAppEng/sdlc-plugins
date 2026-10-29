# Criterion 3: GET /api/v2/package?license=INVALID-999 returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

The PR implements SPDX license validation with 400 Bad Request for invalid identifiers:

1. **Validation logic** (`list.rs`): The `validate_license_param` function validates each identifier:
   ```rust
   Expression::parse(id).map_err(|_| {
       AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
   })?;
   ```
   - Uses the `spdx` crate's `Expression::parse` for validation
   - On failure, returns `AppError::BadRequest` with a descriptive error message that includes the invalid identifier
   - The `?` operator causes early return on the first invalid identifier

2. **Error propagation** (`list.rs`): The handler calls `validate_license_param(license)?` which propagates the `AppError::BadRequest` to the Axum response layer. Per the repository conventions, `AppError` implements `IntoResponse`, converting `BadRequest` to HTTP 400.

3. **Test verification** (`tests/api/package.rs`): The test `test_list_packages_invalid_license_returns_400` queries `?license=INVALID-999` and asserts:
   - Status is `StatusCode::BAD_REQUEST` (400)

The implementation correctly validates license identifiers and returns 400 Bad Request with a descriptive error message for invalid values.
