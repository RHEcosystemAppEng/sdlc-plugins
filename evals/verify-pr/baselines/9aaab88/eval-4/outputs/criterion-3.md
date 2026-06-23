# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

This criterion requires that `vulnerability_count` be computed via a correlated subquery that joins through `sbom_package -> sbom_advisory -> advisory` tables and counts distinct advisories. The implementation notes explicitly specify:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
  JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
  JOIN advisory a ON sa.advisory_id = a.id
  WHERE sp.package_id = p.id
```

However, the actual implementation in `modules/fundamental/src/package/service/mod.rs` does not implement this subquery at all. Instead, it hardcodes the value:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The `TODO` comment explicitly acknowledges that the subquery has not been implemented. As a result:

1. The count does NOT reflect unique advisories -- it reflects nothing, always returning 0.
2. There is no deduplication logic because there is no counting logic at all.
3. The test `test_package_with_vulnerabilities_has_count` seeds 3 advisories and asserts `vulnerability_count == 3`, but the code would return 0, causing the test to fail at runtime.
4. The test `test_vulnerability_count_deduplicates_across_sboms` seeds 2 unique advisories across 3 SBOMs and asserts `vulnerability_count == 2`, but the code would return 0, also failing at runtime.

This is a critical correctness deficiency. The core feature -- computing a vulnerability count from database joins -- is completely unimplemented, replaced by a hardcoded stub.
