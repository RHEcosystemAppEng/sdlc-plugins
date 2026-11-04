# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict: PASS**

## Code evidence
- `validate_license_param` calls `spdx::Expression::parse(id)` on each identifier. On failure it maps the error to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))` and returns early with `?`, before any database access.
- `Expression::parse` uses strict mode, which rejects terms that are not on the SPDX license list. `INVALID-999` is not a known identifier and is not a `LicenseRef-` reference, so parsing fails.
- `AppError` (in `common/src/error.rs`) implements `IntoResponse`. Following the repository convention, `BadRequest` maps to HTTP 400, and the response carries the message `Invalid SPDX license identifier: INVALID-999`.
- This follows the Implementation Note: "Validate license identifiers against a known SPDX license list before querying; return `AppError::BadRequest` for invalid values."

## Test evidence
- `tests/api/package.rs::test_list_packages_invalid_license_returns_400` requests `?license=INVALID-999` and asserts `StatusCode::BAD_REQUEST`.

## Notes (non-blocking)
- The test checks only the status code and does not assert on the error message body. The code clearly produces a message, so the criterion is met.
- `Expression::parse` also accepts compound expressions such as `MIT OR Apache-2.0`. Those would pass validation and then simply match nothing, which is acceptable.
