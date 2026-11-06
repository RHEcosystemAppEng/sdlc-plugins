# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict: PASS**

## Reasoning

- **Comma parsing:** `validate_license_param` splits the raw value on `,` and trims each part, so `MIT,Apache-2.0` becomes `["MIT", "Apache-2.0"]`. Each identifier is validated separately.
- **Union semantics:** the service builds `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))`. That becomes `license IN ('MIT', 'Apache-2.0')`, which is an OR (union) of the requested licenses, not an AND.
- **Join:** the inner join on `PackageLicense` limits results to packages that have a matching license row.

## Test evidence

`test_list_packages_multi_license_filter`:
- Seeds MIT, Apache-2.0 and GPL-3.0-only packages.
- Requests `?license=MIT,Apache-2.0`.
- Asserts 200 OK and 2 items, each with license MIT or Apache-2.0. The GPL package is correctly excluded.

## Observation (non-blocking)

The inner join goes through a package-to-license mapping table. If one package could have several matching license rows (for example both MIT and Apache-2.0), it could appear twice and inflate `total`. `PackageSummary` has a single `license` field, which suggests one license per package, so this is a hardening note and not a defect against the criterion. Adding `.distinct()` would remove the risk if the data model ever allows several licenses per package.

## Conclusion

Comma-separated values are parsed and combined with OR (IN). The criterion is satisfied.
