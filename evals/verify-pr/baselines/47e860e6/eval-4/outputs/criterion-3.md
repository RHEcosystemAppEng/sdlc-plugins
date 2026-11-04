# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

**Verdict: FAIL**

There is no count at all, so nothing is deduplicated. The task Description says to compute it by joining `sbom_package` → `sbom_advisory` → `advisory`, and Implementation Notes give the exact correlated subquery (`SELECT COUNT(DISTINCT a.id) ... WHERE sp.package_id = p.id`). The diff has no subquery, join, `COUNT`, or `DISTINCT`. `PackageService::list` instead sets:

    vulnerability_count: 0, // TODO: implement subquery

The PR's own test `test_vulnerability_count_deduplicates_across_sboms` seeds 2 shared advisories across 3 SBOMs and asserts `vulnerability_count == 2`. It would fail against this code, and so would `test_package_with_vulnerabilities_has_count` (expects 3). The TODO comment confirms the implementation is unfinished.
