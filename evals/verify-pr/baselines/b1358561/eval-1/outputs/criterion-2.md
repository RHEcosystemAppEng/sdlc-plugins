# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict: MET (PASS)**

## Code evidence
- `modules/fundamental/src/package/endpoints/list.rs` — `validate_license_param`: `license.split(',').map(|s| s.trim().to_string()).collect()` parses `MIT,Apache-2.0` into `["MIT", "Apache-2.0"]` (whitespace after commas is tolerated). Each value is validated individually.
- `modules/fundamental/src/package/service/mod.rs`: `Condition::any().add(package_license::Column::License.is_in(...))` produces `license IN ('MIT', 'Apache-2.0')` — OR/union semantics.

## Test evidence
`test_list_packages_multi_license_filter` seeds MIT, Apache-2.0, and GPL-3.0-only packages; requests `?license=MIT,Apache-2.0`; asserts status 200, `items.len() == 2`, and every item is MIT or Apache-2.0 (GPL package excluded).

## Reasoning
The `IN` clause yields the union of both licenses, satisfying "either license". The test verifies inclusion of both and exclusion of a third license. Caveat (non-blocking): the `InnerJoin` without `DISTINCT` means a package with multiple matching `package_license` rows could appear twice; test data uses one license per package, so this is not exercised. The specified behavior is met.
