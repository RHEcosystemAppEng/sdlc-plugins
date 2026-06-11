# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The PR supports comma-separated license values that return the union of matching packages:

1. **Parsing** (`list.rs` - `validate_license_param`):
   - The function splits the input string on commas: `license.split(',')`.
   - Each segment is trimmed and collected into a `Vec<String>`.
   - For input `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`.
   - Each identifier is individually validated via `spdx::Expression::parse()`.

2. **Query construction** (`service/mod.rs`):
   - The filter uses `Condition::any()` with `.add(package_license::Column::License.is_in(licenses.iter().cloned()))`.
   - `is_in` with `["MIT", "Apache-2.0"]` generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause, which returns packages with either license.
   - The `InnerJoin` on `PackageLicense` ensures only packages with a matching license record are included.

3. **Test coverage** (`tests/api/package.rs`):
   - `test_list_packages_multi_license_filter` seeds three packages: MIT, Apache-2.0, and GPL-3.0-only.
   - Queries `?license=MIT,Apache-2.0` and asserts 2 packages returned.
   - Verifies each returned package has either MIT or Apache-2.0 license.

The use of `Condition::any()` with `is_in` correctly implements OR semantics for multiple license values, returning the union of matches.
