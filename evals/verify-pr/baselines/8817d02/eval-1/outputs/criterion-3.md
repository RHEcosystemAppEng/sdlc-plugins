# Criterion 3: GET /api/v2/package?license=INVALID-999 returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The PR implements invalid license rejection through the following code path:

1. **Validation function** (`list.rs`): The `validate_license_param` function validates each license identifier by parsing it as an SPDX expression:
   ```rust
   Expression::parse(id).map_err(|_| {
       AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
   })?;
   ```
   The `?` operator causes early return with the `AppError::BadRequest` error if any identifier fails parsing.

2. **Error propagation** (`list.rs`): In the `list_packages` handler, the validation is called via:
   ```rust
   let license_filter = match &params.license {
       Some(license) => Some(validate_license_param(license)?),
       None => None,
   };
   ```
   The `?` propagates the `AppError::BadRequest` to the handler's return type `Result<Json<...>, AppError>`.

3. **Error response**: Per the repo conventions documented in `common/src/error.rs`, `AppError` implements `IntoResponse`, and `AppError::BadRequest` maps to HTTP 400 status code. The error message "Invalid SPDX license identifier: INVALID-999" is included in the response body.

4. **Test verification** (`tests/api/package.rs`): The `test_list_packages_invalid_license_returns_400` test requests `?license=INVALID-999` and asserts `resp.status() == StatusCode::BAD_REQUEST`.

The implementation correctly validates license identifiers against the SPDX standard using the `spdx` crate and returns a 400 Bad Request with a descriptive error message for invalid identifiers.
