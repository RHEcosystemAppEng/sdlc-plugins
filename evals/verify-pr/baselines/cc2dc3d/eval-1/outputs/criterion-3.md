# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Result: PASS

## Evidence

### Validation Logic (`modules/fundamental/src/package/endpoints/list.rs`)

The `validate_license_param` function validates each license identifier against the SPDX expression parser:

```rust
fn validate_license_param(license: &str) -> Result<Vec<String>, AppError> {
    let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
    for id in &identifiers {
        Expression::parse(id).map_err(|_| {
            AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
        })?;
    }
    Ok(identifiers)
}
```

When `INVALID-999` is passed:
1. It is split as a single-element vector: `["INVALID-999"]`
2. `Expression::parse("INVALID-999")` fails because `INVALID-999` is not a valid SPDX expression
3. The error is mapped to `AppError::BadRequest` with the message `"Invalid SPDX license identifier: INVALID-999"`
4. The `?` operator propagates the error, short-circuiting the handler

### Error Propagation in Handler

The handler calls validation before executing the query:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

The `?` on `validate_license_param(license)?` propagates the `AppError::BadRequest` error to the handler's return type `Result<..., AppError>`. Per the project's `common/src/error.rs`, `AppError` implements `IntoResponse`, so `BadRequest` maps to HTTP 400.

### Error Message Content

The error message format `"Invalid SPDX license identifier: {id}"` provides:
- A clear description of the problem
- The specific identifier that failed validation
- Actionable information for the API consumer

### Test Verification (`tests/api/package.rs`)

The test `test_list_packages_invalid_license_returns_400` verifies this:

```rust
let resp = ctx.get("/api/v2/package?license=INVALID-999").await;
assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
```

The test confirms that the invalid identifier triggers a 400 response status.

## Conclusion

Invalid SPDX license identifiers are properly validated before any database query is executed. The validation uses the `spdx` crate's `Expression::parse` for authoritative SPDX compliance checking. Errors are returned as 400 Bad Request with a descriptive message identifying the invalid identifier.
