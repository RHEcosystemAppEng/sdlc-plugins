# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The PR diff demonstrates that this criterion is satisfied through both implementation code and test coverage.

### Implementation Evidence

1. **Comma-separated parsing** (`validate_license_param` in `list.rs`):
   - The function splits the `license` parameter by comma: `license.split(',').map(|s| s.trim().to_string()).collect()`.
   - For the input `"MIT,Apache-2.0"`, this produces `vec!["MIT", "Apache-2.0"]`.
   - Each identifier is individually validated via `Expression::parse`, ensuring both "MIT" and "Apache-2.0" are valid SPDX identifiers.

2. **OR-based filtering** (`PackageService::list` in `service/mod.rs`):
   - The filter uses `Condition::any()`, which produces a SQL `OR` condition.
   - `package_license::Column::License.is_in(licenses.iter().cloned())` generates a `WHERE license IN ('MIT', 'Apache-2.0')` clause.
   - Combined with the `InnerJoin` on `PackageLicense`, this correctly returns packages that have either MIT or Apache-2.0 as their license.

3. **Union semantics**:
   - `Condition::any()` with `is_in` provides union semantics (packages matching ANY of the provided licenses), which is the correct interpretation for comma-separated license values as specified in the task description.

### Test Evidence

The test `test_list_packages_multi_license_filter` in `tests/api/package.rs`:
- Seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (GPL-3.0-only).
- Sends `GET /api/v2/package?license=MIT,Apache-2.0`.
- Asserts the response status is 200 OK.
- Asserts the response body contains exactly 2 items (MIT and Apache-2.0, not GPL-3.0-only).
- Asserts all returned items have `license == "MIT" || license == "Apache-2.0"`.

This test directly validates the acceptance criterion by confirming that packages with either license are returned while packages with other licenses are excluded.

### Conclusion

The implementation correctly splits comma-separated license values, validates each independently, and applies an OR-based filter (`Condition::any()` with `is_in`) to return the union of matching packages. The integration test confirms this behavior with a three-license dataset.
