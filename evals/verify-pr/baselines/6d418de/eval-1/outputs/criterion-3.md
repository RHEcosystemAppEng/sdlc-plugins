# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The PR implements SPDX validation that rejects invalid license identifiers with a 400 Bad Request response:

1. **Validation logic** (`list.rs` - `validate_license_param`):
   - For each license identifier parsed from the comma-separated string, the function calls `Expression::parse(id)`.
   - If parsing fails (the identifier is not a valid SPDX expression), the error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`.
   - The `?` operator propagates this error, short-circuiting the handler before any database query runs.

2. **Error handling**:
   - `AppError::BadRequest` is defined in `common/src/error.rs` and implements `IntoResponse` (per the repository conventions documented in `repo-backend.md`).
   - The Axum framework automatically converts the `AppError::BadRequest` into an HTTP 400 response with the error message in the body.
   - The error message is descriptive: `"Invalid SPDX license identifier: INVALID-999"`.

3. **Handler integration** (`list.rs` - `list_packages`):
   - The handler calls `validate_license_param(license)?` when the license parameter is present.
   - The `?` operator ensures the 400 error is returned immediately without executing the database query.

4. **Test coverage** (`tests/api/package.rs`):
   - `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999`.
   - Asserts the response status is `StatusCode::BAD_REQUEST`.

The validation correctly rejects invalid SPDX identifiers and returns a meaningful error message with a 400 status code.
