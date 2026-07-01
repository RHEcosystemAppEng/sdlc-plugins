# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The comma-separated license filter is implemented by splitting the `license` query parameter on commas and applying an OR-based database filter.

### Endpoint Layer (list.rs)

The `validate_license_param()` function handles comma separation:

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

For input `MIT,Apache-2.0`, this produces the vector `["MIT", "Apache-2.0"]`. Each identifier is validated as a valid SPDX expression before proceeding.

### Service Layer (mod.rs)

The service layer uses `Condition::any()` which generates an OR condition:

```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```

For the vector `["MIT", "Apache-2.0"]`, this produces `WHERE license IN ('MIT', 'Apache-2.0')`, which returns packages matching either license. The use of `Condition::any()` with `is_in()` is semantically correct -- `is_in` already produces OR semantics (any value matches), and `Condition::any()` wraps it to support extensibility.

### Test Coverage

The test `test_list_packages_multi_license_filter` directly validates this criterion:

```rust
ctx.seed_package("pkg-a", "MIT").await;
ctx.seed_package("pkg-b", "Apache-2.0").await;
ctx.seed_package("pkg-c", "GPL-3.0-only").await;

let resp = ctx.get("/api/v2/package?license=MIT,Apache-2.0").await;

assert_eq!(resp.status(), StatusCode::OK);
let body: PaginatedResults<PackageSummary> = resp.json().await;
assert_eq!(body.items.len(), 2);
assert!(body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0"));
```

This seeds 3 packages with different licenses, filters by `MIT,Apache-2.0`, and asserts exactly 2 results are returned (the MIT and Apache-2.0 packages, excluding the GPL-3.0-only package). The assertion verifies each returned package has one of the two requested licenses.

## Evidence

- `modules/fundamental/src/package/endpoints/list.rs`: `split(',')` in `validate_license_param()` produces a multi-element vector
- `modules/fundamental/src/package/service/mod.rs`: `Condition::any()` with `is_in()` produces SQL `IN` clause for OR semantics
- `tests/api/package.rs`: `test_list_packages_multi_license_filter` validates union behavior with 3 differently-licensed packages
