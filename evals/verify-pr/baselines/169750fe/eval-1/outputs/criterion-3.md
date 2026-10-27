# Criterion 3: Invalid License Returns 400

**Criterion:** `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict:** PASS

## Evidence

The `validate_license_param` function in `list.rs` validates each license identifier using the `spdx` crate's `Expression::parse`:

```rust
Expression::parse(id).map_err(|_| {
    AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
})?;
```

When `Expression::parse` fails for an invalid identifier like `INVALID-999`, it returns an error that is mapped to `AppError::BadRequest` with a descriptive message. The `?` operator propagates this error, causing the handler to return a 400 Bad Request response before any database query is executed.

This follows the project's established error handling pattern where all handlers return `Result<T, AppError>` and `AppError` implements `IntoResponse` (as documented in `common/src/error.rs`).

The integration test `test_list_packages_invalid_license_returns_400` confirms this: it sends a request with `?license=INVALID-999` and asserts `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)`.

**Conclusion:** The implementation correctly validates license identifiers and returns 400 Bad Request with an error message for invalid SPDX identifiers.
