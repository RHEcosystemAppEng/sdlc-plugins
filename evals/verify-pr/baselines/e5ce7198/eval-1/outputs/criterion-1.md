## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Verdict: PASS

### Evidence

**Endpoint implementation (list.rs):**
- The `PackageListParams` struct now includes `pub license: Option<String>`, which Axum's `Query` extractor will parse from the `?license=MIT` query parameter.
- The `validate_license_param` function splits the parameter by comma and validates each identifier via `spdx::Expression::parse`. For a single value like `MIT`, this produces a `Vec<String>` containing `["MIT"]`.
- The validated identifiers are passed to `PackageService::list()` as `license_filter: Option<&[String]>`.

**Service implementation (service/mod.rs):**
- When `license_filter` is `Some(licenses)`, the service adds a `Condition::any()` filter with `package_license::Column::License.is_in(licenses.iter().cloned())`. For a single license `["MIT"]`, this creates a `WHERE license IN ('MIT')` clause.
- An `InnerJoin` on `package::Relation::PackageLicense` is added to join the package-license mapping table, ensuring only packages with matching licenses are returned.

**Test coverage (tests/api/package.rs):**
- `test_list_packages_single_license_filter` seeds three packages (two MIT, one Apache-2.0), queries `?license=MIT`, and asserts:
  - Status is 200 OK
  - Exactly 2 items returned
  - All returned items have `license == "MIT"`

This test directly validates the criterion. The implementation correctly filters by a single license value.
