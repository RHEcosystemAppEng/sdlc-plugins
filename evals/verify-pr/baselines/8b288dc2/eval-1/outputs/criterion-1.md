## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Evidence

**Endpoint layer (`list.rs`):**
- The `PackageListParams` struct gains a new field `pub license: Option<String>`, which Axum's `Query` extractor will populate from the `?license=MIT` query parameter.
- In `list_packages`, when `params.license` is `Some`, `validate_license_param` is called, which splits on comma and validates each identifier. For a single value like `MIT`, this produces `vec!["MIT"]`.
- The validated identifiers are passed to `PackageService::list` as `license_filter: Option<&[String]>`.

**Service layer (`service/mod.rs`):**
- When `license_filter` is `Some`, the query is extended with:
  ```rust
  Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))
  ```
  This filters packages to only those whose license column matches one of the provided values. For `["MIT"]`, only MIT-licensed packages match.
- An `InnerJoin` to `PackageLicense` ensures only packages with a license record are included.

**Test (`tests/api/package.rs`):**
- `test_list_packages_single_license_filter` seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (MIT).
- Queries `GET /api/v2/package?license=MIT`.
- Asserts `resp.status() == StatusCode::OK`.
- Asserts `body.items.len() == 2` (only the two MIT packages).
- Asserts `body.items.iter().all(|p| p.license == "MIT")` confirming all returned items have MIT license.

### Verdict: PASS

The implementation correctly adds the license query parameter, filters at the database level using `is_in`, and the test confirms that only MIT-licensed packages are returned when `?license=MIT` is specified.
