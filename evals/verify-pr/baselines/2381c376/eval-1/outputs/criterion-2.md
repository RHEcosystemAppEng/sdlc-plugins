## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Verdict: PASS

### Analysis

**Code evidence in the diff:**

1. **Comma splitting** (`list.rs`): The `validate_license_param` function splits the input on commas:
   ```rust
   let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
   ```
   For `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`.

2. **Per-identifier validation**: Each identifier is validated individually via `Expression::parse(id)`, so both `MIT` and `Apache-2.0` are checked.

3. **OR-based filtering** (`service/mod.rs`): The filter uses `Condition::any()` with `is_in()`:
   ```rust
   Condition::any()
       .add(package_license::Column::License.is_in(licenses.iter().cloned()))
   ```
   `is_in` with multiple values generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause, which returns the union of packages matching either license.

**Test evidence:**

The test `test_list_packages_multi_license_filter` in `tests/api/package.rs`:
- Seeds three packages: MIT, Apache-2.0, and GPL-3.0-only.
- Requests `GET /api/v2/package?license=MIT,Apache-2.0`.
- Asserts the response status is 200 OK.
- Asserts exactly 2 items are returned (MIT and Apache-2.0, not GPL-3.0-only).
- Asserts all returned items have license equal to either `MIT` or `Apache-2.0`.

This directly verifies the criterion.
