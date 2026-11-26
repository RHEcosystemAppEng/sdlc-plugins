# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

**Verdict: FAIL**

## What was checked
- `modules/fundamental/src/package/service/mod.rs`: whether it uses the correlated subquery from the Implementation Notes (`SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ... WHERE sp.package_id = p.id`).
- The whole diff, for any join through `sbom_package` -> `sbom_advisory` -> `advisory` or any use of `COUNT(DISTINCT ...)`.

## What was found
No vulnerability count is computed anywhere. The service sets a constant:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The PR has no subquery, no join through `sbom_package`/`sbom_advisory`/`advisory`, and no deduplication. The `TODO` shows the core feature in the task Description was left unfinished. A count that is always 0 cannot reflect unique advisories.

## Related test inconsistency
`test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2`, and `test_package_with_vulnerabilities_has_count` asserts `== 3`. With a hard-coded 0, both tests must fail if they run. CI is reported as passing, so these tests are most likely not compiled or run at all. Two signs of this:
- `tests/api/` has no visible module registration for `package_vuln_count.rs`.
- The test file does not import `PaginatedResults`, `PackageSummary`, or the `test_context` macro.

Either way, the passing CI result does not show that this criterion is met.
