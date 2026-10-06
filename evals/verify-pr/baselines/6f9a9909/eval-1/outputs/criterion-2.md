## Criterion 2

**Text:** `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**What was checked:**

1. The `validate_license_param` function splits the license string on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`, producing `["MIT", "Apache-2.0"]` for the input `MIT,Apache-2.0`.
2. Each identifier is validated individually via `Expression::parse(id)`.
3. In `service/mod.rs`, the filter uses `Condition::any()` with `is_in(licenses.iter().cloned())`, which generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause -- returning the union of matching packages.
4. The integration test `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), queries `?license=MIT,Apache-2.0`, and asserts exactly 2 results with each item being either MIT or Apache-2.0.

**Code evidence:**

From `list.rs`:
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

From `tests/api/package.rs`:
```rust
let resp = ctx.get("/api/v2/package?license=MIT,Apache-2.0").await;
assert_eq!(resp.status(), StatusCode::OK);
let body: PaginatedResults<PackageSummary> = resp.json().await;
assert_eq!(body.items.len(), 2);
assert!(body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0"));
```

**Verdict:** PASS
