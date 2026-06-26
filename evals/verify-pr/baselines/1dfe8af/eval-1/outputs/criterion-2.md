## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Verdict: PASS

### Evidence

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**

The `validate_license_param` function splits the `license` parameter by comma:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

For the input `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`. Each identifier is validated as a valid SPDX expression via `Expression::parse(id)`. Both `MIT` and `Apache-2.0` are valid SPDX identifiers, so validation passes.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**

The filter uses `Condition::any()` with `is_in(licenses.iter().cloned())`:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

`Condition::any()` produces an OR-based condition, and `is_in` generates `WHERE license IN ('MIT', 'Apache-2.0')`. This returns the union of packages matching either license.

**Test confirmation (`tests/api/package.rs`):**

The test `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), queries `?license=MIT,Apache-2.0`, and asserts:
- Response status is 200 OK
- Exactly 2 items are returned (MIT and Apache-2.0, not GPL-3.0-only)
- All returned items have either `MIT` or `Apache-2.0` as their license

This directly validates the criterion.
