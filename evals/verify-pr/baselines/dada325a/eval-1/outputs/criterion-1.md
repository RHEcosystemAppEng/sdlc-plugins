# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict: PASS**

## Reasoning

- **Parameter extraction:** in `modules/fundamental/src/package/endpoints/list.rs`, `PackageListParams` gains `pub license: Option<String>`. The handler already uses `Query<PackageListParams>`, so `?license=MIT` is deserialized into this field. This matches the `Query<FilterParams>` pattern the task points to in the advisory endpoint.
- **Validation and propagation:** the handler calls `validate_license_param`, which runs `spdx::Expression::parse` on each identifier and returns `Vec<String>` (here `["MIT"]`). It then passes the result to the service as `license_filter.as_deref()`, which is an `Option<&[String]>`.
- **Query filter:** in `modules/fundamental/src/package/service/mod.rs`, `PackageService::list` takes a new `license_filter: Option<&[String]>` parameter. When the filter is present, the code adds `package_license::Column::License.is_in(licenses)` inside `Condition::any()`, plus an `InnerJoin` on `package::Relation::PackageLicense`. The inner join drops packages that have no matching license row, so only MIT packages remain. The `entity/src/package_license.rs` entity exists in the repository structure.
- **Absent filter:** when `license` is not given, `license_filter` is `None`, the filter block is skipped, and the endpoint behaves as before.

## Test evidence

`test_list_packages_single_license_filter` in `tests/api/package.rs`:
- Seeds pkg-a (MIT), pkg-b (Apache-2.0) and pkg-c (MIT).
- Requests `?license=MIT`.
- Asserts 200 OK, `items.len() == 2`, and that every item has `license == "MIT"`.

## Conclusion

The code and the test both show that only MIT-licensed packages are returned. The criterion is satisfied.
