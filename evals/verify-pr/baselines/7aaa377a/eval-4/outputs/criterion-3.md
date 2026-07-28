# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The acceptance criterion requires that the `vulnerability_count` field reflects the number of unique vulnerability advisories affecting each package, computed via a correlated subquery joining through `sbom_package`, `sbom_advisory`, and `advisory` tables. Specifically, advisories shared across multiple SBOMs must not be double-counted.

## Evidence

The PR diff for `modules/fundamental/src/package/service/mod.rs` reveals that the vulnerability count is **hardcoded to 0** with an explicit TODO comment indicating the subquery has not been implemented:

```diff
+        let items = items.into_iter().map(|p| {
+            PackageSummary {
+                id: p.id,
+                name: p.name,
+                version: p.version,
+                license: p.license,
+                vulnerability_count: 0, // TODO: implement subquery
+            }
+        }).collect();
```

The implementation notes in the task specify the required subquery:

```sql
SELECT COUNT(DISTINCT a.id)
FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery has not been implemented. The `vulnerability_count` is always 0, regardless of whether the package has associated vulnerability advisories.

Additionally, the tests in `tests/api/package_vuln_count.rs` that verify correct counting behavior will fail:

- `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3` for a package seeded with 3 advisories -- this will fail (actual: 0)
- `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2` for a package with shared advisories -- this will fail (actual: 0)

This criterion is clearly not satisfied. The core feature requirement -- computing actual vulnerability counts from the database -- has not been implemented.
