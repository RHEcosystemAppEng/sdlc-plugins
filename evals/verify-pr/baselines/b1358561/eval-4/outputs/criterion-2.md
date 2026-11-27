# Criterion 2: Packages with no vulnerabilities show `vulnerability_count: 0`

**Verdict: PASS (satisfied only by accident, because the value is hardcoded)**

## Reasoning

The criterion says that a package with no linked advisories must report `0`. The diff produces that result, but not by computing it.

## Evidence

- `modules/fundamental/src/package/service/mod.rs` (hunk `@@ -30,6 +30,14 @@`) builds every `PackageSummary` with:
  ```rust
  vulnerability_count: 0, // TODO: implement subquery
  ```
- Every package therefore reports `0`, including packages with no vulnerabilities. Read literally, the criterion holds.
- `tests/api/package_vuln_count.rs::test_package_without_vulnerabilities_has_zero_count` asserts `vulnerability_count == 0`. That assertion would pass against this implementation, but only because of the constant.

## Caveat

This PASS does not show that the feature works. A correlated `COUNT(DISTINCT ...)` subquery would also return `0` for packages with no advisories. Here the zero comes from a placeholder, not from a calculation. The real defect is recorded under criterion 3.
