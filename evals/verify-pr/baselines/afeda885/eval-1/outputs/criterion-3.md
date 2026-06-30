## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict: PASS**

### Reasoning

The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` validates each license identifier by parsing it as an SPDX expression:

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

When `INVALID-999` is provided, `Expression::parse("INVALID-999")` will fail because it is not a valid SPDX license identifier. The error is mapped to `AppError::BadRequest` with a descriptive error message: `"Invalid SPDX license identifier: INVALID-999"`. The `?` operator causes the handler to return this error immediately, which Axum converts to a 400 Bad Request HTTP response (as defined by the `AppError` enum in `common/src/error.rs` per the repository structure).

The integration test `test_list_packages_invalid_license_returns_400` in `tests/api/package.rs` directly verifies this behavior by requesting with `license=INVALID-999` and asserting `StatusCode::BAD_REQUEST`.

This criterion is satisfied by both the implementation and test coverage.
