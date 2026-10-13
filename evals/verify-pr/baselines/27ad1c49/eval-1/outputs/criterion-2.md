# Criterion 2: GET /api/v2/package?license=MIT,Apache-2.0 returns packages with either license

## Verdict: PASS

## Reasoning

### Comma-Separated Parsing

The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` handles comma-separated values by splitting the input string on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. For the input `"MIT,Apache-2.0"`, this produces `["MIT", "Apache-2.0"]`.

Each identifier is individually validated against the SPDX specification via `Expression::parse(id)`. Both `"MIT"` and `"Apache-2.0"` are valid SPDX identifiers, so validation passes for both.

### Union (OR) Filter Semantics

In `modules/fundamental/src/package/service/mod.rs`, the license filter uses `Condition::any()` with `is_in`:

```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```

The `is_in` operator generates SQL `WHERE license IN ('MIT', 'Apache-2.0')`, which returns packages matching ANY of the specified licenses (union/OR semantics). Combined with the `InnerJoin` to `PackageLicense`, this correctly returns all packages that have either an MIT or Apache-2.0 license.

### Test Coverage

The test `test_list_packages_multi_license_filter` validates this behavior:
- Seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (GPL-3.0-only)
- Requests `GET /api/v2/package?license=MIT,Apache-2.0`
- Asserts response status is 200 OK
- Asserts `body.items.len() == 2` (MIT and Apache-2.0 packages, excluding GPL)
- Asserts `body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0")` (all returned items match one of the requested licenses)

The GPL-3.0-only package is correctly excluded, confirming union semantics.

## Evidence

- `modules/fundamental/src/package/endpoints/list.rs`: `license.split(',')` handles comma-separated values with `.trim()` for whitespace tolerance
- `modules/fundamental/src/package/service/mod.rs`: `Condition::any()` + `is_in()` produces OR/union semantics
- `tests/api/package.rs`: `test_list_packages_multi_license_filter` seeds MIT, Apache-2.0, GPL-3.0-only; asserts 2 results matching MIT or Apache-2.0
