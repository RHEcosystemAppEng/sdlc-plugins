# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict: PASS**

## Code that implements it

In `modules/fundamental/src/package/endpoints/list.rs`, each identifier is parsed with the `spdx` crate. A parse failure becomes a `BadRequest` that carries a message:
```rust
Expression::parse(id).map_err(|_| {
    AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
})?;
```
The handler calls `validate_license_param(license)?` before it calls the service. An invalid value therefore short-circuits with `AppError::BadRequest` and no database query runs. The repo structure says `AppError` (in `common/src/error.rs`) implements `IntoResponse`, so `BadRequest` becomes an HTTP 400 response with the message `Invalid SPDX license identifier: INVALID-999`.

This follows the Implementation Note: "Validate license identifiers against a known SPDX license list before querying; return `AppError::BadRequest` for invalid values".

## Test coverage

`tests/api/package.rs::test_list_packages_invalid_license_returns_400` calls `?license=INVALID-999` and asserts `resp.status() == StatusCode::BAD_REQUEST`. This matches the test requirement "invalid license identifier returns 400 status code".

## Caveats (non-blocking)

- The test checks the status code but not the error message in the body. The message comes from the code alone (the `format!` above); no test covers it.
- `Expression::parse` accepts full SPDX expressions (for example `MIT OR Apache-2.0`) and `LicenseRef-*` terms, so it is more lenient than a strict "known identifier" list. `INVALID-999` is not a known SPDX license and is still rejected, so the criterion is met.
