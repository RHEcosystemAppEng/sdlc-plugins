# Criterion 2: GET /api/v2/package?license=MIT,Apache-2.0 returns packages with either license

## Verdict: PASS

## Analysis

### Code Changes

The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` splits the `license` parameter on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. This means `?license=MIT,Apache-2.0` produces the vector `["MIT", "Apache-2.0"]`.

Each identifier is individually validated via `Expression::parse(id)`, ensuring both `MIT` and `Apache-2.0` are valid SPDX expressions before the query executes.

In `modules/fundamental/src/package/service/mod.rs`, the filter uses `Condition::any()` with `.add(package_license::Column::License.is_in(licenses.iter().cloned()))`. The `Condition::any()` combined with `is_in` produces an SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause, which returns the union of packages matching either license. This is correct OR semantics.

### Test Coverage

The test `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), sends `GET /api/v2/package?license=MIT,Apache-2.0`, and asserts:
- Response status is 200 OK
- Result count is 2
- All returned items have license equal to either `"MIT"` or `"Apache-2.0"`

The GPL-3.0-only package is excluded from the results, confirming that only matching licenses are returned.

### Conclusion

The comma-separated parsing, per-identifier validation, and `is_in` filter with `Condition::any()` correctly implement union semantics for multiple license values. The test verifies the behavior with three licenses in the database and a two-value filter.
