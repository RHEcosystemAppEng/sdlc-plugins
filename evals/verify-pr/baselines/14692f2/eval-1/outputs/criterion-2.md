## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Verdict: PASS

### Analysis

**Code changes supporting this criterion:**

1. **Comma-separated parsing** (`modules/fundamental/src/package/endpoints/list.rs`):
   - The `validate_license_param` function splits the `license` parameter on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. For `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`. Each identifier is independently validated against the SPDX expression parser.

2. **OR-based filtering** (`modules/fundamental/src/package/service/mod.rs`):
   - The filter uses `Condition::any()` which creates an OR condition: `package_license::Column::License.is_in(licenses.iter().cloned())`. The `is_in` clause generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` query, which correctly returns packages matching either license.

3. **Test coverage** (`tests/api/package.rs`):
   - `test_list_packages_multi_license_filter` seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses. It queries with `?license=MIT,Apache-2.0` and asserts:
     - Status code is 200 OK
     - 2 items are returned (MIT and Apache-2.0, not GPL-3.0-only)
     - All returned items have either MIT or Apache-2.0 license

### Conclusion

The comma-separated license values are correctly split, validated individually, and used in an OR condition via `is_in`. The test confirms that multiple license values return the union of matching packages while excluding non-matching ones (GPL-3.0-only is excluded).
