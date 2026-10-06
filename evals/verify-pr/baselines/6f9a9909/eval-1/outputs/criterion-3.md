## Criterion 3

**Text:** `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**What was checked:**

1. The `validate_license_param` function iterates over each identifier and calls `Expression::parse(id)`. For an invalid SPDX identifier like `INVALID-999`, the parse fails.
2. The error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`, which produces a 400 status code with a descriptive error message.
3. The `list_packages` handler calls `validate_license_param` with the early-return `?` operator, so validation failure short-circuits before any database query.
4. The integration test `test_list_packages_invalid_license_returns_400` sends `?license=INVALID-999` and asserts `StatusCode::BAD_REQUEST`.

**Code evidence:**

From `list.rs`:
```rust
Expression::parse(id).map_err(|_| {
    AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
})?;
```

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

From `tests/api/package.rs`:
```rust
let resp = ctx.get("/api/v2/package?license=INVALID-999").await;
assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
```

**Verdict:** PASS
