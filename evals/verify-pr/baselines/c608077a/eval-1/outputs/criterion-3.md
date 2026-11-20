# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict: PASS**

## Reasoning

1. **Validation path**: `list_packages` calls `validate_license_param(license)?` before any database access.
2. **Rejection**: `spdx::Expression::parse("INVALID-999")` returns an error, because the default strict parse mode rejects identifiers that are not on the SPDX license list. The error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`, so the response carries a readable message naming the bad value.
3. **HTTP mapping**: `AppError` implements `IntoResponse` (`common/src/error.rs` in the repo structure). `BadRequest` maps to 400, as the task's Implementation Notes require ("return `AppError::BadRequest` for invalid values").
4. **Early return**: the `?` returns the error from the handler before the service is called, so no query runs.
5. **Test coverage**: `test_list_packages_invalid_license_returns_400` requests `?license=INVALID-999` and asserts `StatusCode::BAD_REQUEST`.

## Observations (non-blocking)
- The test checks only the status code, not the error message body. The message comes from the `AppError::BadRequest(String)` payload in the code. A body assertion would make the "with an error message" part of the criterion explicit in tests.
- In a mixed list such as `MIT,INVALID-999`, the first invalid entry causes a 400. That is consistent with the criterion.
