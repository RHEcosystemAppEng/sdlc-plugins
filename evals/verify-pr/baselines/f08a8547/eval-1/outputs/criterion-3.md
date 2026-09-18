# Criterion 3: GET /api/v2/package?license=INVALID-999 returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

This criterion requires that invalid SPDX license identifiers are rejected with a 400 Bad Request response containing an error message.

### Code Changes

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**
- The `validate_license_param` function iterates over each comma-separated identifier and calls `spdx::Expression::parse(id)`.
- If parsing fails, the error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`.
- The `?` operator propagates this error, causing the handler to return early with the 400 response before any database query is executed.
- The error message includes the specific invalid identifier, making it actionable for API consumers.

**Error handling pattern:**
- `AppError::BadRequest` is defined in `common/src/error.rs` and implements `IntoResponse`, which Axum uses to convert it into an HTTP 400 response.
- This follows the existing error handling pattern in the codebase (as noted in the repo conventions: "All handlers return `Result<T, AppError>` with `.context()` wrapping").

### Test Coverage

**`tests/api/package.rs::test_list_packages_invalid_license_returns_400`:**
- Queries `GET /api/v2/package?license=INVALID-999` (a string that is not a valid SPDX expression).
- Asserts `resp.status() == StatusCode::BAD_REQUEST`.
- This validates that the SPDX validation logic correctly rejects invalid identifiers.

### Conclusion

The implementation validates license identifiers against the SPDX specification using the `spdx` crate's `Expression::parse`. Invalid identifiers trigger `AppError::BadRequest` with a descriptive error message. The test confirms that the API returns a 400 status code for the invalid input.
