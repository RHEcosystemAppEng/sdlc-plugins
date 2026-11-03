# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict: PASS**

## Reasoning

1. **Validation before query** — `list_packages` calls `validate_license_param(license)?` before touching the database, matching the Implementation Note "validate license identifiers against a known SPDX license list before querying".
2. **Rejection of unknown identifiers** — each identifier is checked with `spdx::Expression::parse(id)`. In its default (strict) mode the `spdx` crate only accepts identifiers from the SPDX license list, so `INVALID-999` fails to parse.
3. **Error mapping** — the parse error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))` and propagated via `?`. Per the repository conventions, `AppError` (in `common/src/error.rs`) implements `IntoResponse`, and the `BadRequest` variant produces HTTP 400. The response therefore carries the status 400 and a descriptive error message naming the offending identifier — satisfying "with an error message".
4. **Mixed lists** — because validation iterates over every identifier, `?license=MIT,INVALID-999` also fails with 400 (no partial results).
5. **Test evidence** — `test_list_packages_invalid_license_returns_400` requests `?license=INVALID-999` and asserts `StatusCode::BAD_REQUEST`.

## Notes (informational)
- The test asserts on the status code only, not on the error-message body. The message is clearly produced in code (`"Invalid SPDX license identifier: ..."`), so the criterion is met; asserting on the body would be a nice-to-have.
