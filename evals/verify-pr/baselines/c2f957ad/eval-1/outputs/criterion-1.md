# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict: PASS**

## Reasoning
- **Parameter parsing:** `modules/fundamental/src/package/endpoints/list.rs` adds `pub license: Option<String>` to `PackageListParams`. That struct is extracted through the existing `Query<PackageListParams>`, so `?license=MIT` is deserialized.
- **Validation:** when `params.license` is `Some`, it is passed to `validate_license_param`. That function splits on `,` and trims each value (`"MIT"` becomes `["MIT"]`), then checks each value with `spdx::Expression::parse`. `MIT` is a valid SPDX identifier.
- **Service call:** the validated list is passed as `license_filter.as_deref()` to `PackageService::list(offset, limit, license_filter)`.
- **Query filter:** `modules/fundamental/src/package/service/mod.rs` adds two things when `license_filter` is `Some`:
  - `query.filter(Condition::any().add(package_license::Column::License.is_in(licenses...)))`
  - `query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def())`

  The inner join plus the `IN ('MIT')` condition means only packages with an MIT license row are returned. The `entity/src/package_license.rs` mapping entity exists in the repository.
- **Test:** `test_list_packages_single_license_filter` seeds pkg-a (MIT), pkg-b (Apache-2.0) and pkg-c (MIT). It requests `?license=MIT` and asserts status 200, `items.len() == 2`, and that every item has `license == "MIT"`.

## Notes
- This was verified statically from the diff. No Serena instance was available and the repository is not checked out. CI passes, so the code compiles and the tests pass.
