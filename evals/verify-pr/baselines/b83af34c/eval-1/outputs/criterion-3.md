# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

### Code Changes Supporting This Criterion

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**

1. The `validate_license_param` function validates each license identifier against the SPDX expression parser:
   ```rust
   for id in &identifiers {
       Expression::parse(id).map_err(|_| {
           AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
       })?;
   }
   ```

2. `spdx::Expression::parse("INVALID-999")` will fail because `INVALID-999` is not a valid SPDX license expression. The `map_err` transforms the parse error into an `AppError::BadRequest` with a descriptive error message that includes the invalid identifier.

3. The `?` operator propagates the error, causing the handler to return early with the 400 response before any database query is executed.

4. The `AppError::BadRequest` variant (from `common/src/error.rs`) implements `IntoResponse` for Axum, which translates it to an HTTP 400 Bad Request response with the error message in the body.

### Test Coverage

The test `test_list_packages_invalid_license_returns_400` directly verifies this criterion:
- Queries `GET /api/v2/package?license=INVALID-999`
- Asserts response status is `StatusCode::BAD_REQUEST` (400)

The test confirms the error path works correctly. Note that the test does not explicitly assert on the error message body content, but the criterion only requires "400 Bad Request with an error message" and the `AppError::BadRequest` variant includes the formatted message by design.

### Error Message Content

The error message format is: `"Invalid SPDX license identifier: INVALID-999"`. This is clear, identifies the problematic value, and follows the existing `AppError::BadRequest` pattern used elsewhere in the codebase.

### Conclusion

The SPDX validation using `Expression::parse` correctly rejects invalid license identifiers, and the `AppError::BadRequest` mapping produces a 400 response with a descriptive error message. The test verifies the HTTP status code. Criterion is satisfied.
