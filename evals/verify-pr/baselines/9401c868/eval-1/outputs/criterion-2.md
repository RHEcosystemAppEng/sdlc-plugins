## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Result: PASS**

### Evidence

The PR supports comma-separated license values through the following mechanism:

1. **Comma splitting** (`modules/fundamental/src/package/endpoints/list.rs` -- `validate_license_param`): The function splits the raw license string by comma: `license.split(',').map(|s| s.trim().to_string()).collect()`. For `?license=MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`. Each identifier is individually validated via `spdx::Expression::parse(id)`.

2. **OR-based filtering** (`modules/fundamental/src/package/service/mod.rs`): The filter uses `Condition::any()` combined with `is_in(licenses.iter().cloned())`. The `is_in` operator generates a SQL `WHERE package_license.license IN ('MIT', 'Apache-2.0')` clause, which matches packages with either license. `Condition::any()` ensures this is an OR condition, returning the union of matching packages.

3. **Test coverage** (`tests/api/package.rs` -- `test_list_packages_multi_license_filter`): The test seeds three packages with distinct licenses (MIT, Apache-2.0, GPL-3.0-only), queries with `?license=MIT,Apache-2.0`, and asserts:
   - Response status is `200 OK`
   - Result contains exactly 2 items (MIT and Apache-2.0, but not GPL-3.0-only)
   - All returned items have a license of either `MIT` or `Apache-2.0`

The implementation correctly returns the union of packages matching any of the comma-separated license identifiers.
