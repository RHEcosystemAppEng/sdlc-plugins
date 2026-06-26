# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The implementation satisfies this criterion through comma-separated license parsing and OR-based query filtering:

1. **Comma splitting**: The `validate_license_param` function splits the input on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. For `"MIT,Apache-2.0"`, this produces `["MIT", "Apache-2.0"]`. The `.trim()` call handles optional whitespace around identifiers.

2. **Per-identifier validation**: Each identifier in the split list is validated individually via `spdx::Expression::parse(id)`. Both `"MIT"` and `"Apache-2.0"` are valid SPDX identifiers, so validation passes.

3. **OR filtering**: The service layer uses `Condition::any()` with `is_in(licenses.iter().cloned())`, which generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause. The `Condition::any()` ensures OR semantics -- packages matching any of the specified licenses are included.

4. **Test coverage**: `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), filters by `?license=MIT,Apache-2.0`, and asserts:
   - Response status is 200 OK
   - Exactly 2 items returned (MIT and Apache-2.0, not GPL-3.0-only)
   - All returned items have license matching either `"MIT"` or `"Apache-2.0"`

The implementation correctly handles multiple comma-separated license values and returns the union of matching packages.
