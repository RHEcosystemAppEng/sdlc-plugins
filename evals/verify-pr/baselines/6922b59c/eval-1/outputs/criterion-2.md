# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The diff satisfies this criterion through both implementation and testing.

**Implementation**: In `validate_license_param()` (in `list.rs`), the license string is split by commas (`license.split(',')`) and each identifier is trimmed and validated individually. For `MIT,Apache-2.0`, this produces a two-element vector `["MIT", "Apache-2.0"]`. Each is validated against `spdx::Expression::parse()`.

In the service layer (`mod.rs`), the filter uses `Condition::any()` with `is_in(licenses.iter().cloned())`, which translates to a SQL `WHERE package_license.license IN ('MIT', 'Apache-2.0')`. The `Condition::any()` combined with `is_in` provides union semantics -- packages matching any of the listed licenses are returned.

**Test coverage**: The test `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), queries `?license=MIT,Apache-2.0`, and asserts:
- Response status is 200 OK
- Exactly 2 items are returned
- All returned items have either `license == "MIT"` or `license == "Apache-2.0"`

The GPL-3.0-only package is correctly excluded, confirming union semantics work as expected.
