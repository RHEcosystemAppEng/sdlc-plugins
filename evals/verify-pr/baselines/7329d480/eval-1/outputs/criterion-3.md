## Criterion 3: 400 Bad Request for Invalid License

**Result: PASS**

`GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message.

### Evidence

The `validate_license_param` function validates each identifier using the `spdx` crate's `Expression::parse`:

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

When `Expression::parse(id)` fails for an invalid identifier like `INVALID-999`, `map_err` converts the parse error into `AppError::BadRequest` with a descriptive message that includes the offending identifier. The `?` operator propagates this error, short-circuiting the handler before any database query is executed.

Since `AppError` implements `IntoResponse` (as documented in `common/src/error.rs`), the `BadRequest` variant produces an HTTP 400 status code with the error message in the response body.

The integration test `test_list_packages_invalid_license_returns_400` confirms this by requesting `?license=INVALID-999` and asserting `StatusCode::BAD_REQUEST`.
