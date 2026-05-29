## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict: PASS**

### Evidence

The invalid license handling is implemented through SPDX validation:

1. **`modules/fundamental/src/package/endpoints/list.rs`**: The `validate_license_param()` function iterates over each parsed identifier and calls `Expression::parse(id)` (from the `spdx` crate, imported at the top of the file). If parsing fails, it maps the error to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`. The `?` operator propagates this error, causing the handler to return a 400 Bad Request response with the descriptive error message.

2. The handler calls `validate_license_param(license)?` before any database query, ensuring invalid identifiers are rejected early with a clear error message including the offending identifier.

3. **`tests/api/package.rs`**: The test `test_list_packages_invalid_license_returns_400` queries `?license=INVALID-999` and asserts that the response status is `StatusCode::BAD_REQUEST` (400).

The implementation correctly validates license identifiers against known SPDX expressions and returns a 400 Bad Request with a descriptive error message for invalid values.
