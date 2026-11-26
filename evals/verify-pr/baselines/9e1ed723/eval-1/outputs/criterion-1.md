# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict: PASS**

## Code evidence
- `modules/fundamental/src/package/endpoints/list.rs`:
  - `PackageListParams` gains `pub license: Option<String>`, so the Axum `Query<PackageListParams>` extractor picks up `?license=MIT`.
  - `validate_license_param("MIT")` splits on `,`, trims each value, and validates it with `spdx::Expression::parse`. For this input it returns `vec!["MIT"]`.
  - The handler builds `license_filter` from `params.license` and passes it as `license_filter.as_deref()` to `PackageService::list(offset, limit, license_filter)`.
- `modules/fundamental/src/package/service/mod.rs`:
  - `list` now accepts `license_filter: Option<&[String]>`.
  - When it is `Some`, the query adds `package_license::Column::License.is_in(licenses)` and an `InnerJoin` on `package::Relation::PackageLicense`.
  - Only packages with a matching `package_license` row are returned.

## Test evidence
`tests/api/package.rs::test_list_packages_single_license_filter`:
- seeds `pkg-a` (MIT), `pkg-b` (Apache-2.0) and `pkg-c` (MIT);
- requests `?license=MIT`;
- asserts 200 OK, `items.len() == 2`, and that every item has `license == "MIT"`.

CI passes.

## Caveats
None blocking.
