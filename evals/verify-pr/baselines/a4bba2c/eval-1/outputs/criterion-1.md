# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Analysis

### What the criterion requires
The endpoint must accept a `license` query parameter and, when set to a single SPDX identifier like `MIT`, return only packages whose license matches that identifier.

### How the implementation satisfies it

**Parameter parsing (list.rs):**
The `PackageListParams` struct gains a new optional field `pub license: Option<String>`. When the query string contains `?license=MIT`, Axum's `Query` extractor deserializes it into this field.

**Validation (list.rs):**
The `validate_license_param` function splits the comma-separated string into individual identifiers and validates each one against the `spdx::Expression::parse` function. For a single value like `MIT`, this produces a `Vec<String>` containing one element `["MIT"]`.

**Filtering (service/mod.rs):**
The `PackageService::list` method now accepts an `Option<&[String]>` parameter for `license_filter`. When `Some(licenses)` is provided, the query builder applies:
```rust
Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))
```
This generates a SQL `WHERE package_license.license IN ('MIT')` clause. The `InnerJoin` to `PackageLicense` ensures only packages with a matching license row are returned.

**Test coverage:**
`test_list_packages_single_license_filter` seeds three packages (two MIT, one Apache-2.0), requests `?license=MIT`, and asserts:
- Response status is 200 OK
- Exactly 2 items returned
- All returned items have `license == "MIT"`

This directly validates the criterion's requirement.

### Evidence
- `modules/fundamental/src/package/endpoints/list.rs`: `license: Option<String>` field added to `PackageListParams`
- `modules/fundamental/src/package/endpoints/list.rs`: `validate_license_param` function parses and validates SPDX identifiers
- `modules/fundamental/src/package/service/mod.rs`: `is_in` filter applied with `InnerJoin` to `PackageLicense`
- `tests/api/package.rs`: `test_list_packages_single_license_filter` validates the exact scenario
