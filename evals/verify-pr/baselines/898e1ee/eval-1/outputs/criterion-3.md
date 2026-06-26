# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The implementation satisfies this criterion through SPDX validation with proper error mapping:

1. **Validation mechanism**: The `validate_license_param` function validates each license identifier using `spdx::Expression::parse(id)`. The `spdx` crate parses SPDX license expressions according to the SPDX specification. `"INVALID-999"` is not a recognized SPDX license identifier, so `Expression::parse` returns an error.

2. **Error mapping**: The parse error is mapped to an `AppError::BadRequest` with a descriptive message:
   ```rust
   Expression::parse(id).map_err(|_| {
       AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
   })?;
   ```
   The `?` operator propagates the error, short-circuiting the handler and returning the 400 response. The error message includes the specific invalid identifier for debugging purposes.

3. **Error propagation**: In the `list_packages` handler, `validate_license_param(license)?` propagates the `AppError::BadRequest` via the `?` operator. Since the handler returns `Result<..., AppError>` and `AppError` implements `IntoResponse` (per the repository's `common/src/error.rs`), the framework converts this to a 400 HTTP response.

4. **Test coverage**: `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts the response status is `StatusCode::BAD_REQUEST` (400).

The implementation correctly validates license identifiers against the SPDX specification and returns a 400 Bad Request with a descriptive error message for invalid values.
