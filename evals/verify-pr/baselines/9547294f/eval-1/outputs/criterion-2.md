# Acceptance Criterion 2

**Criterion:** `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The implementation supports comma-separated license values and returns the union of matching packages:

1. **Comma splitting:** In `validate_license_param`, the license string is split by comma: `license.split(',').map(|s| s.trim().to_string()).collect()`. For `?license=MIT,Apache-2.0`, this produces `vec!["MIT", "Apache-2.0"]`.

2. **Individual validation:** Each identifier is validated against the SPDX expression parser in a loop: `for id in &identifiers { Expression::parse(id).map_err(...)? }`. Both `MIT` and `Apache-2.0` are valid SPDX identifiers and will pass validation.

3. **OR-semantics filter:** The service layer uses `Condition::any()` which generates an SQL OR condition:
   ```rust
   Condition::any()
       .add(package_license::Column::License.is_in(licenses.iter().cloned()))
   ```
   The `is_in` method with multiple values generates `license IN ('MIT', 'Apache-2.0')`, which returns packages with either license. The use of `Condition::any()` is semantically correct for union-style filtering.

4. **Test coverage:** The test `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), queries `?license=MIT,Apache-2.0`, and asserts:
   - Response status is 200 OK
   - Exactly 2 items returned (MIT and Apache-2.0, but not GPL-3.0-only)
   - All returned items have `license == "MIT" || license == "Apache-2.0"`

## Evidence

- `modules/fundamental/src/package/endpoints/list.rs`: `license.split(',').map(|s| s.trim().to_string()).collect()` handles comma separation
- `modules/fundamental/src/package/service/mod.rs`: `Condition::any().add(package_license::Column::License.is_in(...))` produces OR/IN semantics
- `tests/api/package.rs`: `test_list_packages_multi_license_filter` validates the union behavior
