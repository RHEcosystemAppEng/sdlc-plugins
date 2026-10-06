# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Analysis

The implementation satisfies this criterion through a chain of three components:

### 1. Query Parameter Parsing (list.rs)

The `PackageListParams` struct adds a new field:
```rust
pub license: Option<String>,
```

This allows Axum's `Query` extractor to deserialize the `license` query parameter from the URL.

### 2. License Validation (list.rs)

The `validate_license_param` function processes the license parameter:
```rust
fn validate_license_param(license: &str) -> Result<Vec<String>, AppError> {
    let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
    for id in &identifiers {
        Expression::parse(id).map_err(|_| {
            AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
        })?;
    }
    Ok(identifiers)
}
```

For a single value like `MIT`, this produces a `Vec` containing one element `["MIT"]`, validated against the SPDX expression parser.

### 3. Database Filtering (service/mod.rs)

The `PackageService::list` method applies the filter:
```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

This adds an `InnerJoin` to the `PackageLicense` table and filters on `license IN ('MIT')`, ensuring only packages with the MIT license are returned.

### 4. Test Coverage

The test `test_list_packages_single_license_filter` seeds 3 packages (2 MIT, 1 Apache-2.0), filters by `?license=MIT`, and asserts:
- HTTP 200 status
- 2 items returned
- All items have `license == "MIT"`

This directly verifies the criterion.

## Evidence

- `PackageListParams.license` field added in `list.rs`
- `validate_license_param` validates SPDX identifiers in `list.rs`
- `is_in` filter with `InnerJoin` applied in `service/mod.rs`
- Test `test_list_packages_single_license_filter` validates end-to-end behavior
