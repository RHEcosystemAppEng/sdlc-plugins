## Criterion 3

**Text:** `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### What was checked

1. The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` iterates over each license identifier and attempts to parse it with `Expression::parse(id)`.
2. On parse failure, it returns `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`, which produces a 400 status code with an error message containing the invalid identifier.
3. The `?` operator in the handler (`validate_license_param(license)?`) propagates the `AppError::BadRequest` as the endpoint response, short-circuiting before any database query.
4. The integration test `test_list_packages_invalid_license_returns_400` requests `?license=INVALID-999` and asserts the response status is `StatusCode::BAD_REQUEST`.

### Evidence

- `modules/fundamental/src/package/endpoints/list.rs`: `Expression::parse(id).map_err(|_| AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id)))?;` returns 400 with a descriptive message for invalid identifiers.
- `tests/api/package.rs` lines 46-53: `test_list_packages_invalid_license_returns_400` queries `?license=INVALID-999` and asserts `resp.status() == StatusCode::BAD_REQUEST`.

### Verdict: PASS
