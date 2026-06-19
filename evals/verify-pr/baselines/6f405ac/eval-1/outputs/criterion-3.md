# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The `validate_license_param` function validates each license identifier by attempting to parse it as an SPDX expression:

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

When `Expression::parse(id)` fails (as it would for `INVALID-999`, which is not a recognized SPDX identifier), the error is mapped to `AppError::BadRequest` with a descriptive message: `"Invalid SPDX license identifier: INVALID-999"`. The `?` operator causes the function to return early with this error, which the Axum framework translates into a 400 HTTP response (per the `AppError` `IntoResponse` implementation in `common/src/error.rs`).

The handler calls validation before querying:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

The `?` propagates the `AppError::BadRequest` to the handler's return type `Result<Json<...>, AppError>`, so the error response is returned directly without executing the database query.

The integration test `test_list_packages_invalid_license_returns_400` confirms this by sending `?license=INVALID-999` and asserting `StatusCode::BAD_REQUEST`.

## Evidence

- `list.rs`: `Expression::parse(id)` validates against SPDX standard
- `list.rs`: `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))` provides error message
- `list.rs`: Early return via `?` prevents database query on invalid input
- `common/src/error.rs`: `AppError` implements `IntoResponse` (per repo conventions, translates `BadRequest` to HTTP 400)
- `tests/api/package.rs`: `test_list_packages_invalid_license_returns_400` asserts `StatusCode::BAD_REQUEST`
