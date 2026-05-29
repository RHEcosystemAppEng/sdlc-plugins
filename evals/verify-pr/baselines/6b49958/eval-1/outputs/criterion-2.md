## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict: PASS**

### Evidence

The comma-separated license filtering is implemented through the validation and query pipeline:

1. **`modules/fundamental/src/package/endpoints/list.rs`**: The `validate_license_param()` function splits the input on commas (`license.split(',').map(|s| s.trim().to_string()).collect()`), producing a `Vec<String>` of individual identifiers. For `license=MIT,Apache-2.0`, this yields `["MIT", "Apache-2.0"]`. Each identifier is validated against SPDX expressions.

2. **`modules/fundamental/src/package/service/mod.rs`**: The `license_filter` slice (e.g., `["MIT", "Apache-2.0"]`) is passed to `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))`. The `is_in` clause with `Condition::any()` produces a SQL `WHERE license IN ('MIT', 'Apache-2.0')` condition, which returns the union of packages matching either license.

3. **`tests/api/package.rs`**: The test `test_list_packages_multi_license_filter` seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses, queries `?license=MIT,Apache-2.0`, and asserts:
   - Response status is 200 OK
   - Exactly 2 items returned (MIT and Apache-2.0 packages; GPL-3.0-only excluded)
   - All returned items have license equal to either "MIT" or "Apache-2.0"

The implementation correctly handles comma-separated values and returns the union of matching packages.
