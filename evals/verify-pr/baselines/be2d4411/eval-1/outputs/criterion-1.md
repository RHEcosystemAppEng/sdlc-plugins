## Criterion 1

**Text:** `GET /api/v2/package?license=MIT` returns only packages with MIT license

### What was checked

1. The `license` query parameter is added to `PackageListParams` in `modules/fundamental/src/package/endpoints/list.rs` as `pub license: Option<String>`.
2. The `list_packages` handler extracts `params.license`, passes it through `validate_license_param`, and forwards the resulting `Vec<String>` to `PackageService::list`.
3. In `modules/fundamental/src/package/service/mod.rs`, when `license_filter` is `Some`, the query is filtered using `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))` with an `InnerJoin` on `package::Relation::PackageLicense`. For a single license value like `"MIT"`, the `is_in` clause effectively becomes an equality check, returning only packages whose license matches `"MIT"`.
4. The integration test `test_list_packages_single_license_filter` in `tests/api/package.rs` seeds three packages (two MIT, one Apache-2.0), queries `?license=MIT`, and asserts exactly 2 items are returned, all with `license == "MIT"`.

### Evidence

- `modules/fundamental/src/package/endpoints/list.rs`: `pub license: Option<String>` added to `PackageListParams` struct; `validate_license_param` splits on comma and parses each identifier; handler passes validated filter to service.
- `modules/fundamental/src/package/service/mod.rs`: `license_filter: Option<&[String]>` parameter added to `list()`; `is_in(licenses.iter().cloned())` filter applied when present.
- `tests/api/package.rs` lines 7-25: `test_list_packages_single_license_filter` seeds `"pkg-a"` (MIT), `"pkg-b"` (Apache-2.0), `"pkg-c"` (MIT), requests `?license=MIT`, asserts `body.items.len() == 2` and all items have `license == "MIT"`.

### Verdict: PASS
