# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

**Verdict: FAIL**

## What was checked
- `modules/fundamental/src/package/service/mod.rs`: what the PR adds to compute the count.
- The task's Implementation Notes, which ask for a correlated subquery:
  `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`
- `tests/api/package_vuln_count.rs`: `test_vulnerability_count_deduplicates_across_sboms`.

## What was found
The PR has no subquery, join, or `COUNT(DISTINCT ...)` of any kind. The count is hardcoded:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

Nothing joins `sbom_package` -> `sbom_advisory` -> `advisory`, so nothing reflects advisories, unique or otherwise. The `TODO` comment admits the work is unfinished.

The new tests contradict the code:
- `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3`. The code always returns 0.
- `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2`. The code always returns 0.

Run against this implementation, both tests would fail. The task says CI passes, so either these tests are not compiled or run in CI, or their seeding helpers (`seed_package_with_advisories`, `seed_package_with_shared_advisories`) are missing or stubbed. Neither helper exists in the repository structure provided, and `tests/api/` has no registration of the new module. Either way, the passing CI result does not show that the count works.

## Required fix
Replace the hardcoded `0` with the correlated `COUNT(DISTINCT a.id)` subquery from the Implementation Notes, for example as a SeaORM `column_as` with a subquery expression, or as a raw select expression. Then confirm that the three new tests are actually run by CI.
