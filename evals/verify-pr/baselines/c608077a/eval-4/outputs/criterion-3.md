# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

**Verdict: FAIL**

## Reasoning
- There is no subquery, join, or `COUNT(DISTINCT ...)` anywhere in the diff. The service sets `vulnerability_count: 0` with `// TODO: implement subquery`.
- Nothing is counted, so nothing is deduplicated. The Implementation Notes require `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`, and none of it is implemented.
- The new test `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2`, and `test_package_with_vulnerabilities_has_count` asserts `3`. Both would fail against the hardcoded `0`. CI is reported green anyway, which suggests the new test file is not compiled or run:
  - nothing in the diff registers it as a module
  - it does not import `PaginatedResults`, `PackageSummary` or `test_context`

  The passing CI is therefore not evidence for this criterion.

## Required fix
Implement the distinct-count subquery in `PackageService::list`, and make sure `tests/api/package_vuln_count.rs` is wired into the test harness so its assertions actually run.
