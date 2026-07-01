# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

This criterion requires that the `vulnerability_count` field correctly computes the number of unique advisory associations for each package, using a correlated subquery that joins through `sbom_package -> sbom_advisory -> advisory` tables with `COUNT(DISTINCT a.id)` to avoid double-counting advisories that appear across multiple SBOMs.

The PR diff in `modules/fundamental/src/package/service/mod.rs` shows that the vulnerability count is hardcoded to 0:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The `// TODO: implement subquery` comment explicitly acknowledges that the subquery has not been implemented. The task's Implementation Notes specify the required query:

> `SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id`

This subquery is completely absent from the implementation. The field always returns 0, meaning:
- Packages WITH vulnerabilities will incorrectly show 0
- There is no deduplication logic because there is no counting logic at all
- The test `test_package_with_vulnerabilities_has_count` (which expects count=3) would fail at runtime
- The test `test_vulnerability_count_deduplicates_across_sboms` (which expects count=2) would fail at runtime

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- No join query, no `COUNT(DISTINCT ...)`, no database access for vulnerability counting
- The TODO comment confirms the developer knowingly left this unimplemented
- Two of three integration tests would fail at runtime against this implementation
