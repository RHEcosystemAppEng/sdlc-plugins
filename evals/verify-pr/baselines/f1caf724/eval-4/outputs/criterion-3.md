## Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

**Verdict: FAIL**

### Analysis

This criterion requires that `vulnerability_count` is computed by a subquery that joins through `sbom_package -> sbom_advisory -> advisory` tables and counts DISTINCT advisories. The task description explicitly specifies the query:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id JOIN advisory a ON sa.advisory_id = a.id WHERE sp.package_id = p.id
```

However, the PR diff for `modules/fundamental/src/package/service/mod.rs` shows that **no subquery was implemented**. Instead, `vulnerability_count` is hardcoded to `0` with an explicit TODO comment:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The count does not reflect unique advisories because it does not reflect anything at all -- it is a static placeholder value. The core business logic required by this task has not been implemented.

### Evidence

- File: `modules/fundamental/src/package/service/mod.rs`
- Line: `vulnerability_count: 0, // TODO: implement subquery`
- No join logic exists in the diff connecting `sbom_package`, `sbom_advisory`, or `advisory` tables
- No `COUNT(DISTINCT ...)` or equivalent SeaORM query is present in any changed file
- The test `test_vulnerability_count_deduplicates_across_sboms` in the test file asserts `vulnerability_count == 2`, which would FAIL against the hardcoded `0` at runtime
- The test `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3`, which would also FAIL against the hardcoded `0`

### Impact

This is the central requirement of the task. Without the subquery, the `vulnerability_count` field is non-functional -- it will always return 0 regardless of how many advisories affect a package. Two of the three integration tests would fail at runtime if executed against this code.
