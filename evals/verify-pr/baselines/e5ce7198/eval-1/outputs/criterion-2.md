## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Verdict: PASS

### Evidence

**Endpoint implementation (list.rs):**
- The `validate_license_param` function splits the `license` query parameter by comma: `license.split(',').map(|s| s.trim().to_string()).collect()`. For `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`.
- Each identifier is individually validated via `spdx::Expression::parse`, so both `MIT` and `Apache-2.0` must be valid SPDX identifiers.

**Service implementation (service/mod.rs):**
- The filter uses `Condition::any()` with `.is_in(licenses.iter().cloned())`. `Condition::any()` produces an OR-based condition, and `is_in` generates `WHERE license IN ('MIT', 'Apache-2.0')`. This returns the union of packages matching either license.

**Test coverage (tests/api/package.rs):**
- `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), queries `?license=MIT,Apache-2.0`, and asserts:
  - Status is 200 OK
  - Exactly 2 items returned (MIT and Apache-2.0, excluding GPL-3.0-only)
  - All returned items have license equal to either `MIT` or `Apache-2.0`

This test directly validates the criterion. The implementation correctly returns the union of packages matching any of the comma-separated license identifiers.
