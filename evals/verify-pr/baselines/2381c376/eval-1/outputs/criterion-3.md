## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Verdict: PASS

### Analysis

**Code evidence in the diff:**

1. **SPDX validation** (`list.rs`): The `validate_license_param` function attempts to parse each identifier:
   ```rust
   Expression::parse(id).map_err(|_| {
       AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
   })?;
   ```
   `INVALID-999` is not a valid SPDX expression, so `Expression::parse` will return an error, which is mapped to `AppError::BadRequest` with a descriptive message including the invalid identifier.

2. **Early return via `?` operator**: The `?` operator propagates the error immediately, preventing the query from executing. The `AppError::BadRequest` variant (defined in `common/src/error.rs` per the repo structure) implements `IntoResponse` and returns an HTTP 400 status code.

3. **Handler integration** (`list.rs`): The handler calls `validate_license_param(license)?` before calling `PackageService::list`, ensuring the 400 response is returned before any database query.

**Test evidence:**

The test `test_list_packages_invalid_license_returns_400` in `tests/api/package.rs`:
- Requests `GET /api/v2/package?license=INVALID-999`.
- Asserts the response status is `StatusCode::BAD_REQUEST` (400).

This directly verifies the criterion. The error message format `"Invalid SPDX license identifier: INVALID-999"` satisfies the "with an error message" requirement.
