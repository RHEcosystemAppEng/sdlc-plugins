## Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

### Verdict: FAIL

### Analysis

The acceptance criterion requires that the `vulnerability_count` reflects unique advisories, avoiding double-counting when the same advisory is associated with a package through multiple SBOMs. The implementation notes specified using `COUNT(DISTINCT a.id)` in the correlated subquery to achieve this deduplication.

### Evidence

In `modules/fundamental/src/package/service/mod.rs`, the vulnerability count is hardcoded:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

No subquery of any kind exists. The specified correlated subquery that would join through `sbom_package -> sbom_advisory -> advisory` tables and use `COUNT(DISTINCT a.id)` for deduplication was never implemented. Without a subquery, there is no counting mechanism at all, and therefore no deduplication logic.

The test `test_vulnerability_count_deduplicates_across_sboms` further confirms this gap. It seeds a package with 2 unique advisories shared across 3 SBOMs and asserts `vulnerability_count == 2`. With the hardcoded zero, this test would fail, returning 0 instead of 2.

### Conclusion

The criterion is not satisfied. There is no subquery implementation, no join logic, and no deduplication. The `// TODO: implement subquery` comment explicitly acknowledges this was left unimplemented.
