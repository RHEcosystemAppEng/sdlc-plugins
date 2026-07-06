# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The PR implements comma-separated multi-license filtering through the following mechanism:

1. **Comma splitting** (`list.rs`): The `validate_license_param` function splits the input string on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. For `"MIT,Apache-2.0"`, this produces `["MIT", "Apache-2.0"]`. The `.trim()` call handles optional whitespace around identifiers.

2. **Per-identifier validation** (`list.rs`): Each identifier is validated individually against the SPDX parser (`Expression::parse(id)`). Both "MIT" and "Apache-2.0" are valid SPDX identifiers, so validation passes for both.

3. **OR-based database filtering** (`service/mod.rs`): The service uses `Condition::any()` with `is_in(licenses.iter().cloned())`, which generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause. The `Condition::any()` ensures packages matching ANY of the specified licenses are returned (union semantics).

4. **Test coverage** (`tests/api/package.rs`): The `test_list_packages_multi_license_filter` test seeds three packages (MIT, Apache-2.0, GPL-3.0-only), queries `?license=MIT,Apache-2.0`, and asserts:
   - Response status is 200 OK
   - Exactly 2 items are returned (MIT and Apache-2.0, excluding GPL-3.0-only)
   - All returned items have license equal to either "MIT" or "Apache-2.0"

The implementation correctly returns the union of packages matching any of the comma-separated license identifiers.
