# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

**Result**: FAIL

## Criterion Text
The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Evidence

In `modules/fundamental/src/package/service/mod.rs`, the vulnerability count is hardcoded to zero:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The task description specifies a correlated subquery that should be implemented:

```sql
SELECT COUNT(DISTINCT a.id)
FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery is entirely absent from the implementation. The `COUNT(DISTINCT a.id)` construct is what ensures unique advisory counting across multiple SBOMs, and it was never written.

## Impact

- The field always returns `0` regardless of actual vulnerability data in the database.
- The test `test_package_with_vulnerabilities_has_count` asserts `vulnerability_count == 3` but the implementation always returns `0`, so this test would fail at runtime.
- The test `test_vulnerability_count_deduplicates_across_sboms` asserts `vulnerability_count == 2` but would also fail at runtime.
- The core purpose of this task -- showing the count of unique vulnerability advisories -- is not implemented.

## Reasoning

This is the most critical failure in the PR. The TODO comment explicitly acknowledges the implementation is incomplete. The criterion requires that the count reflects unique advisories, but no counting logic exists at all. The value is a static `0` placeholder. This criterion clearly fails.
