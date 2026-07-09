# Criterion 3: GET /api/v2/package?license=INVALID-999 returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

This criterion requires that invalid SPDX license identifiers are rejected with a 400 Bad Request response containing an error message.

### Code Analysis

**Validation (`modules/fundamental/src/package/endpoints/list.rs`):**

1. The `validate_license_param` function validates each identifier:
   ```rust
   for id in &identifiers {
       Expression::parse(id).map_err(|_| {
           AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
       })?;
   }
   ```

2. `spdx::Expression::parse("INVALID-999")` will fail because "INVALID-999" is not a recognized SPDX license identifier.

3. The parse failure is mapped to `AppError::BadRequest` with a descriptive error message: `"Invalid SPDX license identifier: INVALID-999"`.

4. The `?` operator propagates this error, causing the handler to return an error response. Per the repository conventions documented in `common/src/error.rs`, `AppError` implements `IntoResponse`, so `AppError::BadRequest` maps to HTTP 400 status.

**Error propagation:**

5. In the `list_packages` handler:
   ```rust
   let license_filter = match &params.license {
       Some(license) => Some(validate_license_param(license)?),
       None => None,
   };
   ```
   The `?` on `validate_license_param` means the BadRequest error propagates immediately before any database query is executed.

**Test coverage (`tests/api/package.rs`):**

6. The test `test_list_packages_invalid_license_returns_400` validates this criterion:
   - Requests `GET /api/v2/package?license=INVALID-999`
   - Asserts `resp.status() == StatusCode::BAD_REQUEST`
   - This confirms the 400 response code is returned for invalid identifiers.

### Conclusion

The implementation correctly validates license identifiers against the SPDX standard before querying the database. Invalid identifiers trigger `AppError::BadRequest` with a clear error message containing the invalid identifier. The integration test confirms the 400 status code response. The error message format ("Invalid SPDX license identifier: INVALID-999") satisfies the "with an error message" requirement.
