# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict: PASS**

## Code evidence
- `list.rs`, in `validate_license_param`:
  ```rust
  Expression::parse(id).map_err(|_| AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id)))?
  ```
  `INVALID-999` is not a known SPDX identifier, so `Expression::parse` fails.
- The handler calls `validate_license_param(license)?` before any database access, so the error short-circuits the request.
- `AppError` implements `IntoResponse` (`common/src/error.rs`). `BadRequest` therefore becomes a 400 response, and the body carries the message "Invalid SPDX license identifier: INVALID-999".
- This matches the Implementation Note: validate against SPDX and return `AppError::BadRequest`.

## Test evidence
`test_list_packages_invalid_license_returns_400` requests `?license=INVALID-999` and asserts `StatusCode::BAD_REQUEST`. CI passes.

## Caveats (non-blocking)
- **Untested message:** the test checks only the status code, not the error message in the body. The message exists in code, but no test covers it.
- **Compound expressions:** `Expression::parse` accepts compound expressions such as `MIT OR Apache-2.0`. Such a value would pass validation and then be matched as a literal string. This edge case is outside the stated criterion.
