## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict: PASS**

### Reasoning

The PR implements single-license filtering through the following code changes:

**1. Query parameter parsing (list.rs)**

The `PackageListParams` struct adds a new field `pub license: Option<String>`, which Axum's `Query` extractor will automatically bind from the `?license=MIT` query parameter. When the parameter is absent, it defaults to `None`, preserving backward compatibility.

**2. Validation (list.rs)**

The `validate_license_param` function splits the input on commas, trims whitespace, and validates each identifier against the SPDX expression parser (`spdx::Expression::parse`). For a single value like `MIT`, this produces a `Vec<String>` containing one element `["MIT"]`. If parsing fails, it returns `AppError::BadRequest`.

**3. Filtering (service/mod.rs)**

In `PackageService::list()`, the new `license_filter: Option<&[String]>` parameter is used to conditionally apply a WHERE clause:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

For a single license `["MIT"]`, this generates a SQL `WHERE package_license.license IN ('MIT')` with an INNER JOIN to the `package_license` table. This correctly restricts results to only packages whose license matches MIT.

**4. Test coverage**

The test `test_list_packages_single_license_filter` seeds three packages (two with MIT, one with Apache-2.0), sends `GET /api/v2/package?license=MIT`, and asserts:
- Response status is 200 OK
- Exactly 2 items are returned
- All returned items have `license == "MIT"`

This directly verifies the criterion's requirement that only MIT-licensed packages are returned.

### Evidence

- `PackageListParams.license` field added in `list.rs` (line 15 of diff)
- `validate_license_param` function validates SPDX identifiers (lines 25-33 of diff)
- `license_filter` applied via `Condition::any().add(is_in(...))` in `service/mod.rs` (lines 68-73 of diff)
- `INNER JOIN` to `package_license` table ensures only packages with matching licenses are returned (line 73 of diff)
- Test `test_list_packages_single_license_filter` in `tests/api/package.rs` (lines 89-105 of diff) validates the behavior end-to-end
