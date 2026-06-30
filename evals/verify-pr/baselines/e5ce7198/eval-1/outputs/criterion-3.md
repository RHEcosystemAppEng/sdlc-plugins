## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Verdict: PASS

### Evidence

**Endpoint implementation (list.rs):**
- The `validate_license_param` function iterates over each comma-separated identifier and calls `spdx::Expression::parse(id)`. If parsing fails (i.e., the identifier is not a valid SPDX expression), it maps the error to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`.
- The `?` operator propagates this error, causing the handler to return early with the `AppError::BadRequest` response before any database query is executed.
- `INVALID-999` is not a recognized SPDX license identifier, so `Expression::parse("INVALID-999")` will fail, triggering the 400 response.

**Error handling:**
- Per the repository conventions (`common/src/error.rs`), `AppError` implements `IntoResponse`, so `AppError::BadRequest` will produce an HTTP 400 status code with the error message in the response body.

**Test coverage (tests/api/package.rs):**
- `test_list_packages_invalid_license_returns_400` queries `?license=INVALID-999` and asserts:
  - Status is `StatusCode::BAD_REQUEST` (400)

This test directly validates the criterion. The implementation correctly validates SPDX identifiers and returns 400 for invalid ones with an appropriate error message.
