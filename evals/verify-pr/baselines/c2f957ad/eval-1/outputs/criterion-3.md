# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict: PASS**

## Reasoning
- **Validation:** `validate_license_param` calls `spdx::Expression::parse(id)` for each identifier (imported with `use spdx::Expression;`). `INVALID-999` is not a known SPDX license, so parsing fails.
- **Error mapping:** a parse failure maps to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`, so the error message names the bad value.
- **Short-circuit:** the handler runs `Some(validate_license_param(license)?)`. The `?` returns the error before any database query runs. `AppError` implements `IntoResponse` (`common/src/error.rs`), and `BadRequest` maps to HTTP 400. This matches the task's Implementation Note to "return `AppError::BadRequest` for invalid values".
- **Test:** `test_list_packages_invalid_license_returns_400` requests `?license=INVALID-999` and asserts `StatusCode::BAD_REQUEST`.

## Notes
- The test asserts only the status code, not the error message body. The message itself is confirmed statically from the `format!` call. Asserting on the body would strengthen the test, but that is optional.
