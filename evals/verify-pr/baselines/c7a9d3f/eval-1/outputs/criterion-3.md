# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The PR implements SPDX license validation that rejects invalid identifiers with a 400 Bad Request response:

### Validation Logic (`modules/fundamental/src/package/endpoints/list.rs`)

1. **SPDX parsing:** The `validate_license_param` function iterates over each comma-separated identifier and calls `Expression::parse(id)`. The `spdx` crate's `Expression::parse` validates against the SPDX license list. "INVALID-999" is not a recognized SPDX license identifier, so `Expression::parse("INVALID-999")` returns an `Err`.

2. **Error mapping:** The `.map_err(|_| AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id)))` converts the parse error into an `AppError::BadRequest` with a descriptive message: `"Invalid SPDX license identifier: INVALID-999"`.

3. **Early return:** The `?` operator propagates the error immediately, short-circuiting before any database query is executed.

4. **HTTP response:** The `AppError::BadRequest` variant (defined in `common/src/error.rs` per the repository structure) implements `IntoResponse` to produce an HTTP 400 Bad Request response. The error message is included in the response body.

### Error Message Content

The error message format `"Invalid SPDX license identifier: INVALID-999"` satisfies the criterion's requirement for "an error message" -- it clearly identifies which identifier was invalid and why (not a valid SPDX expression).

### Test Coverage

The test `test_list_packages_invalid_license_returns_400` directly exercises this criterion:
- Requests `GET /api/v2/package?license=INVALID-999`
- Asserts response status is `StatusCode::BAD_REQUEST` (400)

The test confirms the 400 status code. Note that the test does not assert on the error message body content, but the code clearly includes the descriptive message via `format!("Invalid SPDX license identifier: {}", id)`.
