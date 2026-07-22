## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Verdict: PASS

### Reasoning

This criterion requires that comma-separated license values return the union of packages matching any of the specified licenses.

**Comma splitting (`list.rs`):**
The `validate_license_param` function splits the input string by comma and trims whitespace:
```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```
For the input `"MIT,Apache-2.0"`, this produces `["MIT", "Apache-2.0"]`. Each identifier is individually validated against the SPDX expression parser.

**Union semantics (`mod.rs`):**
The filter uses `Condition::any()` combined with `is_in(licenses.iter().cloned())`:
```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```
The `is_in` predicate generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause, which inherently returns the union of rows matching either value. The `Condition::any()` wrapper ensures OR semantics if additional conditions were added (though currently only one condition is used).

**Test coverage (`tests/api/package.rs`):**
The test `test_list_packages_multi_license_filter` seeds three packages with MIT, Apache-2.0, and GPL-3.0-only licenses, sends `GET /api/v2/package?license=MIT,Apache-2.0`, and asserts:
- Response status is 200 OK
- Response body contains exactly 2 items (MIT and Apache-2.0, not GPL-3.0-only)
- All returned items have license equal to either "MIT" or "Apache-2.0"

This confirms the union behavior: packages matching any of the specified licenses are returned, and packages with other licenses are excluded.

### Evidence

- `list.rs`: `license.split(',')` handles comma separation
- `mod.rs`: `is_in(licenses.iter().cloned())` implements SQL `IN` clause for union semantics
- `tests/api/package.rs`: `test_list_packages_multi_license_filter` verifies union of MIT and Apache-2.0
