# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Analysis

This criterion requires that comma-separated license values return the union (OR) of matching packages, not the intersection.

### Code Evidence

**Comma Parsing (`modules/fundamental/src/package/endpoints/list.rs`):**

The `validate_license_param` function handles comma separation:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

For input `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`. Each identifier is individually validated against the SPDX expression parser. The `.trim()` call handles whitespace around commas.

**Union Filtering (`modules/fundamental/src/package/service/mod.rs`):**

The filter uses `Condition::any()` with `is_in`:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

`Condition::any()` produces an OR condition in SeaORM, and `is_in` with multiple values produces `WHERE license IN ('MIT', 'Apache-2.0')`. This correctly implements union semantics -- a package with either license will match.

**Test Coverage (`tests/api/package.rs`):**

The test `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), queries `?license=MIT,Apache-2.0`, and asserts:
- Response status is 200 OK
- Exactly 2 items are returned (MIT and Apache-2.0, but not GPL-3.0-only)
- All returned items have `license == "MIT" || license == "Apache-2.0"`

This directly validates union behavior -- the GPL-3.0-only package is excluded, while both MIT and Apache-2.0 packages are included.

### Conclusion

The implementation correctly splits comma-separated license values, validates each one, and applies them as an OR filter. The test confirms union semantics with a three-license dataset where only two match.
