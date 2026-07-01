## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Evidence

**Endpoint layer (`list.rs`):**
- `validate_license_param` iterates over each identifier and calls `spdx::Expression::parse(id)`.
- On parse failure, it maps the error to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`.
- The `?` operator propagates this error, causing the handler to return early with the 400 response.
- `AppError::BadRequest` (defined in `common/src/error.rs` per repo structure) implements `IntoResponse` to produce a 400 HTTP status with the error message in the body.

**Test (`tests/api/package.rs`):**
- `test_list_packages_invalid_license_returns_400` sends `GET /api/v2/package?license=INVALID-999`.
- Asserts `resp.status() == StatusCode::BAD_REQUEST`.
- `INVALID-999` is not a valid SPDX expression, so `spdx::Expression::parse` will fail, triggering the `AppError::BadRequest` path.

### Verdict: PASS

The validation logic correctly rejects invalid SPDX identifiers by leveraging the `spdx` crate's parser. The error message includes the specific invalid identifier. The test confirms a 400 status code is returned.
