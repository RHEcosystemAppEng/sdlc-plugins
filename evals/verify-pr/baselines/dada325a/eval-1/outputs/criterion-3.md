# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict: PASS**

## Reasoning

- **Validation:** `validate_license_param` calls `spdx::Expression::parse(id)` for each identifier. `INVALID-999` is not a valid SPDX identifier, so the parse fails.
- **Error mapping:** the parse error becomes `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`. That is the variant the Implementation Notes ask for, and it carries a readable message that names the bad value.
- **Early return:** the handler uses `?` on `validate_license_param(license)`, so the error returns before any database query runs.
- **HTTP mapping:** `AppError` implements `IntoResponse` (`common/src/error.rs`), and `BadRequest` maps to HTTP 400 with the message in the body.

## Test evidence

`test_list_packages_invalid_license_returns_400` requests `?license=INVALID-999` and asserts `StatusCode::BAD_REQUEST`.

## Observation (non-blocking)

The test checks the status code but not the error message text. The message is confirmed by reading the code (the `format!` string), not by a test. A body assertion would make the test stronger, but the criterion is met.

## Conclusion

Invalid identifiers produce a 400 Bad Request that includes an error message. The criterion is satisfied.
