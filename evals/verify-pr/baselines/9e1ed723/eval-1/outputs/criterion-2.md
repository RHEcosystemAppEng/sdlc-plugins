# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict: PASS**

## Code evidence
- `list.rs`: `license.split(',').map(|s| s.trim().to_string())` gives `["MIT", "Apache-2.0"]`, and each value is validated as SPDX.
- `service/mod.rs`: `Condition::any().add(package_license::Column::License.is_in(licenses...))` produces `license IN ('MIT','Apache-2.0')`. That is OR (union) matching, as the criterion requires.

## Test evidence
`test_list_packages_multi_license_filter`:
- seeds MIT, Apache-2.0 and GPL-3.0-only packages;
- requests `?license=MIT,Apache-2.0`;
- asserts 200 OK, 2 items, and that each item is MIT or Apache-2.0. This also shows the GPL package is excluded.

CI passes.

## Caveats (non-blocking)
- **Possible duplicates:** the filter uses an inner join on the `package_license` mapping table. If one package has several license rows that all match, it could appear more than once. The test seeds only single-license packages, so it would not catch this.
- **Redundant wrapper:** `Condition::any()` around a single `is_in` adds nothing. It is harmless.
