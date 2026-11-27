# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict: MET (PASS)**

## Code evidence
- `modules/fundamental/src/package/endpoints/list.rs`: new import `use spdx::Expression;`.
- `validate_license_param`: `Expression::parse(id).map_err(|_| AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id)))?;`
- The handler calls `validate_license_param(license)?` before any database query, so invalid input short-circuits the request.
- `AppError` implements `IntoResponse` (`common/src/error.rs`); `AppError::BadRequest` maps to HTTP 400 with the message naming the offending identifier.

## Test evidence
`test_list_packages_invalid_license_returns_400` requests `?license=INVALID-999` and asserts `StatusCode::BAD_REQUEST`.

## Reasoning
`spdx::Expression::parse` (strict mode) rejects identifiers not in the SPDX license list, so `INVALID-999` produces `AppError::BadRequest("Invalid SPDX license identifier: INVALID-999")` → 400 with an error message. This matches the Implementation Note to validate against a known SPDX list and return `AppError::BadRequest`. Caveats: the test asserts only the status code, not the message body (the message is evidenced by code); `Expression::parse` also accepts valid compound expressions and `LicenseRef-*`, which is lenient but does not contradict the criterion.
