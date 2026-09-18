# Criterion 2: GET /api/v2/package?license=MIT,Apache-2.0 returns packages with either license

## Verdict: PASS

## Analysis

This criterion requires that when the `license` query parameter contains comma-separated values, the endpoint returns packages matching any of the specified licenses (union/OR semantics).

### Code Changes

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**
- The `validate_license_param` function splits the input string on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`.
- For `?license=MIT,Apache-2.0`, this produces `vec!["MIT".to_string(), "Apache-2.0".to_string()]`.
- Each identifier is individually validated against SPDX via `Expression::parse(id)`.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**
- The filter uses `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))`.
- `Condition::any()` produces OR semantics, and `is_in` with multiple values generates `WHERE package_license.license IN ('MIT', 'Apache-2.0')`.
- This correctly returns the union of packages with either license.

### Test Coverage

**`tests/api/package.rs::test_list_packages_multi_license_filter`:**
- Seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (GPL-3.0-only).
- Queries `GET /api/v2/package?license=MIT,Apache-2.0`.
- Asserts response status is 200 OK.
- Asserts `body.items.len() == 2` (MIT and Apache-2.0 packages, excluding GPL-3.0-only).
- Asserts `body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0")` (confirms union semantics).

### Conclusion

The implementation correctly handles comma-separated license values by splitting, validating each, and using an IN clause with OR semantics. The test directly exercises the multi-license scenario and verifies that the union of matching packages is returned while non-matching packages are excluded.
