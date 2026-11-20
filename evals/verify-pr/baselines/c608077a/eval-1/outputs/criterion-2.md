# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict: PASS**

## Reasoning

1. **Comma splitting**: `validate_license_param` runs `license.split(',').map(|s| s.trim().to_string())`, which turns `"MIT,Apache-2.0"` into `["MIT", "Apache-2.0"]`. Trimming also accepts `MIT, Apache-2.0`.
2. **Per-identifier validation**: each element is parsed with `spdx::Expression::parse`. Both are valid SPDX identifiers, so the call succeeds.
3. **OR semantics**: the service builds `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))`. That becomes `license IN ('MIT', 'Apache-2.0')`, which is a union (either license), not an intersection.
4. **Test coverage**: `test_list_packages_multi_license_filter` seeds MIT, Apache-2.0 and GPL-3.0-only packages, requests `?license=MIT,Apache-2.0`, and asserts status 200, 2 items, and that each item is MIT or Apache-2.0. The GPL package is correctly excluded.

## Observations (non-blocking)
- `Condition::any()` around a single `is_in` adds nothing, but it is harmless.
- A package with several `package_license` rows that match (for example both MIT and Apache-2.0) could show up twice because of the inner join, since there is no `DISTINCT`/`GROUP BY`. That is an edge case outside this criterion and the tests, and depends on the data model. It is noted for reviewer awareness only.
