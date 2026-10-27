# Criterion 2: Comma-Separated License Filter

**Criterion:** `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict:** PASS

## Evidence

The `validate_license_param` function in `list.rs` handles comma separation:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

Each identifier is individually validated via `Expression::parse`. The resulting vector (e.g., `["MIT", "Apache-2.0"]`) is passed to `PackageService::list()`.

In `service/mod.rs`, the filter uses `Condition::any()` with `is_in`:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

`Condition::any()` produces an OR-based condition, and `is_in` generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause. This returns the union of packages matching any of the provided licenses.

The integration test `test_list_packages_multi_license_filter` confirms this: it seeds three packages (MIT, Apache-2.0, GPL-3.0-only), filters by `MIT,Apache-2.0`, and asserts that exactly 2 packages are returned, each with either MIT or Apache-2.0 license.

**Conclusion:** The implementation correctly supports comma-separated license identifiers and returns the union of matching packages.
