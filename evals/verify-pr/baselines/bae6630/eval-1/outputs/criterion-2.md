## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Result: PASS**

### Evidence

The `validate_license_param` function in `list.rs` splits the comma-separated license string into individual identifiers:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

Each identifier is validated against the SPDX expression parser, and the resulting vector is passed to the service layer.

In the service layer (`mod.rs`), the filter uses `Condition::any()` with `is_in()`:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

`Condition::any()` produces a SQL `OR` condition, and `is_in` generates `WHERE license IN ('MIT', 'Apache-2.0')`, which correctly returns packages matching either license.

The integration test `test_list_packages_multi_license_filter` verifies this by seeding packages with MIT, Apache-2.0, and GPL-3.0-only licenses, querying with `?license=MIT,Apache-2.0`, and asserting:

```rust
assert_eq!(body.items.len(), 2);
assert!(body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0"));
```

The GPL-3.0-only package is correctly excluded from the results. This criterion is fully satisfied.
