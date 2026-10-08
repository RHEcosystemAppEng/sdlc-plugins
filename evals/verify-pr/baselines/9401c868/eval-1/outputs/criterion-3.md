## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Result: PASS**

### Evidence

The PR implements license identifier validation with proper error responses:

1. **Validation logic** (`modules/fundamental/src/package/endpoints/list.rs` -- `validate_license_param`): Each comma-separated license identifier is validated against the SPDX specification using `spdx::Expression::parse(id)`. If parsing fails (i.e., the identifier is not a recognized SPDX expression), the error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`.

2. **Error propagation**: The `validate_license_param` function returns `Result<Vec<String>, AppError>`. In the handler, the `?` operator propagates the error. Since `AppError` implements `IntoResponse` (as noted in the repo structure at `common/src/error.rs`), a `BadRequest` variant is automatically converted to a 400 HTTP response with the error message in the response body.

3. **Early return**: The validation occurs before any database query is executed, so invalid license identifiers are rejected immediately without wasting database resources.

4. **Test coverage** (`tests/api/package.rs` -- `test_list_packages_invalid_license_returns_400`): The test sends a request with `?license=INVALID-999` and asserts:
   - Response status is `400 BAD_REQUEST`

The error message format `"Invalid SPDX license identifier: INVALID-999"` provides clear feedback about which identifier was invalid, satisfying the "with an error message" part of the criterion.
