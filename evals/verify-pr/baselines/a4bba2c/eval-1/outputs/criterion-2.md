# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Analysis

### What the criterion requires
The endpoint must support comma-separated license values in the `license` query parameter and return the union of packages matching any of the specified licenses.

### How the implementation satisfies it

**Comma splitting (list.rs):**
The `validate_license_param` function splits the input string on commas and trims whitespace:
```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```
For `?license=MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`.

**Per-identifier validation (list.rs):**
Each identifier is validated individually via `Expression::parse(id)`, ensuring both `MIT` and `Apache-2.0` are valid SPDX identifiers before proceeding to the query.

**OR filtering (service/mod.rs):**
The filter uses `Condition::any()` with `is_in`:
```rust
Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))
```
`Condition::any()` produces SQL `OR` semantics, and `is_in` with multiple values generates `WHERE package_license.license IN ('MIT', 'Apache-2.0')`. This correctly returns the union of matching packages.

**Test coverage:**
`test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), requests `?license=MIT,Apache-2.0`, and asserts:
- Response status is 200 OK
- Exactly 2 items returned
- All items have license either `MIT` or `Apache-2.0`

This directly validates the union behavior required by the criterion.

### Evidence
- `modules/fundamental/src/package/endpoints/list.rs`: `license.split(',')` handles comma separation
- `modules/fundamental/src/package/service/mod.rs`: `Condition::any()` with `is_in` implements OR semantics
- `tests/api/package.rs`: `test_list_packages_multi_license_filter` validates the exact scenario
