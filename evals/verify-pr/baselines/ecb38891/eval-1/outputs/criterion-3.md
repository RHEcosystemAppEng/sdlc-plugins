## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Verdict: PASS

### Reasoning

The implementation validates license identifiers before querying the database:

**Validation logic** (`modules/fundamental/src/package/endpoints/list.rs`):
- `validate_license_param` iterates over each comma-separated identifier and calls `Expression::parse(id)`.
- "INVALID-999" is not a valid SPDX license expression, so `Expression::parse` returns an error.
- The error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`, which produces a 400 HTTP response with a descriptive error message.
- The `?` operator propagates the error immediately, short-circuiting the handler before any database query occurs.

**Error response path**:
- `AppError::BadRequest` is part of the project's `common/src/error.rs` module which implements `IntoResponse` for Axum, converting `BadRequest` variants into HTTP 400 responses.
- The error message format string includes the invalid identifier, providing context to the API consumer.

**Test coverage** (`tests/api/package.rs`):
- `test_list_packages_invalid_license_returns_400` requests `?license=INVALID-999` and asserts:
  - Response status is `StatusCode::BAD_REQUEST` (400)

The criterion explicitly requires both the 400 status code and an error message. The code produces both: the status code via `AppError::BadRequest` and the message via the format string `"Invalid SPDX license identifier: INVALID-999"`.
