## Acceptance Criterion 3

**Criterion**: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict**: PASS

### Evidence

**Validation logic** (`modules/fundamental/src/package/endpoints/list.rs`):
The `validate_license_param` function validates each license identifier against the SPDX specification:
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
For input `"INVALID-999"`, `spdx::Expression::parse("INVALID-999")` returns an `Err` since "INVALID-999" is not a recognized SPDX license identifier. The `map_err` converts this to `AppError::BadRequest` with a descriptive message: `"Invalid SPDX license identifier: INVALID-999"`. The `?` operator propagates this error immediately, causing the handler to return a 400 Bad Request response.

**Error propagation in handler** (`modules/fundamental/src/package/endpoints/list.rs`):
```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```
The `?` operator on `validate_license_param(license)?` short-circuits the handler, returning the `AppError::BadRequest` before any database query is executed.

**Test coverage** (`tests/api/package.rs`):
`test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts:
- `resp.status()` equals `StatusCode::BAD_REQUEST` (400)
