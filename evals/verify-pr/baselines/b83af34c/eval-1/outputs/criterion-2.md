# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Analysis

### Code Changes Supporting This Criterion

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**

1. The `validate_license_param` function handles comma-separated values by splitting on commas and trimming whitespace:
   ```rust
   let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
   ```
   For input `"MIT,Apache-2.0"`, this produces `["MIT", "Apache-2.0"]`.

2. Each identifier is individually validated against the SPDX expression parser, ensuring both `MIT` and `Apache-2.0` are valid SPDX identifiers before proceeding.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**

3. The `is_in` filter receives the full list of license identifiers:
   ```rust
   Condition::any()
       .add(package_license::Column::License.is_in(licenses.iter().cloned()))
   ```
   `Condition::any()` combined with `is_in(["MIT", "Apache-2.0"])` generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause, which returns packages matching either license (a union/OR semantic).

### Test Coverage

The test `test_list_packages_multi_license_filter` directly verifies this criterion:
- Seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (GPL-3.0-only)
- Queries `GET /api/v2/package?license=MIT,Apache-2.0`
- Asserts response status is 200 OK
- Asserts exactly 2 items are returned (MIT and Apache-2.0, excluding GPL-3.0-only)
- Asserts all returned items have either MIT or Apache-2.0 license

This confirms that the comma-separated syntax produces a union of matching packages and excludes non-matching packages.

### Conclusion

The comma-splitting logic in `validate_license_param` combined with `is_in` on the SeaORM query correctly implements multi-license filtering with OR semantics. The test verifies the behavior with three distinct licenses, confirming the union behavior. Criterion is satisfied.
