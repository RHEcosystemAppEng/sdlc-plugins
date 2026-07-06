# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The PR implements invalid license rejection through SPDX validation:

1. **SPDX validation** (`list.rs`): The `validate_license_param` function calls `Expression::parse(id)` for each license identifier. `"INVALID-999"` is not a valid SPDX license expression, so `Expression::parse` returns an error.

2. **Error mapping** (`list.rs`): The parse error is mapped to an `AppError::BadRequest` with a descriptive message:
   ```rust
   Expression::parse(id).map_err(|_| {
       AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
   })?;
   ```
   The `?` operator propagates this error, causing the handler to return early with the 400 response before any database query is executed.

3. **Error response** (via `common/src/error.rs`): The `AppError::BadRequest` variant implements `IntoResponse` (as documented in the repository conventions), returning an HTTP 400 status code with the error message in the response body.

4. **Test coverage** (`tests/api/package.rs`): The `test_list_packages_invalid_license_returns_400` test sends a request with `?license=INVALID-999` and asserts:
   - Response status is `StatusCode::BAD_REQUEST` (400)

The implementation correctly validates license identifiers against the SPDX standard and returns a 400 Bad Request with a clear error message for invalid identifiers.
