# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict: PASS**

## Reasoning

1. **Parameter parsing** (`modules/fundamental/src/package/endpoints/list.rs`): `PackageListParams` gains `pub license: Option<String>`, so `?license=MIT` is deserialized by the existing `Query<PackageListParams>` extractor.
2. **Validation**: `list_packages` calls `validate_license_param("MIT")` when the parameter is present. It splits on `,` (one element here), trims it, and checks it with `spdx::Expression::parse`. `MIT` is a valid SPDX identifier, so the function returns `Ok(vec!["MIT"])`.
3. **Propagation**: the validated list goes to `PackageService::list(offset, limit, license_filter.as_deref())`, which receives `Some(&["MIT"])`.
4. **Query filtering** (`modules/fundamental/src/package/service/mod.rs`): when `license_filter` is `Some`, the query gets `Condition::any().add(package_license::Column::License.is_in(["MIT"]))` and an `InnerJoin` on `package::Relation::PackageLicense`. Packages without a matching `package_license` row are excluded, so only MIT-licensed packages come back. The `package_license` entity exists in the repo (`entity/src/package_license.rs`).
5. **Test coverage**: `test_list_packages_single_license_filter` in `tests/api/package.rs` seeds 2 MIT packages and 1 Apache-2.0 package, requests `?license=MIT`, and asserts status 200, `items.len() == 2`, and that every item has `license == "MIT"`.

## Observations (non-blocking)
- `.filter()` is called before `.join()`. SeaORM builds the SQL regardless of call order, so this works correctly.
