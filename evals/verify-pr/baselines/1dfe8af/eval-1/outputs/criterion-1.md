## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Verdict: PASS

### Evidence

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**

The `PackageListParams` struct now includes an optional `license` field:

```rust
pub license: Option<String>,
```

When the `license` parameter is present, the handler calls `validate_license_param(license)` which parses each comma-separated identifier as an SPDX expression. For a single value like `MIT`, this produces a `Vec<String>` containing `["MIT"]`. This vector is passed to `PackageService::list()` as `license_filter`.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**

The `list` method now accepts `license_filter: Option<&[String]>`. When `Some(licenses)` is provided, the method:

1. Adds a `Condition::any()` filter with `package_license::Column::License.is_in(licenses.iter().cloned())` -- this generates a SQL `WHERE license IN ('MIT')` clause.
2. Joins `package::Relation::PackageLicense` via `InnerJoin`, ensuring only packages that have a matching license record are returned.

For a single `?license=MIT` query, only packages whose `package_license` row has `license = 'MIT'` will be included in the result set.

**Test confirmation (`tests/api/package.rs`):**

The test `test_list_packages_single_license_filter` seeds three packages (two MIT, one Apache-2.0), queries `?license=MIT`, and asserts:
- Response status is 200 OK
- Exactly 2 items are returned
- All items have `license == "MIT"`

This directly validates the criterion.
