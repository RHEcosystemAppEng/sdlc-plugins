## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict: PASS**

### Reasoning

The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` splits the license parameter on commas:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

This produces `["MIT", "Apache-2.0"]` when `license=MIT,Apache-2.0` is provided. Each identifier is individually validated as a valid SPDX expression.

In `modules/fundamental/src/package/service/mod.rs`, the filter uses `Condition::any()` with `is_in()`:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

The `is_in` clause generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` condition, which returns packages matching either license. The `Condition::any()` wrapper ensures this is an OR-based filter, correctly implementing the union semantics described in the criterion.

The integration test `test_list_packages_multi_license_filter` in `tests/api/package.rs` verifies this behavior by seeding three packages with MIT, Apache-2.0, and GPL-3.0-only licenses, filtering by `MIT,Apache-2.0`, and asserting that exactly 2 packages are returned with licenses matching either MIT or Apache-2.0.

This criterion is satisfied by both the implementation and test coverage.
