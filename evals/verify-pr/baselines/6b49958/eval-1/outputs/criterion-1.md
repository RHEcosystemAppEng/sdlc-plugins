## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict: PASS**

### Evidence

The PR diff implements this criterion through changes in two files:

1. **`modules/fundamental/src/package/endpoints/list.rs`**: Added `license: Option<String>` field to `PackageListParams` struct. The `list_packages` handler extracts the license parameter and passes it through `validate_license_param()` to parse individual identifiers. When `license=MIT` is provided, the handler passes `Some(["MIT"])` to `PackageService::list()`.

2. **`modules/fundamental/src/package/service/mod.rs`**: The `list()` method now accepts `license_filter: Option<&[String]>`. When a license filter is present, it applies a `Condition::any()` filter using `package_license::Column::License.is_in(licenses.iter().cloned())` with an `InnerJoin` on `package::Relation::PackageLicense`. This ensures only packages matching the given license identifier are returned.

3. **`tests/api/package.rs`**: The test `test_list_packages_single_license_filter` seeds packages with MIT and Apache-2.0 licenses, queries `?license=MIT`, and asserts:
   - Response status is 200 OK
   - Exactly 2 items returned (matching the 2 MIT-licensed packages seeded)
   - All returned items have `license == "MIT"`

The implementation correctly filters by a single license identifier and the test validates this behavior.
