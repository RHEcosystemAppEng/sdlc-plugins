# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

### Code Implementation Evidence

The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` validates each license identifier using `spdx::Expression::parse()`:

```rust
for id in &identifiers {
    Expression::parse(id).map_err(|_| {
        AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
    })?;
}
```

When `Expression::parse("INVALID-999")` fails (since "INVALID-999" is not a valid SPDX expression), the error is mapped to `AppError::BadRequest` with a descriptive message: `"Invalid SPDX license identifier: INVALID-999"`.

The `?` operator propagates this error up through the handler, which returns `Result<..., AppError>`. Per the repository's convention (documented in `common/src/error.rs`), `AppError::BadRequest` renders as an HTTP 400 response.

### Test Evidence

The test `test_list_packages_invalid_license_returns_400` verifies this behavior:
- Requests `GET /api/v2/package?license=INVALID-999`
- Asserts the response status is `StatusCode::BAD_REQUEST` (HTTP 400)

### Conclusion

The implementation correctly validates license identifiers against the SPDX specification and returns a 400 Bad Request response with a descriptive error message for invalid identifiers. The validation uses the `spdx` crate for authoritative validation. Criterion satisfied.
