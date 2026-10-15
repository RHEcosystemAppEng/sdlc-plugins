# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Analysis

This criterion requires that when the `license` query parameter is set to `MIT`, the endpoint returns only packages whose license is MIT.

### Implementation Evidence

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**
- The `PackageListParams` struct now includes `pub license: Option<String>`, which Axum's `Query` extractor automatically deserializes from the URL query string.
- When `params.license` is `Some`, the handler calls `validate_license_param(license)` which splits the value on commas, trims whitespace, and validates each identifier via `spdx::Expression::parse(id)`. For a single value like `MIT`, this produces a `Vec<String>` containing `["MIT"]`.
- The validated identifiers are passed to `PackageService::list` as `license_filter: Option<&[String]>`.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**
- When `license_filter` is `Some`, the service applies:
  - `query = query.filter(Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned())))` -- generates a `WHERE package_license.license IN ('MIT')` clause
  - `query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def())` -- joins to the `package_license` table
- This ensures only packages with a matching license are returned.

**Test coverage (`tests/api/package.rs`):**
- `test_list_packages_single_license_filter` seeds three packages (two MIT, one Apache-2.0), queries `?license=MIT`, and asserts:
  - Status is 200 OK
  - `body.items.len() == 2` (only the two MIT packages)
  - `body.items.iter().all(|p| p.license == "MIT")` (all returned packages are MIT)

### Conclusion

The implementation correctly adds a `license` query parameter that, when set to a single value like `MIT`, filters the database query using an `IN` clause on the `package_license` table, returning only matching packages. The test validates this behavior end-to-end.
