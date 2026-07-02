# Acceptance Criterion 2: Multi-License Filter

**Criterion**: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict**: PASS

## Evidence from Diff

### Comma-Separated Parsing

The `validate_license_param` function in `list.rs` splits the license parameter on commas:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

For `license=MIT,Apache-2.0`, this produces `vec!["MIT", "Apache-2.0"]`. Each identifier is individually validated against the SPDX expression parser, so both `MIT` and `Apache-2.0` must be valid SPDX identifiers.

### Union Query

In `service/mod.rs`, the filter uses `Condition::any()` with `is_in()`:

```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```

`Condition::any()` creates an OR condition, and `is_in` generates a SQL `IN ('MIT', 'Apache-2.0')` clause. Combined with the inner join on `PackageLicense`, this returns packages that have either MIT or Apache-2.0 as their license -- the union of both sets.

### Test Coverage

The test `test_list_packages_multi_license_filter` seeds 3 packages with MIT, Apache-2.0, and GPL-3.0-only licenses, then requests `?license=MIT,Apache-2.0` and asserts:
- Response status is 200 OK
- Exactly 2 items are returned (MIT and Apache-2.0, not GPL-3.0-only)
- All returned items have a license that is either `MIT` or `Apache-2.0`

This directly validates the union behavior specified in the criterion.
