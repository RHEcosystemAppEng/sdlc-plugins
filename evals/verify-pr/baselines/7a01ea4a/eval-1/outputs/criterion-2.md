## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict: PASS**

### Reasoning

The PR implements multi-license (comma-separated) filtering through the following mechanism:

**1. Comma splitting in validation (list.rs)**

The `validate_license_param` function handles comma-separated values:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

For the input `"MIT,Apache-2.0"`, this produces `["MIT", "Apache-2.0"]`. Each identifier is individually validated against the SPDX expression parser, ensuring both values are valid SPDX license identifiers.

**2. OR-based filtering (service/mod.rs)**

The filter uses `Condition::any()` combined with `is_in()`:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

`is_in` with the list `["MIT", "Apache-2.0"]` generates a SQL `WHERE package_license.license IN ('MIT', 'Apache-2.0')`, which matches packages with either license. The `Condition::any()` wrapper ensures this is an OR condition, meaning packages with MIT OR Apache-2.0 licenses are returned.

**3. Union semantics**

The task specifies that multiple license values should return "packages with either license" (union semantics). The `IN` clause naturally provides union semantics -- a row matches if its license value equals any of the provided values. This is the correct interpretation.

**4. Test coverage**

The test `test_list_packages_multi_license_filter` seeds three packages with distinct licenses (MIT, Apache-2.0, GPL-3.0-only), sends `GET /api/v2/package?license=MIT,Apache-2.0`, and asserts:
- Response status is 200 OK
- Exactly 2 items are returned (MIT + Apache-2.0, excluding GPL-3.0-only)
- All returned items have license equal to either "MIT" or "Apache-2.0"

This directly verifies the union behavior described in the criterion.

### Evidence

- `license.split(',')` in `validate_license_param` (line 26 of diff) handles comma separation
- `.trim().to_string()` handles whitespace around delimiters (line 26 of diff)
- Each identifier validated individually via `Expression::parse(id)` in the loop (lines 27-30 of diff)
- `is_in(licenses.iter().cloned())` produces SQL `IN` clause for union matching (line 71 of diff)
- Test `test_list_packages_multi_license_filter` in `tests/api/package.rs` (lines 108-124 of diff) validates multi-license filtering end-to-end
