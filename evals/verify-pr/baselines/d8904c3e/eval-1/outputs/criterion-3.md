# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

### What the criterion requires

When an invalid SPDX license identifier is provided, the endpoint must reject the request with HTTP 400 Bad Request and include a descriptive error message.

### Evidence from the diff

**1. SPDX validation (list.rs)**

The `validate_license_param` function parses each identifier using `spdx::Expression::parse`:

```rust
Expression::parse(id).map_err(|_| {
    AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
})?;
```

`INVALID-999` is not a recognized SPDX license identifier, so `Expression::parse("INVALID-999")` returns an `Err`. The `map_err` converts this into `AppError::BadRequest` with a descriptive message that includes the offending identifier: `"Invalid SPDX license identifier: INVALID-999"`.

**2. Error propagation (list.rs)**

The `?` operator propagates the error from `validate_license_param` up to the `list_packages` handler, which returns `Result<..., AppError>`. The `AppError::BadRequest` variant (defined in `common/src/error.rs`) implements `IntoResponse` and maps to HTTP 400 status code as per the repository conventions.

**3. Error message inclusion**

The `format!("Invalid SPDX license identifier: {}", id)` ensures the error response body contains a human-readable message identifying which license identifier was invalid. This satisfies the "with an error message" part of the criterion.

**4. Test coverage (tests/api/package.rs)**

The test `test_list_packages_invalid_license_returns_400` verifies this criterion:
- Sends `GET /api/v2/package?license=INVALID-999`
- Asserts the response status is `StatusCode::BAD_REQUEST` (400)

### Conclusion

The SPDX validation catches invalid identifiers, converts them to `AppError::BadRequest` with a descriptive message, and returns a 400 response. The integration test confirms the expected status code. The criterion is satisfied.
