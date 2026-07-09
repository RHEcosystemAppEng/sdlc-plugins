# Criterion 2: GET /api/v2/package?license=MIT,Apache-2.0 returns packages with either license

## Verdict: PASS

## Reasoning

This criterion requires that comma-separated license values are supported, returning the union of packages matching any of the specified licenses.

### Code Analysis

**Parsing (`modules/fundamental/src/package/endpoints/list.rs`):**

1. The `validate_license_param` function handles comma separation:
   ```rust
   let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
   ```
   For input `"MIT,Apache-2.0"`, this produces `vec!["MIT", "Apache-2.0"]`.

2. Each identifier is validated individually against SPDX:
   ```rust
   for id in &identifiers {
       Expression::parse(id).map_err(|_| {
           AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
       })?;
   }
   ```
   Both "MIT" and "Apache-2.0" are valid SPDX identifiers, so validation passes.

**Query building (`modules/fundamental/src/package/service/mod.rs`):**

3. The service layer uses `Condition::any()` with `is_in`:
   ```rust
   Condition::any()
       .add(package_license::Column::License.is_in(licenses.iter().cloned()))
   ```
   The `is_in` with `["MIT", "Apache-2.0"]` generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause, which returns packages with either license (union semantics).

4. The `Condition::any()` wrapper ensures OR semantics, which aligns with the "either license" requirement.

**Test coverage (`tests/api/package.rs`):**

5. The test `test_list_packages_multi_license_filter` validates this criterion:
   - Seeds packages: "pkg-a" (MIT), "pkg-b" (Apache-2.0), "pkg-c" (GPL-3.0-only)
   - Requests `GET /api/v2/package?license=MIT,Apache-2.0`
   - Asserts response status is 200 OK
   - Asserts `body.items.len() == 2` (MIT and Apache-2.0 packages, excluding GPL-3.0-only)
   - Asserts `body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0")` (correct union)

### Conclusion

The comma-splitting logic in `validate_license_param` correctly parses multiple identifiers. The `is_in` clause in the service layer implements union (OR) semantics. The integration test confirms that only packages matching any of the specified licenses are returned, while packages with other licenses are excluded.
