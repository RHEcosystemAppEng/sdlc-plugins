# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

The acceptance criterion requires that `vulnerability_count` reflects the actual count of unique advisories affecting each package, computed by joining through `sbom_package`, `sbom_advisory`, and `advisory` tables as described in the Implementation Notes.

However, the PR diff for `modules/fundamental/src/package/service/mod.rs` shows:

```rust
+                vulnerability_count: 0, // TODO: implement subquery
```

The value is hardcoded to `0` for ALL packages. The correlated subquery specified in the Implementation Notes has NOT been implemented:

```sql
SELECT COUNT(DISTINCT a.id) FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

The `// TODO: implement subquery` comment explicitly acknowledges that this is not yet done. This means:

1. Packages WITH vulnerabilities will incorrectly show `vulnerability_count: 0`
2. The deduplication logic (`COUNT(DISTINCT ...)`) is entirely absent
3. The test `test_package_with_vulnerabilities_has_count` (which asserts `vulnerability_count == 3` for a package with 3 advisories) would FAIL at runtime
4. The test `test_vulnerability_count_deduplicates_across_sboms` (which asserts `vulnerability_count == 2` for deduplicated advisories) would also FAIL at runtime

This is a critical gap -- the core functionality of the feature is not implemented.

## Evidence

- File: `modules/fundamental/src/package/service/mod.rs` -- `vulnerability_count: 0` hardcoded with TODO comment
- Implementation Notes specify a correlated subquery that was never implemented
- Two of three integration tests would fail at runtime due to the hardcoded zero value
