# Criterion 2: GET /api/v2/package?license=MIT,Apache-2.0 returns packages with either license

## Verdict: PASS

## Reasoning

The PR implements comma-separated multi-license filtering through the following code path:

1. **Comma splitting** (`list.rs`): The `validate_license_param` function splits the license parameter by comma: `license.split(',').map(|s| s.trim().to_string()).collect()`. For input `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`.

2. **Per-identifier validation** (`list.rs`): Each identifier is validated via `Expression::parse(id)`, ensuring both `MIT` and `Apache-2.0` are valid SPDX expressions before proceeding.

3. **OR-based filter** (`service/mod.rs`): The filter uses `Condition::any()` which produces an OR condition:
   ```rust
   Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))
   ```
   The `is_in` operator generates a SQL `IN ('MIT', 'Apache-2.0')` clause, which matches packages with either license. This correctly implements union semantics.

4. **Test verification** (`tests/api/package.rs`): The `test_list_packages_multi_license_filter` test seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses, requests `?license=MIT,Apache-2.0`, and asserts:
   - Response status is 200 OK
   - Result contains exactly 2 items (MIT and Apache-2.0 packages; GPL-3.0-only is excluded)
   - All returned items have `license == "MIT" || license == "Apache-2.0"`

The implementation correctly returns the union of packages matching any of the comma-separated license identifiers. The `is_in` operator naturally handles multiple values as an OR condition.
