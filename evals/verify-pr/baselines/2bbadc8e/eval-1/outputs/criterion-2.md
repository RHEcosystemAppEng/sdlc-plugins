# Criterion 2: GET /api/v2/package?license=MIT,Apache-2.0 returns packages with either license

## Verdict: PASS

## Analysis

The PR implements comma-separated license filtering:

1. **Comma splitting** (`list.rs`): The `validate_license_param` function splits the license parameter by comma:
   ```rust
   let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
   ```
   Each identifier is individually validated against SPDX expressions.

2. **OR query** (`service/mod.rs`): The filter uses `Condition::any()` with `is_in()`:
   ```rust
   Condition::any()
       .add(package_license::Column::License.is_in(licenses.iter().cloned()))
   ```
   `is_in` generates a SQL `IN (...)` clause, which is semantically an OR — returning packages matching any of the provided license identifiers.

3. **Test verification** (`tests/api/package.rs`): The test `test_list_packages_multi_license_filter` seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses, then queries `?license=MIT,Apache-2.0`. It asserts:
   - Status is 200 OK
   - Exactly 2 items returned (MIT and Apache-2.0 packages)
   - All returned items have license equal to either "MIT" or "Apache-2.0"
   - The GPL-3.0-only package is excluded

The implementation correctly handles comma-separated license values and returns the union of matching packages.
