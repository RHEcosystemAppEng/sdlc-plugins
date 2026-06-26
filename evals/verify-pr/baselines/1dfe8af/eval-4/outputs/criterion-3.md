# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Evidence

In `modules/fundamental/src/package/service/mod.rs`, the vulnerability count is hardcoded to zero:

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

No such subquery (or any query) is present in the diff. The `TODO` comment explicitly acknowledges this is not implemented.

## Reasoning

This criterion requires the count to reflect unique advisories, meaning the implementation must:
1. Actually query the database to count advisories
2. Use `COUNT(DISTINCT ...)` or equivalent to deduplicate across SBOMs

Neither of these is done. The value is unconditionally set to 0. A package with 5 distinct advisories would incorrectly report `vulnerability_count: 0`. This is the core functional deficiency of the PR — the feature's primary value (showing accurate vulnerability counts) is not implemented.

The `// TODO: implement subquery` comment confirms this is known-incomplete code that should not pass verification.
