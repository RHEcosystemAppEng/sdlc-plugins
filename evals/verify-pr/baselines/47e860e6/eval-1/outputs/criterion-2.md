# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict: PASS**

## Code evidence
- `validate_license_param` splits `"MIT,Apache-2.0"` on commas and trims each part, giving `["MIT", "Apache-2.0"]`. Both are valid SPDX identifiers.
- In the service, `package_license::Column::License.is_in(["MIT", "Apache-2.0"])` produces `WHERE license IN ('MIT','Apache-2.0')`, which is a union (OR) of the values. Wrapping it in `Condition::any()` is redundant for a single clause but harmless.

## Test evidence
- `tests/api/package.rs::test_list_packages_multi_license_filter` seeds MIT, Apache-2.0, and GPL-3.0-only packages, requests `?license=MIT,Apache-2.0`, and asserts status 200, 2 items, and that every item is MIT or Apache-2.0. The GPL package is correctly excluded.

## Notes (non-blocking)
- The query uses an INNER JOIN on the `package_license` mapping table with no `DISTINCT`. If one package can have several license rows, a package carrying both MIT and Apache-2.0 could appear twice. The tests seed only single-license packages, so they would not catch this. This is a robustness concern to confirm against the entity model, not a demonstrated failure of the criterion.
