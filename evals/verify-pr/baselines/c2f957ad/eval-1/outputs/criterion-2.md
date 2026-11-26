# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict: PASS**

## Reasoning
- **Comma separation:** `validate_license_param` runs `license.split(',').map(|s| s.trim().to_string())`, which turns `MIT,Apache-2.0` into `["MIT", "Apache-2.0"]`. Each value is validated separately as an SPDX expression, and both are valid.
- **OR semantics:** the service builds `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))`. That is SQL `license IN ('MIT', 'Apache-2.0')`, which returns the union of packages with either license.
- **Test:** `test_list_packages_multi_license_filter` seeds MIT, Apache-2.0 and GPL-3.0-only packages. It requests `?license=MIT,Apache-2.0` and asserts status 200, `items.len() == 2`, and that each item is MIT or Apache-2.0. The GPL package is correctly excluded.

## Notes
- Possible issue, not blocking: a single package with both an MIT and an Apache-2.0 license row could appear twice because of the inner join. The test seeds one license per package and would not catch this. Adding `DISTINCT` or using an `EXISTS` subquery would harden it. This does not violate the criterion as written.
