# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The diff satisfies this criterion through both implementation and testing.

**Implementation**: In `modules/fundamental/src/package/endpoints/list.rs`, the `validate_license_param()` function iterates over each comma-separated license identifier and calls `Expression::parse(id)`. If parsing fails (i.e., the identifier is not a valid SPDX expression), it maps the error to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`. The `?` operator propagates this error, which short-circuits the handler and returns a 400 Bad Request response with the error message.

The error message includes the specific invalid identifier, providing clear feedback to the API consumer about which value was invalid.

**Test coverage**: The test `test_list_packages_invalid_license_returns_400` queries `?license=INVALID-999` and asserts that the response status is `StatusCode::BAD_REQUEST` (400). This directly verifies the criterion. The test does not assert on the error message body, but the implementation clearly includes one via the `format!()` call in the `AppError::BadRequest` variant.
