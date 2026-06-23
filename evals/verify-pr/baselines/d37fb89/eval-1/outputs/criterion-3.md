# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The implementation validates license identifiers against the SPDX specification and returns a 400 Bad Request for invalid values.

### Validation Logic (`modules/fundamental/src/package/endpoints/list.rs`)

- `validate_license_param` iterates over each identifier after splitting on commas.
- For each identifier, `Expression::parse(id)` is called. This uses the `spdx` crate to parse the string as a valid SPDX license expression.
- If parsing fails (as it would for `"INVALID-999"`, which is not a recognized SPDX identifier), the error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`.
- The `?` operator propagates this error, causing the handler to return the 400 response immediately.

### Error Response

- The error message is included in the response body via `AppError::BadRequest`, which per the project's `common/src/error.rs` module implements `IntoResponse` to produce a 400 status code with the message as the response body.
- For input `"INVALID-999"`, the error message would be: `"Invalid SPDX license identifier: INVALID-999"`.

### Test Coverage

- `test_list_packages_invalid_license_returns_400` sends `?license=INVALID-999` and asserts:
  - Response status is `StatusCode::BAD_REQUEST` (400)

Note: The test asserts only the status code, not the error message body. The criterion states "returns 400 Bad Request with an error message" -- the implementation does produce an error message (`"Invalid SPDX license identifier: INVALID-999"`), so the criterion is satisfied even though the test does not explicitly verify the message content. The test could be more thorough by asserting on the message, but this is a test quality observation, not a criterion failure.
