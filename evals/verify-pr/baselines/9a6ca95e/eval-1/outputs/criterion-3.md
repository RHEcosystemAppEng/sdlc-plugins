## Criterion 3

**Text:** `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Analysis

The validation and error handling are implemented as follows:

1. **Validation logic** (`list.rs`): The `validate_license_param` function iterates over each parsed identifier and validates it against the SPDX specification:
   ```rust
   for id in &identifiers {
       Expression::parse(id).map_err(|_| {
           AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
       })?;
   }
   ```
   When `Expression::parse("INVALID-999")` fails (as it is not a valid SPDX identifier), the error is mapped to `AppError::BadRequest` with a descriptive message: `"Invalid SPDX license identifier: INVALID-999"`.

2. **Error propagation** (`list.rs`): The `?` operator propagates the `AppError::BadRequest` from `validate_license_param` up through the handler, which has return type `Result<Json<PaginatedResults<PackageSummary>>, AppError>`. The `AppError` type implements `IntoResponse` (per `common/src/error.rs` in the repo structure), converting it to an HTTP 400 response.

3. **Error message**: The format string `"Invalid SPDX license identifier: {}"` provides a clear, actionable error message that includes the offending identifier.

4. **Test coverage** (`tests/api/package.rs`): `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts:
   ```rust
   assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
   ```

### Verdict: PASS

The implementation validates license identifiers against the SPDX standard, returns a 400 Bad Request with a descriptive error message for invalid values, and the test verifies this behavior.
