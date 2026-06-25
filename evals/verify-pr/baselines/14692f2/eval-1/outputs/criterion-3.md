## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Verdict: PASS

### Analysis

**Code changes supporting this criterion:**

1. **SPDX validation** (`modules/fundamental/src/package/endpoints/list.rs`):
   - The `validate_license_param` function calls `Expression::parse(id)` for each license identifier. `INVALID-999` is not a valid SPDX expression, so `Expression::parse` returns an error.

2. **Error mapping** (`modules/fundamental/src/package/endpoints/list.rs`):
   - The parse error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`. According to the repository conventions (in `common/src/error.rs`), `AppError` implements `IntoResponse`, so `AppError::BadRequest` produces a 400 HTTP response.

3. **Early return via `?` operator** (`modules/fundamental/src/package/endpoints/list.rs`):
   - The `?` operator on `Expression::parse(id).map_err(...)` ensures the function returns immediately with the `AppError::BadRequest` when validation fails, before any database query is executed.

4. **Error propagation in handler** (`modules/fundamental/src/package/endpoints/list.rs`):
   - The handler calls `validate_license_param(license)?` with the `?` operator, so the `AppError::BadRequest` propagates up as the function's `Result` error type, which Axum converts to a 400 response.

5. **Test coverage** (`tests/api/package.rs`):
   - `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts `resp.status() == StatusCode::BAD_REQUEST`.

### Conclusion

Invalid SPDX identifiers are caught by the `spdx::Expression::parse` validation, mapped to `AppError::BadRequest` with a descriptive error message, and returned as a 400 response. The test confirms this behavior.
