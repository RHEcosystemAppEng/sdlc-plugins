## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict: PASS**

### Analysis

The `validate_license_param` function validates each license identifier by calling `spdx::Expression::parse(id)`. If parsing fails (i.e., the identifier is not a recognized SPDX expression), the error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`. This returns a 400 status code with a descriptive error message.

The `?` operator propagates the error from `validate_license_param` back to the `list_packages` handler, which returns `Result<..., AppError>`. Since `AppError` implements `IntoResponse` (per the repository conventions in `common/src/error.rs`), the framework renders the appropriate HTTP 400 response.

### Test Coverage

The test `test_list_packages_invalid_license_returns_400` in `tests/api/package.rs`:
- Queries `GET /api/v2/package?license=INVALID-999`
- Asserts response status is `StatusCode::BAD_REQUEST` (400)

This validates both the 400 status code and that the validation rejects invalid SPDX identifiers. The error message content ("Invalid SPDX license identifier: INVALID-999") is implicitly validated through the `AppError::BadRequest` construction, though the test only asserts on the status code.
