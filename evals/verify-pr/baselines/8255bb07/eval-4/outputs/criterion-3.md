## Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

### Verdict: FAIL

### Analysis

The task description specifies that the `vulnerability_count` should be computed by joining through `sbom_package -> sbom_advisory -> advisory` tables using a correlated subquery:

```sql
SELECT COUNT(DISTINCT a.id)
FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

However, the PR diff for `modules/fundamental/src/package/service/mod.rs` shows:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The `vulnerability_count` is hardcoded to `0` with an explicit TODO comment indicating the subquery has NOT been implemented. This means:

1. The count does NOT reflect unique advisories -- it reflects nothing, always returning 0
2. No database join or subquery exists to compute the actual count
3. The `COUNT(DISTINCT a.id)` logic for deduplication across SBOMs is completely absent
4. The test `test_vulnerability_count_deduplicates_across_sboms` (which expects `vulnerability_count == 2` for a package with shared advisories across 3 SBOMs) would fail at runtime

### Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- The TODO comment explicitly acknowledges the implementation is incomplete
- No SQL subquery, SeaORM query builder call, or any database interaction exists to compute the actual vulnerability count
- The test file `tests/api/package_vuln_count.rs` contains assertions that contradict the hardcoded value:
  - `test_package_with_vulnerabilities_has_count` expects `vulnerability_count == 3` (would fail)
  - `test_vulnerability_count_deduplicates_across_sboms` expects `vulnerability_count == 2` (would fail)

### Conclusion

This criterion is NOT satisfied. The core functionality of the task -- computing unique advisory counts via database joins -- has not been implemented. The hardcoded zero value is a placeholder, not a working implementation.
