# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Analysis

The implementation satisfies this criterion through comma-separated value parsing and SQL `IN` clause generation:

### 1. Comma Separation Parsing (list.rs)

The `validate_license_param` function splits on commas:
```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

For `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`. Each identifier is individually validated against the SPDX expression parser. The `.trim()` call handles whitespace around commas.

### 2. OR-Based Filtering (service/mod.rs)

The filter uses `Condition::any()` with `is_in`:
```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

The `is_in` clause generates SQL equivalent to `WHERE license IN ('MIT', 'Apache-2.0')`, which matches packages with either license (union semantics).

### 3. Test Coverage

The test `test_list_packages_multi_license_filter` seeds 3 packages (MIT, Apache-2.0, GPL-3.0-only), filters by `?license=MIT,Apache-2.0`, and asserts:
- HTTP 200 status
- 2 items returned (the GPL-3.0-only package is excluded)
- All items have either MIT or Apache-2.0 license

This directly verifies the union behavior specified in the criterion.

## Evidence

- `license.split(',')` in `validate_license_param` handles comma separation
- `.trim()` handles whitespace between comma-separated values
- `is_in(licenses.iter().cloned())` generates SQL `IN (...)` clause for union matching
- Test `test_list_packages_multi_license_filter` validates multi-license filtering end-to-end
