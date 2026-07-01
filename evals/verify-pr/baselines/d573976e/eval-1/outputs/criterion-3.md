# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The implementation correctly validates license identifiers against the SPDX standard and returns a 400 Bad Request with a descriptive error message for invalid values.

### 1. SPDX Validation

In `modules/fundamental/src/package/endpoints/list.rs`, the `validate_license_param` function uses the `spdx` crate's `Expression::parse()` to validate each identifier:

```rust
for id in &identifiers {
    Expression::parse(id).map_err(|_| {
        AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
    })?;
}
```

For `"INVALID-999"`, `Expression::parse("INVALID-999")` returns an `Err` because `INVALID-999` is not a recognized SPDX license identifier. This error is mapped to `AppError::BadRequest` with the message `"Invalid SPDX license identifier: INVALID-999"`.

### 2. Error Propagation

The handler calls `validate_license_param(license)?` with the `?` operator, which propagates the `AppError::BadRequest` up to the handler's return type `Result<Json<PaginatedResults<PackageSummary>>, AppError>`. Since `AppError` implements `IntoResponse` (as documented in the repository's `common/src/error.rs`), Axum converts this to a 400 Bad Request HTTP response with the error message in the body.

### 3. Error Message Included

The criterion specifies "returns 400 Bad Request with an error message." The implementation includes a descriptive message via `format!("Invalid SPDX license identifier: {}", id)`, satisfying the error message requirement. This tells the consumer exactly which identifier was invalid, which is useful when multiple comma-separated values are provided.

### 4. Test Coverage

The test `test_list_packages_invalid_license_returns_400` in `tests/api/package.rs` directly verifies this criterion:
- Queries `GET /api/v2/package?license=INVALID-999`
- Asserts `resp.status() == StatusCode::BAD_REQUEST`

This confirms the 400 status code is returned for invalid SPDX identifiers.
