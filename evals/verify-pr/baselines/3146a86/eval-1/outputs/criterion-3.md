# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The PR diff demonstrates that this criterion is satisfied through both implementation code and test coverage.

### Implementation Evidence

1. **SPDX validation** (`validate_license_param` in `list.rs`):
   - The function iterates over each comma-separated identifier and calls `Expression::parse(id)`.
   - `Expression::parse` is from the `spdx` crate (imported at the top of the file: `use spdx::Expression;`), which validates whether the input is a recognized SPDX license expression.
   - "INVALID-999" is not a valid SPDX license identifier, so `Expression::parse` will return an `Err`.

2. **Error mapping to 400 Bad Request**:
   - The `map_err` closure converts the parse error into `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`.
   - The `?` operator propagates this error, causing the `validate_license_param` function to return `Err(AppError::BadRequest(...))`.
   - In the handler, `validate_license_param(license)?` propagates the error to the handler return type `Result<Json<PaginatedResults<PackageSummary>>, AppError>`.
   - The `AppError::BadRequest` variant (defined in `common/src/error.rs` per the repo structure) implements `IntoResponse` and returns HTTP 400 status code.

3. **Error message content**:
   - The error message includes the invalid identifier: `"Invalid SPDX license identifier: INVALID-999"`. This satisfies the "with an error message" part of the criterion.

### Test Evidence

The test `test_list_packages_invalid_license_returns_400` in `tests/api/package.rs`:
- Sends `GET /api/v2/package?license=INVALID-999`.
- Asserts the response status is `StatusCode::BAD_REQUEST` (HTTP 400).

This test directly validates the acceptance criterion.

### Conclusion

The implementation validates license identifiers against the SPDX standard using the `spdx` crate's `Expression::parse`. Invalid identifiers cause an `AppError::BadRequest` with a descriptive error message, which the Axum framework translates to an HTTP 400 Bad Request response. The integration test confirms the expected 400 status code.
