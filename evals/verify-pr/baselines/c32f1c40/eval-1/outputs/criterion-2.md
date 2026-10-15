# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Analysis

This criterion requires that comma-separated license values in the query parameter return the union of packages matching any of the specified licenses.

### Implementation Evidence

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**
- `validate_license_param` splits the `license` parameter on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`.
- For `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`.
- Each identifier is individually validated with `spdx::Expression::parse(id)`, ensuring both are valid SPDX identifiers.
- The full vector is passed to the service layer.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**
- The filter uses `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))`.
- `Condition::any()` generates an OR-based condition, and `is_in` with `["MIT", "Apache-2.0"]` produces `WHERE package_license.license IN ('MIT', 'Apache-2.0')`.
- This correctly returns the union of packages matching either license.

**Test coverage (`tests/api/package.rs`):**
- `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), queries `?license=MIT,Apache-2.0`, and asserts:
  - Status is 200 OK
  - `body.items.len() == 2` (MIT and Apache-2.0 packages, excluding GPL-3.0-only)
  - `body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0")` (all returned packages match one of the two licenses)

### Conclusion

The comma-separated license handling is implemented through string splitting in the validation layer and SQL `IN` clause generation in the service layer. The test confirms that the union of matching packages is returned while non-matching packages are excluded.
