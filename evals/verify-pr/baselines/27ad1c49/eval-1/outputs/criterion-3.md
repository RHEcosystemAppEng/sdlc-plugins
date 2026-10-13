# Criterion 3: GET /api/v2/package?license=INVALID-999 returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

### Validation Logic

The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` validates each license identifier by calling `spdx::Expression::parse(id)`. The `spdx` crate provides strict SPDX license expression parsing -- `"INVALID-999"` is not a recognized SPDX license identifier and will cause `Expression::parse` to return an error.

### Error Mapping

When `Expression::parse(id)` fails, the error is mapped to `AppError::BadRequest` with a descriptive message:

```rust
Expression::parse(id).map_err(|_| {
    AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
})?;
```

The `?` operator propagates this error immediately, short-circuiting the validation loop. This means the function returns the error before proceeding to any database query, which is efficient and correct.

### Error Response

The `AppError::BadRequest` variant (defined in `common/src/error.rs`, per the repository structure) implements `IntoResponse` for Axum, which converts it to an HTTP 400 Bad Request response. The error message `"Invalid SPDX license identifier: INVALID-999"` is included in the response body, fulfilling the "with an error message" requirement of the acceptance criterion.

### Handler Integration

In the `list_packages` handler, `validate_license_param` is called with the `?` operator:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

The `?` propagates the `AppError::BadRequest` to the handler's return type `Result<Json<...>, AppError>`, which Axum renders as the 400 response.

### Test Coverage

The test `test_list_packages_invalid_license_returns_400` validates this behavior:
- Requests `GET /api/v2/package?license=INVALID-999`
- Asserts `resp.status() == StatusCode::BAD_REQUEST`

This confirms that invalid SPDX identifiers are rejected with a 400 status code.

## Evidence

- `modules/fundamental/src/package/endpoints/list.rs`: `Expression::parse(id)` validates against SPDX spec
- `modules/fundamental/src/package/endpoints/list.rs`: `.map_err(|_| AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id)))` produces descriptive error
- `common/src/error.rs`: `AppError` enum implements `IntoResponse` (per repository conventions)
- `tests/api/package.rs`: `test_list_packages_invalid_license_returns_400` asserts `StatusCode::BAD_REQUEST`
