## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Verdict: PASS

### Reasoning

The implementation satisfies this criterion through two complementary code changes:

**Endpoint layer** (`modules/fundamental/src/package/endpoints/list.rs`):
- The `PackageListParams` struct now includes `pub license: Option<String>`, which Axum's `Query` extractor will parse from the `?license=MIT` query parameter.
- The `list_packages` handler calls `validate_license_param(license)` when the parameter is present, which parses "MIT" as a single SPDX expression via `Expression::parse(id)`. MIT is a valid SPDX identifier, so validation passes.
- The validated identifiers (`vec!["MIT"]`) are passed to `PackageService::list()` as `license_filter`.

**Service layer** (`modules/fundamental/src/package/service/mod.rs`):
- When `license_filter` is `Some(["MIT"])`, the service adds a `Condition::any()` filter with `package_license::Column::License.is_in(["MIT"])`, which produces a SQL `WHERE license IN ('MIT')` clause.
- An `InnerJoin` to the `PackageLicense` relation ensures only packages with a matching license association are returned.
- The existing pagination logic (`total` count and `items` query) operates on the filtered query, so only MIT-licensed packages appear in the response.

**Test coverage** (`tests/api/package.rs`):
- `test_list_packages_single_license_filter` seeds 3 packages (2 MIT, 1 Apache-2.0), requests `?license=MIT`, and asserts:
  - Response status is 200 OK
  - Exactly 2 items returned
  - All returned items have `license == "MIT"`

This test directly validates the criterion end-to-end.
