# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The implementation does NOT compute a count of unique advisories. In `modules/fundamental/src/package/service/mod.rs`, the `vulnerability_count` is hardcoded to `0`:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The task's Implementation Notes specify using a correlated subquery:
```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id
```

This subquery is entirely missing from the implementation. There is no join through `sbom_package → sbom_advisory → advisory` tables. The `COUNT(DISTINCT a.id)` logic that would ensure deduplication across SBOMs is absent.

The test `test_vulnerability_count_deduplicates_across_sboms` seeds a package with 2 advisories shared across 3 SBOMs and expects `vulnerability_count == 2`, but with the hardcoded `0`, this test would FAIL at runtime.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs`, line 32: `vulnerability_count: 0, // TODO: implement subquery`
- No SQL subquery or join logic exists in the diff
- The TODO comment explicitly acknowledges the subquery is not implemented
- Test `test_vulnerability_count_deduplicates_across_sboms` expects count=2 but would get count=0
