# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Classification: LEGITIMATE

This is a genuine acceptance criterion requiring that the vulnerability count uses `COUNT(DISTINCT a.id)` semantics so that advisories shared across multiple SBOMs are not double-counted.

## Verification

The PR diff for `modules/fundamental/src/package/service/mod.rs` shows that `vulnerability_count` is hardcoded to `0`:

```rust
+            vulnerability_count: 0, // TODO: implement subquery
```

The implementation notes specified a correlated subquery:
```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery was never implemented. The `// TODO: implement subquery` comment explicitly acknowledges that the work is incomplete. Because the count is hardcoded to 0, it does not reflect any advisories at all -- unique or otherwise. The deduplication logic required by this criterion is entirely absent.

The test `test_vulnerability_count_deduplicates_across_sboms` in the new test file expects `vulnerability_count: 2` for a package with shared advisories, which would fail at runtime against this implementation since the hardcoded value is always 0.

## Verdict: FAIL

The vulnerability count does not reflect unique advisories because no advisory counting logic exists. The value is hardcoded to 0 with a TODO comment indicating the subquery was never implemented.
