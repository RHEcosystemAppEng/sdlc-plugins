## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Result: PASS**

### Evidence

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

When `Expression::parse(id)` fails for an invalid identifier like "INVALID-999", it returns an `AppError::BadRequest` with a descriptive error message including the invalid identifier. The `?` operator causes early return from the handler with this error, which (per the repository conventions and `common/src/error.rs`) is rendered as an HTTP 400 Bad Request response.

The integration test `test_list_packages_invalid_license_returns_400` confirms this:

```rust
let resp = ctx.get("/api/v2/package?license=INVALID-999").await;
assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
```

Both the implementation and the test verify that invalid SPDX license identifiers produce a 400 response with an error message.
