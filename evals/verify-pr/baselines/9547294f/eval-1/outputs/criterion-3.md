# Acceptance Criterion 3

**Criterion:** `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The implementation validates license identifiers and returns 400 Bad Request for invalid values:

1. **Validation logic:** The `validate_license_param` function iterates over each license identifier and attempts to parse it as an SPDX expression:
   ```rust
   Expression::parse(id).map_err(|_| {
       AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
   })?;
   ```
   `INVALID-999` is not a valid SPDX license identifier, so `Expression::parse` will return an error.

2. **Error propagation:** The `map_err` converts the SPDX parse error into `AppError::BadRequest` with a descriptive message: `"Invalid SPDX license identifier: INVALID-999"`. The `?` operator propagates this error up through the handler, which returns `Result<..., AppError>`.

3. **Error response:** The repository structure shows `common/src/error.rs` contains the `AppError` enum which implements `IntoResponse`. `AppError::BadRequest` maps to HTTP 400 status code. The error message is included in the response body.

4. **Early validation:** The validation occurs in the handler before calling the service layer. The `validate_license_param` call happens at:
   ```rust
   let license_filter = match &params.license {
       Some(license) => Some(validate_license_param(license)?),
       None => None,
   };
   ```
   This ensures invalid licenses are caught before any database query is attempted.

5. **Test coverage:** The test `test_list_packages_invalid_license_returns_400` sends `?license=INVALID-999` and asserts `resp.status() == StatusCode::BAD_REQUEST`.

## Evidence

- `modules/fundamental/src/package/endpoints/list.rs`: `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))` produces 400 with error message
- `modules/fundamental/src/package/endpoints/list.rs`: Validation occurs before service call via `validate_license_param(license)?`
- `tests/api/package.rs`: `test_list_packages_invalid_license_returns_400` confirms 400 response
