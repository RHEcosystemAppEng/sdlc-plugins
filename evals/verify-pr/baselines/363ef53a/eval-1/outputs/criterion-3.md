# Criterion 3: GET /api/v2/package?license=INVALID-999 returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

### Code Changes

The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` validates each license identifier by calling `Expression::parse(id)`. When parsing fails (i.e., the identifier is not a recognized SPDX expression), the error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`.

The `?` operator propagates this error out of `validate_license_param`, and since the handler returns `Result<..., AppError>`, the `AppError::BadRequest` variant is converted into an HTTP 400 response by the `IntoResponse` implementation defined in `common/src/error.rs` (per the repository structure).

The error message includes the specific invalid identifier, making it clear to the caller which value was rejected.

### Test Coverage

The test `test_list_packages_invalid_license_returns_400` sends `GET /api/v2/package?license=INVALID-999` and asserts:
- Response status is `StatusCode::BAD_REQUEST` (400)

This directly validates the criterion. The test does not assert on the error message body, but the criterion only requires "400 Bad Request with an error message" and the code clearly produces both.

### Conclusion

Invalid SPDX license identifiers are caught by `Expression::parse`, converted to `AppError::BadRequest` with a descriptive message, and returned as HTTP 400 responses. The validation runs before any database query, ensuring invalid input never reaches the query layer.
