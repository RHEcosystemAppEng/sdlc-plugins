# Acceptance Criterion 3: Invalid License Returns 400

**Criterion**: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict**: PASS

## Evidence from Diff

### SPDX Validation

The `validate_license_param` function in `list.rs` validates each license identifier using the `spdx` crate's `Expression::parse`:

```rust
for id in &identifiers {
    Expression::parse(id).map_err(|_| {
        AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
    })?;
}
```

`INVALID-999` is not a recognized SPDX license identifier, so `Expression::parse("INVALID-999")` will return an `Err`. This error is mapped to `AppError::BadRequest` with a descriptive message: `"Invalid SPDX license identifier: INVALID-999"`.

### Error Propagation

The handler uses the `?` operator on the validation result:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

When `validate_license_param` returns `Err(AppError::BadRequest(...))`, the `?` operator short-circuits the handler and returns the error. Since the repository uses `AppError` which implements `IntoResponse` (per `common/src/error.rs`), this converts to a 400 Bad Request HTTP response with the error message in the body.

### Test Coverage

The test `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts:

```rust
assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
```

This directly validates that invalid SPDX identifiers produce a 400 response. The error message content is ensured by the `format!("Invalid SPDX license identifier: {}", id)` in the validation function.
