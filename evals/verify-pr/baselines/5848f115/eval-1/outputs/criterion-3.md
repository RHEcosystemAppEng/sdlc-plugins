# Criterion 3: GET /api/v2/package?license=INVALID-999 returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The implementation satisfies this criterion through SPDX validation with proper error propagation:

### Validation Logic (list.rs)

The `validate_license_param("INVALID-999")` function:
1. Splits the input on commas: produces `["INVALID-999"]`
2. Attempts to validate with `spdx::Expression::parse("INVALID-999")`
3. "INVALID-999" is not a valid SPDX license expression, so `Expression::parse()` returns an error
4. The error is mapped via `.map_err(|_| AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id)))` to produce `AppError::BadRequest("Invalid SPDX license identifier: INVALID-999")`
5. The `?` operator propagates this error, returning `Err(AppError::BadRequest(...))` immediately

### Error Propagation (list.rs)

In `list_packages`, the call to `validate_license_param(license)?` propagates the `AppError::BadRequest` error. Since the handler returns `Result<Json<PaginatedResults<PackageSummary>>, AppError>`, and `AppError` implements `IntoResponse` (per the repository's `common/src/error.rs`), this produces a 400 Bad Request HTTP response with the error message included in the response body.

### Error Message Content

The error message follows the format `"Invalid SPDX license identifier: INVALID-999"`, which provides clear feedback about which identifier failed validation. This satisfies the "with an error message" part of the criterion.

### Test Coverage

The test `test_list_packages_invalid_license_returns_400` validates this criterion:
- Queries `GET /api/v2/package?license=INVALID-999`
- Asserts `resp.status() == StatusCode::BAD_REQUEST`
- Confirms the 400 status code is returned for invalid identifiers

### Conclusion

The implementation uses the `spdx` crate for validation, which provides authoritative SPDX license identifier checking. Invalid identifiers are caught before any database query is executed, and a descriptive 400 Bad Request error is returned following the project's existing `AppError` pattern.
