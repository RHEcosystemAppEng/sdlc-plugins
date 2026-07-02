## Criterion 2

**Text:** `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### What was checked

1. The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` splits the `license` query parameter on commas (`license.split(',')`) and trims each value, producing a `Vec<String>` of individual identifiers.
2. Each identifier is validated via `Expression::parse(id)`, so both `"MIT"` and `"Apache-2.0"` are validated independently.
3. The resulting vector is passed to `PackageService::list` as `license_filter: Option<&[String]>`.
4. In `modules/fundamental/src/package/service/mod.rs`, the filter uses `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))`. The `is_in` clause with multiple values produces a SQL `IN ('MIT', 'Apache-2.0')` condition, returning the union of packages matching either license. `Condition::any()` ensures OR semantics.
5. The integration test `test_list_packages_multi_license_filter` seeds three packages with MIT, Apache-2.0, and GPL-3.0-only licenses, queries `?license=MIT,Apache-2.0`, and asserts exactly 2 items are returned with licenses being either MIT or Apache-2.0.

### Evidence

- `modules/fundamental/src/package/endpoints/list.rs`: `license.split(',').map(|s| s.trim().to_string()).collect()` produces multiple identifiers from comma-separated input.
- `modules/fundamental/src/package/service/mod.rs`: `is_in(licenses.iter().cloned())` matches any of the provided license values.
- `tests/api/package.rs` lines 27-44: `test_list_packages_multi_license_filter` seeds MIT, Apache-2.0, and GPL-3.0-only packages, queries `?license=MIT,Apache-2.0`, asserts `body.items.len() == 2` and all items have license `"MIT"` or `"Apache-2.0"`.

### Verdict: PASS
