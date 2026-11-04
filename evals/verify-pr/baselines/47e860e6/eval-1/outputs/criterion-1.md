# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict: PASS**

## Code evidence
- `modules/fundamental/src/package/endpoints/list.rs`
  - `PackageListParams` gains `pub license: Option<String>`, so axum's `Query<PackageListParams>` extraction picks up `?license=MIT`.
  - `list_packages` sends a present `license` through `validate_license_param`. That function splits on `,` and trims each value, so `"MIT"` becomes `vec!["MIT"]`, and checks each identifier with `spdx::Expression::parse`.
  - The validated list is passed to the service as `.list(params.offset, params.limit, license_filter.as_deref())`.
- `modules/fundamental/src/package/service/mod.rs`
  - When `license_filter` is `Some`, the query gets `Condition::any().add(package_license::Column::License.is_in(licenses...))` and an `InnerJoin` on `package::Relation::PackageLicense`. The resulting SQL is roughly `... INNER JOIN package_license ... WHERE package_license.license IN ('MIT')`, which excludes every non-MIT package.

## Test evidence
- `tests/api/package.rs::test_list_packages_single_license_filter` seeds two MIT packages and one Apache-2.0 package, requests `?license=MIT`, and asserts status 200, `items.len() == 2`, and that every returned item has `license == "MIT"`.

## Notes (non-blocking)
- The match is exact (`IN`). If the database stores compound SPDX expressions such as `MIT OR Apache-2.0` in one row, those packages would not match `?license=MIT`. This depends on the data model, and the criterion as written is met.
