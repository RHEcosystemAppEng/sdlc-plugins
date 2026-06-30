## Acceptance Criterion 2

**Criterion**: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict**: PASS

### Evidence

**Comma-separated parsing** (`modules/fundamental/src/package/endpoints/list.rs`):
The `validate_license_param` function splits the input on commas:
```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```
For input `"MIT,Apache-2.0"`, this produces `["MIT", "Apache-2.0"]`. Each identifier is validated individually via `Expression::parse(id)`, and both are valid SPDX identifiers.

**Union query** (`modules/fundamental/src/package/service/mod.rs`):
The service receives `license_filter: Some(&["MIT", "Apache-2.0"])` and applies:
```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```
`Condition::any()` combined with `is_in` generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause, which returns the union of packages matching either license. The `InnerJoin` to `PackageLicense` ensures only packages with a matching license record are returned.

**Test coverage** (`tests/api/package.rs`):
`test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), queries `?license=MIT,Apache-2.0`, and asserts:
- Response status is 200 OK
- `body.items.len()` equals 2 (MIT and Apache-2.0 packages; GPL-3.0-only excluded)
- All returned items have `license == "MIT" || license == "Apache-2.0"`
