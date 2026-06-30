## Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

### Result: FAIL

### Evidence

The diff in `modules/fundamental/src/package/service/mod.rs` shows the vulnerability count is hardcoded to zero:

```rust
let items = items.into_iter().map(|p| {
    PackageSummary {
        id: p.id,
        name: p.name,
        version: p.version,
        license: p.license,
        vulnerability_count: 0, // TODO: implement subquery
    }
}).collect();
```

The `// TODO: implement subquery` comment explicitly acknowledges that the actual computation is not implemented. The task description specifies a correlated subquery should be used:

```sql
SELECT COUNT(DISTINCT a.id)
FROM sbom_package sp
JOIN sbom_advisory sa ON sp.sbom_id = sa.sbom_id
JOIN advisory a ON sa.advisory_id = a.id
WHERE sp.package_id = p.id
```

This subquery was never implemented. The count does NOT reflect unique advisories because no query is performed at all -- every package returns 0 regardless of how many advisories exist.

The tests in `tests/api/package_vuln_count.rs` include:
- `test_package_with_vulnerabilities_has_count` -- expects `vulnerability_count == 3` for a package with 3 advisories. This test would FAIL against the current implementation (hardcoded 0).
- `test_vulnerability_count_deduplicates_across_sboms` -- expects `vulnerability_count == 2` for a package with shared advisories. This test would also FAIL (hardcoded 0).

### Conclusion

FAIL -- the vulnerability count is hardcoded to 0 with a TODO comment. No subquery is implemented to compute actual counts. Packages with vulnerabilities will incorrectly report zero vulnerabilities. This is a critical correctness issue.
