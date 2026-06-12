## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict:** PASS

### Reasoning

The `validate_license_param` function handles comma-separated values by splitting the input string on commas:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

For the input `"MIT,Apache-2.0"`, this produces `vec!["MIT", "Apache-2.0"]`. Each identifier is validated individually via `spdx::Expression::parse(id)` -- both "MIT" and "Apache-2.0" are valid SPDX identifiers, so validation passes.

In the service layer, the filter uses `Condition::any()` with `is_in`:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

The `is_in` clause generates SQL `package_license.license IN ('MIT', 'Apache-2.0')`, which returns rows matching either license. The `Condition::any()` wrapper is semantically redundant for a single `is_in` clause but does not change correctness -- it still produces OR semantics.

The inner join on `PackageLicense` ensures only packages with matching license rows are included, effectively returning the union of packages with either MIT or Apache-2.0 licenses.

The integration test `test_list_packages_multi_license_filter` seeds 3 packages (MIT, Apache-2.0, GPL-3.0-only), filters by `MIT,Apache-2.0`, and asserts that exactly 2 packages are returned, all with either MIT or Apache-2.0 licenses.

### Evidence

- `list.rs`: `license.split(',')` handles comma separation
- `list.rs`: `.map(|s| s.trim().to_string())` trims whitespace around each identifier
- `service/mod.rs`: `is_in(licenses.iter().cloned())` produces SQL IN clause for multiple values
- `tests/api/package.rs`: `test_list_packages_multi_license_filter` validates this behavior
