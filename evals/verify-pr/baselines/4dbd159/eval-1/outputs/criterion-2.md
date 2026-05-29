## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Verdict: PASS

### Evidence

**Endpoint layer** (`modules/fundamental/src/package/endpoints/list.rs`):
- `validate_license_param("MIT,Apache-2.0")` splits by comma and trims, producing `vec!["MIT", "Apache-2.0"]`.
- Each identifier is validated via `spdx::Expression::parse()`. Both "MIT" and "Apache-2.0" are valid SPDX identifiers, so validation passes.
- The resulting vector is passed to the service layer.

**Service layer** (`modules/fundamental/src/package/service/mod.rs`):
- `Condition::any()` with `is_in(licenses.iter().cloned())` generates SQL: `WHERE package_license.license IN ('MIT', 'Apache-2.0')`.
- `Condition::any()` is the correct choice here -- it produces an OR-style filter, meaning packages with *either* license will match. This implements the union semantics required by the criterion.

**Test coverage** (`tests/api/package.rs`):
- `test_list_packages_multi_license_filter` seeds 3 packages (MIT, Apache-2.0, GPL-3.0-only), requests `?license=MIT,Apache-2.0`, and asserts:
  - Status 200 OK
  - 2 items returned (MIT and Apache-2.0 packages, excluding GPL-3.0-only)
  - All items have license equal to "MIT" or "Apache-2.0"

The implementation correctly handles comma-separated license values and returns the union of matching packages.
