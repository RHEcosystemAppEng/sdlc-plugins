# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

**Verdict: FAIL**

## What was checked
- `modules/fundamental/src/package/service/mod.rs`, which should compute the count.
- The Implementation Notes, which prescribe a correlated subquery:
  `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`
- `tests/api/package_vuln_count.rs`.

## Evidence
The PR never counts advisories. The service hardcodes the value:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The diff has no subquery, no join through `sbom_package` / `sbom_advisory` / `advisory`, and no
`COUNT(DISTINCT ...)`. The `TODO` comment admits the work was not done. The count is always 0, so it does not
reflect unique advisories, or any advisories at all.

The new tests confirm this. Against this implementation they would fail:
- `test_package_with_vulnerabilities_has_count` expects `3` and gets `0`.
- `test_vulnerability_count_deduplicates_across_sboms` expects `2` and gets `0`.

CI is reported green, so these integration tests are probably not run in CI (they need a real PostgreSQL test
database). Green CI does not show this criterion is met.

The file `endpoints/list.rs` has only a comment change
(`// vulnerability_count now included in response`), with no functional change.

## Required fix
Implement the correlated `COUNT(DISTINCT a.id)` subquery from the Implementation Notes in `PackageService::list`
and fill `vulnerability_count` from its result, then confirm the three integration tests pass against a real
database.
