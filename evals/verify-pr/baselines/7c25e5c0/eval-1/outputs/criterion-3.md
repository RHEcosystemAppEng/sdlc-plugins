# Criterion 3: Invalid License Returns 400

**Criterion:** `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict: PASS**

## What was checked

Inspected the PR diff for:
1. Validation of license identifiers against SPDX
2. Error response for invalid identifiers
3. Test coverage for the 400 response

## Code-level evidence

### SPDX validation (list.rs)

`validate_license_param` validates each identifier using `spdx::Expression::parse`:
```rust
Expression::parse(id).map_err(|_| {
    AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
})?;
```

When `INVALID-999` is passed, `Expression::parse` fails (it is not a recognized SPDX identifier), and `map_err` converts the error to `AppError::BadRequest` with a descriptive message including the invalid identifier.

### Error propagation (list.rs)

The `?` operator in `validate_license_param` propagates the `AppError::BadRequest` up through `list_packages`, which has the return type `Result<Json<PaginatedResults<PackageSummary>>, AppError>`. The `AppError` enum implements `IntoResponse` (per `common/src/error.rs` noted in the repo structure), converting `BadRequest` to an HTTP 400 response.

### Test coverage (tests/api/package.rs)

`test_list_packages_invalid_license_returns_400` queries with an invalid license and asserts:
```rust
let resp = ctx.get("/api/v2/package?license=INVALID-999").await;
assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
```

This confirms a 400 status code is returned for invalid SPDX identifiers.
