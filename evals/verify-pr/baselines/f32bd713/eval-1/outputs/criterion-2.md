## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Verdict: PASS

### Reasoning

The PR implements comma-separated multi-license filtering through the following mechanism:

1. **Comma splitting:** The `validate_license_param` function in `list.rs` splits the license parameter on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. For `?license=MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`.

2. **Per-identifier validation:** Each split identifier is validated individually via `Expression::parse(id)`, ensuring both "MIT" and "Apache-2.0" are valid SPDX identifiers before querying.

3. **OR semantics via `is_in`:** The service layer uses `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))`. The `is_in` method generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause, which returns packages matching any of the specified licenses (union/OR semantics). The `Condition::any()` wrapper ensures OR behavior if additional conditions were added.

4. **Test coverage:** The `test_list_packages_multi_license_filter` integration test directly verifies this criterion:
   - Seeds three packages with MIT, Apache-2.0, and GPL-3.0-only licenses
   - Sends `GET /api/v2/package?license=MIT,Apache-2.0`
   - Asserts response status is 200 OK
   - Asserts exactly 2 items are returned (MIT and Apache-2.0, not GPL-3.0-only)
   - Asserts all returned items have either MIT or Apache-2.0 license

### Evidence

- `list.rs`: `license.split(',').map(|s| s.trim().to_string()).collect()` handles comma separation
- `mod.rs`: `package_license::Column::License.is_in(licenses.iter().cloned())` produces SQL IN clause for union semantics
- Test: `test_list_packages_multi_license_filter` verifies multi-value filtering with assertion `body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0")`
