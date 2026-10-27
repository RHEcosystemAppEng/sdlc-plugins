# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Evidence

The implementation in `modules/fundamental/src/package/service/mod.rs` hardcodes `vulnerability_count: 0`:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The task description specifies a correlated subquery should be used:
```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

No such subquery exists in the diff. The `TODO: implement subquery` comment explicitly acknowledges the implementation is incomplete. Since the count is always 0, it cannot reflect unique advisories — the deduplication logic has not been implemented at all.

The test `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2` for a package with shared advisories, but the service would return 0, meaning this test would fail at runtime.

## Conclusion

This criterion **fails**. The vulnerability count computation is entirely missing — it is hardcoded to 0, making deduplication impossible.
