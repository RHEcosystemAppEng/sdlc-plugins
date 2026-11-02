# Criterion 2: Comma-Separated License Filter

**Criterion:** `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict: PASS**

## What was checked

Inspected the PR diff for:
1. Parsing of comma-separated license values
2. OR-based filtering in the database query
3. Test coverage for multi-license filtering

## Code-level evidence

### Comma splitting (list.rs)

`validate_license_param` splits the input on commas:
```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

For input `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`. Each identifier is validated individually via `Expression::parse(id)`.

### OR-based filtering (service/mod.rs)

The filter uses `Condition::any()` with `is_in`, which generates a SQL `IN` clause:
```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```

For `["MIT", "Apache-2.0"]`, this produces `WHERE license IN ('MIT', 'Apache-2.0')`, returning packages with either license.

### Test coverage (tests/api/package.rs)

`test_list_packages_multi_license_filter` seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses, queries `?license=MIT,Apache-2.0`, and asserts:
```rust
assert_eq!(body.items.len(), 2);
assert!(body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0"));
```

This confirms the union of matching packages is returned and the GPL-3.0 package is excluded.
