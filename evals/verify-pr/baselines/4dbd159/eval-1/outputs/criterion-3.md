## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Verdict: PASS

### Evidence

**Endpoint layer** (`modules/fundamental/src/package/endpoints/list.rs`):
- `validate_license_param("INVALID-999")` attempts `spdx::Expression::parse("INVALID-999")`.
- "INVALID-999" is not a valid SPDX license identifier, so `Expression::parse` returns an error.
- The error is mapped via `.map_err(|_| AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id)))`, which returns a 400 Bad Request response.
- The `?` operator propagates this error, causing the handler to short-circuit and return the 400 response before any database query is executed.
- The error message includes the specific invalid identifier, satisfying the "with an error message" part of the criterion.

**Test coverage** (`tests/api/package.rs`):
- `test_list_packages_invalid_license_returns_400` requests `?license=INVALID-999` and asserts:
  - `resp.status() == StatusCode::BAD_REQUEST`

The implementation correctly validates SPDX identifiers and returns 400 Bad Request with a descriptive error message for invalid values.
