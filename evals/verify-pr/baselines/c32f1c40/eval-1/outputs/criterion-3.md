# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

This criterion requires that invalid SPDX license identifiers in the query parameter are rejected with a 400 Bad Request response containing an error message.

### Implementation Evidence

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**
- `validate_license_param` iterates over each comma-separated identifier and calls `spdx::Expression::parse(id)`.
- If parsing fails (indicating an invalid SPDX identifier), the error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`.
- The `?` operator propagates this error, causing the handler to return early with the 400 response.
- `INVALID-999` is not a valid SPDX expression, so `Expression::parse("INVALID-999")` will return an error.

**Error handling:**
- `AppError::BadRequest` is defined in `common/src/error.rs` and implements `IntoResponse` (per the repository conventions), which produces an HTTP 400 status code with the error message in the response body.

**Test coverage (`tests/api/package.rs`):**
- `test_list_packages_invalid_license_returns_400` queries `?license=INVALID-999` and asserts:
  - `resp.status() == StatusCode::BAD_REQUEST` (400)

### Conclusion

The implementation validates license identifiers against the SPDX specification using the `spdx` crate's `Expression::parse`. Invalid identifiers trigger `AppError::BadRequest` with a descriptive error message, which the framework converts to a 400 HTTP response. The test confirms the 400 status code is returned.
