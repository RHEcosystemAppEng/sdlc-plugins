# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict: MET (PASS)**

## Code evidence
- `modules/fundamental/src/package/endpoints/list.rs`: adds `pub license: Option<String>` to `PackageListParams`, so `Query<PackageListParams>` extracts the `license` query parameter (follows the `Query<FilterParams>` pattern from the advisory endpoint).
- `list_packages` handler: `let license_filter = match &params.license { Some(license) => Some(validate_license_param(license)?), None => None };` then passes `license_filter.as_deref()` to `PackageService::list`.
- `validate_license_param` splits on `,`, trims, validates each value, and returns `Vec<String>` (`["MIT"]` here).
- `modules/fundamental/src/package/service/mod.rs`: when a filter is present, applies `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))` and `query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def())`, restricting results to packages whose mapped license (via existing `entity/src/package_license.rs`) is in the set.

## Test evidence
`test_list_packages_single_license_filter` seeds pkg-a (MIT), pkg-b (Apache-2.0), pkg-c (MIT); requests `?license=MIT`; asserts status 200, `items.len() == 2`, and `items.iter().all(|p| p.license == "MIT")`.

## Reasoning
With a single value, the `IN` clause is an equality filter on the joined license column, so only MIT packages are returned. The test asserts both the count and that every item is MIT, excluding the Apache-2.0 package. Caveat: matching is exact string equality, so a package stored with a compound expression (e.g. `MIT OR Apache-2.0`) would not match — consistent with the criterion as written.
