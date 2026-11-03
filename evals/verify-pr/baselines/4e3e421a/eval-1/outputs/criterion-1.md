# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict: PASS**

## Reasoning

1. **Parameter parsing** — `modules/fundamental/src/package/endpoints/list.rs` adds `pub license: Option<String>` to `PackageListParams`, so the query string `?license=MIT` is deserialized by the existing `Query<PackageListParams>` extractor (consistent with the `Query<FilterParams>` pattern referenced in the Implementation Notes).
2. **Validation** — `validate_license_param("MIT")` splits on `,` (yielding `["MIT"]`), trims, and runs `spdx::Expression::parse` on each identifier. `MIT` is a valid SPDX identifier, so it returns `Ok(vec!["MIT"])`.
3. **Plumbing** — `list_packages` passes `license_filter.as_deref()` (an `Option<&[String]>`) into `PackageService::list`.
4. **Filtering** — in `modules/fundamental/src/package/service/mod.rs`, when `license_filter` is `Some`, the query is:
   - filtered with `Condition::any().add(package_license::Column::License.is_in(licenses...))`, and
   - inner-joined to `package_license` via `package::Relation::PackageLicense.def()` (the `entity/src/package_license.rs` mapping exists in the repo).
   With a single value, `IS IN ('MIT')` is equivalent to `= 'MIT'`, and the INNER JOIN excludes packages without a matching license row. Only MIT packages are returned.
5. **Test evidence** — `test_list_packages_single_license_filter` seeds 2 MIT + 1 Apache-2.0 package, requests `?license=MIT`, and asserts status 200, `items.len() == 2`, and that every item's `license == "MIT"`.

## Notes
- No issues found. The filter and join are applied before both the `count` and the paginated fetch, so both reflect the filtered set.
