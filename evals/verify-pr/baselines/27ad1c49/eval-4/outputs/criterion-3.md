# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Reasoning

The implementation does NOT compute the vulnerability count at all. In `modules/fundamental/src/package/service/mod.rs`, the value is hardcoded to zero with a TODO comment:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The task's Implementation Notes specified a correlated subquery to be used:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery was never implemented. There is:
- No database query computing advisory counts
- No JOIN through `sbom_package`, `sbom_advisory`, and `advisory` tables
- No `COUNT(DISTINCT ...)` to deduplicate advisories across SBOMs
- No deduplication logic of any kind

The `vulnerability_count` returns 0 for ALL packages, regardless of how many vulnerabilities or advisories they actually have. This is a stub/placeholder implementation that does not satisfy the criterion.

Additionally, the test `test_package_with_vulnerabilities_has_count` (which asserts `vulnerability_count == 3`) and `test_vulnerability_count_deduplicates_across_sboms` (which asserts `vulnerability_count == 2`) would both fail against this implementation, since the hardcoded value is always 0.
