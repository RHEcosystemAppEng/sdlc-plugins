# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The implementation validates license identifiers and returns a 400 Bad Request for invalid values.

**Endpoint layer** (`modules/fundamental/src/package/endpoints/list.rs`):
- The `validate_license_param` function iterates over each comma-separated identifier and calls `Expression::parse(id)` from the `spdx` crate.
- If parsing fails, it maps the error to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`.
- The `?` operator propagates this error immediately, causing the handler to return before any database query is executed.
- Since `INVALID-999` is not a valid SPDX expression, `Expression::parse("INVALID-999")` will return an `Err`, triggering the `AppError::BadRequest` response.
- The error message includes the specific invalid identifier, satisfying the "with an error message" requirement.

**Test coverage** (`tests/api/package.rs`):
- The test `test_list_packages_invalid_license_returns_400` requests `GET /api/v2/package?license=INVALID-999` and asserts that the response status is `StatusCode::BAD_REQUEST` (400).
- This directly validates the criterion. The test does not assert the error message body, but the implementation clearly includes one via the `format!("Invalid SPDX license identifier: {}", id)` string.
