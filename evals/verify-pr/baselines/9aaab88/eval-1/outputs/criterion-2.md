## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict: PASS**

### Analysis

The `validate_license_param` function in `list.rs` splits the license parameter by comma (`license.split(',')`) and trims each value. Each identifier is independently validated against SPDX. The resulting `Vec<String>` (e.g., `["MIT", "Apache-2.0"]`) is passed to the service layer.

In `mod.rs`, the filter uses `Condition::any()` with `is_in(licenses.iter().cloned())`. The `Condition::any()` wrapper combined with `is_in` produces a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause, returning packages matching either license (union semantics).

### Test Coverage

The test `test_list_packages_multi_license_filter` in `tests/api/package.rs`:
- Seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses
- Queries `GET /api/v2/package?license=MIT,Apache-2.0`
- Asserts response status is 200 OK
- Asserts exactly 2 items returned (MIT and Apache-2.0, excluding GPL-3.0-only)
- Asserts all returned packages have license equal to "MIT" or "Apache-2.0"

This directly validates the union behavior for comma-separated license values.
