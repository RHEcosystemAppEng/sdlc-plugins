## Criterion 2

**Text:** `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Analysis

The comma-separated multi-license filter is handled through the following code path:

1. **Parsing** (`list.rs`): `validate_license_param` splits the raw string on commas:
   ```rust
   let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
   ```
   For `"MIT,Apache-2.0"`, this produces `["MIT", "Apache-2.0"]`. Each identifier is independently validated via `Expression::parse(id)`.

2. **OR filtering** (`service/mod.rs`): The service uses `Condition::any()` with `is_in`:
   ```rust
   Condition::any()
       .add(package_license::Column::License.is_in(licenses.iter().cloned()))
   ```
   `is_in` with `["MIT", "Apache-2.0"]` generates `WHERE license IN ('MIT', 'Apache-2.0')`, which is an OR (union) semantic -- a package is included if its license matches any of the specified values.

3. **Test coverage** (`tests/api/package.rs`): `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), queries `?license=MIT,Apache-2.0`, and asserts:
   - Response status is 200 OK
   - Exactly 2 items returned (MIT and Apache-2.0; GPL-3.0-only excluded)
   - All returned items have `license == "MIT"` or `license == "Apache-2.0"`

### Verdict: PASS

The implementation correctly parses comma-separated license identifiers, validates each one, and applies an OR-based filter. The test covers this exact multi-license scenario with correct assertions.
