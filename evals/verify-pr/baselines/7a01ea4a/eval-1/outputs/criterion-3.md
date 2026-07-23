## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict: PASS**

### Reasoning

The PR implements SPDX license identifier validation that rejects invalid identifiers with an appropriate error response:

**1. Validation logic (list.rs)**

The `validate_license_param` function validates each identifier using the `spdx` crate's `Expression::parse`:

```rust
for id in &identifiers {
    Expression::parse(id).map_err(|_| {
        AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
    })?;
}
```

When `Expression::parse("INVALID-999")` fails (because "INVALID-999" is not a recognized SPDX license identifier), the error is mapped to `AppError::BadRequest` with a descriptive message: `"Invalid SPDX license identifier: INVALID-999"`.

**2. Error propagation**

The `?` operator propagates the `AppError::BadRequest` from `validate_license_param` back to the `list_packages` handler. Since the handler returns `Result<Json<PaginatedResults<PackageSummary>>, AppError>`, the `AppError` is converted to an HTTP response. Based on the repository conventions (the `common/src/error.rs` module implements `IntoResponse` for `AppError`), `AppError::BadRequest` maps to HTTP 400 Bad Request.

**3. Error message included**

The criterion requires an error message to accompany the 400 response. The `format!("Invalid SPDX license identifier: {}", id)` ensures the error message is specific and identifies which identifier was invalid. This follows the existing `AppError::BadRequest` pattern used in the codebase, which includes the message in the response body.

**4. Test coverage**

The test `test_list_packages_invalid_license_returns_400` sends `GET /api/v2/package?license=INVALID-999` and asserts:
- Response status is `StatusCode::BAD_REQUEST` (400)

This directly verifies the criterion's requirement. The test does not explicitly check the error message body content, but the code produces the message string as part of the `AppError::BadRequest` variant, which the `IntoResponse` implementation serializes into the response.

### Evidence

- `Expression::parse(id)` validates against the SPDX license list (line 28 of diff)
- `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))` creates the error with a descriptive message (lines 28-30 of diff)
- `?` operator propagates the error back to the handler, short-circuiting before any database query (line 30 of diff)
- The handler's return type `Result<..., AppError>` ensures the error is rendered as an HTTP response (handler signature in diff)
- Test `test_list_packages_invalid_license_returns_400` in `tests/api/package.rs` (lines 129-135 of diff) validates the 400 response
