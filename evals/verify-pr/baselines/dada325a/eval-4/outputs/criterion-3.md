# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

**Verdict: FAIL**

## Reasoning
- The task requires a correlated subquery: `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`.
- The PR has no subquery, join, or `COUNT(DISTINCT ...)`. `PackageService::list` maps each row to `PackageSummary` with a hardcoded `vulnerability_count: 0` and a `// TODO: implement subquery` comment.
- No count is computed at all, so it cannot reflect unique advisories. Any package linked to advisories reports 0.
- The dedup test `test_vulnerability_count_deduplicates_across_sboms` expects `2`. Against this implementation it would return `0` and fail. The same goes for `test_package_with_vulnerabilities_has_count`, which expects `3`. The PR reports passing CI, so these tests are most likely not compiled or run. The new file uses `PaginatedResults`/`PackageSummary` without importing them, and the repo layout shows no registration of `package_vuln_count.rs` in the `tests/` crate. Passing CI is not evidence that this criterion is met.

## Evidence
- `modules/fundamental/src/package/service/mod.rs`: `+                vulnerability_count: 0, // TODO: implement subquery`
- No change to entity joins or query helpers (`entity/src/sbom_package.rs`, `entity/src/sbom_advisory.rs`, `common/src/db/query.rs`) and no raw SQL in the diff.
- `tests/api/package_vuln_count.rs`: `assert_eq!(pkg.vulnerability_count, 2);` cannot pass against a hardcoded 0.
