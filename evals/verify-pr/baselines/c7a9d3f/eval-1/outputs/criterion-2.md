# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The PR implements comma-separated multi-license filtering through the following mechanism:

### Parsing and Validation (`modules/fundamental/src/package/endpoints/list.rs`)

1. **Comma splitting:** The `validate_license_param` function receives the raw string `"MIT,Apache-2.0"` and splits it on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. This produces `vec!["MIT", "Apache-2.0"]`.

2. **Per-identifier validation:** Each identifier is validated individually with `Expression::parse(id)`. Both "MIT" and "Apache-2.0" are valid SPDX identifiers, so both pass validation.

3. **Result:** The function returns `Ok(vec!["MIT".to_string(), "Apache-2.0".to_string()])`.

### OR-based Filtering (`modules/fundamental/src/package/service/mod.rs`)

4. **Condition::any():** The service uses `Condition::any()` which generates a SQL `OR` clause. The `.add(package_license::Column::License.is_in(licenses.iter().cloned()))` creates an `IN ('MIT', 'Apache-2.0')` SQL condition.

5. **Union semantics:** The `IN` clause naturally provides union semantics -- a package matches if its license is MIT OR Apache-2.0. This is exactly the "either license" behavior required by the criterion.

6. **Inner join:** The `InnerJoin` on `PackageLicense` ensures only packages that have an entry in the `package_license` table with a matching license are returned.

### Test Coverage

The test `test_list_packages_multi_license_filter` directly exercises this criterion:
- Seeds 3 packages: pkg-a (MIT), pkg-b (Apache-2.0), pkg-c (GPL-3.0-only)
- Requests `GET /api/v2/package?license=MIT,Apache-2.0`
- Asserts response status is 200 OK
- Asserts exactly 2 items returned (MIT and Apache-2.0, not GPL-3.0-only)
- Asserts all returned items have license "MIT" or "Apache-2.0"

This confirms the union/OR filtering behavior works as specified.
