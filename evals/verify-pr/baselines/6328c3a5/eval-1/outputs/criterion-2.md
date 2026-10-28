# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The implementation supports comma-separated license values and returns the union of matching packages.

**Endpoint layer** (`modules/fundamental/src/package/endpoints/list.rs`):
- The `validate_license_param` function splits the raw `license` string on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. For input `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`.
- Each identifier is validated individually via `Expression::parse(id)`, ensuring both `MIT` and `Apache-2.0` are valid SPDX identifiers before proceeding.

**Service layer** (`modules/fundamental/src/package/service/mod.rs`):
- The filter uses `Condition::any()` combined with `is_in(licenses.iter().cloned())`. The `is_in` clause generates `WHERE package_license.license IN ('MIT', 'Apache-2.0')`, which naturally returns the union of packages matching either license.
- The `Condition::any()` wrapper ensures OR semantics, which is correct for a union query.

**Test coverage** (`tests/api/package.rs`):
- The test `test_list_packages_multi_license_filter` seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (GPL-3.0-only). It then requests `GET /api/v2/package?license=MIT,Apache-2.0` and asserts:
  - Status is 200 OK
  - Exactly 2 items are returned (the MIT and Apache-2.0 packages, excluding GPL-3.0-only)
  - All returned items have license equal to `"MIT"` or `"Apache-2.0"`
- This directly validates the union behavior required by the criterion.
