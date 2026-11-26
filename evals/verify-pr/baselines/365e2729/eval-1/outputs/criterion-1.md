# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict: PASS**

## Code that implements it

`modules/fundamental/src/package/endpoints/list.rs`:
- Adds the query parameter to `PackageListParams`: `pub license: Option<String>,`
- When the parameter is present, the handler validates it and passes it to the service:
  ```rust
  let license_filter = match &params.license {
      Some(license) => Some(validate_license_param(license)?),
      None => None,
  };
  ...
  .list(params.offset, params.limit, license_filter.as_deref())
  ```

`modules/fundamental/src/package/service/mod.rs`:
- `PackageService::list` takes a new parameter, `license_filter: Option<&[String]>`, and applies it:
  ```rust
  if let Some(licenses) = license_filter {
      query = query.filter(
          Condition::any()
              .add(package_license::Column::License.is_in(licenses.iter().cloned()))
      );
      query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
  }
  ```
- With the single value `["MIT"]`, the inner join to `package_license` plus `License IN ('MIT')` keeps only packages that have an MIT license row.

## Test coverage

`tests/api/package.rs::test_list_packages_single_license_filter` seeds `pkg-a` (MIT), `pkg-b` (Apache-2.0) and `pkg-c` (MIT), then calls `GET /api/v2/package?license=MIT`. It asserts:
- the status is `200 OK`
- `items.len() == 2`
- every returned item has `license == "MIT"`

This matches the test requirement "single license filter returns matching packages only".

## Caveats

- The imports for `Condition`, `JoinType`, `package_license` and `AppError` are not shown in the diff hunks. CI passes, so they must already be in scope.
- This was checked by reading the diff only. No Serena instance was available and the repo was not checked out. The passing integration test covers the runtime behavior.
