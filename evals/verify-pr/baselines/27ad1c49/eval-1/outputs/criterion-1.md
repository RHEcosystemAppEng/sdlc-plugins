# Criterion 1: GET /api/v2/package?license=MIT returns only packages with MIT license

## Verdict: PASS

## Reasoning

### Endpoint Parameter Parsing

The `PackageListParams` struct in `modules/fundamental/src/package/endpoints/list.rs` adds a new `license: Option<String>` field. When a request includes `?license=MIT`, Axum's `Query` extractor deserializes this into `Some("MIT")`.

### Validation

The `validate_license_param` function splits the license string on commas and validates each identifier by calling `spdx::Expression::parse(id)`. For a single value like `"MIT"`, this produces a one-element `Vec<String>` containing `"MIT"`. Since `"MIT"` is a valid SPDX identifier, validation succeeds.

### Filter Application

In the handler `list_packages`, the validated license identifiers are passed to `PackageService::list()` as `license_filter: Option<&[String]>`. In `modules/fundamental/src/package/service/mod.rs`, when `license_filter` is `Some`, the service:

1. Applies a `Condition::any()` filter with `package_license::Column::License.is_in(licenses.iter().cloned())` -- for a single value `["MIT"]`, this generates `WHERE license IN ('MIT')`, matching only MIT-licensed packages.
2. Adds an `InnerJoin` to the `PackageLicense` relation, ensuring only packages with a matching license row are returned.

The filter is applied before the `total = query.clone().count()` call and the paginated items query, so both the count and results reflect the filtered set.

### Test Coverage

The test `test_list_packages_single_license_filter` validates this behavior:
- Seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (MIT)
- Requests `GET /api/v2/package?license=MIT`
- Asserts response status is 200 OK
- Asserts `body.items.len() == 2` (only the two MIT packages)
- Asserts `body.items.iter().all(|p| p.license == "MIT")` (all returned packages have MIT license)

This confirms that non-MIT packages (pkg-b with Apache-2.0) are excluded from the results.

## Evidence

- `modules/fundamental/src/package/endpoints/list.rs`: `pub license: Option<String>` added to `PackageListParams`
- `modules/fundamental/src/package/endpoints/list.rs`: `validate_license_param` splits on comma, validates with `spdx::Expression::parse`
- `modules/fundamental/src/package/service/mod.rs`: `Condition::any().add(package_license::Column::License.is_in(...))` with `InnerJoin`
- `tests/api/package.rs`: `test_list_packages_single_license_filter` asserts count=2 and all items have MIT license
