# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Analysis

The `validate_license_param` function in `list.rs` splits the license parameter on commas:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

Each identifier is individually validated via `spdx::Expression::parse()`, so `MIT,Apache-2.0` produces `["MIT", "Apache-2.0"]`.

In `service/mod.rs`, the multiple identifiers are passed to `is_in()`:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

This produces a SQL `WHERE license IN ('MIT', 'Apache-2.0')`, which matches packages with either license (union semantics).

The test `test_list_packages_multi_license_filter` in `tests/api/package.rs` verifies this:
- Seeds 3 packages (MIT, Apache-2.0, GPL-3.0-only)
- Queries `?license=MIT,Apache-2.0`
- Asserts 200 OK, 2 items returned, all with license == "MIT" or "Apache-2.0"

## Evidence

- `list.rs`: `license.split(',')` handles comma separation
- `list.rs`: Each identifier validated individually via `Expression::parse()`
- `service/mod.rs`: `is_in(licenses.iter().cloned())` produces OR-matching SQL
- `tests/api/package.rs`: `test_list_packages_multi_license_filter` verifies union semantics
