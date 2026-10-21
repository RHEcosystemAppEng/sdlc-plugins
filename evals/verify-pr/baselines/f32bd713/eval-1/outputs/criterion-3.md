## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Verdict: PASS

### Reasoning

The PR implements SPDX license validation with proper 400 error handling:

1. **Validation logic:** The `validate_license_param` function validates each license identifier by parsing it with `spdx::Expression::parse(id)`. The `spdx` crate is a well-known Rust library for SPDX license expression parsing. An identifier like `INVALID-999` is not a recognized SPDX license, so `Expression::parse` returns an error.

2. **Error mapping:** The parse error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))` using `.map_err(|_| ...)`. The `AppError::BadRequest` variant is defined in `common/src/error.rs` and implements `IntoResponse`, returning an HTTP 400 status code.

3. **Early return:** The `?` operator after `map_err` propagates the error immediately, so validation occurs before any database query is executed. This is the correct pattern -- fail fast on invalid input.

4. **Error message content:** The error message includes the specific invalid identifier: `"Invalid SPDX license identifier: INVALID-999"`, which satisfies the criterion's requirement for "an error message."

5. **Test coverage:** The `test_list_packages_invalid_license_returns_400` integration test directly verifies this criterion:
   - Sends `GET /api/v2/package?license=INVALID-999`
   - Asserts response status is `StatusCode::BAD_REQUEST` (400)

### Evidence

- `list.rs`: `Expression::parse(id).map_err(|_| AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id)))?;`
- The `spdx` crate import: `use spdx::Expression;`
- `common/src/error.rs`: `AppError` enum with `BadRequest` variant that returns HTTP 400
- Test: `test_list_packages_invalid_license_returns_400` asserts `StatusCode::BAD_REQUEST`
